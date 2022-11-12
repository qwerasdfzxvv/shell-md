import requests
import dataclasses
import typing
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class BaseRequest:
    url: str
    method: str = 'GET'
    params: typing.Dict = dataclasses.field(default_factory=dict)
    data: typing.Dict = dataclasses.field(default_factory=dict)
    json: typing.Dict = dataclasses.field(default_factory=dict)
    headers: typing.Dict = dataclasses.field(default_factory=dict)
    auth: typing.Dict = dataclasses.field(default_factory=set)
    timeout: int = 5


@dataclasses.dataclass
class BaseResponse:
    status_code: int = None
    raw_content: typing.Any = None


class HttpClient:

    def __init__(self):
        self.model_package = None
        self._client_session = requests.Session()

    def do_http_request(self, url, method='GET', params=None, data=None, json=None, headers=None, auth=None,
                        request_type=None, response_type=None):
        client_request = BaseRequest(url=url, method=method, params=params, data=data, json=json, headers=headers,
                                     auth=auth)
        logger.info(f'request-->{client_request}')
        response = self.do_http_request_rsync(client_request)
        self.response_error_hook_factory(response)
        return_data = self.model_deserialize(response, response_type)
        self.set_base_response(return_data, response)
        logger.info(f'result: {return_data}')
        return return_data

    def do_http_request_rsync(self, request: BaseRequest):
        request_kwagrs = dataclasses.asdict(request)
        return self._client_session.request(**request_kwagrs)

    def model_deserialize(self, response, response_type):
        """
        deserialize response to response_type class
        Args:
            response: requests.Response
            response_type: model class
        """
        if type(response_type) == str and hasattr(self.model_package, response_type):
            model_class = getattr(self.model_package, response_type)
            if response.status_code != 200:
                return model_class()
            kwargs = response.json()
            return model_class(**kwargs)
        return BaseResponse()

    @classmethod
    def set_base_response(cls, return_data, response):
        setattr(return_data, "status_code", response.status_code)
        setattr(return_data, "raw_content", response.content)

    @staticmethod
    def response_error_hook_factory(response):
        """
        logger exceptions info
        Args:
            response:  requests.Response

        """
        try:
            response.raise_for_status()
        except Exception as ex:
            logger.exception(ex)
