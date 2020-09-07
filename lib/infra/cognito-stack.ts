import * as cdk from '@aws-cdk/core';
import { CfnOutput } from '@aws-cdk/core';
import {
  CfnIdentityPool, CfnIdentityPoolRoleAttachment,
  Mfa, OAuthScope,
  UserPool,
} from '@aws-cdk/aws-cognito';
import {Role, WebIdentityPrincipal} from "@aws-cdk/aws-iam";

interface CognitoStackProps extends cdk.StackProps {
  readonly domainName: string;
  readonly callbackUrls: string[];
  readonly logoutUrls: string[];
}

export class CognitoStack extends cdk.Stack {

  public readonly userPoolId: CfnOutput;
  public readonly identityPoolId: CfnOutput;
  public readonly userPoolDomain: CfnOutput;
  public readonly userPoolAppClientId: CfnOutput;
  public readonly authRoleArn: CfnOutput;
  public readonly unauthRoleArn: CfnOutput;

  constructor(scope: cdk.Construct, id: string, props: CognitoStackProps) {
    super(scope, id, props);

    const pool = new UserPool(this, 'UserPool', {
      standardAttributes: {
        email: {
          required: true,
          mutable: true,
        },
      },

      mfa: Mfa.OFF,
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
          authorizationCodeGrant: true,
        },
        scopes: [ OAuthScope.OPENID, OAuthScope.EMAIL, OAuthScope.PHONE, OAuthScope.PROFILE, OAuthScope.COGNITO_ADMIN ],
        callbackUrls: props.callbackUrls,
      },
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

    this.userPoolId = new CfnOutput(this, 'userPoolId', {
      value: pool.userPoolId,
      exportName: 'TFCHubBack-UserPoolId'
    });

    this.identityPoolId = new CfnOutput(this, 'identityPoolId', {
      value: identityPool.ref,
      exportName: 'TFCHubBack-IdentityPoolId'
    });

    this.userPoolAppClientId = new CfnOutput(this, 'userPoolAppClientId', {
      value: userPoolAppClient.userPoolClientId,
      exportName: 'TFCHubBack-UserPoolAppClientId'
    });

    this.userPoolDomain = new CfnOutput(this, 'userPoolDomain', {
      value: domain.baseUrl(),
      exportName: 'TFCHubBack-UserPoolDomain'
    });

    this.unauthRoleArn = new CfnOutput(this, 'UnauthRoleArn', {
      value: unauthRole.roleArn,
    });

    this.authRoleArn = new CfnOutput(this, 'AuthRoleArn', {
      value: authRole.roleArn,
    });

  }
}