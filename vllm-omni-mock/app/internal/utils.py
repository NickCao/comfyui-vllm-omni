from PIL import Image
from .image_api_utils import encode_image_base64


def random_image_base64(width, height) -> str:
    return encode_image_base64(Image.effect_noise((width, height), sigma=50))
