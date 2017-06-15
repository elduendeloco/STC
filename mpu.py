# Functions to read data from sensors

import smbus
import time
import math
from numpy import mean
from timeit import default_timer as timer

class Error(Exception):
    """Base class for other exceptions"""
    pass


class SensorError(Error):
    """Raised when the input value is too small"""
    pass



bus = smbus.SMBus(1)
power_mgmt_1 = 0x6b
ACC_LSB = 16384.0
TEMP_LSB = 340.0


def read_byte(add, adr):
    return bus.read_byte_data(add, adr)


def read_word(add, adr):
    high = bus.read_byte_data(add, adr)
    low = bus.read_byte_data(add, adr + 1)
    val = (high << 8) + low
    return val


def read_word_2c(add, adr):
    val = read_word(add, adr)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val


def read_acc_x(add):
    return read_word_2c(add, 0x3b) / ACC_LSB


def read_acc_y(add):
    return read_word_2c(add, 0x3d) / ACC_LSB


def read_acc_z(add):
    return read_word_2c(add, 0x3f) / ACC_LSB


def read_temp_C(add):
    return(read_word_2c(add, 0x41) / TEMP_LSB) + 36.53


def wakeup(add):
    bus.write_byte_data(add, power_mgmt_1, 0)


# Function to order axis
def axis_ordering(means):
    if abs(means[0]) > abs(means[1]) and abs(means[0]) > abs(means[2]):
        return [1, 2, 0]
    elif abs(means[1]) > abs(means[0]) and abs(means[1]) > abs(means[2]):
        return [2, 0, 1]
    else:
        return [0, 1, 2]


def read_signals(period):
    add1 = 0x68
    add2 = 0x69
    sig1 = [[], [], []]
    sig2 = [[], [], []]
    mean1 = []
    mean2 = []
    rms1 = []
    rms2 = []
    temp = []
    freq = []

    currtime = time.strftime("%H:%M:%S")
    currday = time.strftime("%d.%m.%Y")

    try:
        wakeup(add1)  # Wake up the sensor
        wakeup(add2)
    except:
        raise SensorError

    start = timer()
    end = start + period

    temp[0] = read_temp_C(add1)
    while start < end:
        try:
            sig1[0].append(read_acc_x(add1))
            sig1[1].append(read_acc_y(add1))
            sig1[2].append(read_acc_z(add1))
            sig2[0].append(read_acc_x(add2))
            sig2[1].append(read_acc_y(add2))
            sig2[2].append(read_acc_z(add2))
        except:
            raise SensorError
        time.sleep(0.0005)
        freq.append(round(timer() - start, 5))
        start = timer()
    temp[1] = read_temp_C(add1)

    mean1.append(mean(sig1[0]))
    mean1.append(mean(sig1[1]))
    mean1.append(mean(sig1[2]))

    mean2.append(mean(sig2[0]))
    mean2.append(mean(sig2[1]))
    mean2.append(mean(sig2[2]))

    sig1 = [sig1[i] for i in axis_ordering(mean1)]
    mean1 = [mean1[i] for i in axis_ordering(mean1)]

    sig2 = [sig2[i] for i in axis_ordering(mean2)]
    mean2 = [mean2[i] for i in axis_ordering(mean2)]

    rms1.append(math.rms(sig1[0]))
    rms1.append(math.rms(sig1[1]))
    rms1.append(math.rms(sig1[2]))

    rms2.append(math.rms(sig2[0]))
    rms2.append(math.rms(sig2[1]))
    rms2.append(math.rms(sig2[2]))

    return [sig1, sig2], [mean1, mean2], [rms1, rms2], temp, [currtime, currday], freq
