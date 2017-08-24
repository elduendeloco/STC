#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
import time
import math
import requests
import mpu
import stc
import threading

lock_acq = threading.Lock()
lock_check = threading.Lock()

## ACQUISIZIONE DEI DATI DAI SENSORI ##

def acquisition_prog(duration, interval):
    with lock_acq:
        threading.Timer(r_interval*60, acquisition_prog, [duration, interval]).start()
        a_data=mpu.read_signals(duration)
        if mpu.rms_check(a_data[2], best_rms):
            best_data=a_data

def status_check(refresh):
    with lock_check:
        threading.Timer(refresh, status_check).start()
        status=stc.status()
        if status=="test":
            a_data = mpu.read_signals(r_duration)
            msg = {'MAC_Address': mac, 'tipo_test': 1, 'Date': a_data[4][1], 'Hour': a_data[4][0], 'Validation': validation,
                   'Frequency Mean': math.fr_mean(a_data[5][0]), 'Temperature': {'Start': a_data[3][0], 'End': a_data[3][1]},
                   'Signals': [
                       {'id': id[0], 'X': {'RMS': a_data[2][0][0], 'Mean': a_data[1][0][0], 'Data': a_data[0][0][0]},
                        'Y': {'RMS': a_data[2][0][1], 'Mean': a_data[1][0][1], 'Data': a_data[0][0][1]},
                        'Z': {'RMS': a_data[2][0][2], 'Mean': a_data[1][0][2], 'Data': a_data[0][0][2]}},
                       {'id': id[1], 'X': {'RMS': a_data[2][1][0]], 'Mean': a_data[1][1][0], 'Data': a_data[0][1][0]},
                        'Y': {'RMS': a_data[2][1][1], 'Mean': a_data[1][1][1], 'Data': a_data[0][1][1]},
                        'Z': {'RMS': a_data[2][1][2], 'Mean': a_data[1][1][2], 'Data': a_data[0][1][2]}}], 'Time': a_data[5]}
            stc.send(a_data)
        else if status=="config"

## LEGGO CONFIGURAZIONE ##
path = os.path.dirname(os.path.realpath(__file__))

with open(path + "/config.json", "R") as file:
    dati=json.loads(file)
    rms_edge=dati["acquisition"]["soglia_rms"]
    r_duration=dati["acquisition"]["durata_lettura"]
    r_interval=dati["acquisition"]["intervallo_lettura"]
    send_time=dati["acquisition"]["orario_invio"]
    refresh_time=dati["acquisition"]["tempo_refresh"]
    id=dati["unit"]["id"]
    first_boot=dati["first_boot"]
    req_acq=dati["req_ack"]
    registered=dati["registered"]

mac = stc.get_MAC()

## CONTROLLO REGISTRAZIONE ##
if not req_acq:
    if stc.register(2, mac):
        req_acq=True
    while not registered:
        r=registered(mac)
        if r[0]:
            registered=True
            id=r[1]
        else:
            time.sleep(60)

## CREO LA TEMPORIZZAZIONE DELLE ACQUISIZIONI ##
acquisition_prog(r_duration, r_interval)
status_check(refresh_time)

