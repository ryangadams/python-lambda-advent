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

        google_sheet_id = self.node.try_get_context("sheet_id")

        google_sheet_range = self.node.try_get_context("sheet_range")

        advent_function = _lambda.Function(
            self,
            f"{id}-function",
            code=_lambda.Code.from_asset("_build/_build.zip"),
            handler="functions/advent/handler.handler",
            runtime=_lambda.Runtime.PYTHON_3_8,
            environment={
                "GDRIVE_CREDENTIALS_SECRET": credentials_secret_name,
                "SHEET_ID": google_sheet_id,
                "SHEET_RANGE": google_sheet_range,
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

        core.CfnOutput(self, f"{id}-url", value=api.api_endpoint)
