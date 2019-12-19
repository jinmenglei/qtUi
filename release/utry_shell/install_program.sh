#! /bin/bash
echo "begin to install program"
sleep 1
echo "step 1 copy start file"
sudo cp ./start_ui.sh /etc/profile.d/start_ui.sh
echo "step 2 chmod start file"
sudo chmod a+x /etc/profile.d/start_ui.sh
echo "step 3 cp ubuntu.desktop to computer"
sudo cp install_ubuntu.desktop /usr/share/xsessions/ubuntu.desktop
echo "step 4 cp start_ui to computer"
sudo cp /home/utry/release/utry_shell/start_ui /usr/bin/
echo "register cmd"
RET=$(grep "complete -W" ~/.bashrc)
CODE=" complete -W 'start stop install uninstall test deltest' start_ui"
if [ "" == "$RET" ]
then
  echo "install init"
  echo "$CODE" >> ~/.bashrc
else
  echo "install change"
  sed -i "/^complete -W/c$CODE" ~/.bashrc
fi
echo "install ok! begin to restart"
sleep 1
sudo reboot
