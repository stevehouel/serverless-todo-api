import {AssetApiDefinition, SpecRestApi} from "@aws-cdk/aws-apigateway";
import {CfnOutput, Construct, Duration, Fn, Stack, StackProps} from "@aws-cdk/core";
import {Asset} from "@aws-cdk/aws-s3-assets";
import {PythonFunction} from "@aws-cdk/aws-lambda-python";
import {CfnFunction, Runtime, Tracing} from "@aws-cdk/aws-lambda";

interface ApiStackProps extends StackProps {

}

export class ApiStack extends Stack {

    public readonly restApiId: CfnOutput;

    constructor(scope: Construct, id: string, props: ApiStackProps) {
        super(scope, id, props);

        const createTodoFunction = new PythonFunction(this, 'MyFunction', {
            functionName: 'CreateTodo',
            entry: 'lib/todo-api/src',
            index: 'handlers/create_todo.py',
            handler: 'create_todo',
            runtime: Runtime.PYTHON_3_8,
            profiling: true,
            timeout: Duration.seconds(10),
            tracing: Tracing.ACTIVE
        });

        // const forceLambdaId = createTodoFunction.node.defaultChild as CfnFunction;
        // forceLambdaId.overrideLogicalId('CreateTodo');

        // Create Api Specs asset
        const asset = new Asset(this, 'TodoApiAsset', {
            path: 'lib/todo-api/specs/specs.yaml',
        });

        // Transform Specs file
        const specsContent = Fn.transform('AWS::Include', {'Location': asset.s3ObjectUrl})

        const api = new SpecRestApi(this, 'todoApi', {
            apiDefinition: AssetApiDefinition.fromInline(specsContent)
        });

        this.restApiId = new CfnOutput(this, 'restApiId', {
            value: api.restApiId
        });
    }
}