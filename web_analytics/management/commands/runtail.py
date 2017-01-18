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

from django.core.management.base import BaseCommand
from web_analytics.base import Tail


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        log_file = options['file']
        tail = Tail(log_file)
        tail.run()



