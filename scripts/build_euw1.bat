cd ..
if not exist "tmp" mkdir tmp

echo "****************Packaging SAM****************"
aws cloudformation package --template-file sam/lambda-gateway-sam.yml --output-template-file tmp/cf-lambda-gateway-sam.yml --s3-bucket lambda-sam-euw1 --region eu-west-1

echo "****************Deploy CloudFormation resources****************"
aws cloudformation deploy --template-file tmp/cf-lambda-gateway-sam.yml --stack-name S3FileService-dev-euw1 --capabilities CAPABILITY_IAM --region eu-west-1

echo "****************FINISH****************"
PAUSE