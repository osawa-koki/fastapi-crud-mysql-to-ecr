import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ecr from 'aws-cdk-lib/aws-ecr';

export class IndexStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, {
      ...props,
      stackName: process.env.STACK_NAME!,
    });

    const repository = new ecr.Repository(this, process.env.STACK_NAME!, {
      repositoryName: process.env.ECR_REPOSITORY_NAME!,
    });

    new cdk.CfnOutput(this, 'RepositoryURI', {
      value: repository.repositoryUri,
      description: 'The URI of the ECR repository',
    });
  }
}
