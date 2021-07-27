from collections import defaultdict

from access_preview import SQSAccessPreview, RoleTrustPolicyAccessPreview
from colors import colors

import boto3
import json
import os
import sys


aa_client = boto3.client('accessanalyzer')


def validate_policy(full_policy_filename, policy_document):
    parent_directory = os.path.basename(os.path.dirname(full_policy_filename))
    if parent_directory.lower() == 'identity':
        policy_type = 'IDENTITY_POLICY'
    else:
        policy_type = 'RESOURCE_POLICY'

    validate_policy_response = aa_client.validate_policy(
        policyDocument=json.dumps(policy_document),
        policyType=policy_type
    )

    findings = []
    for finding in validate_policy_response['findings']:
        findings.append(finding)

    return findings


def get_access_preview_findings(full_policy_filename, policy_document):
    parent_directory = os.path.basename(os.path.dirname(full_policy_filename)).lower()
    if parent_directory == 'role':
        access_preview = RoleTrustPolicyAccessPreview()
    elif parent_directory == 'sns':
        return []
    elif parent_directory == 'sqs':
        access_preview = SQSAccessPreview()
    elif parent_directory == 's3':
        return []
    elif parent_directory == 'kms':
        return []
    else:
        return []

    access_preview.create(policy_document)
    access_preview.get()
    return access_preview.list_findings()


def get_count(results, finding_type):
    return len([finding for filename, findings in results.items()
                for finding in findings if finding['findingType'] == finding_type])


def validate():
    this_scripts_directory = os.path.dirname(os.path.realpath(__file__))
    policies_directory = os.path.join(this_scripts_directory, 'policies')

    results = defaultdict()

    print(f'{colors.OKBLUE}Starting analysis of {policies_directory}..')
    print()

    for root, dirs, files in os.walk(policies_directory, topdown=True):
        for file in files:
            full_policy_filename = os.path.join(root, file)
            with open(full_policy_filename, 'r') as file:
                policy_document = json.load(file)

                findings = []
                findings.extend(validate_policy(file.name, policy_document))
                findings.extend(get_access_preview_findings(file.name, policy_document))

            results[full_policy_filename] = findings

    should_exit_with_non_zero_code = False

    for filename, findings in results.items():
        print(f'{colors.OKBLUE}{filename}')
        for finding in findings:
            finding_type = finding['findingType']
            if finding_type == 'ERROR' or finding_type == 'SECURITY_WARNING':
                should_exit_with_non_zero_code = True
                print(f'{colors.FAIL}{finding}')
                print()
            else:
                print(f'{colors.WARNING}{finding}')
                print()

        print(colors.RESET)

    print(f'{colors.OKBLUE}ERRORS: {get_count(results, "ERROR")}')
    print(f'{colors.OKBLUE}SECURITY_WARNINGS: {get_count(results, "SECURITY_WARNING")}')
    print(f'{colors.OKBLUE}WARNINGS: {get_count(results, "WARNING")}')
    print(f'{colors.OKBLUE}SUGGESTIONS: {get_count(results, "SUGGESTION")}')

    if should_exit_with_non_zero_code:
        print(f'{colors.FAIL}FAILED: ERROR or SECURITY_WARNING findings.')
        print(colors.RESET)
        sys.exit(1)


if __name__ == "__main__":
    validate()
