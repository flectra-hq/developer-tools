#!/bin/bash
# cd /home/erp/workspace/f3/back_v16

# git checkout . && git reset --hard && git clean -df && rm -rf flectra && git pull origin 16.0

cd  /home/erp/workspace/f3/developer-tools/flectra_rename_script && python3 odoo_flectra.py /home/erp/workspace/f3/back_v16/

cd  /home/erp/workspace/f3/eef3

# cp /home/erp/workspace/f3/eef3/addons/web_flectra /tmp -R
 
rm -rf *

cp /home/erp/workspace/f3/back_v16/*  /home/erp/workspace/f3/eef3/ -R

# cd /home/erp/workspace/f3/f3old && git pull origin 3.0

# cp /home/erp/workspace/f3/f3old/addons/web_flectra /home/erp/workspace/f3/eef3/addons/  -R

cd /home/erp/workspace/f3/eef3

chmod +x flectra-bin 

# git checkout flectra/addons/base/static/description/

cd /home/erp/workspace/f3/eef3 && git status

git apply /home/erp/workspace/f3/developer-tools/lice.patch

cd /home/erp/workspace/f3/eef3
# git pull origin 3.0
# git add --all

# git commit -a -m "[PATCH] upstream patch"

#git push origin 3.0
