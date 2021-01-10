#! /usr/bin/bash

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

echo -e "Creating configuration file for template"
mkdir -p ~/.config/cpparsercli
if [ -f "~/.config/cpparsercli/config.json" ]; then
   echo "Configuration file already exists"
else
   touch ~/.config/cpparsercli/config.json
   echo  "{  \"Template\" : \"/home/temp.cpp\", \"lang\" : \"cpp\"  }" > ~/.config/cpparsercli/config.json
   echo -e "\e[1m\e[33mConfiguration file created at ~/.config/cpparsercli/config.json\e[0m"
fi

echo -e "\e[32mAll done!\e[0m\n\n"

echo -e "To uninstall run \e[1m./uninstall.sh\e[0m (But We hope you never do that)"
