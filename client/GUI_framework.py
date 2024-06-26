from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showwarning, showerror
import threading
import time

import client

def login():
    '''启动登录界面'''
    def check():
        out_account = in_account.get()#用户输入的账号
        out_password = in_password.get()#用户输入的密码
        if out_account == '':
            showinfo(title = '提示', message = '您还没有输入账号！')
        elif out_password == '':
            showinfo(title = '提示', message = '您还没有输入密码！')
        else:
            re0 = client.login(client.sock_client, out_account, out_password)
            if re0 == 1:
                root.destroy()
                menu()
            if re0 == 0:
                showwarning(title = '警告', message = '密码错误！\n请检查您输入的密码是否正确！')
            if re0 == -1:
                showwarning(title = '警告', message = '该账号不存在！\n请先注册一个账号！')
            if re0 == -8080:
                showwarning(title = '警告', message = '该账号已经登录！\n不能重复登录！')
    def goregister():
        root.destroy()
        register()

    #框架大小固定为400x300,设置为总是在屏幕中央的最上层显示,不可调整大小
    root = Tk()
    root.title('微信')
    root.iconbitmap('pics\\icon.ico')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 400
    height = 300
    pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 380, height = 280)
    labelframe = ttk.Labelframe(root, text = '登录')
    labelframe.place(x = 20, y = 20, width = 360, height = 180)

    Label(labelframe, text = '账号', font = ('微软雅黑', 12)).place(x = 40, y = 20)
    in_account = StringVar()
    Entry(labelframe, textvariable = in_account, font = ('微软雅黑', 12)).place(x = 110, y = 20, width = 200, height = 30)

    Label(labelframe, text = '密码', font = ('微软雅黑', 12)).place(x = 40, y = 90)
    in_password = StringVar()
    Entry(labelframe, textvariable = in_password, show = '*', font = ('微软雅黑', 12)).place(x = 110, y = 90, width = 200, height = 30)

    Button(frame, text = '登录', command = check, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 80, y = 210, width = 80, height = 50)
    Button(frame, text = '注册', command = goregister, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 220, y = 210, width = 80, height = 50)
    
    root.mainloop()
########################################################################
def register():
    '''启动注册界面'''
    def check():
        out_name = in_name.get()
        out_account = in_account.get()
        out_password = in_password.get()
        if len(out_name) == 0:
            showinfo(title = '提示', message = '您还没有输入昵称！')
        elif len(out_name) > 8:
            showwarning(title = '警告', message = '昵称长度至多为8！')
        elif len(out_account) == 0:
            showinfo(title = '提示', message = '您还没有输入账号！')
        elif (not out_account.isnumeric()) or (len(out_account) > 4):
            showwarning(title = '警告', message = '账号必须为四位以内的数字字符串！')
        elif len(out_password) == 0:
            showinfo(title = '提示', message = '您还没有输入密码！')
        elif len(out_password) > 12:
            showwarning(title = '警告', message = '密码长度至多为12！')
        else:
            re0 = client.register(client.sock_client, out_account, out_password, out_name)
            if re0 == 0:
                showwarning(title = '警告', message = '该账号已经被注册！')
            if re0 == 1: 
                showinfo(title = '提示', message = '注册成功！')
    def goback():
        root.destroy()
        login()

    #框架大小固定为400x360,设置为总是在屏幕中央的最上层显示,不可调整大小
    root = Tk()
    root.title('微信')
    root.iconbitmap('pics\\icon.ico')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 400
    height = 360
    pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 380, height = 340)
    labelframe = ttk.Labelframe(root, text = '注册')
    labelframe.place(x = 20, y = 20, width = 360, height = 240)

    Label(labelframe, text = '昵称', font = ('微软雅黑', 12)).place(x = 40, y = 20)
    in_name = StringVar()
    Entry(labelframe, textvariable = in_name, font = ('微软雅黑', 12)).place(x = 110, y = 20, width = 200, height = 30)

    Label(labelframe, text = '账号', font = ('微软雅黑', 12)).place(x = 40, y = 90)
    in_account = StringVar()
    Entry(labelframe, textvariable = in_account, font = ('微软雅黑', 12)).place(x = 110, y = 90, width = 200, height = 30)

    Label(labelframe, text = '密码', font = ('微软雅黑', 12)).place(x = 40, y = 160)
    in_password = StringVar()
    Entry(labelframe, textvariable = in_password, font = ('微软雅黑', 12)).place(x = 110, y = 160, width = 200, height = 30)
    
    Button(frame, text = '确认信息并注册', command = check, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 40, y = 270, width = 140, height = 50)
    Button(frame, text = '返回登录界面', command = goback, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 200, y = 270, width = 140, height = 50)
    
    root.mainloop()
########################################################################
def menu():
    '''启动菜单界面'''
    def add():
        root.destroy()
        add_friend()
    def logout():
        root.destroy()
        client.logout(client.sock_client)
        login()
    def gochat():
        l_target = l_lb.curselection()
        r_target = r_lb.curselection()
        if l_target:
            root.destroy()
            privatechat(list(client.mydict_friends.keys())[l_target[0]])
        elif r_target:
            root.destroy()
            chatroom(str(r_target[0]))
        else:
            showinfo(title = '提示', message = '您尚未选择好友或聊天室！')

    #框架大小固定为360x500,设置为总是在屏幕中央显示
    root = Tk()
    root.title('微信')
    root.iconbitmap('pics\\icon.ico')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 360
    height = 500
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    pos = width, height, (screenwidth - width) / 2, (screenheight - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 340, height = 480)
    up_labelframe = ttk.Labelframe(frame, text = '账户信息')
    up_labelframe.place(x = 10, y = 10, width = 200, height = 130)
    down_labelframe = ttk.Labelframe(frame, text = '开始聊天')
    down_labelframe.place(x = 10, y = 150, width = 320, height = 320)
    l_frame = ttk.Frame(down_labelframe)
    l_frame.place(x = 10, y = 40, width = 165, height = 250)
    r_frame = ttk.Frame(down_labelframe)
    r_frame.place(x = 185, y = 40, width = 125, height = 190)

    Label(up_labelframe, text = '账号：' + client.myaccount, font = ('微软雅黑', 12, 'bold')).place(x = 10, y = 10)
    Label(up_labelframe, text = '昵称：' + client.myname, font = ('微软雅黑', 12, 'bold')).place(x = 10, y = 40)
    Label(up_labelframe, text = '状态：在线', font = ('微软雅黑', 12, 'bold')).place(x = 10, y = 70)
    Button(frame, text = '添加好友', command = add, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 230, y = 30, width = 100, height = 40)
    Button(frame, text = '登出账号', command = logout, font = ('微软雅黑', 12, 'bold'), relief = GROOVE).place(x = 230, y = 80, width = 100, height = 40)
    Label(down_labelframe, text = '好友列表:', font = ('微软雅黑', 12)).place(x = 10, y = 10)
    Label(down_labelframe, text = '聊天室列表:', font = ('微软雅黑', 12)).place(x = 185, y = 10)

    l_sb = Scrollbar(l_frame)
    l_sb.pack(side = RIGHT,fill = BOTH)
    l_lb = Listbox(l_frame, selectmode = SINGLE, yscrollcommand = l_sb.set, font = ('微软雅黑', 10))
    l_lb.place(x = 0, y = 0, width = 150, height = 250)
    for i, item in enumerate(client.mydict_friends.keys()):
        l_lb.insert(i, '(' + item + ')' + client.mydict_friends[item])
    l_sb.configure(command = l_lb.yview)

    r_sb = Scrollbar(r_frame)
    r_sb.pack(side = RIGHT,fill = BOTH)
    r_lb = Listbox(r_frame, selectmode = SINGLE, yscrollcommand = r_sb.set, font = ('微软雅黑', 10))
    r_lb.place(x = 0, y = 0, width = 110, height = 190)
    chatrooms = []
    for x in list(client.dict_chatrooms.values()):
        chatrooms.append(x[1])

    for i, item in enumerate(chatrooms):
        r_lb.insert(i, chatrooms[i])
    r_sb.configure(command = r_lb.yview)

    Button(down_labelframe, text = '开始聊天', command = gochat, font = ('微软雅黑', 12, 'bold'), relief = RAISED).place(x = 190, y = 240, width = 100, height = 40)

    mainloop()
########################################################################
def add_friend():
    '''启动添加好友界面'''
    def search():
        friend_account = in_account.get()
        if len(friend_account) == 0:
            showinfo(title = '提示', message = '您还没有输入昵称！')
        elif len(friend_account) > 4:
            showwarning(title = '警告', message = '合法的账号至多有四位！')
        elif friend_account == client.myaccount:
            showwarning(title = '警告', message = '您不能添加自己为好友！')
        else:
            re0 = client.add_friend(client.sock_client, friend_account)
            if re0 == 0:
                showwarning(title = '警告', message = '添加好友关系失败！\n您可能已经添加过该好友！')
            if re0 == 1: 
                showinfo(title = '提示', message = '添加好友成功！')
            if re0 == -1:
                showwarning(title = '警告', message = '添加好友关系失败！\n您输入的账号不存在！')
    def goback():
        root.destroy()
        menu()

    #框架大小固定为260x200,设置为总是在屏幕中央的最上层显示,不可调整大小
    root = Tk()
    root.title('微信')
    root.iconbitmap('pics\\icon.ico')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 260
    height = 200
    pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 240, height = 180)
    labelframe = ttk.Labelframe(root, text = '寻找好友')
    labelframe.place(x = 20, y = 20, width = 220, height = 100)

    Label(labelframe, text = '请输入好友的账号：', font = ('微软雅黑', 10)).place(x = 10, y = 10)
    in_account = StringVar()
    Entry(labelframe, textvariable = in_account, font = ('微软雅黑', 12)).place(x = 10, y = 40, width = 200, height = 30)

    Button(frame, text = '添加好友', command = search, font = ('微软雅黑', 10, 'bold'), relief = GROOVE).place(x = 30, y = 130, width = 80, height = 30)
    Button(frame, text = '返回', command = goback, font = ('微软雅黑', 10, 'bold'), relief = GROOVE).place(x = 130, y = 130, width = 80, height = 30)
    
    root.mainloop()
########################################################################
def privatechat(account_friend:str):
    '''启动私聊界面'''
    client.buf = ''
    client.bufon = True
    client.position = account_friend
    client.isroom = False
    def recv_message():
        '''启用一个子线程，加载GUI缓冲到聊天框内，工作判定：bufon'''
        while client.bufon:
            time.sleep(0.05)
            if len(client.buf) > 0:
                print('收到一条消息！')
                print(client.buf)
                out_text.configure(state = NORMAL)
                out_text.insert(END, client.buf)
                out_text.configure(state = DISABLED)
                client.buf = ''
    
    def goback():
        root.destroy()
        client.buf = ''
        client.bufon = False
        client.position = ''
        client.isroom = False
        time.sleep(0.1)
        menu()
    def send():
        in_textcontent = in_text.get(1.0, END)
        in_text.delete(1.0, END)
        re0 = client.send_message(client.sock_client, account_friend, in_textcontent)
        if re0 == 0:
            showinfo(title = '提示', message = '好友当前不在线！')
    def sendimage():
        showinfo(title = '提示', message = '该功能尚未部署，请继续关注后续版本！')
    def gohistory():
        history = client.ask_privatehistory(client.sock_client, client.position)
        showhistory(history)

    #框架大小固定为480x440,设置为总是在屏幕中央的最上层显示,不可调整大小
    root = Tk()
    root.title('微信')
    root.iconbitmap('pics\\icon.ico')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 480
    height = 440
    pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 460, height = 420)
    topframe = ttk.Frame(root, relief = 'groove')
    topframe.place(x = 10, y = 10, width = 460, height = 40)
    buttomframe = ttk.Frame(root, relief = 'groove')
    buttomframe.place(x = 10, y = 340, width = 460, height = 90)
    miniframe = ttk.Frame(root, relief = 'groove')
    miniframe.place(x = 300, y = 340, width = 170, height = 90)
    labelframe = ttk.Labelframe(root, text = '聊天框')
    labelframe.place(x = 20, y = 50, width = 440, height = 285)

    in_text = Text(buttomframe, font = ('微软雅黑', 10))
    in_text.place(x = 5, y = 5, width = 280, height = 80)
    out_text = Text(labelframe, font = ('微软雅黑', 12), state = DISABLED)
    out_text.place(x = 5, y = 5, width = 425, height = 250)

    Label(topframe, text = ('正在和 %s 聊天~' % client.mydict_friends[account_friend]), font = ('微软雅黑', 12, 'bold')).place(x = 100, y = 5)
    Label(topframe, text = ('私聊状态：安全'), font = ('微软雅黑', 12, 'bold')).place(x = 330, y = 5)

    Button(topframe, text = '返回大厅', command = goback, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 10, y = 5, width = 60, height = 30)
    Button(miniframe, text = '发送', command = send, font = ('微软雅黑', 14, 'bold'), relief = GROOVE).place(x = 10, y = 15, width = 80, height = 60)
    Button(miniframe, text = '发送图片', command = sendimage, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 95, y = 45, width = 70, height = 30)
    Button(miniframe, text = '查看聊天记录', command = gohistory, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 95, y = 15, width = 70, height = 30)
    
    threading.Thread(target = recv_message).start()
    root.mainloop()
########################################################################
def chatroom(roomid:str):
    '''启动聊天室界面'''
    temptuple = client.check_roominfo(client.sock_client, roomid)
    num = len(temptuple[0]) + 1
    cap = client.dict_chatrooms[roomid][0]
    if num > cap:
        showwarning(title = '警告', message = '聊天室已满！')
        print('聊天室已满！')
        menu()
    else:
        client.buf = ''
        client.bufon = True
        client.position = roomid
        client.isroom = True
        client.getin_chatroom(client.sock_client, roomid)
        def recv_message():
            '''启用一个子线程，加载GUI缓冲到聊天框内，工作判定：bufon'''
            while client.bufon:
                time.sleep(0.05)
                if len(client.buf) > 0:
                    print('收到一条消息！')
                    print(client.buf)
                    out_text.configure(state = NORMAL)
                    out_text.insert(END, client.buf)
                    out_text.configure(state = DISABLED)
                    client.buf = ''

        def goback():
            showinfo(title = '提示', message = '您已成功退出聊天室！')
            root.destroy()
            client.buf = ''
            client.bufon = False
            client.position = ''
            client.isroom = False
            client.getout_chatroom(client.sock_client, roomid)
            time.sleep(0.1)
            menu()
        def send():
            in_textcontent = in_text.get(1.0, END)
            in_text.delete(1.0, END)
            client.call_message(client.sock_client, roomid, in_textcontent)
        def sendimage():
            showinfo(title = '提示', message = '该功能尚未部署，请继续关注后续版本！')
        def gohistory():
            showhistory(client.ask_chatroomhistory(client.sock_client, client.position))
        def refresh():
            print('正在刷新聊天室成员信息...')
            temptuple = client.check_roominfo(client.sock_client, roomid)
            tt.configure(state = NORMAL)
            tt.delete('1.0','end')
            for account, name in zip(temptuple[0], temptuple[1]):
                tt.insert(END, '(' + account + ')' + name + '\n')
            tt.configure(state = DISABLED)

        #框架大小固定为480x440,设置为总是在屏幕中央的最上层显示,不可调整大小
        root = Tk()
        root.title('微信')
        root.iconbitmap('pics\\icon.ico')
        root.wm_attributes('-topmost', 1)
        root.resizable(False, False)
        width = 480
        height = 440
        pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
        root.geometry('%dx%d+%d+%d' % pos)

        frame = ttk.Frame(root, relief = 'groove')
        frame.place(x = 10, y = 10, width = 460, height = 420)
        topframe = ttk.Frame(root, relief = 'groove')
        topframe.place(x = 10, y = 10, width = 460, height = 40)
        buttomframe = ttk.Frame(root, relief = 'groove')
        buttomframe.place(x = 10, y = 340, width = 460, height = 90)
        miniframe = ttk.Frame(root, relief = 'groove')
        miniframe.place(x = 300, y = 340, width = 170, height = 90)
        labelframe = ttk.Labelframe(root, text = '聊天框')
        labelframe.place(x = 20, y = 50, width = 440, height = 285)

        in_text = Text(buttomframe, font = ('微软雅黑', 10))
        in_text.place(x = 5, y = 5, width = 280, height = 80)
        out_text = Text(labelframe, font = ('微软雅黑', 12), state = DISABLED)
        out_text.place(x = 5, y = 5, width = 325, height = 250)

        Label(topframe, text = ('正在 %s 中~' % client.dict_chatrooms[roomid][1]), font = ('微软雅黑', 12, 'bold')).place(x = 100, y = 5)
        Label(topframe, text = ('聊天室容量：%d' % (cap)), font = ('微软雅黑', 12, 'bold')).place(x = 300, y = 5)
        Label(labelframe, text = ('聊天室成员'), font = ('微软雅黑', 10, 'bold')).place(x = 340, y = 10)
        Button(labelframe, text = '刷新', command = refresh, font = ('微软雅黑', 10, 'bold'), relief = GROOVE).place(x = 345, y = 225, width = 60, height = 30)

        sb = Scrollbar(labelframe)
        sb.pack(side = RIGHT,fill = BOTH)
        tt = Text(labelframe, yscrollcommand = sb.set, font = ('微软雅黑', 8))
        tt.place(x = 335, y = 45, width = 80, height = 170)
        sb.configure(command = tt.yview)
        temptuple = client.check_roominfo(client.sock_client, roomid)
        for account, name in zip(temptuple[0], temptuple[1]):
            tt.insert(END, '(' + account + ')' + name + '\n')
        tt.configure(state = DISABLED)

        Button(topframe, text = '返回大厅', command = goback, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 10, y = 5, width = 60, height = 30)
        Button(miniframe, text = '发送', command = send, font = ('微软雅黑', 14, 'bold'), relief = GROOVE).place(x = 10, y = 15, width = 80, height = 60)
        Button(miniframe, text = '发送图片', command = sendimage, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 95, y = 45, width = 70, height = 30)
        Button(miniframe, text = '查看聊天记录', command = gohistory, font = ('微软雅黑', 8, 'bold'), relief = GROOVE).place(x = 95, y = 15, width = 70, height = 30)
        
        threading.Thread(target = recv_message).start()
        root.mainloop()
########################################################################
def showhistory(history:tuple):
    '''展示聊天记录'''
    #框架大小固定为300x360,设置为总是在屏幕中央的最上层显示,不可调整大小
    root = Tk()
    root.title('微信')
    root.wm_attributes('-topmost', 1)
    root.resizable(False, False)
    width = 300
    height = 360
    pos = width, height, (root.winfo_screenwidth() - width) / 2, (root.winfo_screenheight() - height) / 2
    root.geometry('%dx%d+%d+%d' % pos)

    frame = ttk.Frame(root, relief = 'groove')
    frame.place(x = 10, y = 10, width = 280, height = 340)
    topframe = ttk.Frame(root, relief = 'groove')
    topframe.place(x = 10, y = 10, width = 280, height = 40)
    mainframe = ttk.Frame(root)
    mainframe.place(x = 20, y = 60, width = 260, height = 280)

    Label(topframe, text = ('聊 天 记 录'), font = ('微软雅黑', 12, 'bold')).place(x = 100, y = 5)

    sb = Scrollbar(mainframe)
    sb.pack(side = RIGHT,fill = BOTH)
    tt = Text(mainframe, yscrollcommand = sb.set, font = ('微软雅黑', 10))
    tt.place(x = 0, y = 0, width = 240, height = 280)
    sb.configure(command = tt.yview)
    if len(history) != 0:
        timestamps = history[0]
        accounts = history[1]
        contents = history[2]
        for timestamp, account, content in zip(timestamps, accounts, contents):
            dtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            piece = '时间：%s\n发送者账号：%s\n消息内容：%s\n' % (dtime, account, content)
            tt.insert(END, piece)
    else:
        tt.insert(END, '没有聊天记录！')
    tt.configure(state = DISABLED)

    root.mainloop()
########################################################################
def neterror():
    '''弹窗，提示和服务器断开了连接'''
    showerror(title = '错误', message = '和服务器断开了连接！')
    print('和服务器断开了连接！')

if __name__ == '__main__':
    login()