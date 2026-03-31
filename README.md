# Pychat

基于 TCP socket 的多人聊天室系统，清华大学谌卫军老师「Python 程序设计」课程大作业。

## 功能

- 账号注册与登录，支持重复登录检测
- 好友管理：添加好友、查看好友列表
- 好友私聊：实时一对一消息收发
- 聊天室：13 个预设聊天室（5–30 人容量），支持多人同时在线
- 聊天记录：私聊与聊天室的历史消息均可查看
- 数据持久化：用户信息、好友关系、聊天记录存储于 SQLite 数据库

## 技术栈

| 类别 | 技术 |
|------|------|
| 网络通信 | TCP socket |
| 图形界面 | tkinter / ttk |
| 数据库 | SQLite3 |
| 并发 | threading |

## 架构

采用客户端-服务器架构。每个客户端与服务器建立两条 TCP 连接：

- **主连接**：发送请求、接收响应
- **后台连接**：异步接收其他用户发来的消息

客户端与服务器通过自定义指令码协议通信（如 `__login__`、`__chat__`、`__broadcast__` 等），服务端为每个连接分配独立线程处理请求。

![运行结构图](docs/pics/运行结构图.png)

## 项目结构

```
Pychat/
├── server/
│   ├── main.py          # 服务端入口
│   ├── server.py        # 服务端核心逻辑（12 个接口）
│   ├── database.py      # 数据库操作层（9 个接口）
│   └── data/
│       ├── Info.db      # 账户、好友、聊天室信息
│       └── History.db   # 聊天记录
├── client/
│   ├── main.py          # 客户端入口
│   ├── client.py        # 客户端核心逻辑（12 个接口）
│   ├── GUI_framework.py # 图形界面框架（8 个窗口）
│   └── pics/
│       └── icon.ico
└── docs/
    ├── report.md        # 实验报告（Markdown）
    ├── report.pdf       # 实验报告（PDF）
    └── pics/            # 界面截图
```

## 运行方式

### 启动服务端

```bash
cd server
python main.py
```

服务端默认监听 `localhost:49152`，最大容纳 256 个并发连接。

### 启动客户端

```bash
cd client
python main.py
```

可同时启动多个客户端实例进行测试。

### 预置账号

管理员账号 `10086`，密码 `admin`。也可自行注册新账号（纯数字，不超过 4 位）。

## 截图

<details>
<summary>点击展开截图</summary>

**登录界面**

![登录界面](docs/pics/登录界面.png)

**账号注册**

![账号注册](docs/pics/账号注册.png)

**聊天目录**

![聊天目录](docs/pics/聊天目录.png)

**好友私聊**

![好友私聊](docs/pics/好友私聊.png)

**聊天室聊天**

![聊天室聊天](docs/pics/聊天室聊天.png)

**查看聊天记录**

![查看聊天记录](docs/pics/查看聊天记录.png)

</details>
