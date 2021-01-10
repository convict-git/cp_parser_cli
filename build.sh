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

echo -e "Installing npm dependencies"
if npm install;
then
   echo -e "\e[32mNpm dependencies were installed\e[0m"
else
   echo -e "\e[31mError installing dependencies\e[0m"
   exit
fi

mkdir -p bin

if pkg --targets node10-linux-x64 index.js -o ./bin/cp-parse;
then
   echo -e "\e[32mBuild successfully.\e[0m"
else
   echo -e "\e[31mBuild failed\e[0m"
   exit
fi

echo -e "\e[1m\e[33mNow please run ./install.sh to Install...\e[0m"
chmod +x ./install.sh
