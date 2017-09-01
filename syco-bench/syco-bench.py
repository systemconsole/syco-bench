#!/usr/bin/env python
"""
Benchmark mysql database with sysbench and displays result in syco-bench.html.

The script creates an SQLite database (syco-bench.db) with all data returned
by sysbench. The data is than calculated into a json file (syco-bench.js)
with graph readable data. That files is viewable through an html file
(syco-bench.html).


Threads in the code is equal to number of connections

"""

import MySQLdb
import subprocess
import sqlite3
import simplejson as json
import sys
import argparse
from datetime import datetime
from decimal import *

from utils import yamlstr2dict

# SQLite settings
SQLLITE_DB_FILE = "syco-bench.db"


# Mysql settings
MYSQL_HOST="10.101.11.91"
MYSQL_USER="sbtest"
MYSQL_PASSWORD="my-secret-pw"
MYSQL_DB="sbtest"


# Print information to stdout
VERBOSE=True


# Folder where sysbench tests are stored.
TEST_DIR="/usr/share/sysbench/tests/include/oltp_legacy"


# Tests for result.js
TESTS = {
    "rndrw": "Random reads/writes"
}


# Metrics for result.js
METRICS = {
    "total_num_events": "Total number of events",

    "req_95p": "95th percentile latency",
    "req_avg": "Avg. latency",
    "req_max": "Max. latency",
    "req_min": "Min. latency",

    "nother": "Queries other",
    "nread": "Queries read",
    "ntotal": "Queries total",
    "nwrite": "Queries write",
    "nqueries": "Queries/s",
    "ierrors": "Ignored errors/s",

    "transactions": "Transactions/s",

    "tevents": "Thread events"
}


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
    """Execute linux cmd sysbench"""
    cmd = cmd.format(
        MYSQL_HOST=MYSQL_HOST,
        MYSQL_USER=MYSQL_USER,
        MYSQL_PASSWORD=MYSQL_PASSWORD,
        TEST_DIR=TEST_DIR,
        THREADS=threads
    )
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    if result.returncode:
        printv("error")
        if "FATAL: error 1040: Too many connections" in str(result.stdout):
            raise MySQLdb.OperationalError(1040, "Too many connections")
        else:
            printv("---- cmd")
            printv(cmd.strip())
            printv("---- return code")
            printv(result.returncode)
            printv("---- stdout")
            printv(result.stdout)
            printv("---- stderr")
            printv(result.stderr)
            printv("----")
    return result.stdout


def sysbench_oltp_prepare():
    """Prepare the sysbench database"""
    printv("* sysbench mysql oltp prepare")
    cmd = """
    sysbench \
      --db-driver=mysql \
      --mysql-host={MYSQL_HOST} \
      --mysql-user={MYSQL_USER} \
      --mysql-password={MYSQL_PASSWORD} \
      --mysql-table-engine=InnoDB \
      --oltp-table-size=800000 \
      --oltp-tables-count=40 \
      {TEST_DIR}/oltp.lua \
      prepare
    """
    return cmd, sysbench(cmd, None)


def sysbench_oltp_rw(threads):
    """Run oltp read/write sysbench test."""
    printv("* sysbench mysql oltp run threads %s." % threads)
    cmd = """
    sysbench \
        --db-driver=mysql \
        --mysql-host={MYSQL_HOST} \
        --mysql-user={MYSQL_USER} \
        --mysql-password={MYSQL_PASSWORD} \
        --mysql-table-engine=InnoDB \
        --oltp-table-size=800000 \
        --oltp-tables-count=40 \
        --max-requests=0 \
        --time=30 \
        --warmup-time=2 \
        --report-interval=5 \
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
        sqlite_prepare()
    return conn, c


def sqlite_prepare():
    """Create the database if it doesn't exist."""
    conn, c = sqlite_connect()
    c.execute("SELECT count(*) FROM sqlite_master WHERE type='table'")
    if c.fetchone()[0] == 0:
        printv("* SQLite create table sysbench_oltp.")
        # TABLE: sysbench_oltp
        c.execute("""
        CREATE TABLE sysbench_oltp
        (
          id INTEGER PRIMARY KEY ASC, 
          command text, 
          result text,
          config text,
          test_mode text,
          threads INTEGER ,
          created text 
        )
        """)
        conn.commit()


def sqlite_store_sysbench_oltp(command, result, config, test_mode, threads):
    """Store sysbench json result in sqllite database."""
    printv("* SQLite store to sysbench_oltp.")
    command = ' '.join(command.strip().split())
    j = json.dumps(result, sort_keys=True, indent=4)
    created = str(datetime.now())

    conn, c = sqlite_connect()
    c.execute("""
    INSERT INTO sysbench_oltp
      (command, result, config, test_mode, threads, created) 
    VALUES
      (?, ?, ?, ?, ?, ?)
    """, (command, j, config, test_mode, threads, created))
    conn.commit()


def copy_graf_data(row, data):
    """Retrive all metrics"""
    d = json.loads(row['result'])
    data["total_num_events"].setdefault(row['threads'], []).append(
        d["General statistics"]["total number of events"]
    )

    # 95th percentile latency
    data["req_95p"].setdefault(row['threads'], []).append(
        d["Latency (ms)"]["95th percentile"]
    )

    # Avg. latency
    data["req_avg"].setdefault(row['threads'], []).append(
        d["Latency (ms)"]["avg"]
    )

    # Max. latency
    data["req_max"].setdefault(row['threads'], []).append(
        d["Latency (ms)"]["max"]
    )

    # "Min. latency
    data["req_min"].setdefault(row['threads'], []).append(
        d["Latency (ms)"]["min"]
    )

    # Queries/s
    data["nqueries"].setdefault(row['threads'], []).append(
        per_sec_cut(d["SQL statistics"]["queries"])
    )

    # Queries/s
    data["ierrors"].setdefault(row['threads'], []).append(
        per_sec_cut(d["SQL statistics"]["ignored errors"])
    )

    # Queries other
    data["nother"].setdefault(row['threads'], []).append(
        d["SQL statistics"]["queries performed"]["other"]
    )

    # Queries read
    data["nread"].setdefault(row['threads'], []).append(
        d["SQL statistics"]["queries performed"]["read"]
    )

    # Queries total
    data["ntotal"].setdefault(row['threads'], []).append(
        d["SQL statistics"]["queries performed"]["total"]
    )

    # Queries write
    data["nwrite"].setdefault(row['threads'], []).append(
        d["SQL statistics"]["queries performed"]["write"]
    )

    # Transactions/s",
    data["transactions"].setdefault(row['threads'], []).append(
        per_sec_cut(d["SQL statistics"]["transactions"])
    )

    # Thread events
    #data["tevents"].setdefault(row['threads'], []).append(
    #    d["Threads fairness"]["events (avg/stddev)"]
    #)

    return data


def build_graf_data():
    """Return all sysbench_oltp results."""
    printv("* Calculate graf data for result.js")
    conn, c = sqlite_connect()
    c.execute("SELECT count(*) as num_of_rows FROM sysbench_oltp")
    row = c.fetchone()
    printv("* num_of_rows: %s" % row["num_of_rows"])

    #
    results = {}
    for row in c.execute("SELECT * FROM sysbench_oltp"):
        printv("* Calculate results for thread %s." % row['threads'])

        # Set defaults
        results.setdefault(row["config"], {}).setdefault(row["test_mode"],
                                                         {})
        if "results" in results[row["config"]][row["test_mode"]]:
            data = results[row["config"]][row["test_mode"]]["results"]
        else:
            data = dict((metric, {}) for metric in METRICS)

        try:
            data = copy_graf_data(row, data)
        except TypeError as e:
            printv("Error:%s" % e)

        results[row['config']][row['test_mode']]["results"] = data

    calculate_averages(results)
    return results


def per_sec_cut(s):
    """Return the per sec value from a string
    "0      (0.090 per sec.)" will return "0.090"
    """
    return Decimal(s[s.find("(") + 1:s.find("per sec")].strip())


def calculate_averages(config2results):
    """Calculate the averages from results."""
    printv("* Calculate averages")
    for config, results in config2results.items():
        for test_mode, data in results.items():
            data["averages"] = dict(
                (metric, [[num_threads, int(sum(vs) / len(vs))] for num_threads, vs in sorted(values.items())])
                for metric, values in data["results"].items()
            )


def create_result_file(results):
    """Create the result.js file used by syco-bench.html containing graf data"""
    printv("* Create result.js")
    with open("syco-bench.js", "w") as f:
        f.write("TESTS = ");
        json.dump(TESTS, f, indent=2)
        f.write(";\nMETRICS = ");
        json.dump(METRICS, f, indent=2)
        f.write("\nresults = ");
        json.dump(results, f, indent=2, use_decimal=True)
        f.write(";")


def view_db_data():
    """Print output from database."""
    conn, c = sqlite_connect()

    for row in c.execute("SELECT * FROM sysbench_oltp"):
        print("Threads: %s" % row['threads'])
        print(row['result'])
        print("-"*80)


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark mysql database with sysbench and '
                    'displays result in syco-bench.html.'
    )
    parser.add_argument("--prepare", help="prepare the server benchmark",
                        action = "store_true")
    parser.add_argument("--bench", help="benchmark the server",
                        action = "store_true")
    parser.add_argument("--build", help="build result.js",
                        action = "store_true")
    parser.add_argument("--view", help="view SQLite contents",
                        action="store_true")
    args = parser.parse_args()
    if args.prepare:
        prepare()
    elif args.bench:
        benchmark()
    elif args.view:
        view()
    elif args.build:
        buildresult()
    else:
        parser.print_help()


def prepare():
    """Prepare database before benchmark test"""
    mysql_prepare()
    sysbench_oltp_prepare()


def benchmark():
    # Run tests against mysql
    for threads in [1024, 768, 512, 256, 128, 64, 32, 16, 8 ,4, 2, 1]:
        try:
            cmd, result = sysbench_oltp_rw(threads)
            d = sysbench2dict(result)
            sqlite_store_sysbench_oltp(cmd, d, "mariadb", "rndrw", threads)
        except MySQLdb.OperationalError as e:
            if e.args[0] == 1040:
                printv(e.args[1])
                printv("* Further number of threads will probably also crach.")
                break

    buildresult()


def buildresult():
    results = build_graf_data()
    create_result_file(results)


def view():
    view_db_data()

def test_conn():
    db =dict()
    c= dict()
    for x in range(1025):
        print(x)
        db[x]=MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD)
        c[x]=db[x].cursor()
        c[x].execute("""select True""")

    sys.exit()

if __name__ == "__main__":
  sys.exit(main())