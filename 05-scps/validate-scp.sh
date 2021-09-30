#!/bin/bash

export PAGER='cat'

NUMBER_OF_ERRORS=0
NUMBER_OF_WARNINGS=0

for file in policies/*; do
    echo $file
    echo "Validating policy $file.."
    FINDINGS=$(aws accessanalyzer validate-policy --policy-document file://"$file" --policy-type SERVICE_CONTROL_POLICY)

    ERRORS=$(echo $FINDINGS | jq '.findings | map(select(.findingType == "ERROR" or .findingType == "SECURITY_WARNING"))')
    WARNINGS=$(echo $FINDINGS | jq '.findings | map(select(.findingType == "WARNING" or .findingType == "SUGGESTION"))')

    ERRORS_LENGTH=$(echo $ERRORS | jq '. | length')
    WARNINGS_LENGTH=$(echo $WARNINGS | jq '. | length')

    NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS + ERRORS_LENGTH))
    NUMBER_OF_WARNINGS=$((NUMBER_OF_WARNINGS + WARNINGS_LENGTH))

    echo $ERRORS | jq .
done

echo Errors: $NUMBER_OF_ERRORS, Warnings: $NUMBER_OF_WARNINGS