import numpy as np
import time
import cv2
import sounddevice as sd
#import pyaudio
from sonification import Sonifier

camera_ind = 0
last_image_time = time.time()
cap = cv2.VideoCapture(camera_ind)

samplerate = sd.query_devices('output')['default_samplerate']
sonifier = Sonifier(samplerate)
start_idx = 0
volume = 0.8

def callback(outdata, frames, time, status):
    global start_idx
    t = (start_idx + np.arange(frames)) / samplerate
    t = t.reshape(-1, 1)
    outdata[:] = sonifier.ConstructSound(t)
    start_idx += frames

stream = sd.OutputStream(channels=1, callback=callback, samplerate=samplerate)
stream.start()
while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    sonifier.Sonify(frame)


stream.close()

cap.release()
cv2.destroyAllWindows()
