cd ..
if not exist "tmp" mkdir tmp

echo "****************Packaging SAM****************"
aws cloudformation package --template-file sam/lambda-gateway-sam.yml --output-template-file tmp/cf-lambda-gateway-sam.yml --s3-bucket lambda-sam-euw1 --region eu-west-1

zip -jFS tmp/aws-sam-lambda-python.zip src/main/python/test_sam.py

echo "****************Upload lambdas to S3****************"
aws s3 cp tmp/aws-sam-lambda-python.zip s3://a205027-content-mcalrt-main-dev-euw1

echo "****************Deploy CloudFormation resources****************"
aws cloudformation deploy --template-file tmp/cf-sam.yml --stack-name a205027-TestSam-test-dev-euw1 --capabilities CAPABILITY_IAM --region eu-west-1

echo "****************FINISH****************"
PAUSE