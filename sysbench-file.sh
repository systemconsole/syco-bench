# Benchmark File IO
rm -rf /var/bench
mkdir -p /var/bench
cd /var/bench
sysbench --file-total-size=50G fileio prepare
sysbench --file-total-size=50G --file-test-mode=rndrw --time=300 --max-requests=0 fileio run
sysbench --file-total-size=150G fileio cleanup