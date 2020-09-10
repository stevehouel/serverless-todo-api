import { CfnOutput, Construct, Stage, StageProps } from '@aws-cdk/core';
import { InfraStack } from './infra-stack';

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

    const infraStack = new InfraStack(this, 'ServerlessTodoApi-Infra', {
      domainName: props.domainName,
      callbackUrls: props.callbackUrls,
    });


    // Outputs
    this.userPoolId = infraStack.userPoolId;
    this.identityPoolId = infraStack.identityPoolId;
    this.userPoolAppClientId = infraStack.userPoolAppClientId;
    this.userPoolDomain = infraStack.userPoolDomain;
    this.restApiId = infraStack.restApiId;
  }
}
