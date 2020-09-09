import {App, SecretValue, Stack, StackProps} from '@aws-cdk/core';
import {CdkPipeline, SimpleSynthAction} from '@aws-cdk/pipelines';
import { InfraStage } from './infra-stage';
import {GitHubSourceAction, GitHubTrigger} from '@aws-cdk/aws-codepipeline-actions';
import { Artifact } from '@aws-cdk/aws-codepipeline';
import {LinuxBuildImage} from "@aws-cdk/aws-codebuild";

interface PipelineStackProps extends StackProps {
  readonly repositoryName: string;
  readonly ownerName: string;
  readonly branchName: string;
}

export class PipelineStack extends Stack {
  constructor(app: App, id: string, props: PipelineStackProps) {
    super(app, id, props);

    const sourceArtifact = new Artifact('SourceOutput');
    const cloudAssemblyArtifact = new Artifact();

    // Creating CodePipeline object
    const pipeline = new CdkPipeline(this, 'ServerlessTodoApi-Pipeline', {
      cloudAssemblyArtifact,
      sourceAction: new GitHubSourceAction({
        actionName: 'Github',
        // Replace these with your actual GitHub project name
        owner: props.ownerName,
        repo: props.repositoryName,
        trigger: GitHubTrigger.POLL,
        oauthToken: SecretValue.secretsManager('GITHUB_TOKEN'),
        branch: props.branchName,
        output: sourceArtifact,
      }),
      // How it will be built and synthesized
      synthAction: SimpleSynthAction.standardYarnSynth({
        sourceArtifact,
        cloudAssemblyArtifact,
        // We need a build step to compile the TypeScript Lambda
        installCommand: 'make install',
        buildCommand: 'make build',
        environment: {
          buildImage: LinuxBuildImage.STANDARD_4_0,
          privileged: true
        }
      })
    });

    // Beta Stage
    pipeline.addApplicationStage(new InfraStage(this, 'ServerlessTodoApi-Beta', {
      domainName: 'todo-beta',
      callbackUrls: [ 'http://localhost:3000' ],
      env: { account: '910421270336', region: 'eu-west-1' },
    }));
  }
}
