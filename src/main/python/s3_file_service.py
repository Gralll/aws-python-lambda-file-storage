import boto3
import logging
import uuid
from botocore.exceptions import ClientError

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

BUCKET_NAME = 's3-file-service-storage-dev-euw1'
S3 = boto3.resource('s3')
S3_CLIENT = boto3.client('s3')


def lambda_handler(event, context):
    try:
        httpMethod = event.get('httpMethod')
        if (httpMethod == 'GET'):
            return handle_get(event)
        elif (httpMethod == 'POST'):
            return handle_post(event)
        elif (httpMethod == 'PUT'):
            return handle_put(event)
    except ClientError as ex:
        logger.error("Request wasn't handled successfully. Details: {}".format(str(ex)))
        return build_response_with_headers(500, "Request wasn't handled successfully. Details: {}".format(str(ex)))

    logger.error('Unsupported http method {}'.format(event.get('httpMethod')))
    return build_response_with_headers(400, 'Only GET, POST, PUT are supported.')


def handle_get(request):
    logger.info('Get request: {}'.format(str(request)))
    file_name = get_proxy_param(request)
    if file_name:
        return get_file(file_name)
    else:
        return get_files_list()


def handle_post(request):
    file_name = get_proxy_param(request)
    if file_name:
        return build_response_with_headers(400, 'Unsupported method POST with fileName')
    file_name = 'File-{}'.format(uuid.uuid4())
    return send_file(file_name, request.get('body'))


def handle_put(request):
    file_name = get_proxy_param(request)
    if file_name:
        return send_file(file_name, request.get('body'))
    return build_response_with_headers(400, 'Unsupported method PUT without fileName')


def get_files_list():
    contents = S3_CLIENT.list_objects_v2(Bucket=BUCKET_NAME)['Contents']
    logger.info('Get files list {}'.format(contents))
    keys = ', '.join(content.get('Key') for content in contents) if contents else ''
    return build_response_with_headers(200, keys)


def get_file(file_name):
    file = S3.Object(BUCKET_NAME, file_name)
    file_content = file.get()['Body'].read().decode('utf-8')
    return build_response_with_headers(200, file_content)


def send_file(file_name, body):
    file = S3.Object(BUCKET_NAME, file_name)
    response = file.put(Body=body.encode())
    logger.info('Send file response: {}'.format(response))
    return build_response_with_headers(200, 'File was uploaded: {}'.format(file_name))


def get_proxy_param(request):
    return (request.get('pathParameters') or {}).get('proxy', '')


def build_response_with_headers(status, body):
    return {
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        "statusCode": status,
        "body": body
    }