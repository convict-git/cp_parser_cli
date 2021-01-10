#! /usr/bin/bash

echo -e "Removing all scripts from /usr/bin and removing the config file..."
if sudo rm -rfv /usr/bin/cp-parse &&
   sudo rm -rfv /usr/bin/cp-compile &&
   sudo rm -rfv /usr/bin/cp-random &&
   sudo rm -rfv /usr/bin/cp-tester &&
   sudo rm -rfv ~/.config/cpparsercli/config.json
then
   echo -e "\e[1m\e[32mUninstalled successfully. I hope you enjoyed!\e[0m"
else
   echo -e "\e[1m\e[31mFailed Uninstallation!\e[0m"
fi
