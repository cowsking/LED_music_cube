import librosa
import numpy as np
import pandas as pd
import os
# analyzer.load(filename)
file_list = ['Warriors']
for filename in file_list:
    os.mkdir(filename)
    time_series, sample_rate = librosa.load(filename+'.mp3')  # getting information from the file

    # getting a matrix which cont   ains amplitude values according to frequency and time indexes
    stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

    spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

    frequencies =librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies
    times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)
    # print(frequencies)
    # print(spectrogram.shape)
    frequences = np.arange(100, 8000, 1400)
    frequences = frequences * 0.37160998
    frequences = [int(x) for x in list(frequences.astype(int))]
    spectrogram = pd.DataFrame(spectrogram)
    print(spectrogram.shape)
    spectrogram = spectrogram.iloc[frequences, :]
    print(frequencies)
    spectrogram.to_csv(filename+'/spectrogram.csv', index = False, header=False)
    times = pd.DataFrame(times)
    times.to_csv(filename+'/times.csv', index = False,header=False)
    # frequencies = pd.DataFrame(frequencies)
    # frequencies.to_csv(filename+'/frequencies.csv', index = False,header=False)
