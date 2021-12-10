import pandas as pd
import numpy as np
# import librosa
avg_bass = 0
bass_trigger = -30
# def clamp(min_value, max_value, value):
#     if value < min_value:
#         return 0
#     if value > max_value:
#         return 6
#     differences = max_value - min_value
#     res = int( -value / differences * 6)
#     return res

# def get_decibel(target_time, freq):
#     return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]

file_list = ['test']
for filename in file_list:

    spectrogram = np.array(pd.read_csv(filename+'/spectrogram.csv',header=None))
    # time_series, sample_rate = librosa.load(filename)  # getting information from the file
    times = pd.read_csv(filename+'/times.csv',header=None).values
    frequencies = pd.read_csv(filename+'/frequencies.csv',header=None).values
    time_index_ratio = len(times)/times[len(times) - 1]
    frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

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
            cube = np.roll(cube, -1, axis=0)
            # area = np.zeros((6,6))
            # ind = 0
            # for freq in frequencies:
            #     decibel = get_decibel(time_dif, freq)
            #     num = clamp(-80, 0, decibel)
            #     # print(decibel,num)
            #     for i in range(num):
            #         area[i][ind] = 1
            #     ind += 1
            # cube[5] = area
            # print(cube)
            # count += 0.2
    



class AudioAnalyzer:

    def __init__(self,name):

        self.name = name
        self.avg_bass = 0
        self.bass_trigger = -30
        self.time = 0
        self.spectrogram = np.array(pd.read_csv(name+'/spectrogram.csv',header=None))
        # time_series, sample_rate = librosa.load(filename)  # getting information from the file
        times = pd.read_csv(name+'/times.csv',header=None).values
        frequencies = pd.read_csv(name+'/frequencies.csv',header=None).values
        time_index_ratio = len(times)/times[len(times) - 1]
        frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

    def clamp(min_value, max_value, value):
        if value < min_value:
            return 0
        if value > max_value:
            return 6

    def get_decibel(target_time, freq):
        return self.spectrogram[int(self.freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]

    def set_time(time):
        self.time = time
    
    def area_generation(frequencies):
        area = np.zeros((6,6))
        ind = 0
        for freq in frequencies:
            decibel = get_decibel(time_dif, freq)
            num = clamp(-80, 0, decibel)
            for i in range(num):
                area[i][ind] = 1
            ind += 1
        return area