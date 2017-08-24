#!/usr/bin/python
# -*- coding: utf-8 -*-
# UPDATE - i file vengono salvati su smarttowercontrol.it


# Function to order axis
def axis_ordering(means):
    if abs(data[0]) > abs(means[1]) and abs(means[0]) > abs(means[2]):
        return [1, 2, 0]
    elif abs(means[1]) > abs(means[0]) and abs(means[1]) > abs(means[2]):
        return [2, 0, 1]
    else:
        return [0, 1, 2]









freq = []

mac = get_MAC()
n_unit = 2

###### READ CONF ######
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

if not req_acq
    try:
        reg=stc.registered()
        if reg[0]
            r = requests.post("http://78.47.195.213/api/register2", data={'n_unit': n_unit, 'mac_address': mac})
            if r.ok:
                content = json.loads(r.content)
                if content["description"] == "OK":
                    data["req_ack"] = "true"
    except:
        print "Error: Connessione register2"
        while not data["registered"]:
            try:
                r = requests.get("http://78.47.195.213/api/registered", params={'mac_address': mac})
                if r.ok:
                    content = json.loads(r.content)
                    if content["success"]:
                        data["unit"]["ID"] = content["units"]
                        data["registered"] = "true"
            except:
                print "Error: Connessione registered"
                time.sleep(60)


            ###### LOAD CONF #######
    id = data["unit"]["ID"]
    durata = data["acquisition"]["time"]
    rms_edge = data["acquisition"]["rms_edge"]

# best list
## TM2 temp
## dtm2 send_time
## dtt2 read_time
## sensor_read


flag = 1


print "Inizia Ciclo"
while True:

    ########################### Verifica richiesta ###########################################

    while flag == 1:
        status = stc.status(mac)
        if status=="test":
            try:
                signals, means, rms, temp, date, hour, frequence = mpu.read_signals(durata)

            except:
                sensor_error=True
            validation = "OK"
            data = {'MAC_Address': mac, 'tipo_test': 1, 'Date': date, 'Hour': hour, 'Validation': validation,
                'Frequency Mean': math.fr_mean(frequence), 'Temperature': {'Start': temp[0], 'End': temp[1]}, 'Signals': [
                {'id': id[0], 'X': {'RMS': rms[0][0], 'Mean': means[0][0], 'Data': signals[0][0]},
                 'Y': {'RMS': rms[0][1], 'Mean': means[0][1], 'Data': signals[0][1]},
                 'Z': {'RMS': rms[0][2], 'Mean': means[0][2], 'Data': signals[0][2]}},
                {'id': id[1], 'X': {'RMS': rms[1][0], 'Mean': means[1][0], 'Data': signals[1][0]},
                 'Y': {'RMS': rms[1][1], 'Mean': means[1][1], 'Data': signals[1][1]},
                 'Z': {'RMS': rms[1][2], 'Mean': means[1][2], 'Data': signals[1][2]}}], 'Time': frequence}
            try:
                stc.send(data)
            except:
                print("make a log")
        elif status=="config":
            path = os.path.dirname(os.path.realpath(__file__))
            with open(path + '/config.json') as data_file:
                data = json.load(data_file)
                try:
                    config=stc.config(mac)





    flag = 1
    test = 0
    '''
    finame = "" + currday + "_" + currtime + ".json"
    with open(path + "/" + finame, "w") as file:
        file = data
    print finame + " creato con succeso"
    '''
