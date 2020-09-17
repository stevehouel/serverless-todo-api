import * as cdk from '@aws-cdk/core';
import {CfnOutput, Construct, Duration, Fn} from '@aws-cdk/core';
import {CfnIdentityPool, CfnIdentityPoolRoleAttachment, Mfa, UserPool,} from '@aws-cdk/aws-cognito';
import {Role, ServicePrincipal, WebIdentityPrincipal} from "@aws-cdk/aws-iam";
import {Asset} from "@aws-cdk/aws-s3-assets";
import {AssetApiDefinition, RestApi, SpecRestApi} from "@aws-cdk/aws-apigateway";
import {PythonFunction} from "@aws-cdk/aws-lambda-python";
import {Alias, CfnFunction, Runtime, Tracing} from "@aws-cdk/aws-lambda";
import {AttributeType, BillingMode, Table, TableEncryption} from "@aws-cdk/aws-dynamodb";

interface CognitoStackProps extends cdk.StackProps {
  readonly domainName: string;
  readonly callbackUrls: string[];
}

export class InfraStack extends cdk.Stack {

  public readonly userPoolId: CfnOutput;
  public readonly identityPoolId: CfnOutput;
  public readonly userPoolDomain: CfnOutput;
  public readonly userPoolAppClientId: CfnOutput;
  public readonly authRoleArn: CfnOutput;
  public readonly unauthRoleArn: CfnOutput;

  public readonly restApiId: CfnOutput;

  constructor(scope: cdk.Construct, id: string, props: CognitoStackProps) {
    super(scope, id, props);

    // Cognito Stack
    const pool = new UserPool(this, 'UserPool', {
      mfa: Mfa.OFF,
      signInAliases: {
        username: false,
        email: true
      },
      standardAttributes: {
        fullname: {
          required: true,
          mutable: false,
        },
      },
      passwordPolicy: {
        minLength: 12,
        requireLowercase: true,
        requireUppercase: true,
        requireDigits: true,
        requireSymbols: true,
        tempPasswordValidity: Duration.days(3),
      },
    });

    // Create CUP domain
    const domain = pool.addDomain('UserPoolDomain', {
      cognitoDomain: {
        domainPrefix: props.domainName,
      },
    });

    // Create App Client
    const userPoolAppClient = pool.addClient('UserPoolAppClient', {
      preventUserExistenceErrors: true,
      oAuth: {
        flows: {
          implicitCodeGrant: true,
        },
        callbackUrls: props.callbackUrls,
      }
    });

    const identityPool = new CfnIdentityPool(this, 'IdentityPool', {
      allowUnauthenticatedIdentities: true,
      cognitoIdentityProviders: [
        {
          clientId: userPoolAppClient.userPoolClientId,
          providerName: pool.userPoolProviderName
        }
      ]
    });
    identityPool.node.addDependency(pool, userPoolAppClient);

    // Table
    const table = new Table(this, 'TodoTable', {
      tableName: 'todo',
      partitionKey: { name: 'todoId', type: AttributeType.STRING },
      removalPolicy:  cdk.RemovalPolicy.DESTROY,
      readCapacity: 1,
      writeCapacity: 1
    });
        
    table.metricConsumedReadCapacityUnits().createAlarm(this, 'ReadCapacityUnitsLimit-BasicAlarm', {
          threshold: 240,
          evaluationPeriods: 1,
          period: cdk.Duration.minutes(1),
          alarmName: `${table.tableName}-ReadCapacityUnitsLimit-BasicAlarm`,
        });
        
    table.metricConsumedReadCapacityUnits().createAlarm(this, 'WriteCapacityUnitsLimit-BasicAlarm', {
      threshold: 240,
      evaluationPeriods: 1,
      period: cdk.Duration.minutes(1),
      alarmName: `${table.tableName}-WriteCapacityUnitsLimit-BasicAlarm`,
    });

    // Api Stack
    const createTodoFunction = this.createFunction('CreateTodoFunction','create_todo', table);
    const updateTodoFunction = this.createFunction('UpdateTodoFunction','update_todo', table);
    const getAllTodosFunction = this.createFunction('GetAllTodosFunction','get_all_todos', table);
    const getTodoFunction = this.createFunction('GetTodoFunction','get_todo', table);
    const deleteTodoFunction = this.createFunction('DeleteTodoFunction','delete_todo', table);

    // Permissions
    table.grantReadData(getAllTodosFunction);
    table.grantReadData(getTodoFunction);

    table.grantWriteData(createTodoFunction);
    table.grantWriteData(updateTodoFunction);
    table.grantWriteData(deleteTodoFunction);

    // Create Api Specs asset
    const asset = new Asset(this, 'TodoApiAsset', {
      path: 'lib/todo-api/specs/specs.yaml',
    });

    // Transform Specs file
    const specsContent = Fn.transform('AWS::Include', {'Location': asset.s3ObjectUrl})

    const api = new SpecRestApi(this, 'todoApi', {
      apiDefinition: AssetApiDefinition.fromInline(specsContent),
      deployOptions: {
        dataTraceEnabled: true
      }
    });

    // Finally give permission to API to execute Lambda functions
    // Add Invoke permission to functions
    const principal = new ServicePrincipal('apigateway.amazonaws.com');
    const createTodoArn = api.arnForExecuteApi('POST', '/todos');
    const getAllTodosArn = api.arnForExecuteApi('GET', '/todos');
    const getTodoArn = api.arnForExecuteApi('GET', '/todos/{idTodo}');
    const deleteTodoArn = api.arnForExecuteApi('DELETE', '/todos/{idTodo}');
    const updateTodoArn = api.arnForExecuteApi('PUT', '/todos/{idTodo}');

    createTodoFunction.addPermission('CreateTodoPermission', {
      principal,
      scope: api,
      sourceArn: createTodoArn,
    });

    getAllTodosFunction.addPermission('GetAllTodosPermission', {
      principal,
      scope: api,
      sourceArn: getAllTodosArn,
    });

    getTodoFunction.addPermission('GetTodoPermission', {
      principal,
      scope: api,
      sourceArn: getTodoArn,
    });

    updateTodoFunction.addPermission('UpdateTodoPermission', {
      principal,
      scope: api,
      sourceArn: updateTodoArn,
    });

    deleteTodoFunction.addPermission('DeleteTodoPermission', {
      principal,
      scope: api,
      sourceArn: deleteTodoArn,
    });

    // Create Auth and UnAuthRole in order to consume the API
    const authRole = new Role(this, 'AuthenticatedRole', {
      assumedBy: new WebIdentityPrincipal('cognito-identity.amazonaws.com')
          .withConditions({
            "StringEquals": { "cognito-identity.amazonaws.com:aud": identityPool.ref },
            "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "authenticated"}
          })
    });

    const unauthRole = new Role(this, 'UnauthenticatedRole', {
      assumedBy: new WebIdentityPrincipal('cognito-identity.amazonaws.com')
          .withConditions({
            "StringEquals": { "cognito-identity.amazonaws.com:aud": identityPool.ref },
            "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "unauthenticated"}
          })
    });

    new CfnIdentityPoolRoleAttachment(this, 'identityPoolRoleattachement', {
      identityPoolId: identityPool.ref,
      roles: {
        'unauthenticated': unauthRole.roleArn,
        'authenticated': authRole.roleArn,
      }
    });

    this.restApiId = new CfnOutput(this, 'restApiId', {
      value: api.restApiId
    });

    this.userPoolId = new CfnOutput(this, 'userPoolId', {
      value: pool.userPoolId,
      exportName: 'ServerlessTodoApi-UserPoolId'
    });

    this.identityPoolId = new CfnOutput(this, 'identityPoolId', {
      value: identityPool.ref,
      exportName: 'ServerlessTodoApi-IdentityPoolId'
    });

    this.userPoolAppClientId = new CfnOutput(this, 'userPoolAppClientId', {
      value: userPoolAppClient.userPoolClientId,
      exportName: 'ServerlessTodoApi-UserPoolAppClientId'
    });

    this.userPoolDomain = new CfnOutput(this, 'userPoolDomain', {
      value: domain.baseUrl(),
      exportName: 'ServerlessTodoApi-UserPoolDomain'
    });

    this.unauthRoleArn = new CfnOutput(this, 'UnauthRoleArn', {
      value: unauthRole.roleArn,
    });

    this.authRoleArn = new CfnOutput(this, 'AuthRoleArn', {
      value: authRole.roleArn,
    });

  }

  createFunction(functionName: string, handler: string, table: Table): Alias {
    const lambdaFunction = new PythonFunction(this, functionName, {
      functionName: functionName,
      entry: 'lib/todo-api',
      index: 'src/handlers/todo.py',
      handler: handler,
      runtime: Runtime.PYTHON_3_8,
      profiling: true,
      timeout: Duration.seconds(60),
      tracing: Tracing.ACTIVE,
      environment: {
        TABLE_NAME: table.tableName,
      }
    });

    const alias = lambdaFunction.currentVersion.addAlias('live');

    const forceLambdaId = lambdaFunction.node.defaultChild as CfnFunction;
    forceLambdaId.overrideLogicalId(functionName);

    return alias;
  }
}