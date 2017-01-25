#!/usr/bin/python3

import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QWidget, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import pyqtSignal

from gui_ import Ui_Soundgen

from sound_handler import SoundHandler

from time import time, sleep

import pyaudio as pya
from threading import Thread, Event
from queue import Queue

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
        self.sh.init_stream(callback=func)
        self.start_time = time()

        # Initialize signal thread
        self.signal_thread = SignalThread(self._generate_signal)
        self.signal_thread.start()

    def _on_stream_request(self, frame_count):
        """ Generate more chunks for signal """
        t = time() - self.start_time + float(frame_count) / 44100
        self.signal_thread.request(t, frame_count)

        while self.signal_thread.bytestream.size < frame_count:
            sleep(0.01)
        return self.signal_thread.bytestream

    def _generate_signal(self, t, frame_count):
        """ Generate signal starting from time `t` """
        print("Generating more signal at time {0}".format(t))
        t_end = t + float(frame_count) / 44100

        ts = np.linspace(t, t_end, frame_count)
        xs = np.sin(2 * np.pi * 440 * ts)

        bytestream = (xs * 65535 / 2).astype(np.int16)
        return bytestream

    def _on_quit(self):
        self.signal_thread.stop()

class SignalThread(Thread):
    def __init__(self, generate_signal_func):
        Thread.__init__(self)
        self.bytestream = np.array([], dtype=np.int16)
        self.requests = Queue()
        self.generate_signal_func = generate_signal_func

        self._stop_event = Event()

    def run(self):
        """ Poll the requests and generate signals as needed. """
        while not self._stop_event.is_set():
            if not self.requests.empty():
                (t, frame_count) = self.requests.get()
                self.bytestream = self.generate_signal_func(t, frame_count)

    def request(self, t, frame_count):
        """ Request `frame_count` frames at time `t` and store it in
            the bytestream

            Args:
                t: time (in float)
                frame_count: number of frames to generate

            Returns:
                bytestream of length `frame_count`
        """
        self.requests.put_nowait((t, frame_count))

    def stop(self):
        """ Stop the thread """
        self._stop_event.set()

if __name__ == "__main__":
    gui = Gui(sys.argv)
    gui.exec_()
