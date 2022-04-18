from scripts.audio import SongAnalysis
from pathlib import Path
import math
import matplotlib.pyplot as plt
import numpy as np

SONG_NAME = "everbeing"
PATH = Path("data/music")


song_path = PATH / (SONG_NAME + ".wav")
analysis = SongAnalysis(str(song_path))

frames = int(analysis.duration) * 60
y_values = []
for i in range(frames):
    x = analysis.duration * (i / frames)
    try:
        y_values.append(np.mean(analysis.calculate_amps(x * 1000)[:10]) * 100)
    except IndexError:
        pass
    if int((i / frames) * 100) % 10 == 0:
        print(int((i / frames) * 100))

plt.plot(y_values)
plt.show()