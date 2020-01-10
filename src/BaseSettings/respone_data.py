from django.http import HttpResponse
import json


def message_handle(message , data,status = 0 ) :
    message_ = {
        "message": message,
        "data": data
    }
    return json.dumps(message_)
    
def responseData(data , status = 200):
    res = HttpResponse(data , status = status)
    res["content"] = data
    res["content_type"] = "application/json; charset=utf-8"
    res["Access-Control-Allow-Origin"] = "*"
    res["Access-Control-Allow-Headers"] = "*"
    return res

