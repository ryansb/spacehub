#!/bin/bash


# turn off iptables, amazon does firewall things for us
service iptables off
chkconfig iptables off

# Upgrade and install misc dependancies
yum upgrade -y
yum install -y git python-devel cmake make gcc openssl openssl-dev zlib zlib-devel libevent-devel libevent

# install pi
easy_install pip

# Install libgit2
git clone git://github.com/libgit2/libgit2.git
cd libgit2
mkdir build
cd build
cmake ..
cmake --build .
make
make install

# setup spacehub user
adduser spacehub

# Install spacehub
cd /home/spacehub

if [ -f "./spacehub"]
then
    su spacehub -c "git update"
else
    su spacehub -c "git clone git://github.com/ryansb/spacehub.git"
fi

cd spacehub
git checkout feature/aws
python /home/spacehub/spacehub/setup.py install

# Install init script
echo '#!/bin/sh
. /etc/rc.d/init.d/functions

exec=pserve
prog=spacehub
config=/home/spacehub/spacehub/production.ini
runas=spacehub
pidfile=/home/spacehub/spacehub.pid
logfile=/home/spacehub/spacehub.log


start() {
    echo "Starting $prog: "
    su $runas -c "$exec $config start --pid-file $pidfile --log-file $logfile"
    retval=$?
    echo 
    [ $retval -eq 0 ] && touch $pidfile
    return $retval
}

stop() {
    echo -n $"Stopping $prog: "
    su $runas -c "$exec $config stop --pid-file $pidfile"
    retval=$?
    echo
    [ $retval -eq 0 ] && rm -f $pidfile
    return $retval
}

restart() {
    stop
    start
}

rh_status() {
    su $runas -c "$exec $config --status"
}

rh_status_q() {
    rh_status > /dev/null 2>&1
}

case "$1" in
start)
    rh_status_q && exit 0
    $1
    ;;
stop)
    rh_status_q || exit 0
    $1
    ;;
restart)
    $1
    ;;
status)
    rh_status
    ;;
*)
    echo $"Usage: $0 {start|stop|status|restart}"
    exit 2
esac
exit $?
' > /etc/init.d/spacehub
chmod +x /etc/init.d/spacehub

