from Utils.ConfigOperate import ConfigOperate
from flask_restful import Resource, reqparse
from flask import jsonify

config_operate = ConfigOperate()

class ConfigResource(Resource):
    def post(self):
        """获取指定配置"""
        parser = reqparse.RequestParser()
        parser.add_argument('key', required=True, help="Key cannot be blank!")
        parser.add_argument('section', required=True, help="Section cannot be blank!")
        args = parser.parse_args()

        result = config_operate.ConfigContent(args['key'], args['section'])
        return jsonify({"result": result})

class UpdateConfigResource(Resource):
    def post(self):
        """修改配置"""
        parser = reqparse.RequestParser()
        parser.add_argument('section', required=True, help="Section cannot be blank!")
        parser.add_argument('key', required=True, help="Key cannot be blank!")
        parser.add_argument('value', required=True, help="Value cannot be blank!")
        args = parser.parse_args()

        config_operate.UpdateConfig(args['section'], args['key'], args['value'])
        return jsonify({"message": "Configuration updated successfully"})

    def get(self):
        """使用GET请求修改配置"""
        parser = reqparse.RequestParser()
        parser.add_argument('section', required=True, help="Section cannot be blank!")
        parser.add_argument('key', required=True, help="Key cannot be blank!")
        parser.add_argument('value', required=True, help="Value cannot be blank!")
        args = parser.parse_args()

        config_operate.UpdateConfig(args['section'], args['key'], args['value'])
        return jsonify({"message": "Configuration updated successfully"})

class AllConfigResource(Resource):
    def get(self):
        """获取全部配置"""
        result = config_operate.GetAllConfig()
        return jsonify(result)

class DeleteConfigResource(Resource):
    def post(self):
        """删除配置"""
        parser = reqparse.RequestParser()
        parser.add_argument('key', required=True, help="Key cannot be blank!")
        parser.add_argument('section', required=True, help="Section cannot be blank!")
        args = parser.parse_args()
        key_to_delete = args['key']
        section = args['section']
        if config_operate.delete_mapping(section, key_to_delete):
            return {"true"}, 200
        else:
            return {"error": "Key not found"}, 404
