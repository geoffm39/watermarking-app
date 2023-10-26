from pathlib import Path


def get_font_dict():
    fonts = {}
    font_folder = Path('fonts')
    for font in font_folder.glob('*'):
        key = font.stem
        fonts[key] = str(font)
    return fonts


def get_font_names(font_dict: dict):
    font_names = []
    for key, val in font_dict.items():
        font_names.append(key)
    return font_names
