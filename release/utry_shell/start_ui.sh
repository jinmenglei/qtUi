#! /bin/sh
source /opt/ros/kinetic/setup.sh
RET=`ps -ef|grep -v grep|grep ui_main`
if [ "" == "$RET" ]
then
   echo "start uio"
   cd /home/utry/release/bin/ui
   ./launchStart &
   ./ui_main &
fi
