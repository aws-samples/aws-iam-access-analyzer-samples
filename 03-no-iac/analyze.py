from collections import defaultdict
from colors import colors

import boto3
import json
import os
import sys


aa_client = boto3.client('accessanalyzer')


def validate_policy(full_policy_filename):
    parent_directory = os.path.basename(os.path.dirname(full_policy_filename))
    if parent_directory.lower() == 'identity':
        policy_type = 'IDENTITY_POLICY'
    else:
        policy_type = 'RESOURCE_POLICY'

    with open(full_policy_filename, 'r') as policy_document:
        policy_document_json = json.load(policy_document)
        validate_policy_response = aa_client.validate_policy(
            policyDocument=json.dumps(policy_document_json),
            policyType=policy_type
        )

        findings = []
        for finding in validate_policy_response['findings']:
            findings.append(finding)

        return findings


def get_access_preview_findings(root, policy_filename):
    pass


def validate():
    this_scripts_directory = os.path.dirname(os.path.realpath(__file__))
    policies_directory = os.path.join(this_scripts_directory, 'policies')

    results = defaultdict()

    print(f'{colors.OKBLUE}Starting analysis of {policies_directory}..')
    print()

    for root, dirs, files in os.walk(policies_directory, topdown=True):
        for file in files:
            full_policy_filename = os.path.join(root, file)

            findings = validate_policy(full_policy_filename)
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

    if should_exit_with_non_zero_code:
        print(f'{colors.FAIL}FAILED: ERROR or SECURITY_WARNING findings.')
        print(colors.RESET)
        sys.exit(1)


if __name__ == "__main__":
    validate()
