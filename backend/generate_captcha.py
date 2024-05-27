import random
import string
from PIL import Image, ImageDraw, ImageFont

def create_captcha_text():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def create_captcha_image(text):
    font_size = 10
    font = ImageFont.load_default(font_size)
    image = Image.new('RGB', (60, 20), color=(173, 216, 230))
    draw = ImageDraw.Draw(image)
    draw.text((10, 5), text, font=font, fill=(0, 0, 0))
    return image