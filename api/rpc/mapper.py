import jsonrpc2

from api.rpc import methods


mapper = jsonrpc2.JsonRpc()
mapper.add_module(methods)
