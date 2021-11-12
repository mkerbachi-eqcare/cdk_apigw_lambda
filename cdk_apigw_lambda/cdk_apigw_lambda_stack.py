from aws_cdk import(
    core as cdk,
    aws_apigateway,
    aws_lambda
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core



class CdkApigwLambdaStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here
        apigw = aws_apigateway.RestApi(
            self,
            "apigw_test"
        )

        with open("lambdas/python/function1.py", encoding="utf8") as fp:
            handler_code = fp.read()

        function1 = aws_lambda.Function(
            self,
            "function1",
            function_name="function1",
            code=aws_lambda.InlineCode(handler_code),
            handler="index.handler",
            timeout=core.Duration.seconds(20),
            runtime=aws_lambda.Runtime.PYTHON_3_9)


        apigw_test1 = apigw.root.add_resource("test1").add_method(
            http_method="GET",
            integration=aws_apigateway.LambdaIntegration(function1)
        )

        apigw_test2 = apigw_test1.resource.add_resource("test2").add_method(
            http_method="GET",
            integration=aws_apigateway.LambdaIntegration(function1)
        )

        #function2 js
        with open("lambdas/js/function2.js", encoding="utf8") as fp:
            handler_code = fp.read()

        function2 = aws_lambda.Function(
            self,
            "function2",
            function_name="function2",
            code=aws_lambda.InlineCode(handler_code),
            handler="index.handler",
            timeout=core.Duration.seconds(20),
            runtime=aws_lambda.Runtime.NODEJS_14_X)

        apigw_test_js = apigw.root.add_resource("test_js").add_method(
            http_method="GET",
            integration=aws_apigateway.LambdaIntegration(function2)
        )