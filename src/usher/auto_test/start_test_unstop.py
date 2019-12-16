import os
import time
import psutil
import csv
import datetime
import subprocess
import pyautogui
# import cv2


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


def start_ui():
    os.system('start_ui start')
    print('do reboot')
    pass


def stop_ui():
    os.system('echo "root" | sudo -S start_ui stop')
    print('do reboot')
    pass


def write_csv_header():
    print('add tmp.csv')
    with open('./tmp.csv', 'w+', newline='')as f:
        headers = ['index', 'record_time', 'start_status', 'ui_main_pid', 'rosmaster_pid', 'rostopic_list']
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
    if not os.path.isdir('./record'):
        os.system('mkdir ./record')
    str_command = 'mv ./tmp.csv ' + './record/' + str_date.replace(' ', '--') + '.csv'
    print(str_command)
    os.system(str_command)
    os.system('zip -r record_' + str_date.replace(' ', '--') + '.zip ./record/*')
    os.system('rm ./record -rf')


def handler_log(date_time):
    str_input_log = './record/' + str(date_time)
    if not os.path.isdir(str_input_log):
        os.system('mkdir -p ' + str(str_input_log))
    os.system('mv /home/utry/release/log/utry_* ' + str_input_log)
    os.system('cp /tmp/start.log ' + str_input_log)
    os.system('rm /home/utry/release/log/utry_*')
    img = pyautogui.screenshot(region=[0, 0, 800, 480])  # x,y,w,h
    img.save(str_input_log + '/screenshot.png')


def get_start():
    return 100


def get_snap_screen(data_time):
    return


if __name__ == '__main__':
    time_cnt = 0
    is_success = True
    print(datetime.datetime.now())

    try:
        while True:
            start_ui()
            if not os.path.isfile('./tmp.csv'):
                write_csv_header()
            target_cnt = get_start()
            current_cnt = read_csv()
            while True:
                time_cnt += 1
                time.sleep(1)

                if len(get_pid_by_name('ui_main')) > 0 and len(get_pid_by_name('rosmaster')) > 0:
                    break

                if time_cnt >= 300:
                    print('start error')
                    is_success = False
                    break

            time.sleep(60)
            print('start write csv')
            date_time = str(datetime.datetime.now()).replace(' ', '--')
            list_row = [str(current_cnt), date_time]
            if is_success:
                list_row.append('success')
            else:
                list_row.append('fail')
            list_row.append(str(get_pid_by_name('ui_main')))
            list_row.append(str(get_pid_by_name('rosmaster')))
            _, result = subprocess.getstatusoutput('rostopic list')
            list_row.append(str(result).replace('\n', ' '))

            write_csv(list_row)
            handler_log(date_time)
            get_snap_screen(date_time)

            if current_cnt >= target_cnt:
                clear_file()
                break
            time.sleep(1)

            stop_ui()
            time.sleep(10)

    except KeyboardInterrupt as e:
        print(' stop by ctrl + c')
        stop_ui()
        clear_file()
        time.sleep(1)
        print('test end')