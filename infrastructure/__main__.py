import json
import os
import pulumi
from pulumi_aws import apigateway, cloudwatch
import yaml


def load_api_schema(schema_file: str) -> str:
    schema_path = os.path.join(os.path.dirname(__file__), schema_file)

    with open(schema_path, "r") as f:
        if schema_file.endswith(".yaml") or schema_file.endswith(".yml"):
            return json.dumps(yaml.safe_load(f))

        return json.dumps(json.load(f))


stack = pulumi.get_stack()
config = pulumi.Config()
app_name = config.require("app_name")

api = apigateway.RestApi(
    f"{app_name}-api-{stack}",
    name=f"{app_name}-api-{stack}",
    description=f"{app_name.title()} API",
    body=load_api_schema("openapi.yaml")
)

api_deployment = apigateway.Deployment(
    f"{app_name}-api-deployment-{stack}",
    rest_api=api.id,
    triggers={
        "redeployment": load_api_schema("openapi.yaml")
    },
    opts=pulumi.ResourceOptions(depends_on=[api])
)

api_log_group = cloudwatch.LogGroup(
    f"{app_name}-api-log-group-{stack}",
    name=f"/aws/apigateway/{app_name}-{stack}",
    retention_in_days=1,
)

stage = apigateway.Stage(
    f"{app_name}-stage-{stack}",
    deployment=api_deployment.id,
    rest_api=api.id,
    stage_name=stack,
    description=f"{app_name.title()} API {stack} stage",
    access_log_settings=apigateway.StageAccessLogSettingsArgs(
        destination_arn=api_log_group.arn,
        format=json.dumps({
            "requestId": "$context.requestId",
            "ip": "$context.identity.sourceIp",
            "caller": "$context.identity.caller",
            "user": "$context.identity.user",
            "requestTime": "$context.requestTime",
            "httpMethod": "$context.httpMethod",
            "resourcePath": "$context.resourcePath",
            "status": "$context.status",
            "protocol": "$context.protocol",
            "responseLength": "$context.responseLength",
            "responseLatency": "$context.responseLatency"
        })
    )
)

pulumi.export(
    "api_url",
    pulumi.Output.concat(
        "https://",
        api.id,
        ".execute-api.",
        pulumi.Config("aws").require("region"),
        ".amazonaws.com/",
        stack
    )
)

pulumi.export("api_log_group_name", api_log_group.name)
