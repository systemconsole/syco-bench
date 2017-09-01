# syco-bench
Benchmarking tool for linux and mysql.

CREDITS:
Partly based on https://github.com/tsuna/sysbench-tools


    # Firewall rule on mysql server
    iptables -A INPUT -p TCP -m multiport --dports 3306 -j ACCEPT
    /sbin/service iptables save


    # Create user and permissions
    # syco-bench.py is configured to use the following user, password and db
    CREATE USER 'sbtest'@'%' IDENTIFIED BY 'my-secret-pw';
    GRANT ALL PRIVILEGES ON sbtest.* TO 'sbtest'@'%';
    FLUSH PRIVILEGES;


Here is the settings that has been added to linux on mysql test servers.

    cat /proc/sys/net/ipv4/tcp_max_syn_backlog
    cat /proc/sys/net/core/somaxconn

    #echo "net.ipv4.tcp_max_syn_backlog=1024" >> /etc/sysctl.conf
    #echo 4096 > /proc/sys/net/ipv4/tcp_max_syn_backlog

    echo "net.core.somaxconn=1024" >> /etc/sysctl.conf
    echo 1024 > /proc/sys/net/core/somaxconn

    sysctl -w
    sysctl -p
