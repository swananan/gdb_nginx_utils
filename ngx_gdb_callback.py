# -*- coding: utf-8 -*-
# File Name: ngx_gdb_callback.py
# Author: wuzhenzhong
# mail: jt26wzz@icloud.com
# Created Time: 2018年07月29日 星期日 16时27分14秒
#=============================================================
#!/usr/bin/python

import atexit
import time
import gdb
import re


# Entry = namedtuple('Entry', ['addr', 'bt', 'timestamp', 'size'])
# MEMORY_POOL = {}
# MEMORY_LOST = defaultdict(list)

# def comm(event):
#     if isinstance(event, gdb.SignalEvent):
#         return

#     # handle BreakpointEvent
#     for bp in event.breakpoints:
#         if bp.number == 1:
#             addr = str(gdb.parse_and_eval('p'))
#             bt = gdb.execute('bt', to_string=True)
#             timestamp = time.strftime('%H:%M:%S', time.localtime())
#             size = int(gdb.parse_and_eval('size'))
#             if addr in MEMORY_POOL:
#                 MEMORY_LOST[addr].append(MEMORY_POOL[addr])
#             MEMORY_POOL[addr] = Entry(addr, bt, timestamp, size)
#         elif bp.number == 2:
#             addr = gdb.parse_and_eval('p')
#             if addr in MEMORY_POOL:
#                 del MEMORY_POOL[addr]
#     gdb.execute('c')


# def dump_memory_lost(memory_lost, filename):
#     with open(filename, 'w') as f:
#         for entries in MEMORY_LOST.values():
#             for e in entries:
#                 f.write("Timestamp: %s\tAddr: %s\tSize: %d" % (
#                         e.timestamp, e.addr, e.size))
#                 f.write('\n%s\n' % e.bt)


# atexit.register(dump_memory_lost, MEMORY_LOST, 'all_funcs')
# # Write to result file once signal catched
# gdb.events.stop.connect(comm)

# gdb.execute('set pagination off')
# gdb.execute('b my_malloc') # breakpoint 1
# gdb.execute('b my_free') # breakpoint 2
# gdb.execute('c')

funcs = []

def dump_all_funcs(funcs, filename):
    with open(filename, 'w') as f:
        for item in funcs:
            f.write('%s\n' % item)

def comm(event):
    if isinstance(event, gdb.SignalEvent):
        return
    bt = gdb.execute('bt 1', to_string=True)
    v = bt.split(' ')
    vv = v[4].split('\n')
    funcs.append(vv[2])
    gdb.execute('c')

gdb.events.stop.connect(comm)
atexit.register(dump_all_funcs, funcs, 'all_funcs')

gdb.execute('rbreak ngx_http_request.c:.*')
