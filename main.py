# -*- coding:utf-8 -*-
from time import sleep, time, strptime, mktime, localtime
from datetime import datetime
import process_task
from config import global_config


def start_worker():
    paths = [path[1] for path in global_config.getItems('start_program')]
    process_task.start_process(paths)


def end_worker():
    end_program = [program[1]
                   for program in global_config.getItems('end_program')]
    for name in end_program:
        process_task.kill_process_list(process_task.find_process_by_name(name))


def process_task_run(select_type=None):
    if not select_type:
        print('-------------- 上班：1 下班：2 --------------')
        select_type = input('-------------- 请选择：')
    if select_type == '1':
        start_worker()
        print('-------------- 一天的工作又开始了 -------------- ')
    elif select_type == '2':
        end_worker()
        print('-------------- 幸苦了,一天的工作结束了! -------------- ')
        sleep(2)
        process_task.lock_screen()
    else:
        print('未选择')
    if int(force_close_str) and select_type != '1':
        exit(0)


def enable_force_stop():
    close_time_everyday = global_config.getRaw(
        'config', 'close_time').__str__()
    now = time()
    localtime_now = localtime(now)
    close_date = datetime.strptime(
        localtime_now.tm_year.__str__() + '-' + localtime_now.tm_mon.__str__() +
        '-' + localtime_now.tm_mday.__str__()
            + ' ' + close_time_everyday,
        "%Y-%m-%d %H:%M")
    close_time = int(mktime(close_date.timetuple()) *
                     1000.0 + close_date.microsecond / 1000)
    now_time = int(round(now * 1000))
    return now_time >= close_time


if __name__ == '__main__':
    start_date = datetime.strptime(
        global_config.getRaw('config', 'start_data'), "%Y-%m-%d")
    force_close_str = global_config.getRaw('config', 'force_close')
    total_day = int((datetime.now() - start_date).total_seconds()/(3600*24))
    print('-------------- 今天是你入职的第 {0} 天 --------------'.format(total_day))
    if int(force_close_str):
        process_task_run()
        print('-------------- 已开启强制退出,今天的下班时间是： {0} --------------'.format(global_config.getRaw('config', 'close_time').__str__()))
    while True:
        if not int(force_close_str):
            process_task_run()
            break
        if enable_force_stop():
            process_task_run('2')
            break
