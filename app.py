#!/usr/bin/env python3

from aws_cdk import core

from todo_api.todo_api_stack import TodoApiStack


app = core.App()
TodoApiStack(app, "todo-api")

app.synth()
