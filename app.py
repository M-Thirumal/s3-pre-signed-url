import os
import boto3
import logging

from botocore.exceptions import ClientError
from chalice import Chalice

app = Chalice(app_name='presigned-url', debug=True, configure_logs=False)
# Logging
app.debug = True
logging.getLogger().setLevel(logging.DEBUG)


# @app.route('/generate-pre-signed-url-for-upload', methods=['POST'], content_types=['application/json'])
# def generate_pre_signed_url_for_upload():
#     logging.debug("Generate Pre-Signed URL for upload")
#     request = app.current_request
#     data = request.json_body
#     response = get_pre_signed_url(data['file_name'])
#     files = {'file': open("/Users/thirumal/Downloads/ACC.png", 'rb')}
#     print(files)
#     http_response = requests.post(response['url'], data=response['fields'], files=files)
#     print(http_response)
#     # If successful, returns HTTP status code 204
#     logging.info(f'File upload HTTP status code: {http_response.text}')
#     return response


@app.lambda_function()
def handler(event, context):
    logging.debug(event)
    version_id = event['arguments']['versionId']
    file_name = event['arguments']['fileName']
    if 'bucket' in event['arguments']:
        logging.debug("Creating pre-signed url for the bucket {}".format(event['arguments']['bucket']))
        return get_pre_signed_url(event['arguments']['bucket'], file_name, version_id)
    return get_pre_signed_url(os.environ.get('bucket'), file_name, version_id)


def get_pre_signed_url(bucket, file_name, version_id):
    print("Creating pre-signed url for {}".format(bucket))
    try:
        # Don't use/depends on policy, "It will create pre-signed url but won't allow to upload the file
        # Will get "The AWS Access Key Id you provided does not exist in our records." error
        s3_client = boto3.client('s3', aws_access_key_id=os.environ.get("aws_access_key_id"), aws_secret_access_key=os
                                 .environ.get("aws_secret_access_key"), region_name=os.environ.get("region_name"))
        if not version_id:
            response = s3_client.generate_presigned_post(Bucket=bucket,
                                                         Key=os.environ.get('folder_location') + file_name,
                                                         ExpiresIn=300)
            logging.debug("Created url without version")
        else:
            response = s3_client.generate_presigned_url(ClientMethod='get_object', Params={
                'Bucket': bucket,
                'Key': os.environ.get('folder_location') + file_name,
                'VersionId': version_id
            })
            logging.debug("Created url for version")

    except ClientError as e:
        logging.error(e)
        return None
    logging.debug("Pre-Signed URL {}".format(response))
    return response
