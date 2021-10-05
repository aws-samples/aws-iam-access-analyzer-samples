
ANALYZER_ARN=$(aws accessanalyzer list-analyzers --query "analyzers[?status=='ACTIVE'].arn | [0]" --output text)
ACCOUNT_ID=$(aws sts get-caller-identity --output text | cut -f1 -d$'\t')

QUEUE_POLICY=$(cat queue-policy.json | jq -c . | sed "s/<YOUR ACCOUNT ID>/${ACCOUNT_ID}/") 

CONFIGURATIONS=$(jq -n -c --arg account_id "$ACCOUNT_ID" --arg queue_policy "$QUEUE_POLICY" '{"arn:aws:sqs:us-east-1:\($account_id):MyQueue": {sqsQueue: {queuePolicy: $queue_policy}}}')

echo $CONFIGURATIONS | jq .

ACCESS_PREVIEW_ID=$(aws accessanalyzer create-access-preview --configurations $CONFIGURATIONS --analyzer-arn $ANALYZER_ARN --query id --output text)
echo $ACCESS_PREVIEW_ID