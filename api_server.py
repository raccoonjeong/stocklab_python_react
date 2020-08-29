from flask import Flask, request 
from flask_cors import CORS
from flask_restful import reqparse, abort, Api, Resource, fields, marshal_with
import datetime
from stocklab.db_handler.mongodb_handler import MongoDBHandler

app = Flask(__name__)
CORS(app)
api = Api(app)

code_hname_to_eng = {
    "단축코드": "code",
    "확장코드": "extend_code",
    "종목명": "name",
    "시장구분": "market",
    "ETF구분": "is_etf",
    "주문수량단위": "memedan",
    "기업인수목적회사여부": "is_spac"
}

code_fields = {
    "code": fields.String,
    "extend_code": fields.String,
    "name": fields.String,
    "memedan": fields.Integer,
    "market": fields.String,
    "is_etf": fields.String,
    "is_spac": fields.String,
    "uri": fields.Url("code")
}

code_list_short_fields = {
    "code": fields.String,
    "name": fields.String
}

code_list_fields = {
    "count": fields.Integer,
    "code_list": fields.List(fields.Nested(code_fields)),
    "uri": fields.Url("codes")
}

mongodb = MongoDBHandler

class Code(Resource):
    @marshal_with(code_fields)
    def get(self, code):
        result = mongodb.find_item({"단축코드": code}, "stocklab", "code_info")
        if result is None:
            return {}, 404
        code_info = {}
        code_info = { code_hname_to_eng[field]: result[field] for field in result.keys() if field in code_hname_to_eng }
        return code_info

class CodeList(Resource):
    @marshal_with(code_list_fields)
    def get(self):
        market = request.args.get('market', default="0", type=str)
        if market == "0":
            results = list(mongodb.find_items({}, "stocklab", "code_info"))
        elif market == "1" or market == "2":
            results = list(mongodb.find_items({"시장구분": market}, "stocklab", "code_info"))
        result_list = []
        for item in results:
            code_info = {}
            code_info = { code_hname_to_eng[field]: item[field] for field in item.keys() if field in code_hname_to_eng }
            result_list.append(code_info)
        return {"code_list": result_list, "count": len(result_list)}, 200

class Price(Resource):
    def get(self, code):
        pass

class OrderList(Resource):
    def get(self):
        pass

api.add_resource(CodeList, "/codes", endpoints="codes")
api.add_resource(Code, "/codes/<string:code>", endpoint="code")
api.add_resource(Price, "/codes/<string:code>/price", endpoint="price")
api.add_resource(OrderList, "/orders", endpoint="orders")

if __name__ == '__main__':
    app.run(debug=True)