#Object to Convert Camera Stream into Sound
import numpy as np
import cv2

class Sonifier():
    def __init__(self, fs):
        self.sample_rate = fs

        self.amplitude = 0.0
        self.smoothing = 0.5

        self.blue_intensity = 0.01
        self.blue_frequency = 0.1

        self.red_intensity = 0.01
        self.red_frequency = 0.01

        self.white_intensity = 0.01
        self.white_frequency = 0.01

        self.black_intensity = 0.01
        self.black_frequnecy = 0.01

        self.white_tone = 2 * np.pi * 200
        self.black_tone = 2 * np.pi * 50
        self.red_tone = 2 * np.pi * 400
        self.blue_tone = 2 * np.pi * 240

    def Smooth(self, newValue, priorValue):
        return self.smoothing * priorValue + (1.0 - self.smoothing) * newValue

    def Sonify(self, img):
        img_hsl = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        is_black = (img_hsl[:,:,2] < 0.3)
        is_white = np.logical_and((img_hsl[:,:,2] >= 0.3) , (img_hsl[:,:,1] < 0.3))
        is_color = np.logical_and((img_hsl[:,:,2] >= 0.3) , (img_hsl[:,:,1] > 0.3))
        is_blue = np.logical_and(is_color, np.logical_and((img_hsl[:,:,0] < 260), (img_hsl[:,:,0] > 90)))
        is_red = np.logical_and(is_color, np.logical_and((img_hsl[:,:,0] >= 260), (img_hsl[:,:,0] <= 90)))

        self.white_intensity = self.Smooth(np.mean(is_white), self.white_intensity)
        self.black_intensity = self.Smooth(np.mean(is_black), self.black_intensity)
        self.red_intensity = self.Smooth(np.mean(is_red), self.red_intensity)
        self.blue_intensity = self.Smooth(np.mean(is_blue), self.blue_intensity)

    def ConstructSound(self, t):
        white_signal = 0.3 * self.white_intensity * np.sin(self.white_tone * t)
        blue_signal = 0.4 * self.blue_intensity * np.sin(self.blue_tone * t)
        red_signal = 0.2 * self.red_intensity * np.sin(self.red_tone * t)
        black_signal = 0.1 * self.black_intensity * np.sin(self.black_tone * t)
        return white_signal + blue_signal + red_signal + black_signal
