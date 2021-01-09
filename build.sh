#!/bin/bash

echo -e "Checking if npm is installed.."
if npm -v;
then
   echo -e "\e[32mnpm found\e[0m"
else
   echo -e "\e[31mnpm not found. Installing npm....\e[0m"
   if sudo apt-get install npm;
   then
      echo -e "\e[32mnpm installed.\e[0m"
   else
      echo -e "\e[31mError installing npm\e[0m"
      exit
   fi
fi

echo -e "Checking if node pkg is installed.."
if npm list -g | grep pkg;
then
   echo -e "\e[32mpkg was found\e[0m"
else
   echo -e "\e[31mpkg not found. Installing node pkg.\e[0m"
   if sudo npm install -g pkg;
   then
      echo -e "\e[32mpkg installed\e[0m"
   else
      echo -e "\e[31mError installing node pkg\e[0m"
      exit
   fi
fi

if pkg --targets node10-linux-x64 index.js;
then
   echo -e "\e[32Build uccessfully.\e[0m"
else
   echo -e "\e[31mBuild failed\e[0m"
   exit
fi

sudo cp -v bin/compile_cp_parser_cli-linux /usr/bin/cp-compile
sudo cp -v bin/cp_parser_cli-linux /usr/bin/cp-parse
sudo cp -v bin/tester_cp_parser_cli-linux /usr/bin/cp-tester
sudo chmod +x /usr/bin/cp-compile
sudo chmod +x /usr/bin/cp-parse
sudo chmod +x /usr/bin/cp-tester


