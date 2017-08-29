# Prepare proxy server
/etc/squid/acl/domains_general
	# MariaDB
	downloads.mariadb.com

# Install MariaDB
yum -y update
curl -sS https://downloads.mariadb.com/MariaDB/mariadb_repo_setup | sudo bash
yum install MariaDB-server
service mysqld start
/usr/bin/mysql_secure_installation
#/usr/bin/mysqladmin -u root password 'new-password'



# Benchmark Cpu
# https://wiki.mikejung.biz/Sysbench

sysbench --test=cpu --cpu-max-prime=20000 run



# Benchmark File IO
rm -rf /var/bench
mkdir -p /var/bench
cd /var/bench
sysbench --file-total-size=50G fileio prepare
sysbench --file-total-size=50G --file-test-mode=rndrw --time=300 --max-requests=0 fileio run
sysbench --file-total-size=150G fileio cleanup