# -*- coding: utf-8 -*-
# File Name: ngx_gdb_commond.py
# Author: wuzhenzhong
# mail: jt26wzz@icloud.com
# Created Time: 2018年07月29日 星期日 16时21分51秒
#=============================================================
#!/usr/bin/python

import gdb
import gdbutils


# 用户自定义命令需要继承自gdb.Command类
class PrintChain(gdb.Command):
    # docstring里面的文本是不是很眼熟？gdb会提取该类的__doc__属性作为对应命令的文档
    """PrintChain ngx_chain_t *
    """

    def __init__(self):
        # 在构造函数中注册该命令的名字
        super(self.__class__, self).__init__("print-chain", gdb.COMMAND_USER)

    def type_lookup(self):
        self.chain_pointer_type = gdb.lookup_type('ngx_chain_t').pointer()

    #  在invoke方法中实现该自定义命令具体的功能
    # args表示该命令后面所衔接的参数，这里通过string_to_argv转换成数组
    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 1:
            raise gdb.GdbError('输入参数数目不对，help print-chain 以获得用法')

        self.type_lookup()

        # gdb.execute('delete ' + argv[0])
        # gdb.execute('break ' + argv[1])
        m = re.match('0[xX][0-9a-fA-F]+', argv[0])
        if m:
            c = gdb.Value(int(argv[0], 16)).cast(self.chain_pointer_type)

        else:
            c = gdb.parse_and_eval(argv[0])

        if not c:
            print("ngx_chain_t point empty")
            return

        length = 0
        while c != gdbutils.null():
            print ("buf:%s" % str(c['buf']))
            c = c['next']
            length += 1

        print("chain length %s" % length)

#  向gdb会话注册该自定义命令
PrintChain()

class PrintBuf(gdb.Command):
    """PrintBuf ngx_buf_t *
    """

    def __init__(self):
        super(self.__class__, self).__init__("print-buf", gdb.COMMAND_USER)

    def type_lookup(self):
        self.buf_pointer_type = gdb.lookup_type('ngx_buf_t').pointer()

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 1:
            raise gdb.GdbError('输入参数数目不对，help print-chain 以获得用法')

        self.type_lookup()

        m = re.match('0[xX][0-9a-fA-F]+', argv[0])
        if m:
            b = gdb.Value(int(argv[0], 16)).cast(self.buf_pointer_type)

        else:
            b = gdb.parse_and_eval(argv[0])

        if not b:
            print("ngx_buf_t point empty")
            return

        all_size = b['end'] - b['start']
        used_size = b['last'] - b['pos']
        consume_size = b['pos'] - b['start']

        print("buf alloc size: %s  [start, end]" % all_size)
        print("buf used size: %s   [pos, last]" % used_size)
        print("buf consume size: %s  [start, pos]" % consume_size)
        print("buf alloc data:")
        print("")

        data = b['start']
        ascii_list = []
        if all_size > 0:
            for i in xrange(all_size):
                p = int(data[i])
                if p < 32:
                    if data[i + 1] == ord('\n') and i != all_size:
                        ascii_list.append(ord('\r'))

                    elif data[i] != ord('\n'):
                        ascii_list.append(ord(':'))
                    else:
                        ascii_list.append(p)

                else:
                    ascii_list.append(p)
            res = ''.join(map(chr, ascii_list))
            print(res)

        # print(b['start'].string())

PrintBuf()


class PrintArray(gdb.Command):
    """PrintArray ngx_array_t *
    print-array ngx_array_t* elts_type
    """

    def __init__(self):
        super(self.__class__, self).__init__("print-array", gdb.COMMAND_USER)

    def type_lookup(self):
        self.array_pointer_type = gdb.lookup_type('ngx_array_t').pointer()

    def invoke(self, args, from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) == 0:
            raise gdb.GdbError('输入参数数目不对，help print-array 以获得用法')

        self.type_lookup()

        m = re.match('0[xX][0-9a-fA-F]+', argv[0])
        if m:
            a = gdb.Value(int(argv[0], 16)).cast(self.array_pointer_type)

        else:
            a = gdb.parse_and_eval(argv[0])

        if not a:
            print("ngx_array_t point empty")
            return

        print("ngx_array_t alloc size: %d" % int(a['nalloc']))
        print("ngx_array_t used size: %d" % int(a['nelts']))
        print("ngx_array_t elts size: %d" % int(a['size']))
        print("ngx_array_t every elts:")

        if len(argv) == 1:
            print("ngx_array_t just first elts pointer: %s" % str(a['elts']))

        elif len(argv) == 2:
            # elt_type = gdb.lookup_type(argv[1])
            # e = gdb.Value(int(a['elts'], 16)).cast(elt_type)
            e = a['elts'].cast(gdb.lookup_type('u_char').point())
            elt_type = argv[1]
            elt_size = int(a['size'])
            for i in xrange(a['nelts']):
                comm = 'p ' + argv[0] + '(' + str(e+i*elt_size) + ')'
                print(comm)
                gdb.execute(comm)


PrintArray()
