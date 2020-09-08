from src.main import init, tracer, logger

# Initialize context
init()

@tracer.capture_lambda_handler
@logger.inject_lambda_context
def get_all_todos(event, context, resource):
    return None, "Success"