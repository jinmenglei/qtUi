#! /bin/bash
echo "begin to install program"
sleep 1
echo "step 1 copy start file"
sudo cp ./start_ui.sh /etc/profile.d/start_ui.sh
echo "step 2 chmod start file"
sudo chmod a+x /etc/profile.d/start_ui.sh
echo "step 3 cp ubuntu.desktop to computer"
sudo cp install_ubuntu.desktop /usr/share/xsessions/ubuntu.desktop
echo "install ok! begin to restart"
sleep 1
sudo reboot
