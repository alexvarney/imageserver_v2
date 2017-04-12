from flask import Blueprint, url_for, request, render_template, redirect, send_from_directory, abort
from flask import current_app as app
from imageserver.admin.authentication import requires_auth
import random, os

main = Blueprint('main', __name__, template_folder='templates', static_folder='static/img')

def generate_random_string(length = 6) -> str:
    '''
    :param length: Length of string to generate
    :return: A string of random digits from the ALPHA_CHARS config
    '''
    alpha_chars = "abcdefghjkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    return ''.join([random.choice(alpha_chars) for x in range(length)])

def allowed_file(filename):
    '''
    Checks if a file is allowed to be uploaded based on the file name
    :param filename:
    :return:
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def strip_extenstion(filename: str) -> str:
    '''
    Strips the file extension from a file
    :param filename: A filename, such as 'example.txt'
    :return: A string of the extension type, such as 'txt', or None if there is no extension
    '''
    if '.' in filename:
        return filename.lower().rsplit('.', 1)[1]

    return None

@main.route('/')
def index():
    return redirect(url_for('main.view_image'))

@main.route('/i')
@main.route('/i/')
@main.route('/i/<filename>')
@main.route('/i/<filename>/')
def view_image(filename=None):
    if filename:
        if os.path.exists(os.path.abspath(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))):
            return send_from_directory(os.path.abspath(app.config['UPLOADED_IMAGES_DEST']), filename)
        else:
            abort(404)

    return redirect(url_for('main.upload'))

@main.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        file = request.files['photo']

        if not allowed_file(file.filename):
            return "Invalid filetype, the file was not saved."

        filename = generate_random_string() + '.' + strip_extenstion(file.filename)
        file.save(os.path.abspath(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename)))
        return redirect(url_for('main.view_image') + filename)

    else:
        return render_template('upload.html')

@main.route('/delete')
@main.route('/delete/')
@main.route('/delete/<filename>/confirm') #this is stupid but it stops hover zoom from calling the deletion url
@requires_auth
def delete(filename=None):

    filepath = os.path.abspath(os.path.join(app.config['UPLOADED_IMAGES_DEST'], filename))
    if not filename or not os.path.exists(filepath):
        return abort(404)
    os.remove(filepath)
    return redirect(url_for('admin.file_list'))

