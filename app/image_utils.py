import base64

import cv2
import numpy as np


def decode_base64_to_image(base64_image: str) -> np.ndarray:
    decoded_base64_image = base64.b64decode(base64_image)
    image_array = np.frombuffer(decoded_base64_image, np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image


def encode_image_to_base64(image: np.ndarray) -> str:
    _, image_array = cv2.imencode(".jpg", image)
    image_bytes = image_array.tobytes()
    encoded_base64_image = base64.b64encode(image_bytes).decode("utf-8")
    return encoded_base64_image
