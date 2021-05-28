from evdev import InputDevice, ecodes, list_devices, categorize
import signal, sys
import requests
from flask import jsonify

sys.path.append("/home/pi/backend/")

barCodeDeviceString = "HID 0581:0106"  # barcode device name
scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
}
state = 0

def signal_handler(signal, frame):
    print('Stopping')
    dev.ungrab()
    sys.exit(0)


def update(prd_id):
    try:
        if state == 1: # start adding
            return requests.get('http://127.0.0.1:5000/stock/'+prd_id+'/'+'ADD')

        elif state == -1: # start deleting
            return requests.get('http://127.0.0.1:5000/stock/' + prd_id + '/' + 'DELETE')
    except Exception as e:
        print(str(e))


def not_found():
    print("not found")
    response_object = {
        "status": "Not Found",
        "message": "product dosen\'t exist."
    }
    return jsonify(response_object), 404


if __name__ == '__main__':
    devices = map(InputDevice, list_devices())
    for device in devices:
        # print(device.name, device.fn)
        if barCodeDeviceString in device.name:
            dev = InputDevice(device.path)
        else:
            print('No barcode device found')
            sys.exit()
    signal.signal(signal.SIGINT, signal_handler)
    dev.grab()
    # process usb hid events and format barcode data
    barcode = ""
    try:
        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1 and data.scancode != 42:  # Catch only keydown, and not Enter
                    key_lookup = scancodes.get(data.scancode) or u'UNKNOWN:{}'.format(
                        data.scancode)  # lookup corresponding ascii value
                    if data.scancode == 28:  # if enter detected print barcode value and then clear it
                        buff = barcode
                        try:
                            if buff == 'ADD':
                                state = 1
                            elif buff == 'DELETE':
                                state = -1
                            else:
                                print(update(int(buff)))
                        except Exception as stateError:
                            # print('{} is not available'.format(state))
                            pass

                        print(state)
                        print(buff)

                        # print(word[2])
                        barcode = ""
                        # print(word[3], word[4])

                    else:
                        barcode += key_lookup  # append character to barcode string

    except KeyboardInterrupt:
        dev.close()


