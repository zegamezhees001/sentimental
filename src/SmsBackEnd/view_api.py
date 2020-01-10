from django.http import HttpResponse
import json
from .presenters.EventsPresenter import EventsPresenter


def responseData(data):
    res = HttpResponse(data)
    res["content"] = data
    res["content_type"] = "application/json; charset=utf-8"
    res["Access-Control-Allow-Origin"] = "*"
    res["Access-Control-Allow-Headers"] = "*"
    return res


def load_events(request):
    eventPresenter = EventsPresenter()
    dataGetFromDatabase = eventPresenter.loadDataFromDatabase()
    return responseData(json.dumps(dataGetFromDatabase))


def insert_events(request):
    pass
