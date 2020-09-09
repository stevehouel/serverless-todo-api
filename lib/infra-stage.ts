import { CfnOutput, Construct, Stage, StageProps } from '@aws-cdk/core';
import { CognitoStack } from './infra/cognito-stack';
import {ApiStack} from "./infra/api-stack";

interface PipelineStageProps extends StageProps {
  readonly domainName: string;
  readonly callbackUrls: string[];
}

export class InfraStage extends Stage {

  public readonly userPoolId: CfnOutput;
  public readonly identityPoolId: CfnOutput;
  public readonly userPoolDomain: CfnOutput;
  public readonly userPoolAppClientId: CfnOutput;
  public readonly restApiId: CfnOutput;

  constructor(scope: Construct, id: string, props: PipelineStageProps) {
    super(scope, id, props);

    const cognitoStack = new CognitoStack(this, 'Cognito', {
      domainName: props.domainName,
      callbackUrls: props.callbackUrls,
    });

    const apiStack = new ApiStack(this, 'Api', {});

    // Outputs
    this.userPoolId = cognitoStack.userPoolId;
    this.identityPoolId = cognitoStack.identityPoolId;
    this.userPoolAppClientId = cognitoStack.userPoolAppClientId;
    this.userPoolDomain = cognitoStack.userPoolDomain;

    this.restApiId = apiStack.restApiId;
  }
}
