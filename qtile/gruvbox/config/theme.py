
from os import path
import subprocess
import json

from .path import qtile_path


def load_theme():

    theme_file = path.join(qtile_path, "gruvbox/themes", 'theme.json')
    if not path.isfile(theme_file):
        raise Exception(f'"{theme_file}" does not exist')

    with open(path.join(theme_file)) as f:
        return json.load(f)


if __name__ == "powerlineTheme.settings.theme":
    colors = load_theme()

