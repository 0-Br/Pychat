import socket
import random
import os
os.chdir(os.path.dirname(__file__))

#客户端全局变量
isworking = True#客户端工作状态
myaccount = ''
mypassword = ''
myname = ''
mydict_friends = {}#储存朋友账户信息的字典
buf = ''#GUI缓冲
bufon = False#是否启用GUI缓冲
position = ''#所处聊天区域
isroom = False#所处区域是否是聊天室
isrefreshing = False#检测刷新状态
dict_chatrooms = {}#储存聊天室信息的字典
dict_chatrooms['0'] = (5, '问题反馈区')
dict_chatrooms['1'] = (30, '第一聊天室')
dict_chatrooms['2'] = (30, '第二聊天室')
dict_chatrooms['3'] = (30, '第三聊天室')
dict_chatrooms['4'] = (30, '第四聊天室')
dict_chatrooms['5'] = (30, '第五聊天室')
dict_chatrooms['6'] = (30, '第六聊天室')
dict_chatrooms['7'] = (20, '校园动态聊天室')
dict_chatrooms['8'] = (20, '学习讨论聊天室')
dict_chatrooms['9'] = (10, '时事政治聊天室')
dict_chatrooms['10'] = (10, '动漫交流聊天室')
dict_chatrooms['11'] = (10, '二手交易聊天室')
dict_chatrooms['12'] = (15, '问题反馈区')

#初始化本地客户端套接字
sock_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#主连接套接字
sock_background = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#后台连接套接字
clientname = socket.gethostname()
clienthost = socket.gethostbyname(clientname)
serverhost = clienthost#服务器地址
serverport = 49152#服务器端口
while True:
    try:
        clientport = random.randint(49153, 65535)#随机指定主连接的本地端口
        break
    except:
        pass
while True:
    try:
        backgroundport = random.randint(49153, 65535)#随机指定后台连接的本地端口
        break
    except:
        pass

def start():
    '''启动客户端，并连接服务器'''
    try:
        print('客户端:(%s, %s, %d)' % (clientname, clienthost, clientport))
        sock_client.bind((clienthost, clientport))
        sock_client.connect((serverhost, serverport))
        sock_background.bind((clienthost, backgroundport))
        sock_background.connect((serverhost, serverport))
        print(sock_client.recv(256).decode('utf-8'))
    except:
        global isworking
        isworking = False
        print('连接服务器失败！')

def recv_message(sock_background:socket.socket):
    '''启用一个子线程，从后台端口接收来自服务器端的消息，将消息存入GUI缓冲区，工作判定：isworking'''
    while isworking:
        print('正在接收消息...')
        account_source = sock_background.recv(256).decode('utf-8')#接收消息来源账号
        sock_background.sendall('$'.encode('utf-8'))
        name_source = sock_background.recv(256).decode('utf-8')#接收消息来源昵称
        sock_background.sendall('$'.encode('utf-8'))
        message = sock_background.recv(1048576).decode('utf-8')#接收消息
        print('接收完成!')
        global buf
        if (account_source == position or account_source == myaccount) and not isroom:
            buf += '('+ account_source + ')' + name_source + '：\n' + message
            print('已加载GUI缓冲！')
        elif isroom:
            sock_background.sendall('$'.encode('utf-8'))
            roomid = sock_background.recv(256).decode('utf-8')#若在聊天室中，接收聊天室id
            if roomid == position:
                buf += '('+ account_source + ')' + name_source + '：\n' + message
                print('已加载GUI缓冲！')
    sock_background.close()

def login(sock_client:socket.socket, account:str, password:str) -> int:
    '''
    向服务器上传账号和密码，尝试登录账户，指令码：__login__
    接收验证码，1表示密码正确，0表示密码错误，-1表示不存在该账号，-8080表示该账号已登录
    若密码正确，接收用户昵称和好友账号的元组，并修改客户端的全局变量
    返回验证码
    '''
    print('尝试登录...')
    sock_client.sendall('__login__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(account.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(password.encode('utf-8'))
    print('账号、密码已上传服务器！')
    re0 = int(sock_client.recv(256).decode('utf-8'))
    sock_client.sendall('$'.encode('utf-8'))
    if re0 == -8080:
        print('账号已经登录！')
    if re0 == -1:
        print('账号不存在！')
    if re0 == 1:
        name = sock_client.recv(256).decode('utf-8')
        sock_client.sendall('$'.encode('utf-8'))
        global myaccount, mypassword, myname, mydict_friends
        myaccount = account
        mypassword = password
        myname = name
        accounts_friend = []
        names_friends = []
        while True:#逐次接收好友账号元组，以end代表结束
            t = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if t == 'end':
                break
            else:
                accounts_friend.append(t)
        while True:#逐次接收好友昵称元组，以end代表结束
            t = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if t == 'end':
                break
            else:
                names_friends.append(t)
        for x, y in zip(accounts_friend, names_friends):
            mydict_friends[x] = y
        print('登录成功！')
    if re0 == 0:
        print('密码错误！')
    return re0

def logout(sock_client:socket.socket):
    '''向服务器提交登出申请，指令码：__logout__'''
    print('尝试登出...')
    sock_client.sendall('__logout__'.encode('utf-8'))
    sock_client.recv(1)
    global myaccount, mypassword, myname, mydict_friends
    myaccount = ''
    mypassword = ''
    myname = ''
    mydict_friends = {}
    print('账号已登出！')

def register(sock_client:socket.socket, account:str, password:str, name:str) -> int:
    '''
    向服务器上传账号、密码和昵称，尝试注册一个新的账户，指令码：__register__
    接收验证码，1表示注册成功，0表示账号已存在
    返回验证码
    '''
    print('尝试注册账户...')
    sock_client.sendall('__register__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(account.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(password.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(name.encode('utf-8'))
    print('注册信息已上传服务器！')
    re0 = int(sock_client.recv(256).decode('utf-8'))
    if re0 == 1:
        print('注册成功！')
    if re0 == 0:
        print('账号已存在！')
    return re0

def add_friend(sock_client:socket.socket, account_friend:str) -> int:
    '''
    向服务器上传账号，尝试添加一个好友，接收好友昵称并修改本地的全局变量，指令码：__add__
    接收验证码，1表示添加成功，0表示好友关系已存在，-1表示好友账号不存在，返回验证码
    '''
    print('尝试添加好友...')
    sock_client.sendall('__add__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(account_friend.encode('utf-8'))
    print('好友账号已上传服务器！')
    re0 = int(sock_client.recv(256).decode('utf-8'))
    if re0 == 1:
        sock_client.sendall('$'.encode('utf-8'))
        name_friend = sock_client.recv(256).decode('utf-8')
        mydict_friends[account_friend] = name_friend
        print('添加好友成功！')
    if re0 == 0:
        print('好友关系已存在！')
    if re0 == -1:
        print('好友账号不存在！')
    return re0

def send_message(sock_client:socket.socket, account_friend:str, message:str) -> int:
    '''
    [供私聊使用的接口]
    向服务器上传好友账号和消息，请求向好友发送该消息，指令码：__chat__
    接收验证码，1表示发送成功，0表示好友不在线，返回验证码
    '''
    print('尝试发送一条消息...')
    sock_client.sendall('__chat__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(account_friend.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(message.encode('utf-8'))
    print('消息已上传服务器！')
    re0 = int(sock_client.recv(256).decode('utf-8'))
    if re0 == 0:
        print('好友不在线！')
    if re0 == 1:
        print('发送成功！')
    return re0

def call_message(sock_client:socket.socket, roomid:str, message:str):
    '''
    [供聊天室使用的接口]
    向服务器上传聊天室编号和消息，请求在聊天室发送该消息，指令码：__broadcast__
    '''
    print('尝试发送一条消息...')
    sock_client.sendall('__broadcast__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(roomid.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(message.encode('utf-8'))
    print('消息已上传服务器！')
    print('发送成功')

def getin_chatroom(sock_client:socket.socket, roomid:str):
    '''向服务器上传聊天室编号，请求加入聊天室，指令码：__getin__'''
    print('尝试加入一个聊天室...')
    sock_client.sendall('__getin__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(roomid.encode('utf-8'))
    print('加入聊天室成功！')

def getout_chatroom(sock_client:socket.socket, roomid:str):
    '''向服务器上传聊天室编号，请求退出聊天室，指令码：__getout__'''
    print('尝试退出一个聊天室...')
    sock_client.sendall('__getout__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(roomid.encode('utf-8'))
    print('退出聊天室成功！')

def check_roominfo(sock_client:socket.socket, roomid:str) -> tuple:
    '''
    向服务器上传聊天室编号，接收聊天室成员信息，指令码：__cr__
    以元组格式返回聊天室成员账号和昵称的列表
    '''
    print('查询聊天室成员信息中...')
    sock_client.sendall('__cr__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(roomid.encode('utf-8'))
    accounts_inroom = []
    names_inroom = []
    while True:#逐次接收账号元组，以end代表结束
        t = sock_client.recv(256).decode('utf-8')
        sock_client.sendall('$'.encode('utf-8'))
        if t == 'end':
            break
        else:
            accounts_inroom.append(t)
    while True:#逐次接收昵称元组，以end代表结束
        t = sock_client.recv(256).decode('utf-8')
        sock_client.sendall('$'.encode('utf-8'))
        if t == 'end':
            break
        else:
            names_inroom.append(t)
    print('查询成功！')
    return (accounts_inroom, names_inroom)

def ask_privatehistory(sock_client:socket.socket, account_friend:str) -> tuple:
    '''
    向服务器上传好友的账号，接收聊天记录，指令码：__private__
    以元组格式返回时间戳列表、发送者账号列表和消息内容列表
    '''
    print('查询聊天记录中...')
    sock_client.sendall('__private__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(account_friend.encode('utf-8'))
    timestamps = []
    accounts = []
    contents = []
    re0 = int(sock_client.recv(256).decode('utf-8'))
    sock_client.sendall('$'.encode('utf-8'))
    if re0 == 1:
        print('查询成功！')
        while True:#逐次接收账号元组，以end代表结束
            timestamp = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if timestamp == 'end':
                break
            else:
                timestamps.append(float(timestamp))
        while True:#逐次接收账号元组，以end代表结束
            account = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if account == 'end':
                break
            else:
                accounts.append(account)
        while True:#逐次接收账号元组，以end代表结束
            content = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if content == 'end':
                break
            else:
                contents.append(content)
        return (timestamps, accounts, contents)
    if re0 == 0:
        print('还没有任何聊天记录！')
        return ()

def ask_chatroomhistory(sock_client:socket.socket, roomid:str) -> tuple:
    '''
    向服务器上传聊天室编号，接收聊天记录，指令码：__room__
    以元组格式返回时间戳列表、发送者账号列表和消息内容列表
    '''
    print('查询聊天记录中...')
    sock_client.sendall('__room__'.encode('utf-8'))
    sock_client.recv(1)
    sock_client.sendall(roomid.encode('utf-8'))
    timestamps = []
    accounts = []
    contents = []
    re0 = int(sock_client.recv(256).decode('utf-8'))
    sock_client.sendall('$'.encode('utf-8'))
    if re0 == 1:
        print('查询成功！')
        while True:#逐次接收账号元组，以end代表结束
            timestamp = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if timestamp == 'end':
                break
            else:
                timestamps.append(float(timestamp))
        while True:#逐次接收账号元组，以end代表结束
            account = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if account == 'end':
                break
            else:
                accounts.append(account)
        while True:#逐次接收账号元组，以end代表结束
            content = sock_client.recv(256).decode('utf-8')
            sock_client.sendall('$'.encode('utf-8'))
            if content == 'end':
                break
            else:
                contents.append(content)
        return (timestamps, accounts, contents)
    if re0 == 0:
        print('还没有任何聊天记录！')
        return ()

def recvfile(file:str) -> int:
    '''
    接收来自发送端的文件
    返回验证码，1代表接收成功，返回0代表接收失败
    （用于传输图片的接口，尚未完全实现）
    '''
    print(sock_client.recv(256).decode('utf-8'))
    sock_client.sendall('$'.encode('utf-8'))
    total_size = int(sock_client.recv(256).decode('utf-8'))
    sock_client.sendall('$'.encode('utf-8'))
    print('文件大小：%d' % total_size)
    alrecv_size = 0#保存已接收的文件大小，显示读取进度

    if os.path.exists(file):
        os.remove(file)
    with open(file, "ab") as f:
        while True:
            if alrecv_size < total_size:
                content = sock_client.recv(16384)#每次接收16KB数据
                alrecv_size += len(content)#更新接收的文件大小
                print('传输进度：%d/%d' % (alrecv_size, total_size))
                f.write(content)
            else:
                break

    if alrecv_size == total_size:
        print('接收文件成功！')
        return 1
    else:
        print('接收文件失败！')
        os.remove(file)
        return 0

if __name__ == '__main__':
    start()