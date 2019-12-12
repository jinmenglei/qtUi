#! /bin/bash
# shellcheck disable=SC2039
source /opt/ros/kinetic/setup.sh
source /home/utry/catkin_ws/devel/setup.bash
RET=$(pgrep -f ui_main)
if [ "" == "$RET" ]
then
  {
    xset s 0
    xset s noblank
    xset -dpms
    sleep 2
#    xrandr --output HDMI1 --auto
    echo "start uio"
  } >> /tmp/start.log

  cd /home/utry/release/bin/ui
  #   ./launchStart &
  ./ui_main &

  if [ -f /home/utry/release/utry_shell/start_ini ]; then
    echo 'start test' >> /tmp/start.log
    cd /home/utry/release/utry_shell/
    ./start_test >> /tmp/start_ui.log &
  fi
fi
