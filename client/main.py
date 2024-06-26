import threading
import time
import os

import GUI_framework as GUI
import client

if __name__ == '__main__':
    try:
        client.start()
        t0 = threading.Thread(target = client.recv_message, args = (client.sock_background,))
        t0.start()
        t1 = threading.Thread(target = GUI.login)
        t1.start()
        time.sleep(3)
        if client.isworking:
            print('客户端工作状态：正常')
        else:
            print('客户端工作状态：不正常')
        while True:
            time.sleep(0.5)
            if not t0.is_alive():
                GUI.neterror()
                os._exit(0)
            if not t1.is_alive():
                print('正在退出客户端...')
                client.isworking = False
                time.sleep(2)
                os._exit(0)
    except:
        print('未知错误！')
        os._exit(0)