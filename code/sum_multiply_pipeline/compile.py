import os
import requests

from kfp import components
from kfp.compiler import Compiler
from kfp.dsl import pipeline


@pipeline(name="multiply_sum_pipeline", description="multiply then sum the numbers")
def pipeline(num1: float, num2: float, num3: float):
    username = os.environ.get("GITHUB_USERNAME")
    token = os.environ.get("GITHUB_TOKEN")
    url_op1 = "https://raw.githubusercontent.com/tiketdatastanley/centralized-operators/release/sum_op/v1.0/manifests/sum_op.yaml"
    url_op2 = "https://raw.githubusercontent.com/tiketdatastanley/centralized-operators/release/multiply_op/v1.0/manifests/multiply_op.yaml"
    op1 = components.load_component_from_url(url_op1, auth=(username, token))(num1, num2)
    op1.container.set_image_pull_policy("Always")
    output_op1 = op1.outputs["output"]
    op2 = components.load_component_from_url(url_op2, auth=(username, token))(output_op1, num3)
    op2.container.set_image_pull_policy("Always")

if __name__ == "__main__":
    Compiler().compile(
        pipeline_func=pipeline,
        package_path="./manifests/sum_multiply_pipeline.yaml",
    )