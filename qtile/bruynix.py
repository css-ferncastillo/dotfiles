####################################
# QTILE CONFIG BY MAARTEN BRUYNINX #
####################################

# Imports
from typing import List  # noqa: F401
from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os
from datetime import datetime
import subprocess


# Some quick settings
mod = "mod4"
terminal = "alacritty"
browser = "brave"
home = os.path.expanduser("~/Imágenes")
savePath = os.path.join(home, 'Screenshots')
if not os.path.isdir(savePath):
   os.mkdir(savePath)
datename = datetime.now().strftime("%Y%m%d%I%M%S%f")

autostart = [
        "feh --bg-fill --randomize /usr/share/backgrounds/*",
        "xrandr --output eDP1 --primary --mode 1366x768 --pos 0x0 --rotate normal --output DP1 --mode 1366x768 --pos 1366x0 --rotate normal --output HDMI1 --off --output HDMI2 --off --output VIRTUAL1 --off"
        ]
for x in autostart:
    os.system(x)

#me Keybinds
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
        Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
        Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
        Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
        # Brightness
        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +10%")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 10%-")),
]

# Groups
# I have 9 groups declared, but will autohide the ones not in use
group_names = [
    (" ", {'layout': 'MonadTall'}),
    (" ", {'layout': 'MonadTall'},),
    (" ", {'layout': 'MonadTall'}),
    (" ", {'layout': 'MonadTall'}),
    (" ", {'layout': 'MonadTall'}),
    ("梅", {'layout': 'MonadTall'}),
    ("甆", {'layout': 'MonadTall'}),
    ("", {'layout': 'MonadTall'})
]
groups = [Group(name, **kwargs) for name, kwargs in group_names]
for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # Send current window to another group 

# Colors

background_light = ["#3B4252", "#3B4252"]
background_dark = ["#2E3440", "#2E3440"]
foreground = ["#D8DEE9", "#D8DEE9"]

red = ["#BF616A", "#BF616A"]
green = ["#A3BE8C", "#A3BE8C"]
blue = ["#88c0d0", "#88c0d0"]
yellow = ["#EBCB8B", "#EBCB8B"]
orange = ["#D08770", "#D08770"]
purple = ["#B48EAD", "#B48EAD"]

colors = [["#2e3440", "#2e3440"],
          ["#4c566a", "#4c566a"],
#          ["#88c0d0", "#88c0d0"],
          ["#D8DEE9", "#D8DEE9"],
          ["#434c5e", "#434c5e"],
          ["#3b4252", "#3b4252"],
          ["#81a1c1", "#81a1c1"],
          ["#5E81AC", "#5E81AC"],
          ["#eceff4", "#eceff4"],
          ["#d8dee9", "#d8dee9"],
        ]


darks = [
    ["#2E3440", "#2E3440"],
    ["#3B4252", "#3B4252"],
    ["#434C5E", "#434C5E"],
    ["#4C566A", "#4C566A"],
]

accents =[
    ["#D08770", "#D08770"],
    ["#A3BE8C", "#A3BE8C"],
    ["#B48EAD", "#B48EAD"],
    ["#EBCB8B", "#EBCB8B"],
    ["#5E81AC", "#5E81AC"],
    ["#BF616A", "#BF616A"],
    ["#88c0d0", "#88c0d0"],
]


# Layout theme defines how to place windows in my layout (I only use one layout)
layout_theme = {
    "border_width": 2,
    "margin": 3,
    "border_focus": blue,
    "border_normal": "1D2330",
}
layouts = [
    layout.Columns(**layout_theme),
    layout.Max(),
    layout.MonadTall(**layout_theme),
    layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.RatioTile(**layout_theme)
]

widget_defaults = dict(
    font="Caskaydia Cove Nerd Font",
    fontsize = 11,
    padding = 2,
    background= background_dark,
    foreground = foreground
)
extension_defaults = widget_defaults.copy()

# Incase we need spacing
dark_sep = widget.Sep(linewidth = 0, padding = 6, background = background_dark, foreground = background_dark)
light_sep = widget.Sep(linewidth = 0, padding = 6, background = background_light, foreground = background_light)

# List of widgets, to display on the bottom bar
widgets = [
    # Left side
    # Arch icon to open a terminal
    dark_sep,
   # widget.Image(filename = "~/.config/qtile/arch.png",scale = "Trye", mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}),
    dark_sep,
    # Group box
    dark_sep,
    widget.GroupBox(
        margin_y = 0,
        margin_x = 0,
        padding_y = 0,
        padding_x = 0,
        borderwidth = 1,
        disable_drag = True,
        block_highlight_text_color = colors[2],
        active = darks[3],
        inactive = colors[2],
        rounded = False,
        highlight_color = darks[0],
        highlight_method = "line",
        hide_unused = True,
        this_current_screen_border = colors[2],
        this_screen_border = colors [2],
        spacing = 5, 
        fontsize = 14
    ),
    dark_sep,
    # Powerline-like arrow to right
    widget.TextBox(text = '\ue0b0', background = background_light, foreground = background_dark, padding = 0, fontsize = 16),
    # Middle side
    # Current window
    light_sep,
    widget.WindowName(background = background_light),
    light_sep,
    # Systemtray
    widget.Systray(background = background_light),
    light_sep,
    # Right side
    # Quick settings
    widget.TextBox(text = '\ue0b2', background = background_light, foreground = background_dark, padding = 0, fontsize = 16),
    dark_sep,
    # Updates
    widget.TextBox(text = "  ", padding = 0, foreground = accents[6]),
    widget.CheckUpdates(
        update_interval = 1800,
        distro = "Arch_checkupdates",
        display_format = " {updates}",
        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e yay -Syyuu')},
        no_update_string = " 0",
        padding = 0,
        colour_have_updates = red,
        colour_no_updates = blue,
        custom_command='checkupdates',
    ),
    # Volume
    widget.TextBox(text = "    ", padding = 0, foreground = orange,
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e alsamixer')},
    ),
    widget.Volume(foreground = orange),
    # Microphone
    widget.TextBox(text = "   ", padding = 0, foreground= orange,
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e alsamixer')},
    ),
    widget.Volume(foreground = orange, channel = 'Capture'),
    # Battery
    widget.Battery(battery = 0 ,format=' {percent:2.0%} ', hide_threshold = 0.30, foreground = foreground, update_interval = 1),
    # Wifi
    widget.Net(foreground = red, interface = 'wlan0', format = '  {down} '),
    widget.Net(foreground = green, interface = 'wlan0', format = ' {up} '),
    # CPU
    widget.CPU(foreground = yellow, format = ' {freq_current}GHz {load_percent}%'
            ,mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bashtop')}
    ),
    # GPU
    #widget.NvidiaSensors(foreground = yellow, format = '  {temp}°C', 
    #        mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e nvtop')}
    #),
    widget.Memory(foreground = yellow, measure_mem= 'M', format='  {MemUsed: .0f}{mm}/{MemTotal: .0f}{mm} ', 
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bashtop')}
    ),
    # Clock
    widget.Clock(foreground = purple, format = "   %a %d %b %Y    %H:%M:%S "),
]

# need to re-create the group box or it won't work on 2 monitors
group_and_middle = [
        # Group box   
        dark_sep,
        widget.GroupBox(
            margin_y = 3,
            margin_x = 0,
            padding_y = 5,
            padding_x = 3,
            borderwidth = 3,
            disable_drag = True,
            block_highlight_text_color = colors[2],
            active = darks[3],
            inactive = colors[2],
            rounded = False,
            highlight_color = darks[0],
            highlight_method = "line",
            hide_unused = True,
            this_current_screen_border = colors[2],
            this_screen_border = colors [2],
            spacing = 20, 
            fontsize = 12
        ),
        widget.TextBox(text = '\ue0b0', background = background_light, foreground = background_dark, padding = 0, fontsize = 43),
        # Middle side
        # Current window
        light_sep,
        widget.WindowName(background = background_light),
        light_sep,
        # Systemtray
        widget.Systray(background = background_light),
        light_sep,
]

# Append the bar to the bottom of the screen

screens = [
    Screen(
        top=bar.Bar(widgets,24)
    ),
    Screen(
        top=bar.Bar(widgets[:4] + group_and_middle + widgets[11:],24)),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
    Click([mod, 'shift'], "Button1", lazy.window.disable_floating()),
    Click([mod], "Button1", lazy.window.bring_to_front()) 
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
], **layout_theme)
auto_fullscreen = False
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = False

wmname = "LG3D"
