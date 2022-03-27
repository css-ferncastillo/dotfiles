import copy
import os
import subprocess
from pathlib import Path
from time import time

import fontawesome as fa
from libqtile import hook
from libqtile import layout, bar, widget
from libqtile.command import lazy
from libqtile.config import *
from libqtile.config import Key, Screen, Group, Drag, Click

# ----------------------------
# -------- Colors ------------
# ----------------------------

COLS = {
    "dark_0": "#1d2021",
    "dark_1": "#282828",
    "dark_2": "#32302f",
    "dark_3": "#3c3836",
    "dark_4": "#504945",
    "dark_5": "#665c54",
    "dark_6": "#7c6f64",
    "gray_0": "#928374",
    "light_0": "#f9f5d7",
    "light_1": "#fbf1c7",
    "light_2": "#f2e5bc",
    "light_3": "#ebdbb2",
    "light_4": "#d5c4a1",
    "light_5": "#bdae93",
    "light_6": "#a89984",
    "red_0": "#fb4934",
    "red_1": "#cc241d",
    "red_2": "#9d0006",
    "green_0": "#b8bb26",
    "green_1": "#98971a",
    "green_2": "#79740e",
    "yellow_0": "#fabd2f",
    "yellow_1": "#d79921",
    "yellow_2": "#b57614",
    "blue_0": "#83a598",
    "blue_1": "#458588",
    "blue_2": "#076678",
    "purple_0": "#d3869b",
    "purple_1": "#b16286",
    "purple_2": "#8f3f71",
    "aqua_0": "#8ec07c",
    "aqua_1": "#689d6a",
    "aqua_2": "#427b58",
    "orange_0": "#fe8019",
    "orange_1": "#d65d0e",
    "orange_2": "#af3a03",
    # Additional related colors from the deus colorscheme
    'deus_1': '#2C323B',
    'deus_2': '#646D7A',
    'deus_3': '#48505D',
    'deus_4': '#1A222F',
    'deus_5': '#101A28',
}

BG_COLOR = "#000000"
FG_COLOR = "#FFFFFF"
ALERT_COLOR = "#FF0000"

GROUP_URGENT_BORDER = ALERT_COLOR
GROUP_FG = BG_COLOR
GROUP_INACTIVE_FG = "#888888"
GROUP_ACTIVE_FG = GROUP_FG
GROUP_SELECTED_BG = "#bbbbbb"
GROUP_BG = FG_COLOR
GROUP_OTHER_BORDER = '#00004F'
GROUP_THIS_BORDER = "#0000FF"
FONT_SIZE = 12


# ICON_SIZE=30
# ICON_PADDING=-10

# ----------------------------
# ----- Workspace Box --------
# ----------------------------

def group_as_workspace(g):
    cloned = copy.copy(g)
    cloned.label = cloned.name[1:2]
    return cloned


class WorkspaceBox(widget.GroupBox):
    def __init__(self, **config):
        widget.GroupBox.__init__(self, **config)

    @property
    def groups(self):
        """
        returns list of visible groups.
        The existing groups are filtered by the visible_groups attribute and
        their label. Groups with an empty string as label are never contained.
        Groups that are not named in visible_groups are not returned.
        """
        if super().groups:
            return list(map(group_as_workspace, super().groups))
            # return list(map(lambda g: Group(g.name), super().groups))
        else:
            return super().groups


# ----------------------------
# ------ Screen Shots --------
# ----------------------------

def screenshot(save=True, copy=True):
    def f(qtile):
        path = Path.home() / 'Pictures' / 'screenshots'
        path /= f'screenshot_{str(int(time() * 100))}.png'
        shot = subprocess.run(['maim'], stdout=subprocess.PIPE)

        if save:
            with open(path, 'wb') as sc:
                sc.write(shot.stdout)

        if copy:
            subprocess.run(['xclip', '-selection', 'clipboard', '-t',
                            'image/png'], input=shot.stdout)

    return f


# ----------------------------
# -------- Hotkeys -----------
# ----------------------------

mod = "mod4"
alt = "mod1"
keys = [

    # Layout hotkeys
    Key([mod], "minus", lazy.layout.shrink_main()),
    Key([mod], "plus", lazy.layout.grow_main()),
    Key([alt, "shift"], "Tab", lazy.layout.up()),
    Key([alt], "Tab", lazy.layout.down()),
    Key([mod, "shift"], "Tab", lazy.prev_layout()),
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "n", lazy.layout.normalize()),
    Key([mod], "o", lazy.layout.maximize()),
    # Key([mod],               "grave",  lazy.screen.toggle_group()),
    # Key([mod],               "plus",   lazy.layout.increase_ratio()),
    # Key([mod],               "minus",  lazy.layout.decrease_ratio()),

    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod, alt], "Down", lazy.layout.shuffle_down()),
    Key([mod, alt], "Up", lazy.layout.shuffle_up()),
    Key([mod, alt], "Left", lazy.layout.shuffle_left()),
    Key([mod, alt], "Right", lazy.layout.shuffle_right()),
    Key([mod, "shift"], "Down", lazy.layout.flip_down()),
    Key([mod, "shift"], "Up", lazy.layout.flip_up()),
    Key([mod, "shift"], "Left", lazy.layout.flip_left()),
    Key([mod, "shift"], "Right", lazy.layout.flip_right()),
    Key([mod, "control"], "Down", lazy.layout.grow_down()),
    Key([mod, "control"], "Up", lazy.layout.grow_up()),
    Key([mod, "control"], "Left", lazy.layout.grow_left()),
    Key([mod, "control"], "Right", lazy.layout.grow_right()),
    Key([mod, "control"], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.layout.toggle_split()),

    # Window hotkeys
    Key([mod], "f", lazy.window.toggle_fullscreen()),  # default
    Key([mod, "shift"], "f", lazy.window.toggle_floating()),  # default
    Key([mod, "shift"], "k", lazy.window.kill()),

    # Spec hotkeys
    Key([mod], "Return", lazy.spawncmd()),

    # Apps hotkeys
    Key([mod], "t", lazy.spawn("terminator")),
    Key([mod], "w", lazy.spawn("google-chrome-stable")),
    Key([mod], "c", lazy.spawn("terminator -e \"nano -w ~/.config/qtile/config.py\"")),

    # System hotkeys
    Key([], "Print", lazy.spawn("scrot -e 'mv $f /home/user/screenshots/'")),
    Key([mod, "shift", "control"], "h", lazy.spawn("systemctl hibernate")),
    Key([mod, "shift", "control"], "r", lazy.restart()),
    Key([mod, "shift", "control"], "q", lazy.shutdown()),
    Key([mod], "u", lazy.spawn("terminator -e \"yay -Syu --devel && read -p \\\"Press enter to continue\\\"\"")),
    Key([mod, "shift"], "u",
        lazy.spawn("terminator -e \"yay -yuYc --devel --gendb && read -p \\\"Press enter to continue\\\"\"")),

    # Media hotkeys
    Key([], 'XF86AudioMute', lazy.spawn('amixer -q set Master toggle')),
    Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -c 0 sset Master 1- unmute')),
    Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -c 0 sset Master 1+ unmute')),

    # dmenu
    Key([mod], 'm', lazy.spawn('xfce4-appfinder')),
    # Key([mod], 'm', lazy.spawn('dmenu_run -i -b -p ">>>" -fn "Open Sans-10" -nb "#000" -nf "#fff" -sb "#00BF32" -sf "#fff"')),
    # Key([mod], 'm', lazy.run_extension(extension.J4DmenuDesktop()))

    # screenshots
    Key([], 'Print', lazy.function(screenshot())),
    Key([mod], 'Print', lazy.spawn('deepin-screenshot'))
]


# ----------------------------
# --- Workspaces and Rooms ---
# ----------------------------

# The basic idea behind Workspaces and Rooms is to control
# DIFFERENT subsets of groups with the SAME hotkeys.
# So we can have multiple 'qwerasdf' rooms in a different workspaces.
#
# Qtile Groups are used behind the scenes, but their visibility
# is set dynamically.

def get_group_name(workspace, room):
    """ Calculate Group name based on (workspace,room) combination.
    """
    return "%s%s" % (room, workspace)


# List of available workspaces.
# Each workspace has its own prefix and hotkey.
workspaces = [
    (fa.icons['window-restore'], 'F1'),
    (fa.icons['chrome'], 'F2'),
    (fa.icons['code'], 'F3'),
    (fa.icons['comments'], 'F4'),
]

# List of available rooms.
# Rooms are identical between workspaces, but they can
# be changed to different ones as well. Minor changes required.
rooms = "123!"

# Oops, time fo|r a little hack there.
# This is a global object with information about current workspace.
# (viable as config code, not sure about client-server though)
wsp = {
    'current': workspaces[0][0],  # first workspace is active by default
}
# ... and information about active group in the each workspace.
for w, _ in workspaces:
    wsp[w] = {
        'active_group': get_group_name(w, rooms[0])  # first room is active by default
    }


def get_workspace_groups(workspace):
    """ Get list of Groups that belongs to workspace.
    """
    return [get_group_name(workspace, room) for room in rooms]


def get_room_groups(room):
    """ Get list of Groups that belongs to room.
    """
    return [get_group_name(w, room) for w, _ in workspaces]


def to_workspace(workspace):
    """ Change current workspace to another one.
    """

    def f(qtile):
        global wsp

        # we need to save current active room(group) somewhere
        # to return troomo it later
        wsp[wsp['current']]['active_group'] = qtile.currentGroup.name

        # now we can change current workspace to the new one
        # (no actual switch there)
        wsp['current'] = workspace
        # and navigate to the active group from the workspace
        # (actual switch)
        qtile.groupMap[
            wsp[workspace]['active_group']
        ].cmd_toscreen()

        # we also need to change subset of visible groups in the GroupBox widget
        qtile.widgetMap['groupbox'].visible_groups = get_workspace_groups(workspace)
        qtile.widgetMap['groupbox'].draw()
        qtile.widgetMap['workspacebox'].visible_groups = get_room_groups(wsp[workspace]['active_group'][:1])
        qtile.widgetMap['workspacebox'].draw()
        # You can do some other cosmetic stuff here.
        # For example, change Bar background depending on the current workspace.
        # # qtile.widgetMap['groupbox'].bar.background="ff0000"

    return f


def to_room(room):
    """ Change active room to another within the current workspace.
    """

    def f(qtile):
        global wsp
        qtile.widgetMap['workspacebox'].visible_groups = get_room_groups(room)
        qtile.widgetMap['workspacebox'].draw()
        qtile.groupMap[get_group_name(wsp['current'], room)].cmd_toscreen()

    return f


def window_to_workspace(workspace, room=rooms[0]):
    """ Move active window to another workspace.
    """

    def f(qtile):
        global wsp
        qtile.currentWindow.togroup(wsp[workspace]['active_group'])

    return f


def window_to_room(room):
    """ Move active window to another room within the current workspace.
    """

    def f(qtile):
        global wsp
        qtile.currentWindow.togroup(get_group_name(wsp['current'], room))

    return f


# Create individual Group for each (workspace,room) combination we have
groups = []
for workspace, hotkey in workspaces:
    for room in rooms:
        groups.append(Group(get_group_name(workspace, room), label=room))

# Assign individual hotkeys for each workspace we have
for workspace, hotkey in workspaces:
    keys.append(Key([mod], hotkey, lazy.function(
        to_workspace(workspace))))
    keys.append(Key([mod, "shift"], hotkey, lazy.function(
        window_to_workspace(workspace))))

# Assign shared hotkeys for each room we have.
# Decision about actual group to open is made dynamically.
for room in rooms:
    keys.append(Key([mod], room, lazy.function(
        to_room(room))))
    keys.append(Key([mod, "shift"], room, lazy.function(
        window_to_room(room))))

# ---------------------------
# ---- Layouts & Widgets ----
# ---------------------------

GAP_SIZE = 3

layouts = [
    layout.Bsp(margin=GAP_SIZE),
    layout.MonadTall(margin=GAP_SIZE),
    layout.MonadWide(margin=GAP_SIZE),
    layout.Max(),
    layout.Stack(margin=GAP_SIZE),
    layout.Columns(margin=GAP_SIZE),
    layout.VerticalTile(margin=GAP_SIZE),
    layout.TreeTab(panel_width=200),
]

widget_defaults = dict(
    font='Arial',
    fontsize=12,
    padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(
                    font="Arial",
                    foreground=GROUP_BG,
                    text="  ◢",
                    fontsize=(FONT_SIZE * 5.25),
                    padding=-1
                ),
                WorkspaceBox(
                    visible_groups=get_room_groups("1"),
                    spacing=0,
                    font="font-awesome",

                    other_current_screen_border=GROUP_OTHER_BORDER,
                    this_current_screen_border=GROUP_THIS_BORDER,
                    other_screen_border=GROUP_OTHER_BORDER,
                    this_screen_border=GROUP_THIS_BORDER,
                    highlight_color=GROUP_SELECTED_BG,
                    urgent_border=GROUP_URGENT_BORDER,
                    background=GROUP_BG,
                    highlight_method="line",
                    inactive=GROUP_INACTIVE_FG,
                    active=GROUP_ACTIVE_FG,
                    disable_drag=True,
                    borderwidth=4,
                    fontsize=FONT_SIZE,
                    foreground=GROUP_FG
                ),
                widget.TextBox(
                    font="font-awesome",
                    foreground=GROUP_FG,
                    background=GROUP_BG,
                    text=("→"),
                    fontsize=FONT_SIZE,
                    padding=15
                ),
                widget.GroupBox(
                    visible_groups=get_workspace_groups(wsp['current']),
                    spacing=0,
                    font="font-awesome",
                    # padding=-1,
                    background=GROUP_BG,
                    other_current_screen_border=GROUP_OTHER_BORDER,
                    this_current_screen_border=GROUP_THIS_BORDER,
                    other_screen_border=GROUP_OTHER_BORDER,
                    this_screen_border=GROUP_THIS_BORDER,
                    highlight_color=GROUP_SELECTED_BG,
                    urgent_border=GROUP_URGENT_BORDER,
                    highlight_method="line",
                    inactive=GROUP_INACTIVE_FG,
                    active=GROUP_ACTIVE_FG,
                    disable_drag=True,
                    borderwidth=4,
                    fontsize=FONT_SIZE,
                    foreground=GROUP_INACTIVE_FG
                ),
                widget.TextBox(
                    font="Arial",
                    foreground=GROUP_BG,
                    text="◤  ",
                    fontsize=(FONT_SIZE * 5.25),
                    padding=-20
                ),
                widget.Prompt(
                    prompt="run: ",
                    ignore_dups_history=True,
                    fontsize=FONT_SIZE
                ),
                widget.WindowName(
                    fontsize=FONT_SIZE
                ),
                widget.Spacer(
                    length=50
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.Spacer(
                    length=10
                ),
                widget.Mpris2(
                    background=BG_COLOR,
                    foreground=FG_COLOR,
                    name='spotify',
                    stop_pause_text='',
                    fontsize=FONT_SIZE,
                    scroll_chars=None,
                    display_metadata=['xesam:title', 'xesam:artist'],
                    objname="org.mpris.MediaPlayer2.spotify",
                ),
                widget.Spacer(
                    length=75
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.NetGraph(
                    bandwidth_type="up",
                    type="linefill",
                    line_width=1
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.NetGraph(
                    bandwidth_type="down",
                    type="linefill",
                    line_width=1
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),

     widget.CPUGraph(
                    type="linefill",
                    line_width=1
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.MemoryGraph(
                    type="linefill",
                    line_width=1
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.HDDBusyGraph(
                    device="nvme0n1",
                    type="linefill",
                    line_width=1
                ),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.ThermalSensor(
                    fontsize=FONT_SIZE,
                ),
                widget.Spacer(
                    length=100
                ),
                widget.CheckUpdates(
                    fontsize=FONT_SIZE,
                    display_format=" {updates}",
                    font="font-logos",
                    colour_have_updates=ALERT_COLOR,
                    # padding=15
                ),
                widget.Spacer(
                    length=10
                ),
                widget.Sep(),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.Spacer(
                    length=5
                ),
                widget.Volume(
                    fontsize=FONT_SIZE,
                    update_interval=2
                ),
                widget.Spacer(
                    length=10
                ),
                widget.Sep(),
                widget.Spacer(
                    length=10
                ),
                widget.TextBox(
                    font="font-awesome",
                    text=(""),
                    fontsize=FONT_SIZE,
                    padding=0
                ),
                widget.Spacer(
                    length=5
                ),
                widget.DF(
                    fontsize=FONT_SIZE,
                    warn_space=5,
                    visible_on_warn=False,
                    warn_color=ALERT_COLOR,
                ),
                widget.Spacer(
                    length=50
                ),
                widget.Systray(
                    # icon_size=ICON_SIZE,
                    # padding=ICON_PADDING
                ),
                widget.Spacer(
                    length=10
                ),
                widget.Clock(
                    fontsize=FONT_SIZE,
                    format='%a %b %d, %H:%M',
                ),
                widget.CurrentLayoutIcon(scale=0.65),
                widget.CurrentLayout(
                    fontsize=FONT_SIZE,
                ),
            ],
            (FONT_SIZE * 2),
            opacity=0.75
        ),
    )
]

mouse = [
    Click([mod, "shift"], "Button1", lazy.window.toggle_floating()),
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, alt], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod, "control"], "Button1", lazy.window.bring_to_front())
]

floating_layout = layout.floating.Floating(
    auto_float_types=(
        'notification',
        'toolbar',
        'splash',
        'dialog',
    ),
    float_rules=[{'wmclass': x} for x in (
        'audacious',
        'Download'
        'file_progress',
        'file-roller',
        'gimp',
        'Transmission',
        'Update',
        'Xephyr',
        'xfce4-appfinder',
    )]
)

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
focus_on_window_activation = "smart"
extentions = []
wmname = "LG3D"


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.call([home])



