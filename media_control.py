import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
def set_pos(value):
    global pos 
    pos = value 
def set_name(value):
    global name 
    name = value 
def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    for prop, value in changed.items():
        if prop == 'Position':
            set_pos(value)
        if prop == 'Status':
            print('Playback Status: {}'.format(value))
        # elif prop == 'Track':
        #     print('Music Info:')
        #     for key in ('Title', 'Artist', 'Album'):
        #         print('   {}: {}'.format(key, value.get(key, '')))
        elif prop == 'Track':
            set_name(value.get('Title',''))
def on_playback_control(fd, condition):
    str = fd.readline()
    if str.startswith('play'):
        player_iface.Play()
    elif str.startswith('pause'):
        player_iface.Pause()
    elif str.startswith('next'):
        player_iface.Next()
    elif str.startswith('prev'):
        player_iface.Previous()
    elif str.startswith('vol'):
        vol = int(str.split()[1])
        if vol not in range(0, 128):
            print('Possible Values: 0-127')
            return True
        transport_prop_iface.Set(
                'org.bluez.MediaTransport1',
                'Volume',
                dbus.UInt16(vol))
    return True

if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()
    obj = bus.get_object('org.bluez', "/")
    mgr = dbus.Interface(obj, 'org.freedesktop.DBus.ObjectManager')
    player_iface = None
    transport_prop_iface = None
    for path, ifaces in mgr.GetManagedObjects().items():
        # print(ifaces)
        if 'org.bluez.MediaPlayer1' in ifaces:
            player_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.bluez.MediaPlayer1')
        elif 'org.bluez.MediaTransport1' in ifaces:
            transport_prop_iface = dbus.Interface(
                    bus.get_object('org.bluez', path),
                    'org.freedesktop.DBus.Properties')
    if not player_iface:
        sys.exit('Error: Media Player not found.')
    if not transport_prop_iface:
        sys.exit('Error: DBus.Properties iface not found.')

    bus.add_signal_receiver(
            on_property_changed,
            bus_name='org.bluez',
            signal_name='PropertiesChanged',
            dbus_interface='org.freedesktop.DBus.Properties')
    # GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)
    # GLib.MainLoop().run()
    name = None
    pos = 0
    import pandas as pd
    import numpy as np
    from AudioAnalyzer import *
    cube = np.zeros((6,6,6))
    import time
    start_time = time.time()
    running = True
    time_dif = time.time()-start_time
    count = 1
    cur_name = None
    cur_pos = 0
    frequences = np.arange(100, 8000, 1400)

    while running:
        time.sleep(0.5)
        if cur_name != name:
            cur_name = name
            player = AudioAnalyzer(name)
            player.set_time(0)
        if cur_pos != pos:
            cur_pos = pos
            time_dif = cur_pos
            start_time = time.time()
        else:
            time_dif = time.time() - start_time
            player.set_time(time_dif)
            np.roll(cube, -1, axis=0)
            cube[5] = player.area_generation(frequences)
            
        
        
        