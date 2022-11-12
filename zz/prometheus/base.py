import typing

from polaris.client.http_client import HttpClient
import importlib
from datetime import datetime, timedelta
from enum import Enum

from .model.prometheus import QueryRangeRequest, QueryInstantRequest, QueryResponse


class QueryType(Enum):
    RANGE_TYPE: int = 1
    INSTANT_TYPE: int = 2


class BasePolarisPromethues(HttpClient):
    default_rule: list = []

    def __init__(self, sproject_id: str, regions: list = None, rules: dict = None, includes: dict = None,
                 excludes: dict = None, interval: int = None, query_type: str = None) -> None:
        """BasePolarisPromethues.init

        Args:
            sproject_id:  系统名称
            regions:  区域
            rules: 巡检规则
            includes:  必须项
            excludes:  过虑项
            interval: 统计区间
            query_type: 查询类型
        """
        super(BasePolarisPromethues, self).__init__()
        self.model_package = importlib.import_module("polaris.prometheus.model.prometheus")
        self.sproject_id = str.upper(sproject_id)
        self.regions = regions or []
        self.rules = rules or self.default_rule
        self.includes = includes or {}
        self.excludes = excludes or {}
        self.interval = interval or 300
        self.query_type = query_type or QueryType.RANGE_TYPE
        self.sproject_metrics_mapping=None



    @staticmethod
    def parse_includes_excludes(includes: typing.Dict = None, excludes: typing.Dict = None):
        includes_list = []
        excludes_list = []
        if includes and isinstance(includes, dict):
            for label, label_value in includes.items():
                include_item = '.*'
                if isinstance(label_value, list):
                    include_item = ','.join([f'{lv}.*' for lv in label_value])
                if isinstance(label_value, str):
                    include_item = f'{label_value}.*'
                includes_list.append(f'''{label}=~{include_item}''')
        if excludes and isinstance(excludes, dict):
            for label, label_value in excludes.items():
                exclude_item = '.*'
                if isinstance(label_value, list):
                    exclude_item = ','.join([f'{lv}.*' for lv in label_value])
                if isinstance(label_value, str):
                    exclude_item = f'{label_value}.*'
                excludes_list.append(f'''{label}=~{exclude_item}''')
        return ','.join(includes_list) + ','.join(excludes_list)

    def parse_prometheus_sql(self, query: str, includes: typing.Dict = None, excludes: typing.Dict = None):
        includes_excludes_params = self.parse_includes_excludes(includes=includes, excludes=excludes)
        sproject_metrics=','.join(self.sproject_metrics_mapping) if isinstance(self.sproject_metrics_mapping,list) else self.sproject_metrics_mapping
        query=query.format(sproject_metrics,sproject_metrics)



        query = f'''go_gc_duration_seconds{{job="prometheus",{}}'''

    def query_prometheus_metrics(self, request):
        pass

    def run(self):

    def do_request_api(self, url, method='GET', params=None, data=None, json=None, headers=None, auth=None,
                       request_type=None, response_type=None):
        return self.do_http_request(
            url=url,
            method=method,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            request_type=request_type,
            response_type=response_type)
