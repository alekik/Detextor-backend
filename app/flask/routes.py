from app import core


def say_hello():
    return "Hello API!"


def process_image(payload):
    return core.convert_image_to_text(payload)
