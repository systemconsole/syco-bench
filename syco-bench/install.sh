#
# Installing on syco guest.
#

# Install apache
yum install -y httpd
httpd start
chkconfig start httpd
chkconfig httpd on

iptables -A INPUT -p tcp -m tcp --dport 80 -j ACCEPT
setenforce 0

cat <<EOF >> /etc/httpd/conf/httpd.conf
Alias "/syco-bench.html" "/usr/src/syco-bench/syco-bench.html"
Alias "/syco-bench.js" "/usr/src/syco-bench/syco-bench.js"
Alias "/jquery.flot.js" "/usr/src/syco-bench/jquery.flot.js"
EOF

service httpd restart