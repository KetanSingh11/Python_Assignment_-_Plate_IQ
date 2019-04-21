import os

from flask import Flask, jsonify, request, send_from_directory, Blueprint
from flask_restful import Api
from werkzeug.utils import secure_filename
from resources.invoice import InvoicesResource, InvoiceResource, MarkDigitizedInvoice
# from config import UPLOAD_FOLDER

UPLOAD_FOLDER = "./uploads/"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

@app.route("/hello")
def index():
    return jsonify({'message': 'hello world'})



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename, as_attachment=True)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return "Error! No file selected", 400

        file = request.files['file']
        if file.filename == '':
            return "No file selected", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
                return 'File uploaded successfully', 200
            else:
                return 'Server Error in uploading file', 500
        else:
            return "Invalid file type: {}".format(file.mimetype), 415

    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h2>Upload new File</h2>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


# register APIs
api.add_resource(InvoicesResource, "/invoices")
api.add_resource(InvoiceResource, "/invoices/<id>")
api.add_resource(MarkDigitizedInvoice, "/invoices/<id>/digitize")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    # db.create_all()
    app.run(port=5000, debug=True)
