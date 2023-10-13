from PIL import Image, ImageDraw, ImageFont

class MemeGenerator:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.width, self.height = self.image.size
        self.draw = ImageDraw.Draw(self.image)
        self.font_path = "path_to_your_font.ttf"  # Replace with the path to your desired font file

    def add_text(self, text, x, y, font_size=40, color="white"):
        font = ImageFont.truetype(self.font_path, font_size)
        self.draw.text((x, y), text, font=font, fill=color)

    def save_meme(self, output_path):
        self.image.save(output_path)

# Example usage
meme = MemeGenerator("path_to_your_image.jpg")  # Replace with the path to your image file
meme.add_text("Hello, World!", 50, 50)
meme.save_meme("output.jpg")  # Replace with the desired output file path