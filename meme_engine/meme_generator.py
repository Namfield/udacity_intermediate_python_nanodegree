"""The module is responsible for manipulating and drawing text onto images"""
from PIL import Image, ImageDraw, ImageFont
import random
import os
from time_utils import get_current_time

class MemeGenerator:
    """The class which is responsible for loading images, resizing them, adding captions
    and handling the generation of the final memes."""
    
    def __init__(self, out_path:str):
        """Initialize the MemeGenerator.

            Arguments:
                img_path {str} -- the file location for the input image.
        """
        self.out_path = out_path
        
    def make_meme(self, img_path: str, text: str, author: str, width=500) -> str:
        """Manipulate the given image.
        
            Arguments:
                img_path {str} -- the file location for the input image.
                text {str} -- the text which is the quote body to add to the image
                author {str} -- the author of the quote and need to add to the image
                width {int} -- the desired width of the output image
            
            Return:
                the file location for the output image.
        """
        # Load the image
        try:
            img = Image.open(img_path)
        except FileNotFoundError:
            print(f"File {img_path} is not found")

        """Resize the image
        """
        # the height is scaled proportionally
        ratio = width/float(img.size[0])
        height = int(ratio * float(img.size[1]))
        # resize the image
        img = img.resize((width, height))

        """Add quote to the image
        """
        # create an ImageDraw object from the original image
        draw_img = ImageDraw.Draw(img)
        # define the text coordinates
        text_coords = (
            random.randint(0, int(img.width * 0.75)),
            random.randint(0, int(img.height * 0.75))
        )
        # define the text
        text_content = f"{text} - {author}"
        # define color of the text
        text_color = "blue"
        # define the font of the text
        font = ImageFont.truetype('LilitaOne-Regular.ttf', size=14)
        # add the text
        draw_img.text(text_coords, text_content, fill = text_color, font = font)

        """Save the image
        """
        # out_img_path = os.path.join(self.out_path, get_current_time() + ".jpg")
        # img.save(out_img_path)
        # Check if the output directory exists, create it if it doesn't
        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)
        # Generate the output file name
        file_name = get_current_time() + ".jpg"
        out_img_path = os.path.join(self.out_path, file_name)
        img.save(out_img_path)
        
        return out_img_path