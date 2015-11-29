#!/usr/bin/env python
# -*- coding: utf-8 -

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget
from os.path import expanduser
from network_icon import NetworkIcon

mod = "mod4"
home = expanduser("~")

# Commands to spawn
class Commands(object):
    browser = 'google-chrome'
    file_manager = 'nautilus --no-desktop'
    dev_ide = 'QT_QPA_PLATFORMTHEME=""; qtcreator'
    settings = 'unity-control-center'
    lock_screen = 'gnome-screensaver-command -l'
    screenshot = 'gnome-screenshot'
    terminal = 'gnome-terminal'
    volume_up = 'amixer -q set Master,0 5%+ unmute'
    volume_down = 'amixer -q set Master,0 5%- unmute'
    # This command might not be correct, but it works
    volume_toggle = 'amixer -q -D pulse sset Master 1+ toggle'
    sound_player = 'mplayer'
    disaster_sound = ' ' + home + '/.config/qtile/sounds/nooo.mp3'

keys = [
    # Switch between windows in current stack pane
    Key(
        [mod], "k",
        lazy.layout.down()
    ),
    Key(
        [mod], "j",
        lazy.layout.up()
    ),

    # Move the current window between stacks
    Key(
        [mod, "shift"], "j",
        lazy.layout.client_to_previous()
    ),
    Key(
        [mod, "shift"], "k",
        lazy.layout.client_to_next()
    ),

    # Move windows up or down in current stack
    Key(
        [mod, "control"], "k",
        lazy.layout.shuffle_down()
    ),
    Key(
        [mod, "control"], "j",
        lazy.layout.shuffle_up()
    ),

    # Switch window focus to other pane(s) of stack
    Key(
        [mod], "space",
        lazy.layout.next()
    ),

    # Swap panes of split stack
    Key(
        [mod, "shift"], "space",
        lazy.layout.rotate()
    ),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"], "Return",
        lazy.layout.toggle_split()
    ),

    # Application launchers
    Key([mod], "Return", lazy.spawn(Commands.terminal)),
    Key([mod], 'b', lazy.spawn(Commands.browser)),
    Key([mod], 'f', lazy.spawn(Commands.file_manager)),
    Key([mod], 'q', lazy.spawn(Commands.dev_ide)),
    Key([mod], 'c', lazy.spawn(Commands.settings)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    # Commands for restarting, locking, shutting down
    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod, 'control'], 'l', lazy.spawn(Commands.lock_screen)),

     # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),

    # TODO: What does the PrtSc button map to?
    Key([mod], 's', lazy.spawn(Commands.screenshot)),

    # Press in case of emergency
    Key([mod, "control"], 'n', lazy.spawn(Commands.sound_player + Commands.disaster_sound)),
]

groups = [Group(i) for i in "123456"]

for i in groups:
    # mod1 + letter of group = switch to group
    keys.append(
        Key([mod], i.name, lazy.group[i.name].toscreen())
    )

    # mod1 + shift + letter of group = switch to & move focused window to group
    keys.append(
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name))
    )

layout_defaults = dict(
    border_width=1,
    margin=0,
    border_focus='#ffa500',
    border_normal='#333333',
)

layouts = [
    layout.Max(**layout_defaults),
    layout.Stack(num_stacks=2, **layout_defaults),
    #layout.xmonad.MonadTall(**layout_defaults),
]

widget_defaults = dict(
    font='Arial',
    fontsize=15,
    #padding=3,
)

screens = [
    Screen(
        top=bar.Bar(
            widgets=[
                widget.GroupBox(),
                widget.Prompt(),
                #widget.AGroupBox(),
                widget.WindowName(),
                #widget.TextBox("default config", name="default"),
                widget.Mpris2(objname="org.mpris.MediaPlayer2.rhythmbox"),
                widget.Systray(),
                widget.Spacer(width=12),
                NetworkIcon(theme_path=home+'/.config/qtile/icons/mono'),
                widget.BatteryIcon(theme_path=home+'/.config/qtile/icons/mono', battery_name='BAT0'),
                widget.Volume(theme_path=home+'/.config/qtile/icons/mono'),
                #widget.NetGraph(interface='auto'),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            size=30,
            #icon_size=20,
            background=['222222', '111111'],
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
        start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
        start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(**layout_defaults)
auto_fullscreen = True
wmname = "qtile"
