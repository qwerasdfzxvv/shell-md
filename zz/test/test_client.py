import importlib
import unittest
import pytest
from requests import Response, Request
import mock

from polaris.client.http_client import HttpClient
from polaris.prometheus.model.prometheus import QueryResponse,BaseResponse


def mock_do_http_request_rsync():
    def mock_response(request):
        prometheus_response = Response()
        prometheus_response.status_code = 200
        prometheus_response._content = b"""
                 {
                        "status": "success",
                        "data": {
                            "resultType": "vector",
                            "result": ["data"]}
                }
                """
        prometheus_response.request = Request()
        prometheus_response.request.method = "GET"
        prometheus_response.request.url = ""
        return prometheus_response
    return mock_response


def mock_do_http_request_rsync_with_exception():
    def mock_response(request):
        prometheus_response = Response()
        prometheus_response.status_code = 500
        prometheus_response._content = b"""server-500"""
        prometheus_response.request = Request()
        prometheus_response.request.method = "GET"
        prometheus_response.request.url = ""
        return prometheus_response
    return mock_response


def test_do_http_request(monkeypatch):
    client = HttpClient()
    client.model_package = importlib.import_module('polaris.prometheus.model.prometheus')
    monkeypatch.setattr(client, 'do_http_request_rsync', mock_do_http_request_rsync())
    response = client.do_http_request(url='', response_type='QueryResponse')
    assert response.status_code==200
    assert response.result==['data']


def test_do_http_request_exception(monkeypatch):
    client = HttpClient()
    client.model_package = importlib.import_module('polaris.prometheus.model.prometheus')
    monkeypatch.setattr(client, 'do_http_request_rsync', mock_do_http_request_rsync_with_exception())
    response = client.do_http_request(url='', response_type='QueryResponse')
    assert response.status_code==500
    assert response.result==[]


def test_do_http_request_no_response_type(monkeypatch):
    client = HttpClient()
    client.model_package = importlib.import_module('polaris.prometheus.model.prometheus')
    monkeypatch.setattr(client, 'do_http_request_rsync', mock_do_http_request_rsync())
    response = client.do_http_request(url='', response_type=None)
    assert response.status_code == 200
    assert list(response.__dataclass_fields__.keys())==['status_code', 'raw_content']




def test_abcd():

    dat='aaa{},{}'
    dat.format('')
    print(dat)
