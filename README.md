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


# 使用flask-migrate管理数据库
在项目根目录下执行命令：

```
$flask db init

$flask db migrate -m 'init database'

$flask db upgrade
```
目前仅创建了 user、company、job三个表

可进入mysql，执行以下命令查看是否创建成功

```
mysql> use jobplus_dev;
mysql> show create table user;
mysql> show create table company;
mysql> show create table job;
```
