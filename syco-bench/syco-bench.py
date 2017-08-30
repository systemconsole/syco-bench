#!/usr/bin/env python

import MySQLdb
import subprocess
import sqlite3
import json
import sys
from datetime import datetime

from utils import yamlstr2dict

# Constants / Settings
SQLLITE_DB_FILE = "syco-bench.db"

MYSQL_HOST="syco-mariadb"
MYSQL_USER="root"
MYSQL_PASSWORD="my-secret-pw"
MYSQL_DB="sbtest"

# Print information to stdout
VERBOSE=True

# Folder where sysbench tests are stored.
TEST_DIR="/usr/share/sysbench/tests/include/oltp_legacy"

def printv(txt):
    """Print when verbose output is configured."""
    if VERBOSE:
        print(txt)

def mysql_prepare():
    """Create database for sysbench tests."""
    printv("* Mysql prepare.")
    db=MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
    c=db.cursor()
    c.execute("""create or replace database %s""" % MYSQL_DB)


def sysbench(cmd, threads):
    cmd = cmd.format(
        MYSQL_HOST=MYSQL_HOST,
        MYSQL_USER=MYSQL_USER,
        MYSQL_PASSWORD=MYSQL_PASSWORD,
        TEST_DIR=TEST_DIR,
        THREADS=threads
    )
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    if result.returncode:
        print("---- cmd")
        print(cmd.strip())
        print("---- return code")
        print(result.returncode)
        print("---- stdout")
        print(result.stdout)
        print("---- stderr")
        print(result.stderr)
        print("----")
        exit(1)
    return result.stdout


def sysbench_oltp_prepare(threads):
    printv("* sysbench mysql oltp prepare threads %s." % threads)
    cmd = """
    sysbench \
      --db-driver=mysql \
      --mysql-host={MYSQL_HOST} \
      --mysql-user={MYSQL_USER} \
      --mysql-password={MYSQL_PASSWORD} \
      --mysql-table-engine=InnoDB \
      --oltp-table-size=4000 \
      --oltp-tables-count=2 \
      {TEST_DIR}/oltp.lua \
      prepare
    """
    return cmd, sysbench(cmd, threads)


def sysbench_oltp_rw(threads):
    printv("* sysbench mysql oltp run threads %s." % threads)
    cmd = """
    sysbench \
        --db-driver=mysql \
        --mysql-host={MYSQL_HOST} \
        --mysql-user={MYSQL_USER} \
        --mysql-password={MYSQL_PASSWORD} \
        --mysql-table-engine=InnoDB \
        --oltp-table-size=4000 \
        --oltp-tables-count=2 \
        --max-requests=0 \
        --time=2 \
        --report-interval=0 \
        --threads={THREADS} \
        {TEST_DIR}/oltp.lua \
        run
    """
    return cmd, sysbench(cmd, threads)


def sysbench2dict(str):
    """Convert result from sysbench to dict."""
    return yamlstr2dict(str.decode("utf-8"), "SQL statistics:")


conn = c = None
def sqlite_connect():
    """Create or reuse an sqlite connection and cursor."""
    global conn, c
    if not conn or not c:
        printv("* SQLite connect to %s." % SQLLITE_DB_FILE)
        conn = sqlite3.connect(SQLLITE_DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
    return conn, c


def sqlite_prepare():
    """Create the database if it doesn't exist."""
    conn, c = sqlite_connect()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    if c.fetchone()[0] == 0:
        printv("* SQLite create table sysbench_oltp.")
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


def sqlite_store_sysbench_oltp(command, result, comment):
    """Store sysbench json result in sqllite database."""
    printv("* SQLite store to sysbench_oltp.")
    command = ' '.join(command.strip().split())
    j = json.dumps(result, sort_keys=True, indent=4)
    created = str(datetime.now())

    conn, c = sqlite_connect()
    c.execute("""
    INSERT INTO sysbench_oltp
      (command, result, comment, created) 
    VALUES
      (?, ?, ?, ?)
    """, (command, j, comment, created))
    conn.commit()


def sqlite_select():
    """Return all sysbench_oltp results."""
    conn, c = sqlite_connect()
    t = (1,)
    for row in c.execute("SELECT * FROM sysbench_oltp WHERE 1=?", t):
        print(row['id'])
        print(row['command'])
        print(row['result'])
        print(row['comment'])
        print(row['created'])


def main():
    # Prepare environment.
    sqlite_prepare()
    mysql_prepare()
    sysbench_oltp_prepare(1)

    # Run tests against mysql
    cmd, result = sysbench_oltp_rw(1)
    d = sysbench2dict(result)
    sqlite_store_sysbench_oltp(cmd, d, "This is the comment")

    #sqlite_select()

if __name__ == "__main__":
  sys.exit(main())