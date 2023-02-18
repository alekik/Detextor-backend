from tests.utils import test_dir_path
from unittest import TestCase
import os
import cv2

from app.image_utils import decode_base64_to_image, encode_image_to_base64


class ImageUtilsTest(TestCase):
    def test_decode_base64_to_image(self):
        with open(os.path.join(test_dir_path, "data", "1.txt")) as test_base64_file:
            test_base64_string = test_base64_file.readline()
            image = decode_base64_to_image(test_base64_string)
            self.assertIsNotNone(image)
            self.assertEqual(image.shape[0], 1800)
            self.assertEqual(image.shape[1], 2880)
            self.assertEqual(image.shape[2], 3)  # is RGB

    def test_encode_image_to_base64(self):
        test_image = cv2.imread(os.path.join(test_dir_path, "data", "1.png"))
        base64_string = encode_image_to_base64(test_image)
        self.assertIsNotNone(base64_string)
        self.assertIsInstance(base64_string, str)

    def test_full_conversion_pipeline(self):
        test_image = cv2.imread(os.path.join(test_dir_path, "data", "1.png"))
        base64_string = encode_image_to_base64(test_image)
        image_after_pipeline = decode_base64_to_image(base64_string)
        self.assertEqual(test_image.shape, image_after_pipeline.shape)
        self.assertEqual(test_image.all(), image_after_pipeline.all())
