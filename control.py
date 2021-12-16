import dbus, dbus.mainloop.glib, sys
from gi.repository import GLib
import os
from os.path import exists

import time
def on_property_changed(interface, changed, invalidated):
    if interface != 'org.bluez.MediaPlayer1':
        return
    if not exists('music_fifo'):
        os.mkfifo('music_fifo')
    # print(changed.items())
    
    for prop, value in changed.items():
        

        # time.sleep(0.1)
        if prop == 'Position':
            with open('music_fifo', 'w') as fifo:
                print(value)
                fifo.write(str(value))
                fifo.flush()
        elif prop == 'Status':
            with open('music_fifo', 'w') as fifo:
                print(value)
                fifo.write(value)
                fifo.flush()
        # elif prop == 'Track':
        #     print('Music Info:')
        #     for key in ('Title', 'Artist', 'Album'):
        #         print('   {}: {}'.format(key, value.get(key, '')))
        elif prop == 'Track':
            # set_name(value.get('Title',''))
            # os.mkfifo('music_fifo')
            with open('music_fifo', 'w') as fifo:
                print(value.get('Title', ''))
                fifo.write(value.get('Title',''))
                fifo.flush()
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
    GLib.io_add_watch(sys.stdin, GLib.IO_IN, on_playback_control)
    
    
    GLib.MainLoop().run()
    # print('asd')
    # while True:
    #     f = open('/home/pi/LED_music_cube/TEST_FIFO/music_fifo','r').readlines()
    # print('asd')
    # count = 0    
    # print('asd')
    # while True:
    #     print('asd')
    #     count = len(f.readlines())
    #     print(count)
        # print(f)
        

        