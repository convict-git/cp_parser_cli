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

echo -e "Copying all scripts and parser to /usr/bin"
sudo cp -v ./bin/cp-parse /usr/bin/cp-parse
sudo cp -v ./scripts/cp-compile /usr/bin/cp-compile
sudo cp -v ./scripts/cp-random /usr/bin/cp-random
sudo cp -v ./scripts/cp-tester /usr/bin/cp-tester

echo -e "Giving executable permissions"
sudo chmod +x /usr/bin/cp-parse
sudo chmod +x /usr/bin/cp-compile
sudo chmod +x /usr/bin/cp-random
sudo chmod +x /usr/bin/cp-tester

echo -e "\e[32mAll done!\e[0m"
