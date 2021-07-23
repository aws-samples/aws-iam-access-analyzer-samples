import boto3
import json
import time

from abc import ABC

client = boto3.client('accessanalyzer')

list_analyzers_response = client.list_analyzers(
	type='ACCOUNT'
)

first_active_analyzer = next((analyzer for analyzer in list_analyzers_response['analyzers'] if analyzer['status'] == 'ACTIVE'), None)
if first_active_analyzer is not None:
	analyzer_arn = first_active_analyzer['arn']
else:
	raise Exception('No active analyzers found in account.  You must create an analyzer in your account to run access previews.')

sts_client = boto3.client('sts')
sts_client.get_caller_identity()
identity = sts_client.get_caller_identity()
account_id = identity['Account']

parts = identity['Arn'].split(':')
partition = parts[1]

region = client.meta.region_name


class AccessPreview(ABC):
	def __init__(self):
		self.preview_id = None

	def create(self, policy):
		configuration = self._build_configuration(policy)
		response = client.create_access_preview(
			analyzerArn=analyzer_arn,
			configurations=configuration
		)
		self.preview_id = response['id']

	def get(self):
		number_of_attempts = 0
		while True:
			response = client.get_access_preview(
				accessPreviewId=self.preview_id,
				analyzerArn=analyzer_arn
			)
			status = response['accessPreview']['status']

			if status == 'CREATING':
				number_of_attempts = number_of_attempts + 1
				if number_of_attempts >= 30:
					raise Exception(f'Timed out after 1 minute waiting for access analyzer preview to create.')

				time.sleep(2)
			else:
				break

		if status == 'FAILED':
			reason = response["accessPreview"]["statusReason"]["code"]
			raise Exception(f'Failed to create access preview. Reason: {reason}')

		# status is created if method makes it to this point
		return status

	def list_findings(self):
		findings = []
		paginator = client.get_paginator('list_access_preview_findings')
		for page in paginator.paginate(accessPreviewId=self.preview_id, analyzerArn=analyzer_arn):
			for finding in page['findings']:
				findings.append({'findingType': 'SECURITY_WARNING', 'details': finding})

		return findings


class SQSAccessPreview(AccessPreview):
	@staticmethod
	def _build_configuration(policy):
		resource = policy['Statement'][0]['Resource']
		if isinstance(resource, list):
			resource = resource[0]

		if resource == "*":
			resource = f'arn:{partition}:sqs:{region}:{account_id}:MyQueue'

		return {
			resource: {
				'sqsQueue': {
					'queuePolicy': json.dumps(policy)
				}
			}
		}
