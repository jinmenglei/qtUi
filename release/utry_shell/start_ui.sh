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
  } > /tmp/start.log

  cd /home/utry/release/bin/ui
  #   ./launchStart &
  ./ui_main >> /tmp/start.log &

  if [ -f /home/utry/release/utry_shell/start_ini ] && [ -f /home/utry/release/utry_shell/start_test ]
  then
    if [ "" == "$DISPLAY" ]
    then
      export DISPLAY=:0.0 >> /tmp/start_test.log
      echo 'change DISPLAY'
    else
      echo "$DISPLAY"
      echo 'do nothing' >> /tmp/start_test.log
    fi

    echo 'start test' >> /tmp/start_test.log
    cd /home/utry/release/utry_shell/
    ./start_test >> /tmp/start_test.log &
  else
    echo 'dont need test'
  fi
fi
