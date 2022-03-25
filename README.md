# Serverless TODO API

Sample code used to demonstrate AWS serverless capabilities

## Getting started

1. [Fork this repository on github by clicking here](https://github.com/vikingen13/serverless-todo-api/fork)

1. Create a [personal github access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with the following scopes: `admin:repo_hook` and `repo`. (It will be used by the CICD pipeline to pull changes from your fork)

1. Push token to secrets manager

        aws secretsmanager create-secret --name GITHUB_TOKEN --secret-string <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>

1. Eventually install yarn

1. Clone the repository

        git clone <URL_OF_THE_REPO>

1. Configure the demonstration

   * in the file serverless-todo-api/bin/cdk.ts , change the ownerName to your Github ownerName

   * in the file serverless-todo-api/bin/cdk.ts , change the domainName to your the domain Name of your choice (this domain name shall be unique and available)

   * in the file serverless-todo-api/lib/pipeline-stack.ts, change the domainName to the domain Name of your choice (this domain name shall be unique and available)

   * Commit and push your changes

1. Install dependencies

        make bootstrap


1. build CDK package
        
        make build

1. deploy

        make deploy


## run stress tests
set the environment variable TODO_API_ENDPOINT to the endpoint of your API Gateway

for example:
```
export TODO_API_ENDPOINT=$(aws cloudformation describe-stacks --stack-name ServerlessTodoApi-Dev-ServerlessTodoApi-Infra --query "Stacks[0].Outputs[?OutputKey=='todoApiEndpoint6114C0A4'].OutputValue" --output text))
```
or
```
export TODO_API_ENDPOINT=https://123456789.execute-api.eu-west-1.amazonaws.com/prod
```

set the environment variable AWS_REGION to the region where you deployed the demonstration

for example

```
export AWS_REGION=eu-west-1
```

then run the stress tests

```
make stress
```
