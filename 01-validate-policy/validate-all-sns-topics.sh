#!/bin/zsh

#declare regions
echo "Getting active regions for this AWS account"
regions=$(aws ec2 describe-regions --query "Regions[*].RegionName" --output text)

setopt SH_WORD_SPLIT #required for bash-like forloops in zsh

echo "Beginning check of SNS topics"
echo ""
echo ""

#iterate over regions, get a list of topics, and evaluate send them to access analyzer
for region in $regions;
do
topics=$(aws sns list-topics --query "Topics[*].TopicArn" --output text --region $region)
    for topicArn in $topics;
    do
        policy=$(aws sns get-topic-attributes --topic-arn $topicArn --query Attributes.Policy --output text --region $region)
        echo "Checking topic ARN $topicArn in region $region..."
        output=$(aws accessanalyzer validate-policy --policy-type RESOURCE_POLICY --policy-document $policy --no-cli-pager --output json )
        echo "$output"
        if [[ -z $output ]]
        then
            echo "No Findings From Access Analyzer for $topicArn"
        fi
        echo "------------------"
        echo ""
    done
done
