# AWS IAM Access Analyzer Samples

Welcome! This repository contains sample code used to demo the AWS IAM Access Analyzer APIs and how you can use them to automate your policy validation workflows.

> :warning: **NOTE:** This repository contains example code and is intended for educational purposes __only__. This code should __not__ be used in production environments. :warning:

## About Access Analyzer

AWS IAM Access Analyzer helps you identify the resources in your organization and accounts, such as Amazon S3 buckets or IAM roles, that are shared with an external entity. This lets you identify unintended access to your resources and data, which is a security risk. 

Learn more about Access Analyzer here: https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html

### Policy Validation

You can validate your policies using AWS IAM Access Analyzer policy checks. Access Analyzer validates your policy against IAM policy grammar and best practices. You can view policy validation check findings that include security warnings, errors, general warnings, and suggestions for your policy. These findings provide actionable recommendations that help you author policies that are functional and conform to security best practices. 

You can learn more about this feature here: https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html

## Samples Included in this Repository

Before walking through any of the below samples, please ensure that you are properly authenticated into the AWS CLI and are using AWS CLI v2.

Using the Access Analyzer APIs:
1. [(01) Validate Policy API(s)](01-validate-policy/)
1. [(02) Access Preview API(s)](02-create-access-preview/)

Automating Policy Validation with Access Analyzer:
1. [(03) Scripted, IAM Policies that haven't been defined using Infrastructure as Code](03-no-iac/)
1. [(04) IAM Policies Defined using CloudFormation](04-cloudformation/)
1. [(05) Service Control Policies (SCP)](06-scps/)


### AWS IAM Access Analyzer APIs

#### [(01) Validate Policy API(s)](01-validate-policy/)

Requests the validation of a policy and returns a list of findings. The findings help you identify issues and provide actionable recommendations to resolve the issue and enable you to author functional policies that meet security best practices.

**Learn More:**
AWS API Call: https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ValidatePolicy.html
AWS CLI Call: https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/validate-policy.html

Let's get started! Open up the directory with `cd ./01-validate-policy`.


**To Validate an Identity Policy, run:**
```
sh validate-identity-policy.sh
```

**To Validate a Service Control Policy, run:**
```
sh validate-scp.sh
```

#### [(02) Access Preview API(s)](02-create-access-preview/)

In addition to helping you identify resources that are shared with an external entity, AWS IAM Access Analyzer also enables you to preview Access Analyzer findings before deploying resource permissions so you can validate that your policy changes grant only intended public and cross-account access to your resource. This helps you start with intended external access to your resources.

You can preview and validate public and cross-account access to your Amazon S3 buckets in the Amazon S3 console. You can also use Access Analyzer APIs to preview public and cross-account access for your Amazon S3 buckets, AWS KMS keys, IAM roles, Amazon SQS queues and Secrets Manager secrets by providing proposed permissions for your resource.

Gathering these findings consists of 3 API calls:
1. Create Access Preview (AWS API Call)[https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_CreateAccessPreview.html] (AWS CLI Call)[https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/create-access-preview.html] - launches creation of an access preview
1. Get Access Preview (AWS API Call)[https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_GetAccessPreview.html] (AWS CLI Call)[https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/get-access-preview.html] - gets status of access preview
1. List Access Preview Findings (AWS API Call)[https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAccessPreviewFindings.html] (AWS CLI Call)[https://awscli.amazonaws.com/v2/documentation/api/latest/reference/accessanalyzer/list-access-preview-findings.html] - retrieves a list of findings from the access preview

Let's get started! Open up the directory with `cd ./02-create-access-preview`.


**To Create an Access Preview, run:**
```
sh create-access-preview.sh
```

**To Get an Access Preview Status, run:**
```
sh get-access-preview.sh
```

**Once Status = Completed, Get Access Preview Findings, run:**
```
sh list_access_preview_findings.sh
```

### Automate Policy Validation

Customers often look to automate policy validation in their deployment cycle. Here, we'll take a look at some ways to do that.

#### [(03) Scripted, IAM Policies that haven't been defined using Infrastructure as Code](03-no-iac/)

In this example, we place all of our policies into a folder called `policies/` and use a Python script to orchestrate the IAM Access Analyzer API calls that will validate and return findings on the policies that we have created.  The script relies on a specific directory structure to classify each policy when running CreateAccessPreview.

Let's get started! Open up the directory with `cd ./03-no-iac`.

**To Analyze our policies and return findings, run:**
```
python analyze.py
```

#### [(04) IAM Policies Defined using CloudFormation](04-cloudformation/)

In this example, we

Let's get started! Open up the directory with `cd ./04-cloudformation`.


#### [(05) Service Control Policies (SCP)](06-scps/)

In this example, we will demonstrate how to run automated policy validation on our SCPs for an AWS Organization. We only have the option to run the Validate Policy API here. Our policies are stored in a folder named `policies/`

Let's get started! Open up the directory with `cd ./06-scps`.

**To validate our SCPs, run:**
```
sh validate.scp.sh
```


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

