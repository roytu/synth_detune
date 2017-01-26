
""" Module containing methods to handle sounds. """

import numpy as np
import pyaudio as pya

class SoundHandler(object):
    """ Static class with methods to input / output / play sounds """

    __temp = ".temp.wav"
    """ Filename for temporary wave files """

    def __init__(self):
        self.pyaudio = pya.PyAudio()
        self.stream = None

    def init_stream(self, callback=None, framerate=44100, frames=44100):
        """ Initializes an internal stream object which can be written to live.
        
            Args:
                callback : function that runs when the stream wants
                           more data (default=None)
                framerate : sample rate in Hz (default=44100)
                frames : number of frames per buffer (default=44100)
        """
        self.stream = self.pyaudio.open(format=pya.paInt16,
                                        channels=1,
                                        rate=framerate,
                                        output=True,
                                        stream_callback=callback,
                                        frames_per_buffer=frames
                                        )

    def close(self):
        if self.stream:
            self.stream.stop_stream()
        self.pyaudio.terminate()

    def write_stream(self, data):
        """ Write stream of data to sound card to play it.

            Args:
                data : numpy stream (normalized from -1 to 1)
        """
        data *= 65535 / 2
        bytestream = data.astype(np.int16)
        self.stream.write(bytestream)

if __name__ == "__main__":
    # Testing stream
    sh = SoundHandler()
    sh.init_stream()

    freq = 440

    ts = np.linspace(0, 1, 44100)
    xs = np.sin(2 * np.pi * freq * ts)

    sh.write_stream(xs)
    sh.close()
