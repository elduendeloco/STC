import requests
import json
from time import sleep


class Error(Exception):
    """Base class for other exceptions"""
    pass


class ServerResponceError(Error):
    """Raised when the input value is too small"""
    pass


class RequestsError(Error):
    """Raised when the input value is too large"""
    pass


def registered(mac):
    try:
        r = requests.get("http://78.47.195.213/api/registered", params={'mac_address': mac})
        if r.ok:
            content = json.loads(r.content)
            if content["success"]:
                return True, content['units']
            else:
                return False, []
        else:
            raise ServerResponceError
    except Exception:
        raise RequestsError


def register(num_units, mac):
    try:
        r = requests.post("http://78.47.195.213/api/register2", data={'n_unit': num_units, 'mac_address': mac})
        if r.ok:
            content = json.loads(r.content)
            if content["description"] == "OK":
                return True
            else:
                raise ServerResponceError
    except:
        raise RequestsError


def status(mac):
    try:
        r = requests.get('http://78.47.195.213/api/status', params={'mac_address': mac})
        if r.ok:
            data = json.loads(r.content)
            if data["status"] != 'idle':
                requests.post("http://78.47.195.213/api/status", data={'mac_address': mac, 'status': 'idle'})
            return data["status"]
        else:
            raise ServerResponceError
    except:
        raise RequestsError


def send(data):
    attempts = 0
    try:
        r = requests.post("http://78.47.195.213/api/send2", json=data)
        if r.ok:
            return 'Success'
        else:
            print ("Error: risposta dopo invio" + r.content)
            attempts = attempts + 1
            sleep(5)
            if attempts > 5:
                raise ServerResponceError
    except:
        raise RequestsError


def config(mac):
    try:
        r = requests.get("http://78.47.195.213/api/config", params={'mac_address': mac})
        if r.ok:
            data = json.loads(r.content)
            if data["success"]:
                return data["result"]
            else:
                raise ServerResponceError
        else:
            raise ServerResponceError
    except:
        raise RequestsError

# Function to get device's mac
def get_MAC():
    # Return the MAC address of interface
    try:
        str = open('/sys/class/net/eth0/address').read()
    except:
        str = "00:00:00:00:00:00"
    return str[0:17]
