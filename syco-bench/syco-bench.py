#!/usr/bin/env python

import MySQLdb
import subprocess
import sqlite3
import json
from datetime import datetime


from utils import yamlstr2dict

# Constants / Settings
SQLLITE_DB_FILE = "syco-bench.db"

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
    print("---- return code")
    print(result.returncode)
    print("---- stdout")
    print(result.stdout)
    print("---- stderr")
    print(result.stderr)
    print("----")


def sysbench2dict(str):
    """Convert result from sysbench to dict."""
    return yamlstr2dict(str.decode("utf-8"), "SQL statistics:")

conn = c = None
def sqlite_connect():
    global conn, c
    if not conn or not c:
        conn = sqlite3.connect(SQLLITE_DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    return conn, c


def sqlite_prepare():
    conn, c = sqlite_connect()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    if c.fetchone()[0] == 0:
        # sysbench_oltp
        c.execute("""
        CREATE TABLE sysbench_oltp
        (
          id INTEGER PRIMARY KEY ASC, 
          command text, 
          result text,
          comment text,
          created text 
        )
        """)
        conn.commit()


def sqlite_select():
    conn, c = sqlite_connect()
    t = (1,)
    for row in c.execute("SELECT * FROM sysbench_oltp WHERE 1=?", t):
        print(row['id'])
        print(row['command'])
        print(row['result'])
        print(row['comment'])
        print(row['created'])


def sqlite_store_sysbench_oltp(command, result, comment):
    """Store sysbench result to sqllite database."""
    created = str(datetime.now())
    j = json.dumps(result, sort_keys=True, indent=4)
    conn, c = sqlite_connect()
    c.execute("""
    INSERT INTO sysbench_oltp
      (command, result, comment, created) 
    VALUES
      (?, ?, ?, ?)
    """, (command, j, comment, created))
    conn.commit()


#prepare()
#run_rw()


d = sysbench2dict(
    b'sysbench 1.0.8 (using bundled LuaJIT 2.1.0-beta2)\n\nRunning the test with following options:\nNumber of threads: 1\nReport intermediate results every 1 second(s)\nInitializing random number generator from current time\n\n\nInitializing worker threads...\n\nThreads started!\n\n[ 1s ] thds: 1 tps: 31.88 qps: 656.60 (r/w/o: 460.32/131.52/64.76) lat (ms,95%): 37.56 err/s: 0.00 reconn/s: 0.00\n[ 2s ] thds: 1 tps: 36.04 qps: 703.85 (r/w/o: 491.59/140.17/72.09) lat (ms,95%): 35.59 err/s: 0.00 reconn/s: 0.00\nSQL statistics:\n    queries performed:\n        read:                            966\n        write:                           276\n        other:                           138\n        total:                           1380\n    transactions:                        69     (33.99 per sec.)\n    queries:                             1380   (679.75 per sec.)\n    ignored errors:                      0      (0.00 per sec.)\n    reconnects:                          0      (0.00 per sec.)\n\nGeneral statistics:\n    total time:                          2.0286s\n    total number of events:              69\n\nLatency (ms):\n         min:                                 21.14\n         avg:                                 29.38\n         max:                                 66.43\n         95th percentile:                     38.25\n         sum:                               2027.25\n\nThreads fairness:\n    events (avg/stddev):           69.0000/0.00\n    execution time (avg/stddev):   2.0272/0.00\n\n'
)
cmd ="ls -all"
sqlite_prepare()
sqlite_store_sysbench_oltp(cmd, d, "This is the comment")
sqlite_select()
print("END")
