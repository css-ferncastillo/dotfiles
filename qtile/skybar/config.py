# -*- coding: utf-8 -*-
import os
import psutil
import socket
import subprocess

from libqtile import bar, hook, layout, qtile
from libqtile.config import Click, Drag, Group, Key, Screen
from libqtile.lazy import lazy
from libqtile.log_utils import logger
from libqtile.widget import (Battery, Clock, CurrentLayout, CurrentLayoutIcon,
                             GroupBox, Notify, PulseVolume, Prompt, Sep,
                             Spacer, Systray, TaskList, TextBox)

try:
    import aiomanhole
except ImportError:
    aiomanhole = None

DEBUG = os.environ.get("DEBUG")

GREY = "#222222"
DARK_GREY = "#111111"
BLUE = "#007fdf"
DARK_BLUE = "#002a4a"
ORANGE = "#dd6600"
DARK_ORANGE = "#371900"


def window_to_previous_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    previous_group_name = qtile.current_group.get_previous_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(previous_group_name)
    elif layout.current == 0 and len(layout.cc) == 1:
        if group_index != 0:
            qtile.current_window.togroup(previous_group_name)
    else:
        layout.cmd_shuffle_left()


def window_to_next_column_or_group(qtile):
    layout = qtile.current_group.layout
    group_index = qtile.groups.index(qtile.current_group)
    next_group_name = qtile.current_group.get_next_group().name

    if layout.name != "columns":
        qtile.current_window.togroup(next_group_name)
    elif layout.current + 1 == len(layout.columns) and len(layout.cc) == 1:
        if group_index + 1 != len(qtile.groups):
            qtile.current_window.togroup(next_group_name)
    else:
        layout.cmd_shuffle_right()


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    if len(qtile.screens) == 1:
        previous_switch = getattr(qtile, "previous_switch", None)
        qtile.previous_switch = qtile.current_group
        return qtile.current_screen.toggle_group(previous_switch)

    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


def init_keys():
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
    Key([mod, "control"], "r", lazy.restart()),

    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

    # ------------ App Configs ------------

    # Menu
    Key([mod], "m", lazy.spawn("rofi -show drun")),
    # Window Nav
    Key([mod, "shift"], "m", lazy.spawn("rofi -show")),

    # Browser
    Key([mod], "b", lazy.spawn("brave")),

    # File Explorer
    Key([mod], "e", lazy.spawn("thunar")),

    # Terminal
    Key([mod], "Return", lazy.spawn("alacritty")),

    # Redshift
    Key([mod], "r", lazy.spawn("redshift -O 2400")),
    Key([mod, "shift"], "r", lazy.spawn("redshift -x")),

    # Screenshot
    Key([mod], "s", lazy.spawn("scrot")),
    Key([mod, "shift"], "s", lazy.spawn("scrot -s")),

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
    if DEBUG:
        keys += [
            Key([mod], "Tab", lazy.layout.next()),
            Key([mod, "shift"], "Tab", lazy.layout.previous()),
            Key([mod, "shift"], "f", lazy.layout.flip()),
            Key([mod, "shift"], "s", lazy.group["scratch"].dropdown_toggle("term"))
        ]
    return keys


def init_mouse():
    mouse = [Drag([mod], "Button1", lazy.window.set_position_floating(),
                  start=lazy.window.get_position()),
             Drag([mod], "Button3", lazy.window.set_size_floating(),
                  start=lazy.window.get_size()),
             Click([mod], "Button2", lazy.window.kill())]
    if DEBUG:
        mouse += [Drag([mod, "shift"], "Button1", lazy.window.set_position(),
                       start=lazy.window.get_position())]
    return mouse


def init_groups():
    def _inner(key, name):
        keys.append(Key([mod], key, lazy.group[name].toscreen()))
        keys.append(Key([mod, "shift"], key, lazy.window.togroup(name)))
        return Group(name)

    groups = [("dead_grave", "00")]
    groups += [(str(i), "0" + str(i)) for i in range(1, 10)]
    groups += [("0", "10"), ("minus", "11"), ("equal", "12")]
    groups = [_inner(*i) for i in groups]

    if DEBUG:
        from libqtile.config import DropDown, ScratchPad
        dropdowns = [DropDown("term", terminal, x=0.125, y=0.25,
                              width=0.75, height=0.5, opacity=0.8,
                              on_focus_lost_hide=True)]
        groups.append(ScratchPad("scratch", dropdowns))
    return groups


def init_floating_layout():
    return layout.Floating(border_focus=ORANGE)


def init_layouts():
    margin = 0
    if len(qtile.core.conn.pseudoscreens) > 1:
        margin = 8
    kwargs = dict(margin=margin, border_width=1, border_normal=GREY,
                  border_focus=BLUE, border_focus_stack=ORANGE)
    layouts = [
        layout.Max(),
        layout.Columns(border_on_single=True, num_columns=2, grow_amount=5,
                           **kwargs),
        layout.MonadTall(),
        layout.MonadWide(),
        layout.Bsp(),
        layout.Matrix(),
        layout.RatioTile(),
    ]

    if DEBUG:
        layouts += [
            floating_layout, layout.Bsp(fair=False), layout.Zoomy(), layout.Tile(),
            layout.Matrix(), layout.TreeTab(), layout.MonadTall(margin=10),
            layout.RatioTile(), layout.Stack()
        ]
    return layouts


def parse_notification(message):
    return message.replace("\n", "⏎")


def init_widgets():
    widgets = [
        CurrentLayoutIcon(scale=0.6, padding=8),
        GroupBox(fontsize=9, padding=2, borderwidth=1, urgent_border=DARK_BLUE,
                 disable_drag=True, highlight_method="border",
                 this_screen_border=DARK_BLUE, other_screen_border=DARK_ORANGE,
                 this_current_screen_border=BLUE,
                 other_current_screen_border=ORANGE),

        TextBox(text="◤", fontsize=45, padding=-1, foreground=DARK_GREY,
                background=GREY),

        TaskList(borderwidth=0, highlight_method="block", background=GREY,
                 border=DARK_GREY, urgent_border=DARK_BLUE,
                 markup_floating="<i>{}</i>", markup_minimized="<s>{}</s>"),

        Prompt(background=GREY),
        Systray(background=GREY),
        TextBox(text="◤", fontsize=45, padding=-1,
                foreground=GREY, background=DARK_GREY),
        Notify(fmt=" 🔥 {} ", parse_text=parse_notification),
        PulseVolume(fmt=" {}", emoji=True, volume_app="pavucontrol"),
        #PulseVolume(volume_app="pavucontrol"),
        Clock(format=" ⏱ %H:%M  <span color='#666'>%A %d-%m-%Y</span>  ")
    ]
    if os.path.isdir("/sys/module/battery"):
        widgets.insert(-1, Battery(format=" {char} {percent:2.0%} ",
                                   charge_char=" ", discharge_char=" ",
                                   full_char=" ", unknown_char=" ",
                                   empty_char=" ", update_interval=2,
                                   show_short_text=False,
                                   default_text=""))
        widgets.insert(-1, Battery(fmt="<span color='#666'>{}</span> ",
                                   format="{hour:d}:{min:02d}",
                                   update_interval=2, show_short_text=True,
                                   default_text=""))
    if DEBUG:
        widgets += [Sep(), CurrentLayout()]
    return widgets


@hook.subscribe.client_new
def set_floating(window):
    floating_classes = ("nm-connection-editor", "pavucontrol", "gnome-screenshot")
    try:
        if window.window.get_wm_class()[0] in floating_classes:
            window.floating = True
    except IndexError:
        pass


@hook.subscribe.screen_change
def set_screens(event):
    logger.debug("Handling event: {}".format(event))
    subprocess.run(["autorandr", "--change"])
    qtile.restart()


@hook.subscribe.startup_complete
def set_logging():
    if DEBUG:
        qtile.cmd_debug()


if aiomanhole:
    @hook.subscribe.startup_complete
    def set_manhole():
        aiomanhole.start_manhole(port=7113, namespace={"qtile": qtile})


if __name__ in ["skybar.config", "__main__"]:
    local_bin = os.path.expanduser("~") + "/.local/bin"
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] = "{}:{}".format(local_bin, os.environ["PATH"])

    mod = "mod4"
    browser = "brave"
    terminal = "alacritty"
    screenlocker = "i3lock -d"
    hostname = socket.gethostname()
    cursor_warp = True
    focus_on_window_activation = "never"

    auto_fullscreen = False
    keys = init_keys()
    mouse = init_mouse()
    groups = init_groups()
    floating_layout = init_floating_layout()
    layouts = init_layouts()
    widgets = init_widgets()
    bar = bar.Bar(widgets=widgets, size=22, opacity=1)
    screens = [Screen(top=bar, wallpaper="~/.background.jpg")]
    widget_defaults = {"font": "DejaVu", "fontsize": 11, "padding": 2,
                       "background": DARK_GREY}
