#!/bin/bash
cd /home/erp/workspace/f4/v17

git checkout . && git reset --hard && git clean -dfx && rm -rf flectra && git pull origin 17.0

cd  /home/erp/workspace/f4/developer-tools/flectra_rename_script

python3 odoo_flectra.py /home/erp/workspace/f4/v17/

cd  /home/erp/workspace/f4/f4public

# cp /home/erp/workspace/f4/f4public/addons/web_flectra /tmp -R
 
rm -rf *

cp /home/erp/workspace/f4/v17/*  /home/erp/workspace/f4/f4public/ -R

# cd /home/erp/workspace/f4/f4old && git pull origin 3.0

# cp /home/erp/workspace/f4/f4old/addons/web_flectra /home/erp/workspace/f4/f4public/addons/  -R

cd /home/erp/workspace/f4/f4public

chmod +x flectra-bin 

# git checkout flectra/addons/base/static/description/

# cd /home/erp/workspace/f4/f4public && git status

# git apply /home/erp/workspace/f4/developer-tools/lice.patch

# cd /home/erp/workspace/f4/f4public
# git pull origin 3.0
# git add --all

# git commit -a -m "[PATCH] upstream patch"

#git push origin 3.0
