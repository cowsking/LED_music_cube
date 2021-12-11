import pandas as pd
import numpy as np

class AudioAnalyzer:

    def __init__(self,name):

        self.name = name
        self.avg_bass = 0
        self.bass_trigger = -30
        self.time = 0
        self.spectrogram = np.array(pd.read_csv(name+'/spectrogram.csv',header=None))
        # time_series, sample_rate = librosa.load(filename)  # getting information from the file
        self.times = pd.read_csv(name+'/times.csv',header=None).values
        self.frequencies = pd.read_csv(name+'/frequencies.csv',header=None).values
        self.time_index_ratio = len(self.times)/self.times[len(self.times) - 1]
        self.frequencies_index_ratio = len(self.frequencies)/self.frequencies[len(self.frequencies)-1]

    def clamp(min_value, max_value, value):
        if value < min_value:
            return 0
        if value > max_value:
            return 6

    def get_decibel(self,target_time, freq):
        return self.spectrogram[int(self.freq * self.frequencies_index_ratio)][int(target_time * self.time_index_ratio)]

    def set_time(self,time):
        self.time = time
    
    def area_generation(self,frequencies):
        area = np.zeros((6,6))
        ind = 0
        for freq in frequencies:
            decibel = get_decibel(time_dif, freq)
            num = clamp(-80, 0, decibel)
            for i in range(num):
                area[i][ind] = 1
            ind += 1
        return area