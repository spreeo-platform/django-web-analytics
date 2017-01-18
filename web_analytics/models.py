"""
Copyright 2017 PERSADA TERBILANG SDN. BHD.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
AUTHOR : DALIA DAUD
EMAIL : daliadaud@gmail.com
"""


from django.db import models
import re
from django.contrib.postgres.fields import JSONField
import datetime
from urllib.parse import urlparse, parse_qs
import codecs
from django.conf import settings
TIME_LOCAL_FORMAT = "%d/%b/%Y:%H:%M:%S %z"

# Create your models here.


def string_to_dict(string):
    s = string.replace("{", "")
    final_string = s.replace("}", "")
    l = final_string.split(",")

    d = {}
    for i in l:
        key_value = i.split(":")
        m = key_value[0].strip('\'')
        m = m.replace("\"", "")
        d[m] = key_value[1].strip('"\'')

    return d


class RequestLog(models.Model):
    remote_addr = models.CharField(max_length=255, db_index=True)
    date = models.DateTimeField(db_index=True, blank=True)
    method = models.CharField(max_length=50)
    path = models.TextField(db_index=True)
    status_code = models.IntegerField()
    user_agent = models.TextField(blank=True)
    request_headers = JSONField(blank=True)
    response_headers = JSONField(blank=True)
    query_strings = JSONField(blank=True)

    parsed_raw_data = JSONField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_request_log(data={}):
        if RequestLog.objects.filter(parsed_raw_data=data).exists():
            return None
        
        string_date = data.get('time_local', "")
        date = datetime.datetime.strptime(string_date, TIME_LOCAL_FORMAT)
        request_headers = {}
        response_headers = {}

        request = data.get('request', "")

        method, _, request_rest = request.partition(' ')

        url, _, _ = request_rest.partition(' ')

        parsed_url = urlparse(url=url)
        parsed_query = parse_qs(parsed_url.query)

        for key, value in data.items():
            if isinstance(value, dict):
                new_key = key.strip('http_')
                request_headers[new_key] = value

            if key == 'sent_http_last_modified':
                response_headers[key] = value

        return RequestLog.objects.create(remote_addr=data.get('remote_addr', "-"), date=date, method=method, path=parsed_url.path,
                                         status_code=data.get('status', "-"), user_agent=data.get('http_user_agent', "-"), request_headers=request_headers,
                                         response_headers=response_headers, query_strings=parsed_query, parsed_raw_data=data)

    @staticmethod
    def parse_log_entry(entry):
        headers = re.split('\s', settings.REQUEST_LOG_FORMAT)
        line_column = entry.strip()
        d = {}
        for x in range(0, len(headers)):

            request_key = headers[x]
            if request_key.startswith('"'):
                results = line_column.partition('"')
                value = results[2]
                new_results = value.partition('"')
                d[request_key.strip('"$')] = new_results[0]
                line_column = new_results[2].strip()

            elif request_key.startswith('['):
                results = line_column.partition(']')
                value = results[0]
                new_value = value.replace('[', '')

                d[request_key.strip('[]$')] = new_value
                line_column = results[2].strip()

            else:
                results = line_column.partition(' ')
                value = results[0]
                d[request_key.strip('$')] = value
                line_column = results[2].strip()

        for key, value in d.items():
            if value.startswith('{'):
                new_v = codecs.escape_decode(value)
                d[key] = string_to_dict(new_v[0].decode('utf-8'))
        RequestLog.create_request_log(data=d)
