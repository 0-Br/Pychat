import sqlite3
import time
import os
os.chdir(os.path.dirname(__file__))

def create_Info():
    '''创建主信息数据库，含账户信息表、好友信息表和聊天室信息表'''
    conn = sqlite3.connect('data/Info.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS AccountInfo(
            account text primary key,
            password text not null,
            name text not null)''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS FriendInfo(
            account text,
            account_friend text,
            primary key (account, account_friend),
            foreign key (account) references AccountInfo(account),
            foreign key (account_friend) references AccountInfo(account))''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS ChatroomInfo(
            roomid text primary key,
            capacity int not null,
            roomname text not null)''')
    c.execute('''
        INSERT OR IGNORE INTO AccountInfo VALUES
            ('10086', 'admin', 'Administrator')''')
    c.execute('''
        INSERT OR IGNORE INTO FriendInfo VALUES
            ('10086', '10086')''')
    chatrooms = [
        ('0', 5, '问题反馈区'),
        ('1', 30, '第一聊天室'),
        ('2', 30, '第二聊天室'),
        ('3', 30, '第三聊天室'),
        ('4', 30, '第四聊天室'),
        ('5', 30, '第五聊天室'),
        ('6', 30, '第六聊天室'),
        ('7', 20, '校园动态聊天室'),
        ('8', 20, '学习讨论聊天室'),
        ('9', 10, '时事政治聊天室'),
        ('10', 10, '动漫交流聊天室'),
        ('11', 10, '二手交易聊天室'),
        ('12', 15, '备用聊天室')]
    c.executemany('INSERT OR IGNORE INTO ChatroomInfo VALUES(?, ?, ?)', chatrooms)
    conn.commit()
    c.close()
    conn.close()

def create_History():
    '''创建聊天记录数据库，每一位用户对应着一个聊天记录表'''
    conn = sqlite3.connect('data/History.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ChatHistory(
            timestamp real primary key,
            account text,
            content text,
            position text,
            isroom integer)''')
    conn.commit()
    c.close()
    conn.close()

def search_account(account:str) -> tuple:
    '''根据账号，在数据库中查找账户信息并以元组格式返回'''
    conn = sqlite3.connect('data/Info.db')
    c = conn.cursor()
    re0 = c.execute('''
        SELECT * FROM AccountInfo WHERE 
            account = "%s"''' % account).fetchall()
    c.close()
    conn.close()
    if len(re0) > 0:
        return re0[0]
    else:
        return ()

def search_friends(account:str) -> tuple:
    '''根据账号，在数据库中查找好友的帐户信息，以元组格式返回账号列表和昵称列表'''
    conn = sqlite3.connect('data/Info.db')
    c = conn.cursor()
    re0 = c.execute('''
        SELECT AccountInfo.account, AccountInfo.name FROM AccountInfo, FriendInfo WHERE 
            FriendInfo.account = "%s" and AccountInfo.account = FriendInfo.account_friend''' % account).fetchall()
    c.close()
    conn.close()
    accounts = []
    names = []
    for x in re0:
        accounts.append(x[0])
        names.append(x[1])
    return (accounts, names)

def search_privatehistory(account:str, account_friend:str) -> tuple:
    '''
    根据两个账号，在数据库中查找两账户间的私聊聊天记录
    以元组格式返回时间戳列表、发送者账号列表和消息内容列表
    '''
    conn = sqlite3.connect('data/History.db')
    c = conn.cursor()
    re0 = c.execute('''
        SELECT * FROM ChatHistory WHERE(
            ((account = '%s' and position = '%s') or (account = '%s' and position = '%s')) and
            isroom = 0)''' % (account, account_friend, account_friend, account)).fetchall()
    c.close()
    conn.close()
    timestamps = []
    accounts = []
    contents = []
    for x in re0:
        timestamps.append(x[0])
        accounts.append(x[1])
        contents.append(x[2])
    return (timestamps, accounts, contents)

def search_chatroomhistory(roomid:str) -> tuple:
    '''
    根据聊天室编号，在数据库中查找聊天室的聊天记录
    以元组格式返回时间戳列表、发送者账号列表和消息内容列表
    '''
    conn = sqlite3.connect('data/History.db')
    c = conn.cursor()
    re0 = c.execute('''
        SELECT * FROM ChatHistory WHERE
            position = "%s" and isroom = 1''' % roomid).fetchall()
    c.close()
    conn.close()
    timestamps = []
    accounts = []
    contents = []
    for x in re0:
        timestamps.append(x[0])
        accounts.append(x[1])
        contents.append(x[2])
    return (timestamps, accounts, contents)

def add_account(account:str, password:str, name:str) -> int:
    '''在数据库中添加一条账户信息，返回1表示成功，返回0表示账号重复'''
    try:
        conn = sqlite3.connect('data/Info.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO AccountInfo VALUES
                ('%s', '%s', '%s')''' % (account, password, name))
        conn.commit()
        c.close()
        conn.close()
        add_friend('10086', account)
        return 1
    except sqlite3.IntegrityError:
        return 0

def add_friend(account:str, account_friend:str) -> int:
    '''在数据库中添加一条好友关系，返回1表示成功，返回0表示好友关系重复或不存在好友账号'''
    try:
        conn = sqlite3.connect('data/Info.db')
        c = conn.cursor()
        c.execute('''PRAGMA foreign_keys = ON''')#开启外码约束
        c.execute('''
            INSERT INTO FriendInfo VALUES
                ('%s', '%s')''' % (account, account_friend))
        c.execute('''
            INSERT INTO FriendInfo VALUES
                ('%s', '%s')''' % (account_friend, account))
        conn.commit()
        c.close()
        conn.close()
        return 1
    except sqlite3.IntegrityError:
        return 0

def add_history(account:str, content:str, position:str, isroom:bool) -> int:
    '''在数据库中添加一条聊天记录，返回1表示成功，返回0表示失败'''
    try:
        conn = sqlite3.connect('data/History.db')
        c = conn.cursor()
        c.execute('''
            INSERT INTO ChatHistory VALUES
                ('%f', '%s', '%s', '%s', %d)''' % (time.time(), account, content, position, int(isroom)))
        conn.commit()
        c.close()
        conn.close()
        return 1
    except:
        return 0

create_Info()
create_History()

if __name__ == '__main__':
    create_History()
    create_Info()