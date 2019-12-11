import os
import time
import psutil
import csv
import datetime
import subprocess


def get_pid_by_name(name: str):
    pid = psutil.process_iter()
    list_pid = []
    for pid_sub in pid:
        try:
            if name == pid_sub.name():
                print('get ' + str(name))
                list_pid.append(pid_sub.pid)
        except:
            print('something error')
            break
    return list_pid


def do_restart():
    # os.system('reboot')
    print('do reboot')
    pass


def write_csv_header():
    print('add tmp.csv')
    with open('./tmp.csv', 'w+', newline='')as f:
        headers = ['启动序号', '记录时间', '启动结果', 'ui_main 进程号', 'rosmaster 进程号', 'rostopic list']
        f_csv = csv.DictWriter(f, headers)
        f_csv.writeheader()


def write_csv(dict_row):
    with open('./tmp.csv', "a", newline='') as file:  # 处理csv读写时不同换行符  linux:\n    windows:\r\n    mac:\r
        csv_file = csv.writer(file)
        print(dict_row)
        csv_file.writerow(dict_row)
    pass


def read_csv():
    with open('./tmp.csv')as f:
        f_csv = csv.reader(f)
        index_cnt = 0
        for index in f_csv:
            index_cnt += 1
        return index_cnt


def clear_file():
    os.system('rm ./start_ini')
    str_date = str(datetime.datetime.now())
    str_command = 'mv ./tmp.csv ' + './' + str_date.replace(' ', '--') + '.csv'
    print(str_command)
    os.system(str_command)


def get_start():
    with open('./start_ini', 'r') as f_start:
        start_cnt = f_start.readline()
        if start_cnt == '':
            start_cnt = 0
        else:
            start_cnt = int(start_cnt)
        print('read :' + str(start_cnt))
        return start_cnt


if __name__ == '__main__':
    time_cnt = 0
    is_success = True
    print(datetime.datetime.now())

    if os.path.isfile('./start_ini'):
        if not os.path.isfile('./tmp.csv'):
            write_csv_header()
        target_cnt = get_start()
        current_cnt = read_csv()
        while True:
            time_cnt += 1
            time.sleep(1)

            if len(get_pid_by_name('ui_main')) > 0:
                break

            if time_cnt >= 300:
                print('start error')
                is_success = False
                break

        time.sleep(60)
        print('start write csv')
        list_row = [str(current_cnt), str(datetime.datetime.now())]
        if is_success:
            list_row.append('成功')
        else:
            list_row.append('失败')
        list_row.append(str(get_pid_by_name('ui_main')))
        list_row.append(str(get_pid_by_name('rosmaster')))
        _, result = subprocess.getstatusoutput('rostopic list')
        list_row.append(str(result))

        write_csv(list_row)

        if current_cnt >= target_cnt:
            clear_file()
        time.sleep(1)

        do_restart()