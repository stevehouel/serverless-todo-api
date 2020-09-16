
# Serverless TODO API

## Getting started

1. [Fork this repo on github by clicking here](https://github.com/nmoutschen/serverless-todo-api/fork)

1. Create a [personal github access token](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token) with the following scopes: `admin:repo_hook` and `repo`. (It will be used by the CICD pipeline to pull changes from your fork)

1. Push token to secrets manager

```
aws secretsmanager create-secret --name GITHUB_TOKEN --secret-string <YOUR_GITHUB_PERSONAL_ACCESS_TOKEN>
```

1. Install dependencies

```
make bootstrap
```

1. build CDK package

```
make build
```

1. deploy

```
make deploy
```