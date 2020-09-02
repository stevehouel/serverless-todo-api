from aws_cdk import (
    core,
    aws_apigateway,
    aws_cognito,
    aws_dynamodb,
    aws_lambda
)


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

        # Lambda functions
        list_todos_function = aws_lambda.Function(self, "ListTodosFunction",
            handler="main.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("src/list_todos")
        )
        create_todo_function = aws_lambda.Function(self, "CreateTodoFunction",
            handler="main.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("src/create_todo")
        )
        get_todo_function = aws_lambda.Function(self, "GetTodoFunction",
            handler="main.handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset("src/get_todo")
        )

        # REST Api
        api = aws_apigateway.RestApi(self, "TodoApi")
        api_todos = api.root.add_resource("todos")
        api_todos_todo = api_todos.add_resource(r"{todo}")

        # GET /todos
        api_todos.add_method("GET", aws_apigateway.LambdaIntegration(list_todos_function))
        # POST /todos
        api_todos.add_method("POST", aws_apigateway.LambdaIntegration(create_todo_function))
        # GET /todos/{todo}
        api_todos_todo.add_method("GET", aws_apigateway.LambdaIntegration(get_todo_function))

