#!/usr/bin/python

import collectd
import json
import socket
from subprocess import check_output

metrics = [('cache_hit', 'MAIN.cache_hit'),
           ('cache_hitpass', 'MAIN.cache_hitpass'),
           ('cache_miss', 'MAIN.cache_miss'),
           ('backend_conn', 'MAIN.backend_conn'),
           ('backend_unhealthy', 'MAIN.backend_unhealthy'),
           ('backend_busy', 'MAIN.backend_busy'),
           ('backend_fail', 'MAIN.backend_fail'),
           ('backend_recycle', 'MAIN.backend_recycle'),
           ('backend_retry', 'MAIN.backend_retry'),
           ('backend_req', 'MAIN.backend_req'),
           ('client_bodybytes', 'MAIN.s_req_bodybytes')]

host = socket.gethostname()

def send_stats():
    varnish_stats = json.loads(check_output(['/usr/bin/varnishstat', '-j','-f', 'MAIN.*']))
    for m,v in metrics:
        vl = collectd.Values(type='counter')
        vl.host = host
        vl.plugin =  "varnishstat"
        vl.plugin_instance = m
        vl.dispatch(values = [varnish_stats[v]['value']], time=0)

collectd.register_read(send_stats,interval=5)



