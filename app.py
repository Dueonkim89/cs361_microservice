import io
import os
from base64 import encodebytes
from PIL import Image
from flask import Flask, jsonify
#from Face_extraction import face_extraction_v2

app = Flask(__name__)

def get_images():
    """Get path of all card images stored in directory"""
    list_of_card_path = []
    # open directory and read the file name
    for file in os.listdir('./card_images'):
        list_of_card_path.append('./card_images/' + file)

    return list_of_card_path    


def get_response_image(image_path):
    ''' https://stackoverflow.com/questions/64065587/how-to-return-multiple-images-with-flask '''
    pil_img = Image.open(image_path, mode='r') # reads the PIL image
    byte_arr = io.BytesIO()
    pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
    encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
    return encoded_img


@app.route("/")
def temp():
    return "Hello World!"


@app.route('/get_images',methods=['GET'])
def index():
    # get path to all card images
    card_images = get_images()
    encoded_images = []

    # encode and send as JSON
    for image_path in card_images:
        encoded_images.append(get_response_image(image_path))
    return jsonify({'cards': encoded_images})
