#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { PipelineStack } from '../lib/pipeline-stack';
import {InfraStage} from "../lib/infra-stage";

const app = new cdk.App();

new PipelineStack(app, 'ServerlessTodoApi-PipelineStack', {
    repositoryName: "serverless-todo-api",
    branchName: "main",
    ownerName: "nmoutschen"
});

// Implement Infra Stage for developer environment
new InfraStage(app, 'ServerlessTodoApi-Dev', {
    domainName: "fr-houes",
    callbackUrls: ['http://localhost', 'http://localhost:3000'],
    env: {
        account: process.env.CDK_DEFAULT_ACCOUNT,
        region: process.env.CDK_DEFAULT_REGION
    },
});

app.synth();
