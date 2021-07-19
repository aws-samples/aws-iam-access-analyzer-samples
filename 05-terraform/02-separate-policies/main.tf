resource "aws_s3_bucket" "test_bucket" {
  bucket = "my-test-bucket"
}

resource "aws_iam_policy" "example" {
  name   = "example_policy"
  policy = file("${path.module}/iam-policies/example-s3-policy.json")
}




terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}
