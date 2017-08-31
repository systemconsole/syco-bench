# Benchark MariaDb
TEST_DIR=/usr/share/sysbench/tests/include/oltp_legacy/

NUM_THREADS="1 4 8 16 32 64 128"
SYSBENCH_TESTS="bulk_insert.lua \
delete.lua \
insert.lua \
oltp.lua \
oltp_simple.lua \
parallel_prepare.lua \
select.lua \
select_random_points.lua \
select_random_ranges.lua \
update_index.lua \
update_non_index.lua "

# Prepare database
sysbench \
  --db-driver=mysql \
  --mysql-host=syco-mariadb \
  --mysql-password=my-secret-pw \
  --oltp-table-size=4000 \
  --oltp-tables-count=2 \
  --mysql-table-engine=InnoDB \
  --mysql-user=root \
  ${TEST_DIR}/oltp.lua \
  prepare

for run in 1 2 3 ;do
    for thread in ${NUM_THREADS} ;do
        echo "Performing r/w test SQ-${thread}T-${run}"
        sysbench \
        --db-driver=mysql \
        --mysql-host=syco-mariadb \
        --mysql-user=root \
        --mysql-password=my-secret-pw \
        --max-requests=0 \
        --time=10 \
        --report-interval=1 \
        --oltp-tables-count=2 \
        --oltp-table-size=400000 \
        --threads=${thread} \
        ${TEST_DIR}/oltp.lua \
        run > /root/SQ-${thread}T-${run}
    done
done


# echo "Performing test RW-${thread}T-${run}"
# sysbench --test=fileio --file-total-size=4G --file-test-mode=rndwr --max-time=60 --max-requests=0 --file-block-size=4K --file-num=64 --num-threads=${thread} run > /root/RW-${thread}T-${run}

# echo "Performing test RR-${thread}T-${run}"
# sysbench --test=fileio --file-total-size=4G --file-test-mode=rndrd --max-time=60 --max-requests=0 --file-block-size=4K --file-num=64 --num-threads=${thread} run > /root/RR-${thread}T-${run}

# Make it read only
#    echo "Performing read test SQ-${thread}T-${run}"
#    --oltp-read-only=on \
#    --oltp-skip-trx=on  \
