#!/bin/bash

sudo cp -v bin/compile_cp_parser_cli-linux /usr/bin/cp-compile
sudo cp -v bin/cp_parser_cli-linux /usr/bin/cp-parse
sudo cp -v bin/tester_cp_parser_cli-linux /usr/bin/cp-tester
sudo chmod +x /usr/bin/cp-compile
sudo chmod +x /usr/bin/cp-parse
sudo chmod +x /usr/bin/cp-tester

