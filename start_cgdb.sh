##############################################################
# File Name: start_cgbd.sh
# Author: wuzhenzhong
# mail: jt26wzz@icloud.com
# Created Time: 2018年07月28日 星期六 09时53分53秒
#=============================================================
#!/bin/bash

# only one worker
pids=$(pidof nginx)
master_pid=$(cat /home/wzz/live/logs/nginx.pid)
work_pid=${pids/$master_pid/""}
sudo /usr/local/bin/cgdb -q -p $work_pid -x /home/wzz/Scripts/gdb_nginx_utils/cgdbrc
