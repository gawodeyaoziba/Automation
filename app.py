# app.py
from flask import Flask, jsonify
from Utils.Flask.device import DeviceResource
from flask_restful import Api
from Utils.Flask.mains import MaintResource
from Utils.Flask.config import (
    ConfigResource,
    UpdateConfigResource,
    AllConfigResource,
    DeleteConfigResource,
)


app = Flask(__name__)
api = Api(app)
# 设备
api.add_resource(DeviceResource, '/api/device')
# 配置
api.add_resource(ConfigResource, '/api/config')
api.add_resource(UpdateConfigResource, '/api/update_config')
api.add_resource(AllConfigResource, '/api/all_config')
api.add_resource(DeleteConfigResource, '/api/delete_config')
# 执行
api.add_resource(MaintResource, '/api/main')






@app.errorhandler(Exception)
def handle_exception(e):
    # 为所有异常创建响应对象
    response = {
        "error": str(e)  # 确保这是一个字符串
    }
    return jsonify(response), 500



if __name__ == '__main__':
    app.run(debug=True)
