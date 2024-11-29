import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import * as dotenv from 'dotenv';

import * as IndexStack from '../lib';

beforeAll(() => {
  dotenv.config();
});

test('ECR Repository Created', () => {
  const app = new cdk.App();
  const stack = new IndexStack.IndexStack(app, 'MyTestStack');
  const template = Template.fromStack(stack);

  template.resourceCountIs('AWS::ECR::Repository', 1);
  template.hasResourceProperties('AWS::ECR::Repository', {
    RepositoryName: 'fastapi-crud-app',
  });
});
