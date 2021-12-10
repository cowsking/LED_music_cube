import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy.core.multiarray
f = 'Armageddon.mp3'
x, sr = librosa.load(f, sr=44100)
# print(type(x),type(sr))
print(x)

plt.figure(figsize=(14,5))
librosa.display.waveplot(x,sr=sr)
plt.show()
print('asd')