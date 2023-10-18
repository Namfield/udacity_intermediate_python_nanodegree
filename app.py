import random
import os
import requests
from flask import Flask, render_template, abort, request
from quote_engine.ingestor import Ingestor
from meme_engine.meme_generator import MemeGenerator
from quote_engine import QuoteModel
from time_utils import get_current_time

# create a Flash application instance
app = Flask(__name__)

# a meme instance
meme = MemeGenerator('./static')

def setup():
    """Load all necessary resources for the application."""
    # a list of all quote files
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    """Use the Ingestor class to parse all files in the quote_files variable
    """
    # a list to store all parsed quotes
    quotes = []
    # parse then store each quote
    for quote_file in quote_files:
        quotes.extend(Ingestor.parse(quote_file))

    images_path = "./_data/photos/dog/"
    """Use the pythons standard library os class to find all
    images within the images_path directory.
    """
    # a list of all images
    imgs = []
    # traverse a directory tree and access all the files and directories (include subdir) within it
    for root, dirs, files in os.walk(images_path):
        # store the image with the full path of that image file
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme.
    when a user visits the root URL of the application, 
    this function is executed
    """
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    img = random.choice(imgs)
    # 2. select a random quote from the quotes array
    quote = random.choice(quotes)
    # generate the meme from given image and quote
    path = meme.make_meme(img, quote.quote_body, quote.author)


    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information.
    The route decorator maps the URL '/create' with the HTTP method GET 
    to the meme_form() function"""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme.
    The route decorator maps the URL '/create' with the HTTP method GET 
    to the meme_form() function"""
    # 1. Use requests module to save the image from the image_url
    #    form param to a temp local file.
    img_url = request.form.get('img_url')
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    if img_url:
        # send a get request to the image url
        response = request.get(img_url)
        img = get_current_time + '.jpg'
        # check if the request was successful (status code 200)
        if response.status_code == 200:
            # open a temp file to save the image
            with open(img, "wb") as file:
                file.write(response.content)
    else:
        img = random.choice(imgs)
    
    quote_body = request.form.get('body')
    quote_author = request.form.get('author')
    if not quote_body or not quote_author:
        quote = random.choice(quotes)
        quote_body = quote.quote_body
        quote_author = quote.author

    # 3. Make meme.
    path = meme.make_meme(img, quote_body, quote_author)

    return render_template('meme.html', path=path)

if __name__ == "__main__":
    app.run()
