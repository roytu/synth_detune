from libc.math cimport sin
from libc.time cimport time, time_t
from posix.time cimport timeval, gettimeofday

import numpy as np
cimport numpy as np

cimport cython

DTYPE = np.int16
ctypedef np.int16_t DTYPE_t

DEF FRAME_COUNT = 44100
DEF PI = 3.14159
DEF PI_TIMES_2 = PI * 2
DEF AMPLITUDE = 65535 / 2

@cython.boundscheck(False)
@cython.wraparound(False)
def generate():
    """ Generates the bytestream given things """
    cdef timeval tv;
    gettimeofday(&tv, NULL);

    cdef double t_0 = (tv.tv_sec % 60) + (<double>(tv.tv_usec) / 1000000)
    cdef double t_1 = t_0 + <float>(FRAME_COUNT) / 44100

    cdef double STEP = (t_1 - t_0) / FRAME_COUNT
    cdef np.ndarray[DTYPE_t, ndim=1] xs = np.empty(FRAME_COUNT, dtype=DTYPE)
    cdef int i
    cdef double t

    for i in range(FRAME_COUNT):
        t = t_0 + i * STEP
        xs[i] = <DTYPE_t> (sin(PI_TIMES_2 * 440 * t) * AMPLITUDE)

    return xs
