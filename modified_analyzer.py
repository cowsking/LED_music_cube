import librosa
import numpy as np
# import pygame
import os
avg_bass = 0
bass_trigger = -30
# bass_trigger_started = 0



# bass = {"start": 50, "stop": 100, "count": 12}

# freq_groups = [bass]


# beats = []

# tmp_bars = []


# length = 0

# for group in freq_groups:
#     g = []
#     s = group["stop"] - group["start"]
#     count = group["count"]
#     reminder = s%count
#     step = int(s/count)
#     rng = group["start"]

#     for i in range(count):
#         arr = None
#         if reminder > 0:
#             reminder -= 1
#             arr = np.arange(start=rng, stop=rng + step + 2)
#             rng += step + 3
#         else:
#             arr = np.arange(start=rng, stop=rng + step + 1)
#             rng += step + 2
#         g.append(arr)
#         length += 1
#     tmp_bars.append(g)

def clamp(min_value, max_value, value):
    if value < min_value:
        return 0
    if value > max_value:
        return 6
    differences = max_value - min_value
    res = int(value / differences * 7)
    return res

    
filename = "test.mp3"
# filename = "Armageddon.mp3"

time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
# print('stft 1')
spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix
frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
# print('frequencies')
# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
time_index_ratio = len(times)/times[len(times) - 1]
frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]



bars = []
frequencies = np.arange(100, 8000, 1400)
# r = len(frequencies)
# print(frequencies)

cube = np.zeros((6,6,6))
import time
start_time = time.time()
running = True
time_dif = time.time()-start_time
count = 1
while time_dif<12:
    avg_bass = 0
    time_dif = time.time()-start_time
    if time_dif > count:
        #beat
        for freq in range(50,120):
            avg_bass += get_decibel(time_dif, freq)
        avg_bass /= 70
        if avg_bass > bass_trigger:
            print('beat')



        #freqs
        np.roll(cube, -1, axis=0)
        area = np.zeros((6,6))
        ind = 0
        for freq in frequencies:
            decibel = get_decibel(time_dif, freq)
            num = clamp(-80, 0, decibel)
            for i in range(num):
                area[ind][i] = 1
        cube[5] = area
        print(cube)
        count += 0.2
    


    