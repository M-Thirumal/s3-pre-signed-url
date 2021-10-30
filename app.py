import logging
import requests
import json
import os
import boto3
import logging

from botocore.exceptions import ClientError
from chalice import Chalice

app = Chalice(app_name='presigned-url', debug=True, configure_logs=False)

s3_client = boto3.client('s3', region_name="ap-south-1", aws_access_key_id="${access_key}",
                         aws_secret_access_key="${secret_key}")
bucket = "${bucket_name}"


@app.route('/generate-pre-signed-url-for-upload', methods=['POST'], content_types=['application/json'])
def generate_pre_signed_url_for_upload():
    logging.debug("Generate Pre-Signed URL for upload")
    request = app.current_request
    data = request.json_body
    response = get_pre_signed_url(data['file_name'])
    # files = {'file': open("/Users/thirumal/Downloads/ACC.png", 'rb')}
    # print(files)
    # http_response = requests.post(response['url'], data=response['fields'], files=files)
    # print(http_response)
    # If successful, returns HTTP status code 204
    # logging.info(f'File upload HTTP status code: {http_response.text}')
    return response


def get_pre_signed_url(file_name):
    try:
        response = s3_client \
            .generate_presigned_post(Bucket=bucket, Key=file_name, ExpiresIn=120)
    except ClientError as e:
        logging.error(e)
        return None
    logging.debug("Pre-Signed URL {}".format(response))
    print(response)
    return response
