# syco-bench
Benchmarking tool for linux and mysql.

CREDITS:
Partly based on https://github.com/tsuna/sysbench-tools


    # Firewall rule on mysql server
    iptables -I INPUT -p TCP -m multiport --dports 3306 -j ACCEPT
    /sbin/service iptables save


    # Create user and permissions
    # syco-bench.py is configured to use the following user, password and db
    CREATE USER 'sbtest'@'%' IDENTIFIED BY 'my-secret-pw';
    GRANT ALL PRIVILEGES ON sbtest.* TO 'sbtest'@'%';
    FLUSH PRIVILEGES;


Here is the settings that has been added to linux on mysql test servers.

    cat /proc/sys/net/ipv4/tcp_max_syn_backlog
    cat /proc/sys/net/core/somaxconn

    echo "net.ipv4.tcp_max_syn_backlog=4096" >> /etc/sysctl.conf
    echo 4096 > /proc/sys/net/ipv4/tcp_max_syn_backlog

    echo "net.core.somaxconn=1024" >> /etc/sysctl.conf
    echo 1024 > /proc/sys/net/core/somaxconn

    sysctl -w
    sysctl -p


# Install Centos 7 as a KVM Guest

    lvcreate -L 28G VolGroup00 -ndanlin-sycobench7

    virt-install -d --connect qemu:///system --name danlin-sycobench7 --ram 4096 --vcpus=4,maxvcpus=8 --vnc --noautoconsole --hvm --virt-type=kvm --autostart --disk path=/dev/mapper/VolGroup00-danlin--sycobench7 --os-variant=rhel7 --arch x86_64 --network bridge:br1 --location /var/lib/libvirt/qemu/CentOS-7-x86_64-DVD-1611.iso

    virsh autostart danlin-sycobench7
    virsh start danlin-sycobench7

    # Setup network on the server
    vi /etc/sysconfig/network-scripts/ifcfg-eth0
    BOOTPROTO=static
    IPADDR=10.101.11.71
    NETMASK=255.0.0.0
    GATEWAY=10.101.1.1
    ONBOOT=YES

    echo "nameserver 4.2.2.1" >> /etc/resolv.conf

    yum -y update


# Install Docker CE on Centos 7

    yum remove docker docker-common docker-selinux docker-engine
    yum install -y yum-utils device-mapper-persistent-data lvm2
    yum-config-manager --add-repo \
        https://download.docker.com/linux/centos/docker-ce.repo

    yum makecache fast
    yum list docker-ce.x86_64  --showduplicates | sort -r
    yum install docker-ce-17.06.2.ce-1.el7.centos

    systemctl start docker
    systemctl enable docker
    docker run hello-world

# Install EPEL and sysbench

    #wget http://mirror.nsc.liu.se/fedora-epel/7/x86_64/e/epel-release-7-10.noarch.rpm
    #rpm -ivh epel-release-7-10.noarch.rpm
    curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.rpm.sh | sudo bash
    yum -y install sysbench


# Mount

    mount /dev/VolGroup00/danlin-rentalfront-mysql-extra /var/lib/mysql
    mount -t tmpfs -o size=10240m tmpfs /var/lib/mysql/


Test network speed

# On server
iperf -s -p 3306

# On client
iperf -c 10.101.1.206 -t 20 -p 3306 -w 1k -P20

Guest 10.101.11.70 to Host 10.101.1.206  - 3.04 Gbits/sec
Guest 10.101.1.206 to Host 10.101.1.206  - 277 Mbits/sec



# Sysbench OLTP test
sysbench --db-driver=mysql --mysql-host=10.101.1.206 --mysql-user=sbtest --mysql-password=my-secret-pw --mysql-table-engine=InnoDB --oltp-table-size=800000 --oltp-tables-count=40 --max-requests=0 --time=30 --warmup-time=2 --report-interval=1 --threads=512 /usr/share/sysbench/tests/include/oltp_legacy/oltp.lua run
Guest 10.101.11.71 to Host 10.101.1.206 Queries   701 818 ( 23 165.13 per sec.) (Guest has centos 7)
Guest 10.101.11.70 to Host 10.101.1.206 Queries   769 845 ( 25 356.10 per sec.)
Guest 10.101.11.70 to Host 10.101.1.206 Queries   811 519 ( 26 745.45 per sec.) No iptables
Guest 10.101.11.70 to Host 10.101.11.91 Queries   924 238 ( 29 709.02 per sec.)
Host  10.101.1.201 to Host 10.101.1.206 Queries 1 694 485 ( 55 735.29 per sec.)
Guest 10.101.11.91 to Host 10.101.11.91 Queries 1 938 650 ( 63 888.29 per sec.)
Host  10.101.1.206 to Host 10.101.1.206 Queries 2 845 633  (94 512.60 per sec.) No Iptables
Host  10.101.1.206 to Host 10.101.1.206 Queries 5 020 682 (167 088.18 per sec.) Ram Disk (Probably fast because not battling for disk io with other processes)
Host  10.101.1.206 to Host 10.101.1.206 Queries 5 568 969 (185 291.52 per sec.) Ram Disk No iptables

# Sysbench Memory test
http://blog.siphos.be/2013/04/comparing-performance-with-sysbench-part-3/

sysbench --test=memory --memory-total-size=10G run
10.101.11.70 (1043.57 MiB/sec)
10.101.1.206 (3153.98 MiB/sec)


sysbench --test=memory --memory-block-size=1K --memory-scope=global --memory-total-size=100G --memory-oper=read run
10.101.11.70 - transferred (1207.69 MiB/sec) -- operations: (1 236 678.14 per second)
10.101.1.206 - transferred (4038.41 MiB/sec) -- operations: (4 135 336.34 per second)


sysbench --test=memory --memory-block-size=1K --memory-scope=global --memory-total-size=100G --memory-oper=write run
10.101.11.70 - transferred (1083.87 MiB/sec) -- operations (1 109 886.80 per second)
10.101.1.206 - transferred (3087.75 MiB/sec) -- operations (3 161 860.13 per second)


sysbench --test=threads --num-threads=1 --thread-yields=0 --max-requests=10000000 --thread-locks=1 run
10.101.11.70 - total time: 8.7552s
10.101.1.206 - total time: 2.5513s


sysbench --test=threads --threads=128 --max-time=10 run
10.101.11.70 - 27000
10.101.1.206 - 14184


sysbench --test=mutex --mutex-num=1 --mutex-locks=50000000 --mutex-loops=1 run
10.101.11.70 - total time: 1.5925s
10.101.1.206 - total time: 1.5318s

# Sysbench FileIO
sysbench --test=fileio --file-total-size=6G prepare
sysbench --test=fileio --file-total-size=6G --file-test-mode=rndrw --max-time=300 --max-requests=0 --file-extra-flags=direct run
sysbench --test=fileio --file-total-size=6G cleanup
10.101.11.70 - read, MiB / s: 3.11 written, MiB / s: 2.07
10.101.1.206 - read, MiB / s: 3.41 written, MiB / s: 2.28


