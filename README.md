# louplus3
LouPlus Team 3 https://www.shiyanlou.com/louplus/python

## Contributors

* [louplus](https://github.com/louplus)
* [Avery](https://github.com/wuqize)
* [rainbowjl](https://github.com/rainbowjlinux)
* [chase](https://github.com/goodwillchase)

## 运行前准备

1. 数据库
- 开发用数据库创建
```bash
# 创建数据库
$ mysql -uroot -p
$ CREATE DATABASE jobplus_dev;
# 创建用户并授权
$ CREATE USER 'jobplus'@'localhost' IDENTIFIED BY 'jobplus';
$ GRANT ALL PRIVILEGES ON jobplus_dev.* TO 'jobplus'@'localhost' IDENTIFIED BY 'jobplus' WITH GRANT OPTION;
$ FLUSH PRIVILEGES;
```
- 生产用数据库创建（待补充）
```bash
# 创建数据库
$ mysql -uroot -p
$ CREATE DATABASE jobplus;
```

- 测试用数据库创建
```bash
# 创建数据库
$ mysql -uroot -p
$ CREATE DATABASE jobplus_test;
# 用户授权
$ GRANT ALL PRIVILEGES ON jobplus_test.* TO 'jobplus'@'localhost' IDENTIFIED BY 'jobplus' WITH GRANT OPTION;
$ FLUSH PRIVILEGES;
```

2.设置环境
在 config.py 中设置 CURRENT_ENV
