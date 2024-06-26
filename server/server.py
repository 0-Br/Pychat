import socket
import threading
import time
import os
os.chdir(os.path.dirname(__file__))

import database

#服务器全局变量
clients = {}#储存已连接客户端信息的字典
dict_accounts = {}#账户-客户端编号字典
dict_chatrooms = {}#储存聊天室信息的字典
dict_chatrooms['0'] = (5, '问题反馈区', [])
dict_chatrooms['1'] = (30, '第一聊天室', [])
dict_chatrooms['2'] = (30, '第二聊天室', [])
dict_chatrooms['3'] = (30, '第三聊天室', [])
dict_chatrooms['4'] = (30, '第四聊天室', [])
dict_chatrooms['5'] = (30, '第五聊天室', [])
dict_chatrooms['6'] = (30, '第六聊天室', [])
dict_chatrooms['7'] = (20, '校园动态聊天室', [])
dict_chatrooms['8'] = (20, '学习讨论聊天室', [])
dict_chatrooms['9'] = (10, '时事政治聊天室', [])
dict_chatrooms['10'] = (10, '动漫交流聊天室', [])
dict_chatrooms['11'] = (10, '二手交易聊天室', [])
dict_chatrooms['12'] = (15, '问题反馈区', [])
lock = threading.Lock()#线程锁

#初始化服务器套接字
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servername = socket.gethostname()
serverhost = socket.gethostbyname(servername)
serverport = 49152#指定服务器端口
capacity = 256#最大可接受的用户数量

def start():
    '''启动服务器'''
    print('正在启动服务器...')
    try:
        sock_server.bind((serverhost, serverport))
    except OSError:
        try:
            print('正在等待端口资源释放...')
            time.sleep(5)
            sock_server.bind((serverhost, serverport))
        except:
            print('端口资源释放失败！请检查serverport占用情况！')
            os._exit(0)
    print('服务器：(%s, %s, %d)' % (servername, serverhost, serverport))
    print('服务器已启动，正在等待用户请求...')
    print('当前服务器容量：%d' % capacity)
    sock_server.listen(capacity * 2)

    #服务器监听客户端访问
    while True:
        connection, address = sock_server.accept()
        connection_b, address_b = sock_server.accept()
        if address[0] == address_b[0]:
            print(str(address) + '已连接!')
            print('主编号：' + str(connection.fileno()))
            print('副编号：' + str(connection_b.fileno()))
            threading.Thread(target = toserver, args = (connection, connection_b)).start()
        else:
            print('由于客户端的网络问题，拒绝了一个连接！')

def toserver(connection:socket.socket, connection_b:socket.socket):
    '''启用一个子线程为连接的客户端提供服务，工作判定：网络连接'''
    global clients, dict_accounts
    tempfileno = connection.fileno()
    clients[connection.fileno()] = [False, '', '', '', connection, connection_b]
    connection.sendall(('成功连接服务器！服务器为(%s, %s, %d)' % (servername, serverhost, serverport)
        + '\n当前客户端主编号：%d' % connection.fileno() + '\n当前客户端副编号：%d' % connection_b.fileno()).encode('utf-8'))
    while True:#循环接收来自客户端的请求
        try:
            request = connection.recv(256).decode('utf-8')
            lock.acquire()
            if request == '__login__':
                temptuple = login(connection)
                if temptuple:#若正确登录，更新全局字典
                    account, password, name = temptuple
                    clients[connection.fileno()] = (True, account, password, name, connection, connection_b)
                    dict_accounts[account] = (True, account, password, name, connection, connection_b)
            if request == '__logout__':
                logout(connection)#登出时更新全局字典
                dict_accounts.pop(clients[connection.fileno()][1])
                clients[connection.fileno()] = (False, '', '', '', connection, connection_b)
            if request == '__register__':
                register(connection)
            if request == '__add__':
                add_friend(connection)
            if request == '__chat__':
                exchange_message(connection, connection_b)
            if request == '__broadcast__':
                broadcast_message(connection)
            if request == '__getin__':
                getin_chatroom(connection)
            if request == '__getout__':
                getout_chatroom(connection)
            if request == '__cr__':
                check_roominfo(connection)
            if request == '__private__':
                ask_privatehistory(connection)
            if request == '__room__':
                ask_chatroomhistory(connection)
            lock.release()
        except ConnectionResetError:
            print('%d号客户端已断开连接！' % tempfileno)
            print('正在释放资源...')
            global dict_chatrooms
            for x in range(13):
                try:
                    x = str(x)
                    dict_chatrooms[x][2].remove(clients[tempfileno][1])
                    print('%s号聊天室现有%d位成员：' % (x, len(dict_chatrooms[x][2])))
                    print(str(dict_chatrooms[x][2]))
                except ValueError:
                    pass
            try:
                dict_accounts.pop(clients[tempfileno][1])
            except:
                pass
            try:
                clients.pop(tempfileno)
            except:
                pass
            print('%d号客户端资源已释放！' % tempfileno)
            connection.close()
            connection_b.close()
            break

def login(connection:socket.socket) -> tuple:
    '''
    接收客户端上传的账号和密码，在数据库中检验其正确性
    传回验证码，1表示密码正确，0表示密码错误，-1表示不存在该账号，-8080表示账号已经登陆
    若密码正确，传回其昵称和好友账号、昵称的元组
    返回登录的账户信息
    '''
    print('%d号客户端提交了一个登录申请...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    account = connection.recv(256).decode('utf-8')
    connection.sendall('$'.encode('utf-8'))
    password = connection.recv(256).decode('utf-8')
    print('登录账号：%s' % account)
    print('登录密码：%s' % password)
    info = database.search_account(account)
    temp = database.search_friends(account)
    accounts_friend = temp[0]
    names_friend = temp[1]
    if account in list(dict_accounts.keys()):
        if dict_accounts[account][0]:
            connection.sendall('-8080'.encode('utf-8'))
            connection.recv(1)
            print('账号已经登录！')
    elif len(info) == 0:
        connection.sendall('-1'.encode('utf-8'))
        connection.recv(1)
        print('账号不存在！')
    elif info[1] == password:
        connection.sendall('1'.encode('utf-8'))
        connection.recv(1)
        connection.sendall(info[2].encode('utf-8'))
        connection.recv(1)
        for account_friend in accounts_friend:
            connection.sendall(account_friend.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        for name_friend in names_friend:
            connection.sendall(name_friend.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        print('登录成功！')
        print('%s已登录！' % account)
        return info
    else:
        connection.sendall('0'.encode('utf-8'))
        connection.recv(1)
        print('密码错误！')
    return ()

def logout(connection:socket.socket):
    '''接收客户端提交的登出申请，执行登出账户操作'''
    connection.sendall('$'.encode('utf-8'))
    print('%d号客户端提交了一个登出申请...' % connection.fileno())
    print('账号已登出！')

def register(connection:socket.socket):
    '''
    接收客户端上传的账号、密码和昵称，尝试注册一个新的账户
    传回验证码，1表示注册成功，0表示账号已存在
    '''
    print('%d号客户端提交了一个注册申请...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    account = connection.recv(256).decode('utf-8')
    connection.sendall('$'.encode('utf-8'))
    password = connection.recv(256).decode('utf-8')
    connection.sendall('$'.encode('utf-8'))
    name = connection.recv(256).decode('utf-8')
    print('尝试注册账户：(%s, %s, %s)' % (account, password, name))
    re0 = database.add_account(account, password, name)
    if re0 == 1:
        print('注册成功！')
    if re0 == 0:
        print('账号已存在！')
    connection.sendall(str(re0).encode('utf-8'))

def add_friend(connection:socket.socket):
    '''
    接收客户端上传的账号，尝试添加一个新的好友关系，传回好友昵称
    传回验证码，1表示添加成功，0表示好友关系已存在，-1表示好友账号不存在
    '''
    print('%d号客户端提交了一个添加好友申请...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    account_friend = connection.recv(256).decode('utf-8')
    tempinfo = database.search_account(account_friend)
    if len(tempinfo) == 0:
        connection.sendall('-1'.encode('utf-8'))
        print('好友账号不存在！')
    else:
        name_friend = tempinfo[2]
        re0 = database.add_friend(clients[connection.fileno()][1], account_friend)
        if re0 == 1:
            connection.sendall('1'.encode('utf-8'))
            connection.recv(1)
            connection.sendall(name_friend.encode('utf-8'))
            print('添加好友成功！')
            print('现在%s和%s是好友了！' % (clients[connection.fileno()][1], account_friend))
        if re0 == 0:
            connection.sendall('0'.encode('utf-8'))
            print('好友关系已存在！')

def exchange_message(connection:socket.socket, connection_b:socket.socket):
    '''
    [供私聊使用的接口]
    接收客户端上传的账号和消息，向目标账户和源账户的后台端口发送发送者的账号、昵称和消息
    传回验证码，1表示发送成功，0表示好友不在线
    '''
    print('%d号客户端提交了一个消息...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    account_friend = connection.recv(256).decode('utf-8')
    connection.sendall('$'.encode('utf-8'))
    message = connection.recv(65536).decode('utf-8')
    if not account_friend in list(dict_accounts.keys()):
        connection.sendall('0'.encode('utf-8'))
        print('发送失败！目标账户不在线!')
    else:
        database.add_history(clients[connection.fileno()][1], message, account_friend, False)
        connection_target = dict_accounts[account_friend][5]
        connection_target.sendall(clients[connection.fileno()][1].encode('utf-8'))
        connection_target.recv(1)
        connection_target.sendall(clients[connection.fileno()][3].encode('utf-8'))
        connection_target.recv(1)
        connection_target.sendall(message.encode('utf-8'))
        connection_b.sendall(clients[connection.fileno()][1].encode('utf-8'))
        connection_b.recv(1)
        connection_b.sendall(clients[connection.fileno()][3].encode('utf-8'))
        connection_b.recv(1)
        connection_b.sendall(message.encode('utf-8'))
        connection.sendall('1'.encode('utf-8'))
        print('发送消息成功！')

def broadcast_message(connection:socket.socket):
    '''
    [供聊天室使用的接口]
    接收客户端上传的聊天室编号和消息
    向当前聊天室中的所有后台端口发送发送者的账号、昵称、消息和聊天室编号
    '''
    print('%d号客户端提交了一个消息...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    roomid = connection.recv(256).decode('utf-8')
    connection.sendall('$'.encode('utf-8'))
    message = connection.recv(65536).decode('utf-8')
    database.add_history(clients[connection.fileno()][1], message, roomid, True)
    for account_target in dict_chatrooms[roomid][2]:
        s = dict_accounts[account_target][5]
        s.settimeout(0.2)
        s.sendall(clients[connection.fileno()][1].encode('utf-8'))
        s.recv(1)
        s.sendall(clients[connection.fileno()][3].encode('utf-8'))
        s.recv(1)
        s.sendall(message.encode('utf-8'))
        s.recv(1)
        s.sendall(roomid.encode('utf-8'))
        s.settimeout(None)
    print('发送消息成功！')

def getin_chatroom(connection:socket.socket):
    '''接收客户端上传的聊天室编号，处理其进入聊天室的请求'''
    print('%d号客户端提交了一个加入聊天室申请...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    roomid = connection.recv(256).decode('utf-8')
    global dict_chatrooms
    dict_chatrooms[roomid][2].append(clients[connection.fileno()][1])
    print('请求接受！')
    print('%s号聊天室现有%d位成员：' % (roomid, len(dict_chatrooms[roomid][2])))
    print(str(dict_chatrooms[roomid][2]))

def getout_chatroom(connection:socket.socket):
    '''接收客户端上传的聊天室编号，处理其退出聊天室的请求'''
    print('%d号客户端提交了一个退出聊天室申请...' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    roomid = connection.recv(256).decode('utf-8')
    global dict_chatrooms
    dict_chatrooms[roomid][2].remove(clients[connection.fileno()][1])
    print('请求接受！')
    print('%s号聊天室现有%d位成员：' % (roomid, len(dict_chatrooms[roomid][2])))
    print(str(dict_chatrooms[roomid][2]))

def check_roominfo(connection:socket.socket):
    '''接收客户端上传的聊天室编号，返回聊天室当前成员信息'''
    print('%d号客户端提交了一个检查聊天室成员信息的请求..' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    roomid = connection.recv(256).decode('utf-8')
    accounts_inroom = dict_chatrooms[roomid][2]
    names_inroom = []
    for x in accounts_inroom:
        names_inroom.append(dict_accounts[x][3])
    for account in accounts_inroom:
        connection.sendall(account.encode('utf-8'))
        connection.recv(1)
    connection.sendall('end'.encode('utf-8'))#表示传输结束
    connection.recv(1)
    for name in names_inroom:
        connection.sendall(name.encode('utf-8'))
        connection.recv(1)
    connection.sendall('end'.encode('utf-8'))#表示传输结束
    connection.recv(1)
    print('请求接受！')

def ask_privatehistory(connection:socket.socket):
    '''
    接收客户端上传的账号，传回验证码，1表示查询成功，0表示不存在聊天记录
    返回私聊的聊天记录
    '''
    print('%d号客户端提交了一个获取聊天记录的请求..' % connection.fileno())
    connection.sendall('$'.encode('utf-8'))
    account_friend = connection.recv(256).decode('utf-8')
    history = database.search_privatehistory(clients[connection.fileno()][1], account_friend)
    if len(history[0]) == 0:
        connection.sendall('0'.encode('utf-8'))
        connection.recv(1)
        print('没有聊天记录！')
    else:
        connection.sendall('1'.encode('utf-8'))
        connection.recv(1)
        for time in history[0]:
            connection.sendall(str(time).encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        for account in history[1]:
            connection.sendall(account.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        for content in history[2]:
            connection.sendall(content.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        print('已返回聊天记录！')

def ask_chatroomhistory(connection:socket.socket):
    '''接收客户端上传的聊天室编号，返回聊天室的聊天记录'''
    connection.sendall('$'.encode('utf-8'))
    roomid = connection.recv(256).decode('utf-8')
    history = database.search_chatroomhistory(roomid)
    print(history)##
    if len(history[0]) == 0:
        connection.sendall('0'.encode('utf-8'))
        connection.recv(1)
    else:
        connection.sendall('1'.encode('utf-8'))
        connection.recv(1)
        for time in history[0]:
            connection.sendall(str(time).encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        for account in history[1]:
            connection.sendall(account.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)
        for content in history[2]:
            connection.sendall(content.encode('utf-8'))
            connection.recv(1)
        connection.sendall('end'.encode('utf-8'))#表示传输结束
        connection.recv(1)

def sendfile(connection:socket.socket, file:str) -> int:
    '''
    读取文件并发送到接收端
    返回验证码，1代表发送成功，返回0代表发送失败
    （用于传输图片的接口，尚未完全实现）
    '''
    try:
        alread_size = 0#保存已读取的图片大小，显示读取的进度
        total_size = os.path.getsize(file)#文件总大小
        connection.sendall(bytes('正在接收文件...'.encode('utf-8')))
        connection.recv(1)
        connection.sendall(bytes(('%d' % total_size).encode('utf-8')))
        connection.recv(1)

        with open(file, "rb") as f:
            while True:
                content = f.read(16384)#每次从文件中读取16KB数据
                alread_size += len(content)#更新已读取数据的大小
                if content:
                    connection.sendall(content)
                    print('传输进度：%d/%d' % (alread_size, total_size))
                else:
                    print("传输完成！")
                    return 1
    except:
        print('接收文件失败！')
        return 0

if __name__ == '__main__':
    start()