# AWS IAM Access Analyzer Samples

> :warning: **NOTE:** This repository contains example code and is intended for educational purposes __only__. This code should __not__ be used in production environments. :warning:

---

Welcome! This repository contains sample code used to demo the AWS IAM Access Analyzer APIs and how you can use them to automate your policy validation workflows.

## About Access Analyzer

AWS IAM Access Analyzer helps you identify the resources in your organization and accounts, such as Amazon S3 buckets or IAM roles, that are shared with an external entity. This lets you identify unintended access to your resources and data, which is a security risk. 

Learn more about Access Analyzer here: https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html

### Policy Validation

You can validate your policies using AWS IAM Access Analyzer policy checks. Access Analyzer validates your policy against IAM policy grammar and best practices. You can view policy validation check findings that include security warnings, errors, general warnings, and suggestions for your policy. These findings provide actionable recommendations that help you author policies that are functional and conform to security best practices. 

You can learn more about this feature here: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html

---

## Samples Included in this Repository

Before walking through any of the below samples, please ensure that you are properly authenticated into the AWS CLI and are using AWS CLI v2.

Using the Access Analyzer APIs:
1. [Validate Policy API(s)](#validate-policy-apis)
1. [Access Preview API(s)](#access-preview-apis)

Automating Policy Validation with Access Analyzer:
1. [Scripted, IAM Policies that haven't been defined using Infrastructure as Code](#scripted-iam-policies-that-havent-been-defined-using-infrastructure-as-code)
1. [IAM Policies Defined using CloudFormation](#iam-policies-defined-using-cloudformation)
1. [Service Control Policies (SCP)](#service-control-policies-scp)

### Prequisites
Before running the samples in this repository, you'll need the following:
- An AWS Account
- Access to the AWS IAM Access Analyzer APIs
- [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) - please make sure that you have authenticated into the AWS CLI
- Python 3.6+
- [jq](https://stedolan.github.io/jq/download/) - a command line json processor tool
- zsh for api gateway/sns topics scripts

### How to Run the Sample Code

#### [Validate Policy API(s)](01-validate-policy/)

The ValidatePolicy API requests the validation of a policy and returns a list of findings. The findings help you identify issues and provide actionable recommendations to resolve the issue and enable you to author functional policies that meet security best practices. The ValidatePolicy API supports identity policies, service control policies, and resource policies.

The ValidatePolicy API supports resource policies from resources that are not currently supported by IAM Access Analyzer, such as SNS and API Gateway.

**Learn More:**
- [AWS API](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ValidatePolicy.html)
- [AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/validate-policy.html)

Let's get started! Open up the directory with `cd ./01-validate-policy`.


**To Validate an Identity Policy, run:**
```
. ./validate-identity-policy.sh
```

**To Validate a Service Control Policy, run:**
```
. ./validate-scp.sh
```

**To Validate a Resource Policy, run:**
```
. ./validate-resource-policy.sh
```

**To Validate all SNS topic's policies in all regions in an AWS account, run:**
```
/bin/bash ./validate-all-sns-topics.sh
```

**To Validate all API Gateways policies in all regions in an AWS account, run:**
```
/bin/bash ./validate-all-api-gateways.sh
```

#### [Access Preview API(s)](02-create-access-preview/)

In addition to helping you identify resources that are shared with an external entity, AWS IAM Access Analyzer also enables you to preview Access Analyzer findings before deploying resource permissions so you can validate that your policy changes grant only intended public and cross-account access to your resource. This helps you start with intended external access to your resources.

You can preview and validate public and cross-account access to your Amazon S3 buckets in the Amazon S3 console. You can also use Access Analyzer APIs to preview public and cross-account access for your Amazon S3 buckets, AWS KMS keys, IAM roles, Amazon SQS queues and Secrets Manager secrets by providing proposed permissions for your resource.

Gathering these findings consists of 3 API calls:
1. Create Access Preview ([AWS API](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_CreateAccessPreview.html)) ([AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/create-access-preview.html)) - launches creation of an access preview
1. Get Access Preview ([AWS API](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_GetAccessPreview.html)) ([AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/get-access-preview.html)) - gets status of access preview
1. List Access Preview Findings ([AWS API](https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAccessPreviewFindings.html)) ([AWS CLI](https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/list-access-preview-findings.html)) - retrieves a list of findings from the access preview

Let's get started! Open up the directory with `cd ./02-create-access-preview`.

In Line 13 of `queue-policy.json`, replace `<YOUR ACCOUNT ID>` with your AWS Account ID.


**To Create an Access Preview, run:**
```
. ./create-access-preview.sh
```

**To Get an Access Preview Status, run:**
```
. ./get-access-preview.sh
```

**Once the `status` from the previous command shows as `"COMPLETED"`  run the following command to list the Access Preview findings:**
```
. ./list-access-preview-findings.sh
```


#### [Scripted, IAM Policies that haven't been defined using Infrastructure as Code](03-no-iac/)

In this example, we place all of our policies into a folder called `policies/` and use a Python script to orchestrate the IAM Access Analyzer API calls that will validate and return findings on the policies that we have created.  The script relies on a specific directory structure to classify each policy when running CreateAccessPreview.

Let's get started! Open up the directory with `cd ./03-no-iac`.

**To Analyze our policies and return findings, run:**
```
python analyze.py
```

After running this command, you will see a list of findings and recommendations for remediation.

#### [IAM Policies Defined using CloudFormation](04-cloudformation/)

**Using the IAM Policy Validator tool**: In this example, we will demonstrate how to run automated policy validation on IAM policies defined in a CloudFormation template. To do this, we use the [IAM Policy Validator for AWS CloudFormation command line tool](https://github.com/awslabs/aws-cloudformation-iam-policy-validator). You can learn more about this tool and how to use it in the blog post [Validate IAM policies in CloudFormation templates using IAM Access Analyzer](https://aws.amazon.com/blogs/security/validate-iam-policies-in-cloudformation-templates-using-iam-access-analyzer/).

Let's get started! Open up the directory with `cd ./04-cloudformation`.

Each of the scripts that we will use in this section installs IAM Policy Validator with the following command:
```
pip install cfn-policy-validator
```

**... with AWS CloudFormation templates**: First, we'll show you how to use the IAM Policy Validator tool with a basic **AWS CloudFormation template**. 

Navigate to the `04-cloudformation/01-policy-validator` folder. In this folder, we've defined a CloudFormation template in `template.json`. The `run-policy-validator.sh` script first runs the `cfn-policy-validator validate` command on the template to validate the resources defined in the template using Access Analyzer and then outputs any findings to a new `findings.json` file. 

From the `01-policy-validator` folder, run the following command to test the IAM Policy Validator tool on a CloudFormation template:
```
. ./run-policy-validator.sh
```

From the `01-policy-validator` folder, open the `findings.json` file to inspect the findings produced.


**... with an AWS CDK app**: Next, we'll show you how to use the IAM Policy Validator tool with an **AWS CDK application**. 

Navigate to the `04-cloudformation/02-cdk` folder. In this folder, the `run-policy-validator.sh` script first uses `cdk synth` to generate a CloudFormation template from the CDK code and then runs the same `cfn-policy-validator validate` command to validate the resources defined in the template using Access Analyzer and output any findings to a new `findings.json` file.

From the `04-cloudformation/02-cdk` folder, run the folling command to test the IAM Policy Validator tool on an AWS CDK application:
```
. ./run-policy-validator.sh
```
From the `01-policy-validator` folder, open the `findings.json` file to inspect the findings produced.


#### [Service Control Policies (SCP)](06-scps/)

In this example, we will demonstrate how to run automated policy validation on our SCPs for an AWS Organization. We only have the option to run the Validate Policy API here. Our policies are stored in a folder named `policies/`

Let's get started! Open up the directory with `cd ./05-scps`.

**To validate our SCPs, run:**
```
. ./validate.scp.sh
```


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

