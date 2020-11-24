import aws_cdk.aws_lambda as _lambda
from aws_cdk import core
from aws_cdk.aws_apigatewayv2 import (
    HttpApi,
    HttpMethod,
    HttpIntegration,
    HttpIntegrationType,
)
from aws_cdk.aws_apigatewayv2_integrations import (
    LambdaProxyIntegration,
    HttpProxyIntegration,
)
from aws_cdk.aws_iam import PolicyStatement, Effect
from aws_cdk.aws_s3 import Bucket
import aws_cdk.aws_s3_deployment as s3deploy


class CdkStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        credentials_secret_name = "advent/gdrive-service-credentials"
        super().__init__(scope, id, **kwargs)

        advent_function = _lambda.Function(
            self,
            f"{id}-function",
            code=_lambda.Code.from_asset("_build/_build.zip"),
            handler="functions/advent/handler.handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment={
                "GDRIVE_CREDENTIALS_SECRET": credentials_secret_name,
                "SHEET_ID": "foo",
                "SHEET_RANGE": "Sheet1!A:E",
            },
            timeout=core.Duration.seconds(10),
        )
        advent_function.add_to_role_policy(
            PolicyStatement(
                effect=Effect.ALLOW,
                actions=["secretsmanager:GetSecretValue"],
                resources=["*"],
            )
        )

        api = HttpApi(self, f"{id}-api")
        api.add_routes(
            path="/",
            methods=[HttpMethod.GET],
            integration=(LambdaProxyIntegration(handler=advent_function)),
        )

        # s3_bucket = Bucket(
        #     self,
        #     f"{id}-website-bucket",
        #     public_read_access=True,
        #     website_index_document="index.html",
        #     website_error_document="404.html",
        # )
        # deployment = s3deploy.BucketDeployment(
        #     self,
        #     f"{id}-website-deployment",
        #     sources=[s3deploy.Source.asset("website")],
        #     destination_bucket=s3_bucket,
        # )
        #
        # bucket_integration = HttpProxyIntegration(
        #     url=f"{s3_bucket.bucket_website_url}/{{proxy}}",
        # )
        # api.add_routes(
        #     path="/{proxy+}",
        #     methods=[HttpMethod.GET],
        #     integration=bucket_integration,
        # )
        core.CfnOutput(self, f"{id}-url", value=api.api_endpoint)
