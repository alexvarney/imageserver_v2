from os import getenv

UPLOADED_IMAGES_DEST = r'/code/imageserver/main/static/img'
ALLOWED_EXTENSIONS = ['png', 'gif', 'webm', 'jpeg', 'gifv', 'jpeg', 'jpg']
ADMIN_USERNAME = getenv('ADMIN_USERNAME', 'default')
ADMIN_PASSWORD = getenv('ADMIN_PASSWORD', 'default')
