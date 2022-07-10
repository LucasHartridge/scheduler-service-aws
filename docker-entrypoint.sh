#!/bin/bash

echo "Executing docker entrypoint"

LAMBDA_VARIABLES="Variables={\
SCHEDULER_SERVICE_URL=${LOCALSTACK_DOCKER_EXTERNAL},\
FUNCTION_NAME=${FUNCTION_NAME},\
AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION},\
AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID},\
AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY},\
AWS_SESSION_TOKEN=${AWS_SESSION_TOKEN},\
COIN_API_KEY=${COIN_API_KEY},\
COIN_API_URL=${COIN_API_URL}\
}"

aws --endpoint-url ${SCHEDULER_SERVICE_URL} lambda create-function \
  --code S3Bucket="__local__",S3Key="${S3_KEY}" \
  --function-name ${FUNCTION_NAME} \
	--role role-dummy \
  --handler ${HANDLER} \
  --runtime ${RUNTIME}  \
  --environment ${LAMBDA_VARIABLES}

# Verify email
aws --endpoint-url ${SCHEDULER_SERVICE_URL} ses verify-email-identity \
  --email-address ${EMAIL_SENDER} \
  --region ${AWS_DEFAULT_REGION} 

# Infinite Loop to simulate AWS Event handler invoking the lambda every minute
while true
do
  CURRENT_TIME=$(date +"%Y-%m-%dT%H:00:00Z")
  echo "Invoke Lambda with time : $CURRENT_TIME"
  aws --endpoint-url ${SCHEDULER_SERVICE_URL} lambda invoke --function-name ${FUNCTION_NAME} --invocation-type Event --payload '{"version": "0", "id": "1", "detail-type": "Scheduled Event", "source": "aws.events", "account": "1", "time": "'${CURRENT_TIME}'", "region": "us-west-2", "resources": [ "arn:aws:events:us-east-1:123456789012:rule/my-scheduled-rule"], "detail": "{}" }' response.json 
  sleep 60
done