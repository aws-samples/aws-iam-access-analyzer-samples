export PAGER='cat'

NUMBER_OF_ERRORS=0
NUMBER_OF_WARNINGS=0

for file in policies/identity/*; do
    echo "Validating policy $file.."
    FINDINGS=$(aws accessanalyzer validate-policy --policy-document file://"$file" --policy-type IDENTITY_POLICY)

    ERRORS=$(echo $FINDINGS | jq '.findings[] | select(.findingType == "ERROR" or .findingType == "SECURITY_WARNING")')
    WARNINGS=$(echo $FINDINGS | jq '.findings[] | select(.findingType == "WARNING" or .findingType == "SUGGESTION")')

    ERRORS=$(echo $FINDINGS | jq '.findings | map(select(.findingType == "ERROR" or .findingType == "SECURITY_WARNING"))')
    ERRORS_LENGTH=$(echo $ERRORS | jq '. | length')
    NUMBER_OF_ERRORS=$((NUMBER_OF_ERRORS + ERRORS_LENGTH))

    echo $ERRORS | jq .
done

echo Errors: $NUMBER_OF_ERRORS, Warnings: $NUMBER_OF_WARNINGS