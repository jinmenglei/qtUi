#! /bin/bash
echo "begin to install program"
sleep 1
echo "step 1 remove start file"
sudo rm /etc/profile.d/start_ui.sh

echo "step 2 cp ubuntu.desktop to computer"
sudo cp uninstall_ubuntu.desktop /usr/share/xsessions/ubuntu.desktop
echo "uninstall ok! begin to restart"
sleep 1
sudo reboot