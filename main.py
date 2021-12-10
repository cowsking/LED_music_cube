import librosa
import numpy as np
import pygame
import os
from AudioAnalyzer import *
avg_bass = 0
bass_trigger = -30
bass_trigger_started = 0
analyzer = AudioAnalyzer()

# os.putenv('SDL_VIDEODRIVER', 'fbcon')
# os.putenv('SDL_FBDEV', '/dev/fb0')

bass = {"start": 50, "stop": 100, "count": 12}

freq_groups = [bass]


beats = []

tmp_bars = []


length = 0

for group in freq_groups:

    g = []

    s = group["stop"] - group["start"]

    count = group["count"]

    reminder = s%count

    step = int(s/count)

    rng = group["start"]

    for i in range(count):

        arr = None

        if reminder > 0:
            reminder -= 1
            arr = np.arange(start=rng, stop=rng + step + 2)
            rng += step + 3
        else:
            arr = np.arange(start=rng, stop=rng + step + 1)
            rng += step + 2

        g.append(arr)

        length += 1

    tmp_bars.append(g)




def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


print('process 1')

# filename = "Armageddon.mp3"

filename = "test.mp3"
analyzer.load(filename)
time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))
print('stft 1')

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
print('frequencies')

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]

frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]

print(stft)

def get_decibel(target_time, freq):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]


pygame.init()

infoObject = pygame.display.Info()



screen_w = int(320)
screen_h = int(240)
# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])


print('process 2')

bars = []


frequencies = np.arange(100, 8000, 1600)

r = len(frequencies)


width = screen_w/r


x = (screen_w - width*r)/2

for c in frequencies:
    bars.append(AudioBar(x, 300, c, (255, 0, 0), max_height=400, width=width))
    x += width

for g in tmp_bars:
    gr = []
    for c in g:
        gr.append(
            AverageAudioBar(x, 300, c, (255, 0, 0), max_height=400, width=width))

    beats.append(gr)

print('process 3')

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

# Run until the user asks to quit
print('process 4')

running = True
while running:
    avg_bass = 0
    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
        b.render(screen)
    for b1 in beats:
        for b in b1:
            b.update_all(deltaTime, pygame.mixer.music.get_pos() / 1000.0, analyzer)
    for b in beats[0]:
        avg_bass += b.avg
    avg_bass /= len(beats[0])
    # if avg_bass > bass_trigger:
    #     print('above', avg_bass)
    # else:
    #     print('give up')
    # Flip the display
    pygame.display.flip()

pygame.quit()
