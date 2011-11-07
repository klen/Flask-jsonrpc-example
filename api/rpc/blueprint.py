from flask import request, jsonify, Blueprint

from api.rpc.mapper import mapper


rpc = Blueprint('RPC', __name__)


@rpc.route('/', methods=['GET', 'POST'])
def jsonrpc():
    data = mapper(request.json or [])
    return jsonify(data)
