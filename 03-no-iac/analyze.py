import boto3
import json
import os

aa_client = boto3.client('accessanalyzer')

this_scripts_directory = os.path.dirname(os.path.realpath(__file__))
policies_directory = os.path.join(this_scripts_directory, 'policies')

for root, dirs, files in os.walk(policies_directory, topdown=True):
    parent_directory = os.path.dirname(root)
    if parent_directory.lower() == 'identity':
        policy_type = 'IDENTITY_POLICY'
    else:
        policy_type = 'RESOURCE_POLICY'

    for file in files:
        policy_document_filename = os.path.join(root, file)

        with open(policy_document_filename, 'r') as policy_document:
            policy_document_json = json.load(policy_document)
            validate_policy_response = aa_client.validate_policy(
                policyDocument=json.dumps(policy_document_json),
                policyType=policy_type
            )
            print(validate_policy_response)
    

