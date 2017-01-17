==============
WEB ANALYTICS
==============

WEB ANALYTICS is a simple Django app to store and query web analytics


Quick start
-----------

1. Add "web_analytics" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'web_analytics',
    ]


2. Run `python manage.py migrate` to create the web_analytics models.

3. Set REQUEST_LOG_FORMAT in settings.py::

    e.x : REQUEST_LOG_FORMAT = "$remote_addr - $remote_user [$time_local] \"$request\" $status $body_bytes_sent \"$http_referer\" \"$http_user_agent\" \"$http_x_forwarded_for\" \"$http_x_stub_client_info\" \"$sent_http_last_modified\""

4. To populate log file::

    python manage.py populatelogfile --file file.log
