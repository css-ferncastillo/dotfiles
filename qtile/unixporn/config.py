import os
import subprocess
from libqtile import *
from libqtile.config import *
from libqtile.command import *
from datetime import datetime

from libqtile import hook, layout
from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, extension

import fontawesome as fa
import copy

import subprocess
from time import time

COLORS = {
    "dark0_hard": "#1d2021",
    "dark0": "#282828",
    "dark0_soft": "#32302f",
    "dark1": "#3c3836",
    "dark2": "#504945",
    "dark3": "#665c54",
    "dark4": "#7c6f64",
    "dark4_256": "#7c6f64",

    "gray_245": "#928374",
    "gray_244": "#928374",

    "light0_hard": "#f9f5d7",
    "light0": "#fbf1c7",
    "light0_soft": "#f2e5bc",
    "light1": "#ebdbb2",
    "light2": "#d5c4a1",
    "light3": "#bdae93",
    "light4": "#a89984",
    "light4_256": "#a89984",

    "bright_red": "#fb4934",
    "bright_green": "#b8bb26",
    "bright_yellow": "#fabd2f",
    "bright_blue": "#83a598",
    "bright_purple": "#d3869b",
    "bright_aqua": "#8ec07c",
    "bright_orange": "#fe8019",

    "neutral_red": "#cc241d",
    "neutral_green": "#98971a",
    "neutral_yellow": "#d79921",
    "neutral_blue": "#458588",
    "neutral_purple": "#b16286",
    "neutral_aqua": "#689d6a",
    "neutral_orange": "#d65d0e",

    "faded_red": "#9d0006",
    "faded_green": "#79740e",
    "faded_yellow": "#b57614",
    "faded_blue": "#076678",
    "faded_purple": "#8f3f71",
    "faded_aqua": "#427b58",
    "faded_orange": "#af3a03"
}


# ----------------------------
# ------ Screen Shots --------
# ----------------------------


home = os.path.expanduser('~')
savePath = os.path.join(home, 'Screenshots')
if not os.path.isdir(savePath):
    os.mkdir(savePath)
datename = datetime.now().strftime("%Y%m%d%I%M%S%f")


# ----------------------------
# -------- Hotkeys -----------
# ----------------------------
mod = 'mod4'
keys = [
    # ------------ Window Configs ------------

    # Switch between windows in current stack pane
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

    # Change window sizes (MonadTall)
    Key([mod, "shift"], "l", lazy.layout.grow()),
    Key([mod, "shift"], "h", lazy.layout.shrink()),

    # Toggle floating
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),

    # Move windows up or down in current stack
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),

    # Kill window
    Key([mod], "w", lazy.window.kill()),

    # Switch focus of monitors
    Key([mod], "period", lazy.next_screen()),
    Key([mod], "comma", lazy.prev_screen()),

    # Restart Qtile
    Key([mod, "mod1"], "r", lazy.restart()),

    Key([mod, "mod1"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show drun")),

    # Window Nav
    Key([mod, "shift"], "m", lazy.spawn("rofi -show -modi run,drun,window")),

    # Browser
    Key([mod], "b", lazy.spawn("brave")),

    # File Explorer
    Key([mod], "e", lazy.spawn("thunar")),

    # Terminal
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Redshift
    Key([mod], "r", lazy.spawn("redshift -O 1200")),
    Key([mod, "shift"], "r", lazy.spawn("redshift -x")),

    # Screenshot
    Key([mod], "s", lazy.spawn(f"scrot -s {savePath}/{datename}.png")),

    # ------------ Hardware Configs ------------

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ -5%"
    )),
    Key([], "XF86AudioRaiseVolume", lazy.spawn(
        "pactl set-sink-volume @DEFAULT_SINK@ +5%"
    )),
    Key([], "XF86AudioMute", lazy.spawn(
        "pactl set-sink-mute @DEFAULT_SINK@ toggle"
    )),

    # Brightness
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

# ----------------------------
# -------- Groups ------------
# ----------------------------
groups = [Group(i) for i in ['  ', '  ', ' ', '  ', '  ', '梅  ', '甆  ', ' ']]

for i, group in enumerate(groups):
    actual_key = str(i + 1)
    keys.extend([
        Key([mod], actual_key, lazy.group[group.name].toscreen()),
        Key([mod, "shift"], actual_key, lazy.window.togroup(group.name))
    ])

# ----------------------------
# -------- Layouts -----------
# ----------------------------
layout_conf = {
    'border_focus': COLORS['light0_hard'],
    'border_width': 1,
    'margin': 3
}

layouts = [
    layout.Max(),
    layout.MonadTall(**layout_conf),
    layout.MonadWide(**layout_conf),
    layout.Bsp(**layout_conf),
    layout.Matrix(**layout_conf),
    layout.RatioTile(**layout_conf),
    # layout.Columns(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),
        Match(wm_class='makebranch'),
        Match(wm_class='maketag'),
        Match(wm_class='ssh-askpass'),
        Match(title='branchdialog'),
        Match(title='pinentry'),
    ],
    border_focus=COLORS['faded_aqua']
)

# ----------------------------
# -------- Widgets -----------
# ----------------------------


def base():
    return {
        'foreground': COLORS['light0_soft'],
        'background': COLORS['dark0_soft']
    }


def inverse():
    return {
        'background': COLORS['light0_soft'],
        'foreground': COLORS['dark0_soft']
    }


def separator():
    return widget.Sep(**base(), linewidth=0, padding=5)


def icon(fontsize=16, text="?"):
    return widget.TextBox(
        **base(),
        fontsize=fontsize,
        text=text,
        padding=4
    )

# def my_func(text):
#   for string in [” - Chromium”, ” - Firefox”]:
#   text = text.replace(string, “”)
#   return textthen
# set option parse_text=my_func


def parseText(text):
    s = text.split("-")
    return s[-1]


def workspaces():
    return [
        separator(),
        widget.GroupBox(
            **base(),
            font='UbuntuMono Nerd Font',
            fontsize=19,
            margin_y=3,
            margin_x=0,
            padding_y=8,
            padding_x=5,
            borderwidth=3,
            active=COLORS['bright_blue'],
            inactive=COLORS['light4_256'],
            rounded=False,
            highlight_method='line',
            highlight_color=[COLORS['dark1'], COLORS['dark2']],
            urgent_alert_method='line',
            urgent_border=COLORS['bright_red'],
            this_current_screen_border=COLORS['bright_yellow'],
            this_screen_border=COLORS['gray_245'],
            other_current_screen_border=COLORS['dark2'],
            other_screen_border=COLORS['light4'],
            disable_drag=True
        ),
        separator(),
        widget.WindowName(
            fontsize=14,
            padding=5,
            foreground=COLORS['dark4'],
            background=COLORS['dark0_soft'],
            parse_text=parseText,),

        separator(),
    ]


primary_widgets = [
    *workspaces(),
    separator(),
    icon(fontsize=17, text='ﯲ '),
    widget.Net(**base(), format=' {down} '),
    widget.NetGraph(
        bandwidth_type="down",
        background=COLORS['dark0_soft'],
        graph_color=COLORS['bright_yellow'],
        fill_color=COLORS['bright_yellow'],
        type="linefill",
        line_width=1,
        border_width=0
    ),
    separator(),
    icon(fontsize=17, text='﬙ '),
    widget.CPU(**base(), format='CPU {freq_current}GHz {load_percent}%'),
    widget.CPUGraph(
        background=COLORS['dark0_soft'],
        graph_color=COLORS['bright_purple'],
        fill_color=COLORS['bright_purple'],
        type="linefill",
        line_width=1,
        border_width=0
    ),
    separator(),
    icon(fontsize=17, text=' '),
    widget.Memory(**base(), format='{MemUsed: .0f}{mm}/{MemTotal: .0f}{mm}'),
    widget.MemoryGraph(
        background=COLORS['dark0_soft'],
        graph_color=COLORS['neutral_blue'],
        fill_color=COLORS['neutral_blue'],
        type="linefill",
        line_width=1,
        border_width=0
    ),
    separator(),
    icon(fontsize=17, text=' '),
    widget.HDDBusyGraph(
        device="sda",
        background=COLORS['dark0_soft'],
        graph_color=COLORS['faded_aqua'],
        fill_color=COLORS['faded_aqua'],
        type="linefill",
        line_width=1,
        border_width=0
    ),
    separator(),
    #widget.Mpris2(
    #    background=COLORS['dark0_soft'],
    #    foreground=COLORS['light0_hard'],
    #    name='spotify',
    #    stop_pause_text='懶 ',
    #    fontsize=17,
    #    scroll_chars=None,
    #    display_metadata=['xesam:title', 'xesam:artist'],
    #   objname="org.mpris.MediaPlayer2.spotify",
    #),
    #separator(),
    widget.NvidiaSensors(),
    separator(),
    widget.CheckUpdates(
        background=COLORS['dark0_soft'],
        colour_have_updates=COLORS['neutral_red'],
        colour_no_updates=COLORS['neutral_green'],
        no_update_string=' ',
        display_format=' {updates}',
        update_interval=1800,
        custom_command='checkupdates',
    ),
    separator(),
    icon(fontsize=17, text=' '),  # Icon: nf-mdi-calendar_clock
    widget.Clock(**base(), format='%d/%m/%Y %H:%M:%S '),
    widget.CurrentLayoutIcon(**base(), scale=0.65),
    separator(),
    widget.Systray(background=COLORS['dark2'], padding=5),
]

secondary_widgets = [
    *workspaces(),
    separator(),
    widget.CurrentLayoutIcon(**base(), scale=0.65),
    widget.CurrentLayout(**base(), padding=5),
    widget.Clock(**base(), format='%d/%m/%Y - %H:%M '),
]

widget_defaults = {
    'font': 'UbuntuMono Nerd Font Bold',
    'fontsize': 14,
    'padding': 1,
}
extension_defaults = widget_defaults.copy()

# ----------------------------
# -------- Screens -----------
# ----------------------------


def status_bar(widgets):
    return bar.Bar(widgets, 24, opacity=0.92)


screens = [Screen(top=status_bar(primary_widgets))]

xrandr = "xrandr | grep -w 'connected' | cut -d ' ' -f 2 | wc -l"

command = subprocess.run(
    xrandr,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

if command.returncode != 0:
    error = command.stderr.decode("UTF-8")
    logger.error(f"Failed counting monitors using {xrandr}:\n{error}")
    connected_monitors = 1
else:
    connected_monitors = int(command.stdout.decode("UTF-8"))

if connected_monitors > 1:
    for _ in range(1, connected_monitors):
        screens.append(Screen(top=status_bar(secondary_widgets)))


autostart = ["feh --bg-fill --randomize /usr/share/backgrounds/gruvbox/*"]

for x in autostart:
    os.system(x)


# ----------------------------
# -------- Launcher ----------
# ----------------------------
dgroups_key_binder = None
dgroups_app_rules = []
main = None
auto_fullscreen= False
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []
wmname = "LG3D"
