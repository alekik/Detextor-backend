from unittest import TestCase
import os
from app.core import convert_image_to_text
import cv2
from tests.utils import test_dir_path
from app.image_utils import encode_image_to_base64


class CoreTest(TestCase):
    def test_convert_image_to_text(self):
        test_image = cv2.imread(os.path.join(test_dir_path, "data", "1.png"))
        test_image_shape = test_image.shape
        test_image = encode_image_to_base64(test_image)
        test_image_payload = {"image": test_image, "img_size": test_image_shape}
        recognized_text = convert_image_to_text(test_image_payload)
        self.assertIsInstance(recognized_text, str)
        self.assertIsNotNone(recognized_text)
