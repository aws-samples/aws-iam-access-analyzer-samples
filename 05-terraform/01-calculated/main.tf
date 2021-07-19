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



resource "aws_s3_bucket" "test_bucket" {
  bucket = "my-test-bucket"
}

data "aws_iam_policy_document" "example_policy_document" {
  statement {
    actions = [
      "s3:*",
    ]

    resources = [
      aws_s3_bucket.test_bucket.arn,
      "${aws_s3_bucket.test_bucket.arn}/*"
    ]
  }
}

resource "aws_iam_policy" "example" {
  name   = "example_policy"
  policy = data.aws_iam_policy_document.example_policy_document.json
}