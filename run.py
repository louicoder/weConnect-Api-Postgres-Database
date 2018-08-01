import os
from main import app
from main.app_models import db, User
from flask import jsonify, request, json
from flask_uploads import UploadSet, configure_uploads, IMAGES
from main.user.user_views import token_required


db.init_app(app)
with app.app_context():
    db.create_all()

APP_ROOT = os.path.dirname(os.path.abspath('__filename__'))
path = os.path.join(APP_ROOT, 'images/')

# set images upload directory
photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = path
configure_uploads(app, photos)


@app.route('/api/auth/upload/<username>', methods=['POST'])
# @token_required
def upload(username):
    username = username
    # check if the file key is in the request.
    if not request.files['file']:
        return jsonify({"message":"No photo was uploaded found"})

    # get photo from the request
    file = request.files['file']

    user_object = User.query.filter_by(username=username).first()
    

    # rename the file to user's username
    filename = file.filename.split('.')
    filename = username+'.'+filename[-1]

    user_object.profile_photo = filename
    db.session.add(user_object)
    db.session.commit()

    # set destination for file to be saved
    destination = "/".join([path, filename])

    # save the photo
    file.save(destination)

    # return success message
    return jsonify({"message":"Photo uploaded successfully"})

if __name__ == '__main__':
    app.run(debug=True)