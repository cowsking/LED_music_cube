# f = open('music_fifo', 'r')
# f = open('/home/pi/LED_music_cube/TEST_FIFO/music_fifo','r').readlines()
import time
import sys
from os.path import exists
import os
import pandas as pd
import numpy as np
import serial
# import time

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

if exists('music_fifo'):
    os.remove("music_fifo")


name = None
pos = 0
from AudioAnalyzer import *
cube = np.zeros((6,6,6))
import time
start_time = time.time()
running = True
cur_name = 'Enemy (From the series "Arcane League of Legends")'
frequences = np.arange(100, 8000, 1400)
play = False
player = AudioAnalyzer(cur_name)
play_time = 0
# paused_time = 0
last_time = time.time()
while running:
    time.sleep(0.3)
    # if cur_name != name:
    #     cur_name = name
    #     player = AudioAnalyzer(name)
    #     player.set_time(0)
    # if cur_pos != pos:
    #     cur_pos = pos
    #     time_dif = cur_pos
    #     start_time = time.time()
    # elif name:
    if exists('music_fifo'):
        with open('music_fifo') as fifo:
            # select.select([fifo],[],[fifo])
            # print('2')
            data = fifo.read()
            # print('3')
            # print(data)
            # print(data)
            # print('4')
            if 'paused' in data:
                # pause_start = time.time()
                play = False
            elif 'playing' in data:
                
                play = True
                # if not pause_start:
                #     paused_time = 0
                # else:
                #     paused_time += time.time() - pause_start
                
            if data == 'Enemy (From the series "Arcane League of Legends")' and data != cur_name:
                cur_name = 'Enemy (From the series "Arcane League of Legends")'
                player = AudioAnalyzer(cur_name)
                start_time = time.time()
                play_time = 0
                # play = False
                # pause_start = None
            elif data == 'Warriors' and data != cur_name:
               
                cur_name = 'Warriors'
                player = AudioAnalyzer(cur_name)
                start_time = time.time()
                play_time = 0
                # play = False
                # pause_start = None

            if data.isdigit():
                play_time = int(data) / 1000
                # print(play_time)
                
            # sys.stdout.flush()
        os.remove("music_fifo")
    # print('play',play)
    # if play:
    #     print("pause", paused_time)
    #     play_time = time.time() - paused_time - start_time - 0.5
    #     print(play_time)
        # player.set_time(play_time)
        # np.roll(cube, -1, axis=0)
        # cube[5] = player.area_generation(frequences)
        # print(player.name)
    # print(play)
    if play:
            # print("pause", paused_time)
        cur_time = time.time()
        # print(play_time)
        play_time = play_time + cur_time - last_time
        last_time = cur_time
        # print('play_time',play_time, 'last_time',last_time, 'cur_time', cur_time)
        
        # print(play_time)
        player.set_time(play_time)
        cube = np.roll(cube, -1, axis=0)
        cube[5] = player.area_generation(frequences)
        # print(cube[5])
        lst = []
        for i in range(cube[5].shape[1]):
            for j in range(cube[5].shape[0]):
                lst.append(cube[5][j][i])
        curr_str = "".join([str(int(x)) for x in lst])
        print(curr_str)
        # curr_str = "000000000011111111110000000000000000"
        out_str = curr_str + "\n"
        command = bytes(out_str, 'utf-8')
        # print(command)
        temp1 = time.time()
        ser.reset_input_buffer()
        ser.reset_output_buffer()
        # out_str2 = 'exit'+ "\n"
        # command2 = bytes(out_str2, 'utf-8')
        ser.write(command)
        # ser.write(command2)
        print(time.time()- temp1)

        # print("out_str", out_str)
        
        
        # res = list((cube.flatten()))
   
        # curr_str = "".join([str(int(x)) for x in res])

        # out_str = ""

        # for i in range(len(curr_str)):
        #     if i%6==1:
        #         out_str+=curr_str[i]
        # out_str += "\n"
        # out_str = '000001000000000000100000000100001000\n'
        # command = bytes(out_str, 'utf-8')
        # print(command)
        # ser.write(command)
        # print("out_str", out_str)
                


                
        









