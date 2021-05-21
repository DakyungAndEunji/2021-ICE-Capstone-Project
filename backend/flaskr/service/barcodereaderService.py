from evdev import InputDevice, ecodes, list_devices, categorize
import signal, sys

from flask import jsonify
from flaskr import db
from flaskr.model import Product

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


def signal_handler(signal, frame):
    print('Stopping')
    dev.ungrab()
    sys.exit(0)


def update(func, prd_id, state):  # state 기본 값 0 = 입고
    if func == 'ADD':
        while state == 1:  # 입고 시작
            item = Product.query.filter_by(product_id=prd_id).first()
            if not item:
                return not_found()
            item.product_num += 1
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Successfully add data",
            }
            return jsonify(response_object)
    elif func == 'DELETE':
        while state == -1:  # 입고 시작
            item = Product.query.filter_by(product_id=prd_id).first()
            if not item:
                return not_found()
            item.product_num -= 1
            db.session.commit()
            response_object = {
                "status": "success",
                "message": "Successfully delete data",
            }
            return jsonify(response_object)


def not_found():
    response_object = {
        "status": "Not Found",
        "message": "product dosen\'t exist."
    }
    return jsonify(response_object), 404


if __name__ == '__main__':
    global state
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
                        word = buff.split('/')
                        try:
                            if word[4] == 'ADD':
                                state = 1
                            elif word[4] == 'DELETE':
                                state = -1
                        except Exception as stateError:
                            print('{} is not available'.format(state))

                        if state == 1 or state == -1:
                            update(word[4], [5], state)
                        else:
                            pass
                        print(barcode)
                        barcode = ""
                        # print(word[3], word[4])

                    else:
                        barcode += key_lookup  # append character to barcode string

    except KeyboardInterrupt:
        dev.close()

# 바코드 찍었을 때 /api/product/add/product_id
# 바코드 찍었을 때 /api/product/delete/product_id
