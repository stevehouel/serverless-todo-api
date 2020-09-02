#!/usr/bin/env python3

from aws_cdk import core

from serverless_crud_api.serverless_crud_api_stack import ServerlessCrudApiStack


app = core.App()
ServerlessCrudApiStack(app, "serverless-crud-api")

app.synth()
