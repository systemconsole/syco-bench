#!/usr/bin/env python

import MySQLdb
import subprocess
import sqlite3

def mysql_prepare():
    db=MySQLdb.connect(host="syco-mariadb", passwd="my-secret-pw")
    c=db.cursor()
    c.execute("""create or replace database sbtest""")

    db=MySQLdb.connect(host="syco-mariadb", passwd="my-secret-pw", db="sbtest")
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


def prepare():
    cmd = """
    sysbench \
      --db-driver=mysql \
      --mysql-host=syco-mariadb \
      --mysql-password=my-secret-pw \
      --oltp-table-size=4000 \
      --oltp-tables-count=2 \
      --mysql-table-engine=InnoDB \
      --mysql-user=root \
      {TEST_DIR}/oltp.lua \
      prepare
    """
    sysbench(cmd)


def run_rw():
    cmd = """
    sysbench \
        --db-driver=mysql \
        --mysql-host=syco-mariadb \
        --mysql-user=root \
        --mysql-password=my-secret-pw \
        --max-requests=0 \
        --time=2 \
        --report-interval=1 \
        --oltp-tables-count=2 \
        --oltp-table-size=4000 \
        --threads={THREAD} \
        {TEST_DIR}/oltp.lua \
        run
    """
    sysbench(cmd)


def sysbench(cmd):
    TEST_DIR="/usr/share/sysbench/tests/include/oltp_legacy/"
    THREAD=1
    cmd = cmd.format(TEST_DIR=TEST_DIR, THREAD=THREAD)
    print(cmd)
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    print(result.returncode)
    print(result.stdout)
    print(result.stderr)



def db_prepare():
    conn = sqlite3.connect("syco-bench.db")
    c = conn.cursor()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    if c.fetchone()[0] == 0:
        # Create table
        c.execute("""CREATE TABLE stocks
                     (date text, trans text, symbol text, qty real, price real)""")

        # Insert a row of data
        c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
    conn.close()

def db_select():
    conn = sqlite3.connect("syco-bench.db")
    c = conn.cursor()
    t = ("RHAT",)
    c.execute("SELECT * FROM stocks WHERE symbol=?", t)
    print(c.fetchone())

#prepare()
#run_rw()
db_prepare()
db_select()
print("END")
