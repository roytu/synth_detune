#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow

from gui_ import Ui_Soundgen

from sound_handler import SoundHandler

from time import time
import pyaudio as pya

from c_signals import generate

import timeit

DEBUG = False

class Gui(QApplication):
    def __init__(self, args):
        QApplication.__init__(self, args)

        self.mainWindow = QMainWindow()
        self.ui = Ui_Soundgen()
        self.ui.setupUi(self.mainWindow)
        self.mainWindow.show()

        # Connect signals
        self.aboutToQuit.connect(self._on_quit)

        # Initialize sound handler
        self.sh = SoundHandler()

        def func(in_data, frame_count, time_info, status):
            return (self._on_stream_request(frame_count), pya.paContinue)
        self.sh.init_stream(callback=func, frames=44100)
        self.start_time = time()
        if DEBUG:
            self.ts = np.array([])
            self.xs = np.array([])

    def _on_stream_request(self, frame_count):
        """ Generate more chunks for signal """
        bytestream = generate()

        if DEBUG:
            t_0 = time()
            t_1 = t_0
            ts = np.linspace(t_0, t_1, 44100)
            self.ts = np.hstack([self.ts, ts])
            self.xs = np.hstack([self.xs, bytestream])

        return bytestream

    def _on_quit(self):
        if DEBUG:
            np.save("ts.npy", self.ts)
            np.save("xs.npy", self.xs)

if __name__ == "__main__":
    gui = Gui(sys.argv)
    gui.exec_()
