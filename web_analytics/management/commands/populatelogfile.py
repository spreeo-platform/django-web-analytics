from django.core.management.base import BaseCommand
from web_analytics.models import RequestLog


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str)

    def handle(self, *args, **options):
        log_file = options['file']
        file = open(log_file, 'r')

        for line in file:
            RequestLog.parse_log_entry(entry=line)

