from aws_cdk import (
    core,
    aws_apigateway,
    aws_cognito,
    aws_dynamodb,
    aws_lambda
)


class PythonFunction(aws_lambda.Function):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        kwargs["handler"] = "main.handler"
        kwargs["runtime"] = aws_lambda.Runtime.PYTHON_3_8

        super().__init__(scope, id, **kwargs)


class TodoApiStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Cognito User Pool
        user_pool = aws_cognito.UserPool(self, "UserPool")

        # DynamoDB table
        table = aws_dynamodb.Table(self, "TodoTable",
            billing_mode=aws_dynamodb.BillingMode.PAY_PER_REQUEST,
            # Using the user ID from Cognito as partition key
            partition_key=aws_dynamodb.Attribute(
                name="userId",
                type=aws_dynamodb.AttributeType.STRING
            ),
            sort_key=aws_dynamodb.Attribute(
                name="sk",
                type=aws_dynamodb.AttributeType.STRING
            )
        )

        # Lambda functions environment
        lambda_environment = {
            "TABLE_NAME": table.table_name
        }

        # REST Api
        api = aws_apigateway.RestApi(self, "TodoApi")
        api_todos = api.root.add_resource("todos")
        api_todos_todo = api_todos.add_resource(r"{todo}")

        # GET /todos
        list_todos_function = PythonFunction(self, "ListTodosFunction",
            code=aws_lambda.Code.asset("src/list_todos"),
            environment=lambda_environment
        )
        table.grant_read_data(list_todos_function)
        api_todos.add_method("GET", aws_apigateway.LambdaIntegration(list_todos_function))

        # POST /todos
        create_todo_function = PythonFunction(self, "CreateTodoFunction",
            code=aws_lambda.Code.asset("src/create_todo"),
            environment=lambda_environment
        )
        table.grant_write_data(create_todo_function)
        api_todos.add_method("POST", aws_apigateway.LambdaIntegration(create_todo_function))

        # GET /todos/{todo}
        get_todo_function = PythonFunction(self, "GetTodoFunction",
            code=aws_lambda.Code.asset("src/get_todo"),
            environment=lambda_environment
        )
        table.grant_read_data(get_todo_function)
        api_todos_todo.add_method("GET", aws_apigateway.LambdaIntegration(get_todo_function))

        # DELETE /todos/{todo}
        delete_todo_function = PythonFunction(self, "DeleteTodoFunction",
            code=aws_lambda.Code.asset("src/delete_todo"),
            environment=lambda_environment
        )
        table.grant_write_data(delete_todo_function)
        api_todos_todo.add_method("DELETE", aws_apigateway.LambdaIntegration(delete_todo_function))
