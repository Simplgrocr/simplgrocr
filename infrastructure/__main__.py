import json
import os
import pulumi
from pulumi_aws import apigateway


def load_api_schema(schema_file: str) -> str:
    schema_path = os.path.join(os.path.dirname(
        __file__), "schemas", schema_file)

    with open(schema_path, "r") as f:
        return json.dumps(json.load(f))


api = apigateway.RestApi(
    "SimplgrocrAPI",
    name="SimplgrocrAPI",
    description="Simplgrocr API"
)

api_model = apigateway.Model(
    "SimplgrocrAPIModel",
    rest_api=api.id,
    name="SimplgrocrAPIModel",
    description="Simplgrocr API Model",
    content_type="application/json",
    schema=load_api_schema("api_model.json")
)
