#!/bin/zsh

#declare regions
echo "Getting active regions for this AWS account"
regions=$(aws ec2 describe-regions --query "Regions[*].RegionName" --output text)

setopt SH_WORD_SPLIT #required for bash-like forloops in zsh

echo "Beginning check of Rest API Gateways"
echo ""
echo ""

export AWS_MAX_ATTEMPTS=6 #allow for aggressive retries/max attempts

#iterate over regions, get a list of REST (v1) apis, and check.
for region in $regions;
do
restapis=$(aws apigateway get-rest-apis --query "items[*].id" --output text --no-cli-pager --region $region)
    for restapi in $restapis;
    do
        policy=$(aws apigateway get-rest-api --rest-api-id $restapi --query "policy" --output text --no-cli-pager --region $region)
        echo "Checking Rest API ID $restapi in region $region..."
        if [[ $policy != "None" ]] #As policy on restapi is optional
        then
            policyjson=$(echo $policy | sed 's/\\//g') #remove slashes from API gateway policies so they're json
            output=$(aws accessanalyzer validate-policy --policy-type RESOURCE_POLICY --policy-document $policyjson --no-cli-pager --output json)
        else
            echo "No Resource Policy On Restapi $restapi"
        fi

        if [[ -z $output ]] || [[ -z $(echo $output | jq ".[][]") ]]
        then
            echo "No Findings From Access Analyzer for $restapi"
        else
            echo "findings for $restapi"
            echo "$output"
            output=""
        fi
        echo "------------------"
        echo ""
    done
done