from flask import Flask, request, jsonify
from logic import dicom_to_png
from flask import send_file
from werkzeug.utils import secure_filename
import os
from flask import Response
from extract_img import getClearForSliceNumber, getPredictionSliceNumbers, getCleanSliceCount
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
import json

# mongo invocation start

from flask import Flask
from flask_pymongo import PyMongo

app.config["MONGO_URI"] = "mongodb://localhost:27017/dicom"
mongo = PyMongo(app)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/dicom/icon/<dicom_id>')
def geticonURL(dicom_id):
    return 'http://localhost:5000/dicom/see/image/'+dicom_id+'/1'

@app.route('/dicom/all', methods=['GET'])
def get_dicoms():
    # mongo test st

    dicom_coll = mongo.db.meta
    list_of_records = list(dicom_coll.find({}))

    # mongo test end

    # list_of_records = [
    #     {'id': 1, 'title': "brain#1"},
    #     {'id': 2, 'title': "brain#2"},
    # ]
    return json.dumps(list_of_records)


@app.route('/dicom/<id>', methods=['GET'])
def get_dicom(id):
    dicom_coll = mongo.db.meta
    dicom_from_db = dicom_coll.find_one({'_id': id})
    print(dicom_from_db)
    dicom_from_db['imgAmount'] = getCleanSliceCount()

    # list = [
    #     {'id': 1, 'title': "brain#1", 'imgAmount': 512},
    #     {'id': 2, 'title': "brain#2", 'imgAmount': 256},
    # ]
    return json.dumps(dicom_from_db)


@app.route('/dicom/see/preview/<id>', methods=['GET'])
def get_dicom_preview(id):


    return 'some url - this route does not work for some reason'


@app.route('/dicom/see/image/<dicom_id>/<imageN>', methods=['GET'])
def get_dicom_image(dicom_id, imageN):
    # filename = 'storage\\png_storage\\' + dicom_id + '\\' + imageN + '.png'
    # return send_file(filename, mimetype='image/gif')
    return Response(getClearForSliceNumber(int(imageN)).getvalue(), mimetype='image/png')

@app.route('/dicom/see/proposals/<dicom_id>', methods=['GET'])
def get_dicom_proposals(dicom_id):
    # filename = 'storage\\png_storage\\' + dicom_id + '\\' + imageN + '.png'
    # return send_file(filename, mimetype='image/gif')
    return jsonify(predictions = getPredictionSliceNumbers(dicom_id))


@app.route('/postDicom', methods=['POST'])
def post_dicom():
    dicom_coll = mongo.db.meta
    # dicom_coll.insert_one({'id': 1})
    length = dicom_coll.find({}).count()

    # dir_name = request.form['text']
    # path_to_dicom = './storage/dicom_storage/' + dir_name + '/'
    # path_to_png = './storage/png_storage/' + dir_name + '/'

    # so it doesn't start with 0
    dir_name = str(length + 1)
    path_to_dicom = './storage/dicom_storage/' + dir_name + '/'
    path_to_png = './storage/png_storage/' + dir_name + '/'

    # attached_file = request.files['textfile']
    attached_files = request.files
    dict = request.files.to_dict(flat=False)
    # print(dict)
    # iterating over all items recieved from post request form
    # for item in dict:
    #     print("item: " + item + " associated file in dict: " + str(dict.get(item)))

    # print(request.files)
    if not os.path.exists(path_to_dicom):
        os.makedirs(path_to_dicom)

    data = request.json

    # dicom_to_png.convert_dicom_to_png(request.files['textfile'].read())
    count_of_files = 0
    for filen in attached_files:
        count_of_files = count_of_files +1
        print('the file:')
        file = attached_files[filen]
        print(file)
        file_name = file.filename
        file.save(path_to_dicom + secure_filename(file.filename))
        dicom_to_png.convert_dicom_to_png(file_name, path_to_dicom, path_to_png)
    # safely creates dir

    to_insert = {'_id': dir_name, 'title': request.form.get('title', 'default_name'),
                 'imgAmount': count_of_files}
    # considering the id will be fully connected with records count
    dicom_coll.insert_one(to_insert)
    return json.dumps(to_insert), 200


if __name__ == '__main__':
    app.run()

