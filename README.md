# status_checkout
An automated script that collects server data and displays it on a webpage.
这是一个监控多台服务器状态的简单脚本，分为server端和agent端
server端负责接收agent端的报告信息，并显示在web前端。agent端则负责收集服务器的系统状态，并发送给server
目前支持收集并展示的数据：cpu使用情况、ram使用情况和最近的一次更新时间
目前项目处于基础阶段，还未考虑安全设置等等。
欢迎fork和pull request！

