"""A simple cli app starter."""
import os
import random
import argparse

# Import Ingestor and MemeEngine classes
from quote_engine.ingestor import Ingestor
from meme_engine.meme_generator import MemeGenerator
from quote_engine import QuoteModel

def generate_meme(path=None, body=None, author=None):
    """Generate a meme given an path and a quote."""
    # Init the output image and the quote on it
    img = None
    quote = None

    if path is None:
        # if the user does not specify an image path, use the default image path
        images = "./_data/photos/dog/"
        # list of all images under the default image path
        imgs = []
        # traverse a directory tree and access all the files and directories (include subdir) within it
        for root, dirs, files in os.walk(images):
            # store the image with the full path of that image file
            imgs = [os.path.join(root, name) for name in files]

        # choose a random image from default images
        if len(imgs) == 0:
            print("There is no image to generate a meme")
        else:
            img = random.choice(imgs)
    else:
        # get the input image path
        img = path

    if body is None:
        # the list of all default quote files
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        # a list to store all parsed quotes
        quotes = []
        # parse then store each quote
        for f in quote_files:
            # use extend() to add to the list because
            # we can have multiple quotes in a file
            quotes.extend(Ingestor.parse(f))

        # choose a random quote from default quotes
        if len(quotes) == 0:
            print("There is no quote to generate the meme")
        else:
            quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception('Author Required if Body is Used')
        # create a quote model from given quote
        quote = QuoteModel(body, author)

    # create a meme object with specifying to save manipulated images into a new directory
    meme = MemeGenerator('.\output')
    if quote is None:
        return None
    else:
        path = meme.make_meme(img, quote.quote_body, quote.author)

    return path

if __name__ == "__main__":
    """Parse the following CLI arguments:
        path - path to an image file
        body - quote body to add to the image
        author - quote author to add to the image
    """
    cli_parser = argparse.ArgumentParser(description='Get image path and quote')
    cli_parser.add_argument('--path', type=str, nargs='?', default=None, 
                            help='The path to an image file')
    cli_parser.add_argument('--body', type=str, nargs='?', default=None,
                            help='The quote content to add to the image')
    cli_parser.add_argument('--author', type=str, nargs='?', default=None,
                            help='The author of the quote')
    args = cli_parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))
