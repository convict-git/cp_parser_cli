#! /usr/bin/bash

if
   mkdir -p package &&
   cp -v ./install.sh ./package &&
   cp -v ./uninstall.sh ./package &&
   cp -v ./bin/cp-parse ./package/bin &&
   cp -rv ./scripts ./package
then
   echo "created a temp directory for package..."
else
   rm -rfv ./package
   echo -e "\e[31mPackage creation failed!\e[0m"
   exit
fi

if zip -rv package.zip ./package;
then
   echo -e "\e[32mPackage created as package.zip!\e[0m"
else
   echo -e "\e[31mPackage creation failed!\e[0m"
fi
rm -rfv ./package
