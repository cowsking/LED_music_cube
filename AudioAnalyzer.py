import math

import matplotlib.pyplot as plt
import librosa.display
import numpy as np


# binary search
import pygame






def translate(xy, offset):
    return xy[0] + offset[0], xy[1] + offset[1]


def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioAnalyzer:

    def __init__(self):

        self.frequencies_index_ratio = 0  # array for frequencies
        self.time_index_ratio = 0  # array of time periods
        self.spectrogram = None  # a matrix that contains decibel values according to frequency and time indexes

    def load(self, filename):

        time_series, sample_rate = librosa.load(filename)  # getting information from the file

        # getting a matrix which contains amplitude values according to frequency and time indexes
        stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

        self.spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

        frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

        # getting an array of time periodic
        times = librosa.core.frames_to_time(np.arange(self.spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

        self.time_index_ratio = len(times)/times[len(times) - 1]

        self.frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]




    def show(self):

        librosa.display.specshow(self.spectrogram,
                                 y_axis='log', x_axis='time')

        plt.title('spectrogram')
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()

    def get_decibel(self, target_time, freq):

        return self.spectrogram[int(freq*self.frequencies_index_ratio)][int(target_time*self.time_index_ratio)]

        # returning the current decibel according to the indexes which found by binary search
        # return self.spectrogram[bin_search(self.frequencies, freq), bin_search(self.times, target_time)]

    def get_decibel_array(self, target_time, freq_arr):

        arr = []

        for f in freq_arr:
            arr.append(self.get_decibel(target_time,f))

        return arr


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):

        pygame.draw.rect(screen, self.color, (self.x, self.y + self.max_height - self.height, self.width, self.height))

class AverageAudioBar(AudioBar):

    def __init__(self, x, y, rng, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):
        super().__init__(x, y, 0, color, width, min_height, max_height, min_decibel, max_decibel)

        self.rng = rng

        self.avg = 0

    def update_all(self, dt, time, analyzer):

        self.avg = 0

        for i in self.rng:
            self.avg += analyzer.get_decibel(time, i)
            # print(i, self.avg)
        self.avg /= len(self.rng)
        # print('time', time, self.avg)
        self.update(dt, self.avg)



    def render(self, screen):

        pygame.draw.polygon(screen, self.color, self.rect.points)

    def render_c(self, screen, color):

        pygame.draw.polygon(screen, color, self.rect.points)

 


    def draw(self,screen):
        pygame.draw.polygon(screen, (255,255, 0), self.points)
