from flask import Blueprint, render_template, url_for
from flask import current_app as app
from os import listdir, path
from imageserver.admin.authentication import requires_auth

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/')
@requires_auth
def file_list():

    images_path = path.abspath(app.config['UPLOADED_IMAGES_DEST'])

    #Build list of tuples with first element being the filename and the 2nd the modification date of the file
    files = [(f, path.getmtime(path.join(images_path, f))) for f in listdir(images_path) if path.isfile(path.join(images_path, f))]

    #sort the list based on the filedate
    files = sorted(files, key=lambda x: -x[1])
    print(files)
    return render_template('image_list.html', file_list = files, image_url = url_for('main.view_image'), deletion_url = url_for('main.delete'))
