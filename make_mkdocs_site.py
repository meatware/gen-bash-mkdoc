#!/bin/bash

PROJECT_NAME="mkdocs_sys_bashrc"
SITE_NAME="Sys Bashrc"
SITE_URL="http://fillmein.com"
SITE_AUTHOR="giri"
REPO_URL="https://github.com/meatware/sys_bashrc.git"
MD_SRC_DIR="gbm-docs"
mkdocs new $PROJECT_NAME

# TODO: sort out index.md (copy from REAME.md)
cp /home/bsgt/sys_bashrc/README.md ./${MD_SRC_DIR}/index.md


###################################################################
mkdir -p ${PROJECT_NAME}/docs/

cp -rf custom_assets/custom_css ${PROJECT_NAME}/docs/
cp -rf custom_assets/custom_css ${PROJECT_NAME}/docs/
cp -rf ${MD_SRC_DIR}/*.md ${PROJECT_NAME}/docs/

###########################
cd $PROJECT_NAME/

cat<<EOF > mkdocs.yml
site_name: $SITE_NAME
site_url: $SITE_URL
repo_url: $REPO_URL
site_author: $SITE_AUTHOR
nav:
    - Home: index.md
EOF

###########################
cd docs
all_md_files=$(ls *.md)
cd -


# TODO: make this not flat
for mymd in $all_md_files; do


page_name=$(echo $mymd | sed 's|.sh||' | sed 's|.md||')
echo "mymd: $page_name $mymd"

cat<<EOF2 >> mkdocs.yml
    - ${page_name}: $mymd
EOF2
done #


###########################
cat<<EOF3 >> mkdocs.yml
theme:
    name: windmill-dark

extra_css:
    - custom_css/extra.css
EOF3

###########################
mkdocs build

cd -
###################################################################