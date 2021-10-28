from chalice import Chalice

app = Chalice(app_name='presigned-url')


@app.route('/generate-pre-signed-url-for-upload')
def generate_pre_signed_url_for_upload():
    return {'hello': 'world'}


