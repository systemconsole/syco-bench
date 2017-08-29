#!/usr/bin/env python

import MySQLdb
db=MySQLdb.connect(host="syco-mariadb", passwd="my-secret-pw")
c=db.cursor()
c.execute("""create or replace database thangs""")

db=MySQLdb.connect(host="syco-mariadb", passwd="my-secret-pw", db="thangs")
c=db.cursor()

c.execute("""
create table if not exists test (
  a bigint auto_increment primary key,
  name varchar(128) charset utf8,
  key name (name(32))
) engine=InnoDB default charset latin1;
""")

c.execute("""insert into test values(NULL, "cow")""")

x = c.execute("""SELECT a, name FROM test""")
print(x)
print(c.fetchone())
print("Yes")