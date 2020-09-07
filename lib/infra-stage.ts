import { CfnOutput, Construct, Stage, StageProps } from '@aws-cdk/core';
import { CognitoStack } from './infra/cognito-stack';

interface PipelineStageProps extends StageProps {
  readonly domainName: string;
  readonly callbackUrls: string[];
  readonly logoutUrls: string[];
}

export class InfraStage extends Stage {

  public readonly userPoolId: CfnOutput;
  public readonly identityPoolId: CfnOutput;
  public readonly userPoolDomain: CfnOutput;
  public readonly userPoolAppClientId: CfnOutput;

  constructor(scope: Construct, id: string, props: PipelineStageProps) {
    super(scope, id, props);

    const cognitoStack = new CognitoStack(this, 'Cognito', {
      domainName: props.domainName,
      callbackUrls: props.callbackUrls,
      logoutUrls: props.logoutUrls
    });

    // Outputs
    this.userPoolId = cognitoStack.userPoolId;
    this.identityPoolId = cognitoStack.identityPoolId;
    this.userPoolAppClientId = cognitoStack.userPoolAppClientId;
    this.userPoolDomain = cognitoStack.userPoolDomain;
  }
}
