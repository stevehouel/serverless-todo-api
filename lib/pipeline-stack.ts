import {App, SecretValue, Stack, StackProps} from '@aws-cdk/core';
import {CdkPipeline, SimpleSynthAction} from '@aws-cdk/pipelines';
import { Repository } from '@aws-cdk/aws-codecommit';
import { InfraStage } from './infra-stage';
import { GitHubSourceAction} from '@aws-cdk/aws-codepipeline-actions';
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

    const code = Repository.fromRepositoryName(this, 'ImportedRepository', props.repositoryName);
    const sourceArtifact = new Artifact('SourceOutput');
    const cloudAssemblyArtifact = new Artifact();

    // Creating CodePipeline object
    const pipeline = new CdkPipeline(this, 'Pipeline', {
      cloudAssemblyArtifact,
      sourceAction: new GitHubSourceAction({
        actionName: 'Github',
        // Replace these with your actual GitHub project name
        owner: props.ownerName,
        repo: props.repositoryName,
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
        buildCommand: 'yarn build',
        environment: {
          buildImage: LinuxBuildImage.STANDARD_4_0,
        }
      }),
    });

    // Beta Stage
    pipeline.addApplicationStage(new InfraStage(this, 'Beta', {
      domainName: 'sample-beta',
      callbackUrls: [ 'https://xxx.com' ],
      logoutUrls: [ 'https://xxx.com' ],
      env: { account: '910421270336', region: 'eu-west-1' },
    }));
  }
}
