import io
import os
from base64 import encodebytes
from PIL import Image
from flask import Flask, jsonify
#from Face_extraction import face_extraction_v2

app = Flask(__name__)

def get_images():
    """Get path of all card images stored in directory ./card_images"""
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
    # return description of card and encoded image
    return image_path[14:len(image_path) - 4], encoded_img


@app.route("/")
def temp():
    return "Hello World!"


@app.route('/get_images',methods=['GET'])
def index():
    # get path to all card images
    card_images = get_images()
    encoded_images = {}

    # encode all card images and send as JSON
    for image_path in card_images:
        image = get_response_image(image_path)
        encoded_images[image[0]] = image[1]
    return jsonify({'cards': encoded_images})


@app.route('/get_rules',methods=['GET'])
def rules():
    '''Provide game rules for Conquian'''
    rules = {"pack": 'A standard pack of 52 cards with all the tens, nines and eights removed, leaving a total of 40 cards in the deck.',
    "rank": 'The jack and seven are considered to be in sequence. The rank of an ace is low only so that the sequence A, 2, 3 can be formed, but not A, K, Q.', 
    "objective": 'Each player tries to form matched sets consisting of groups of three or four of a kind, or sequences of three or more cards of the same suit.',
    "deal": 'Each of the two players is dealt 10 cards. The remaining cards form the stock; no upcard is turned.',
    "youtube": "https://www.youtube.com/watch?v=Vq00jSkm96I&ab_channel=GatherTogetherGames",
    "score": "The game ends when a player has melded exactly 11 cards. Therefore, a player may have no card left in their hand but still continues to play because they need another melded card to go out. Each deal is a separate game, and if the stock is exhausted before either player has melded 11 cards, the next game counts double."}
    return jsonify(rules)