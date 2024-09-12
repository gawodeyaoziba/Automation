from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from main.main import main  # 导入你现有的 main 函数

app = Flask(__name__)
api = Api(app)

class MaintResource(Resource):
    def post(self):
        """POST 请求触发 main 函数"""
        # 定义请求参数解析器
        parser = reqparse.RequestParser()
        parser.add_argument('keys', type=list, location='json', required=True, help="Keys cannot be blank!")
        parser.add_argument('names', type=list, location='json', required=True, help="Names cannot be blank!")
        parser.add_argument('sections', type=list, location='json', required=True, help="Sections cannot be blank!")
        args = parser.parse_args()

        # 调用 main 函数并返回结果
        result = main(args['keys'], args['names'], args['sections'])
        return {"message": "Main function executed!", "results": result}, 200

