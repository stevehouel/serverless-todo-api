import * as cdk from '@aws-cdk/core';

interface ApiStackProps extends cdk.StackProps {}

export class ApiStack extends cdk.Stack {

    constructor(scope: cdk.Construct, id: string, props: ApiStackProps) {
        super(scope, id, props);
    }
}