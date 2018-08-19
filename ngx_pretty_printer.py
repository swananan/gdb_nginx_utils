# -*- coding: utf-8 -*-
# File Name: ngx_pretty_printer.py
# Author: wuzhenzhong
# mail: jt26wzz@icloud.com
# Created Time: 2018年07月28日 星期六 18时01分33秒
#!/usr/bin/python
#=============================================================

import gdb
import gdbutils


class NginxArray:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        print_str = "Nginx ngx_array_t *\n"
        print_str += "Array size : %d\nArray elts size : %d\nArray alloc : %d\n" % (self.val['nelts'],
                     self.val['size'], self.val['nalloc'])
        print_str += "Array first elts : %s\n" % (str(self.val['elts']))
        return print_str

    def _iterate(self, pointer, size, pointer_type):
        pointer = pointer.cast(gdb.lookup_type(pointer_type).pointer())
        for i in range(size):
            elem = pointer.dereference()
            pointer = pointer + 1
            yield ('[%d]' % i, elem)

    def _children(self):
        # argv = gdb.string_to_argv(args)
        # print argv[1]
        # return self._iterate(self.val['elts'],
                             # int(self.val['nelts']), argv[1])
        return

    def display_hint(self):
        return 'array'

def register_nginx_array(val):
    if str(val.type) == 'ngx_array_t *':
        return NginxArray(val)
    return None

gdb.pretty_printers.append(register_nginx_array)

class NginxBuf:
    def __init__(self, val):
        self.val = val

    def count_length(self, s, e):
        length = 0
        while s != e:
            s += 1
            length += 1
        return length

    def to_string(self):
        b = self.val
        print_str = "Nginx ngx_buf_t *\n"
        all_size = b['end'] - b['start']
        used_size = b['last'] - b['pos']
        consume_size = b['pos'] - b['start']

        print_str += "buf alloc size: %s  [start, end]\n" % all_size
        print_str += "buf used size: %s   [pos, last]\n" % used_size
        print_str += "buf consume size: %s  [start, pos]\n" % consume_size
        # print_str += b['start'].string() + '\n'
        return print_str

def register_nginx_buf(val):
    if str(val.type) == 'ngx_buf_t *':
        return NginxBuf(val)
    return None

gdb.pretty_printers.append(register_nginx_buf)

class NginxChain:
    def __init__(self, val):
        self.val = val

    def to_string(self):
        c = self.val
        print_str = "Nginx ngx_chain_t *\n"
        length = 0
        while c != gdbutils.null():
            print_str += "the %d buf:%s\n" % (length+1, str(c['buf']))
            c = c['next']
            length += 1
        print_str += "ngx_chain_t size : %d bufs\n" % (length)
        return print_str

def register_nginx_chain(val):
    if str(val.type) == 'ngx_chain_t *':
        return NginxChain(val)
    return None

gdb.pretty_printers.append(register_nginx_chain)

# class BufferPrinter:
#     def __init__(self, val):
#         "构造函数接收一个表示被打印的Buffer的gdb.Value"
#         self.val = val

#     def to_string(self):
#         """必选。输出打印的结果。
#         由于gdb会在调用to_string后调用children，这里我们只输出当前的使用程度。
#         具体的数据留在children函数中输出。
#         """
#         return "used: %d\nfree: %d\n" % (self.val['used'], self.val['free'])

#     def _iterate(self, pointer, size, encoding):
#         # 根据encoding决定pointer的类型
#         typestrs = ['int8_t', 'int16_t', 'int32_t', 'int64_t']
#         pointer = pointer.cast(gdb.lookup_type(typestrs[encoding]).pointer())
#         for i in range(size):
#             elem = pointer.dereference()
#             pointer = pointer + 1
#             yield ('[%d]' % i, elem)

#     def children(self):
#         """可选。在to_string后被调用，可用于打印复杂的成员。
#         要求返回一个迭代器，该迭代器每次迭代返回（名字，值）形式的元组。
#         打印出来的效果类似于“名字 = 值”。
#         """
#         return self._iterate(self.val['data'],
#                              int(self.val['used']), int(self.val['encoding']))

#     def display_hint(self):
#         """可选。影响输出的样式。
#         可选值：array/map/string。
#         返回array表示按类似于vector的方式打印。其它选项同理。
#         """
#         return 'array'

# def register_buffer(val):
#     """val是一个gdb.Value的实例，通过type属性来获取它的类型。
#     如果类型为Buffer，那么就使用自定义的BufferPrinter。
#     """
#     if str(val.type) == 'Buffer':
#         return BufferPrinter(val)
#     return None

# gdb.pretty_printers.append(register_buffer)
