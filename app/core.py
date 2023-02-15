import logging
import config

from app.image_utils import b64_to_img

logging.basicConfig(level=config.LOGLEVEL)
logger = logging.getLogger(__name__)


def convert_image_to_text(payload: dict) -> dict:
    image = b64_to_img(payload["image"])
    return "Hello API!"

