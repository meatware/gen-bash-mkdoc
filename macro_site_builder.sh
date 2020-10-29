#!/bin/bash -e

rm -rf  mkdocs_sys_bashrc gbm-docs
#python src/main.py -i  /home/bsgt/sys_bashrc/aliases/apt_aliases.sh  -o `pwd`/gbm-docs
python src/main.py -i $(find /home/bsgt/sys_bashrc/ -name "*.sh")  -o `pwd`/gbm-docs -x "zsdoc" "test" "theme_settings_BACKUP" "unused_scrap_functions"
#exit 0

./make_mkdocs_site.sh

cd mkdocs_sys_bashrc
mkdocs build
mkdocs serve
cd -
