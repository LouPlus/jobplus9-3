--  方便大伙调试时频繁创建数据库
--  执行方法:  mysql -u root -p'root' < create_db.sql

--  先删库
drop database  if exists `jobplus`;
--  再建库
create database `jobplus` default character set utf8;

