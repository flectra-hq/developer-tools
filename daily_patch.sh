#!/bin/bash
cd /home/erp/workspace/f3/back_v16

git checkout . && git reset --hard && git clean -df && rm -rf flectra && git pull origin 16.0

cd  /home/erp/workspace/f3/developer-tools/flectra_rename_script

python3 odoo_flectra.py /home/erp/workspace/f3/back_v16/

cd  /home/erp/workspace/f3/f3public

cp /home/erp/workspace/f3/f3public/addons/web_flectra /tmp -R
 
rm -rf *

cp /home/erp/workspace/f3/back_v16/*  /home/erp/workspace/f3/f3public/ -R

cd /home/erp/workspace/f3/f3old && git pull origin 3.0

cp /home/erp/workspace/f3/f3old/addons/web_flectra /home/erp/workspace/f3/f3public/addons/  -R

cd /home/erp/workspace/f3/f3public

chmod +x flectra-bin 

git checkout flectra/addons/base/static/description/

cd /home/erp/workspace/f3/f3public && git status

git apply /home/erp/workspace/f3/developer-tools/lice.patch

cd /home/erp/workspace/f3/f3public
# git pull origin 3.0
# git add --all

# git commit -a -m "[PATCH] upstream patch"

#git push origin 3.0
