#! /bin/sh
# /etc/init.d/toulouseos 

### BEGIN INIT INFO
# Provides:          toulouseos
# Required-Start:    $remote_fs $syslog $time $all
# Required-Stop:     $remote_fs $syslog
# Default-Start:     3 4 5
# Default-Stop:      0 1 2 6
# Short-Description: Toulouse OS
# Description:       Toulouse OS start / stop a program at boot / shutdown.
### END INIT INFO

# If you want a command to always run, put it here

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting Toulouse OS"
    # run application you want to start
    python3 -u /home/pi/toulouseos/main.py | tee /home/pi/toulouseos/output.txt
    ;;
  stop)
    echo "Stopping Toulouse OS"
    # kill application you want to stop
    killall python3
    ;;
  *)
    echo "Usage: /etc/init.d/toulouseos {start|stop}"
    exit 1
    ;;
esac

exit 0