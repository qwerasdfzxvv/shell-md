import dataclasses
import typing


@dataclasses.dataclass
class BaseResponse:
    status_code: int = None
    raw_content: typing.Any = None


@dataclasses.dataclass
class QueryResponse(BaseResponse):
    status: str = ''
    data: typing.Any = dataclasses.field(default_factory=dict)
    result: typing.Any = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.result = self.data.get('result', [])


@dataclasses.dataclass
class QueryRangeRequest:
    query: str
    start: float
    end: float
    step: int


@dataclasses.dataclass
class QueryInstantRequest:
    query: str
    time: float





# if __name__ == '__main__':
#     kwargs = {
#         "status": "success",
#         "data": {
#             "resultType": "vector",
#             "result": [
#                 {"metric": {"__name__": "go_gc_duration_seconds", "instance": "localhost:9090", "job": "prometheus",
#                             "quantile": "0"}, "value": [1668226507.572, "0"]},
#             ]}
#     }
#     qs = QueryResponse(**kwargs)
#     print(dataclasses.asdict(qs))
#
#     from datetime import datetime
#     print(datetime.now())
#     print(datetime.now().timestamp())
