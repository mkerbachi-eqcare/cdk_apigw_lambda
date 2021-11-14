from aws_cdk import (
    aws_s3 as s3,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    core as cdk
)

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core


class CdkApigwLambdaPipelineeStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        print(kwargs.values())
        # self.codebuild_number = kwargs['codebuild_number']


        # Stage: Code Checkout

        github_checkout = codebuild.Project(
            self,
            "Checkout code",
            project_name="CheckoutCode_Projet",
            description="Checkout code from Github",
            source=codebuild.Source.git_hub(
                owner="mkerbachi-eqcare",
                repo="cdk_apigw_lambda",
                report_build_status=False,
                webhook=True,
                webhook_filters=[codebuild.FilterGroup.in_event_of(
                    codebuild.EventAction.PUSH).and_branch_is(branch_name="*")
                ]
            ),
            build_spec=codebuild.BuildSpec.from_source_filename(filename="cdk_apigw_lambda_pipeline//pipeline/buildspec_CheckoutCode_Projet.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged=False
            )
        )

        codebuild_bucket = s3.Bucket(
            self,
            id="cdk-codebuild-bucket",
            bucket_name="cdk-codebuild-bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,  #Required by Codebuild to run
            removal_policy=core.RemovalPolicy.DESTROY
        )

        github_checkout.add_to_role_policy(
            statement=iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=[
                    "s3:PutObject",
                    "s3:DeleteObject",
                ],
                resources=[codebuild_bucket.bucket_arn + "/*"],
            )
        )



        source_output = codepipeline.Artifact()

        cdk_code_s3sourceaction = codepipeline_actions.S3SourceAction(
            action_name="cdk_code_bucket_action",
            bucket=codebuild_bucket,
            bucket_key="cdk_code.zip",
            output=source_output,
            trigger=codepipeline_actions.S3Trigger.EVENTS,
            variables_namespace="SourceCDKVariablesNamespace"
        )



        # Stage: Code build

        build_stage = codebuild.PipelineProject(
            self,
            "Build code",
            project_name="BuildCode_Project",
            description="Code build",
            build_spec=codebuild.BuildSpec.from_source_filename(filename="cdk_apigw_lambda_pipeline//pipeline/buildspec_BuildCode_Project.yml"),
            environment=codebuild.BuildEnvironment(
                build_image=codebuild.LinuxBuildImage.STANDARD_5_0,
                privileged=False
            )
        )

        build_stage.add_to_role_policy(
            statement=iam.PolicyStatement(
                sid="ApplicationStackPermissions",
                effect=iam.Effect.ALLOW,
                actions=[
                    "cloudformation:DescribeStacks",
                    "cloudformation:GetTemplate",
                    "cloudformation:DescribeChangeSet",
                    "cloudformation:DeleteChangeSet",
                    "cloudformation:CreateChangeSet",
                    "cloudformation:ExecuteChangeSet"
                ],
                resources=[
                    "arn:aws:cloudformation:us-east-1:059362432186:stack/CdkApigwLambdaStack/*"
                ]
            )
        )

        build_stage.add_to_role_policy(
            statement=iam.PolicyStatement(
                sid="CDKStackPermissions",
                effect=iam.Effect.ALLOW,
                actions=[
                    "cloudformation:DescribeStacks"
                ],
                resources=[
                    "arn:aws:cloudformation:us-east-1:059362432186:stack/CDKToolkit/*"
                ]
            )
        )

        # build_stage.add_to_role_policy(
        #     statement=iam.PolicyStatement(
        #         sid="AllowCDKBucketAccess",
        #         effect=iam.Effect.ALLOW,
        #         actions=["s3:*"],
        #         resources=["arn:aws:s3:::cdktoolkit-stagingbucket-*"]
        #     )
        # )


        cdk_code_codebuildaction = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=build_stage,
            input=source_output,
            variables_namespace="BuildCDKVariablesNamespace"
        )

        ############################
        # CodePipeline
        ############################

        codepipeline_bucket = s3.Bucket(
            self,
            id="cdk-codepipeline-bucket",
            bucket_name="cdk-codepipeline-bucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True,  #Required by Codebuild to run
            removal_policy=core.RemovalPolicy.DESTROY
        )

        pipeline = codepipeline.Pipeline(
            self,
            "ApiGwLambda_Pipeline",
            artifact_bucket=codebuild_bucket,
            pipeline_name="ApiGwLambda_Pipeline",
            stages=[codepipeline.StageProps(
                stage_name="CheckoutCode_Stage",
                actions=[cdk_code_s3sourceaction]
            ),
            codepipeline.StageProps(
                stage_name="BuildCode_Stage",
                actions=[cdk_code_codebuildaction]
            )]
        )

        print(pipeline.is_construct)
        print(pipeline.is_resource)