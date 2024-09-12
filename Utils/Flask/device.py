# device.py
from flask_restful import Resource
from Utils.Device import get_connected_devices
class DeviceResource(Resource):
    def get(self):
        devices = get_connected_devices()
        return devices
