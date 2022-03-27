
from libqtile import hook

from powerlineTheme.settings.keys import mod, keys
from powerlineTheme.settings.groups import groups
from powerlineTheme.settings.layouts import layouts, floating_layout
from powerlineTheme.settings.widget import widget_defaults, extension_defaults
from powerlineTheme.settings.screens import screens
from powerlineTheme.settings.mouse import mouse
from powerlineTheme.settings.path import qtile_path

from os import path
import os
import subprocess

autostart = ["feh --bg-fill --randomize /usr/share/backgrounds/archlinux/*"]

for x in autostart:
     os.system(x)

main = None
dgroups_key_binder = None
dgroups_app_rulers = []
follow_mouse_focus = False
bring_front_click = False
cursor_wrap = True
auto_fullscreen = False
focus_on_window_activation = 'urgent'
wmname = 'LG3D'
