# Functions to calculate RMS and MEANS
from numpy import sqrt, square, mean


def rms(a):
    return sqrt(mean(square(a)))


def fr_mean(t):
    el_sum = 0
    for elem in t:
        el_sum += 1.0 / elem
    return el_sum / len(t)
