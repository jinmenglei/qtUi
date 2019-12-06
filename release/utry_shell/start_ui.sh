#! /bin/sh
# shellcheck disable=SC2039
source /opt/ros/kinetic/setup.sh
source /home/utry/catkin_ws/devel/setup.bash
RET=`ps -ef|grep -v grep|grep ui_main`
if [ "" == "$RET" ]
then
   echo "start uio"
   cd /home/utry/release/bin/ui
#   ./launchStart &
   ./ui_main &
fi
