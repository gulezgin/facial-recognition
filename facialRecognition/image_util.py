import cv2
from PIL import Image

def resize_image(image, target_size=(800, 600)):
    return cv2.resize(image, target_size)

def cv2_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
