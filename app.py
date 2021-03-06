#!/usr/bin/env python3
import os

from aws_cdk import core as cdk

# For consistency with TypeScript code, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core

from cdk_apigw_lambda.cdk_apigw_lambda_stack import CdkApigwLambdaStack

codebuild_number=os.environ.get('CODEBUILD_BUILD_NUMBER', '0')

app = core.App()

# env=core.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION'))
env=core.Environment(account='059362432186', region='us-east-1')

CdkApigwLambdaStack(app,
    "CdkApigwLambdaStack",
    env=env,
    # codebuild_number="3"
)
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #,

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=core.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    # )

#Pipeline
from cdk_apigw_lambda_pipeline.cdk_apigw_lambda_pipeline_stack import CdkApigwLambdaPipelineeStack

CdkApigwLambdaPipelineeStack(app, "CdkApigwLambdaPipelineeStack")


app.synth()
