#!/usr/bin/env python
# -*- coding: utf-8 -

from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = "mod4"

class Widget(object):

    battery = dict(
       energy_now_file='charge_now',
       energy_full_file='charge_full',
       power_now_file='current_now',
    )
    battery_text = battery.copy()
    battery_text.update(
        charge_char='',  # fa-arrow-up
        discharge_char='',  # fa-arrow-down
        format='{char} {hour:d}:{min:02d}',
    )

# Commands to spawn
class Commands(object):
    browser = 'google-chrome'
    file_manager = 'nautilus --no-desktop'
    lock_screen = 'gnome-screensaver-command -l'
    screenshot = 'gnome-screenshot'
    terminal = 'gnome-terminal'
    volume_up = 'amixer -q set Master,0 5%+ unmute'
    volume_down = 'amixer -q set Master,0 5%- unmute'
    # This command might not be correct, but it works
    volume_toggle = 'amixer -q -D pulse sset Master 1+ toggle'

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
    Key([mod], "Return", lazy.spawn(Commands.terminal)),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.nextlayout()),
    Key([mod], "w", lazy.window.kill()),

    Key([mod, "control"], "r", lazy.restart()),
    Key([mod, "control"], "q", lazy.shutdown()),
    Key([mod], "r", lazy.spawncmd()),

     # Commands: Volume Controls
    Key([], 'XF86AudioRaiseVolume', lazy.spawn(Commands.volume_up)),
    Key([], 'XF86AudioLowerVolume', lazy.spawn(Commands.volume_down)),
    Key([], 'XF86AudioMute', lazy.spawn(Commands.volume_toggle)),

    # TODO: What does the PrtSc button map to?
    Key([mod], 'p', lazy.spawn(Commands.screenshot)),
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

layouts = [
    layout.Max(),
    layout.Stack(num_stacks=2)
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
                widget.WindowName(),
                #widget.TextBox("default config", name="default"),
                widget.Systray(),
                widget.BatteryIcon(**Widget.battery),
                widget.Volume(theme_path='/usr/share/icons/Humanity/status/22/'),
                widget.Clock(format='%Y-%m-%d %a %I:%M %p'),
            ],
            size=30,
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
floating_layout = layout.Floating()
auto_fullscreen = True
wmname = "qtile"
