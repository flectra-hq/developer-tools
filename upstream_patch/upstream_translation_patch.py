import os
import subprocess
import optparse
import logging
import sys

arg = sys.argv


def update_translation(src, dest):
    src_dir = os.listdir(os.path.join(src, 'addons'))
    dest_dir = os.listdir(os.path.join(dest, 'addons'))
    # print(src_dir)
    for i in src_dir:
        print(os.path.join(src, 'addons', i))
        if i in dest_dir:
            if os.path.isdir(os.path.join(src, 'addons', i)):
                dir_list = os.listdir(os.path.join(src, 'addons', i))
                if 'i18n' in dir_list:
                    dir_list = ['i18n',]
                    for j in dir_list:
                        subprocess.call(['cp', os.path.join(
                            src, 'addons', i, j), os.path.join(dest, 'addons', i), '-r'])
            else:
                subprocess.call(
                    ['cp', os.path.join(src, 'addons', i), os.path.join(dest, 'addons', i)])
    branch = "master-translation-upstream-patch"
    create_merge_request(dest, branch)



def create_merge_request(dest, branch):
    cmd = dict(
        cmd4=f'cd {dest} && git pull origin master',
        cmd=f"cd {dest} && git checkout -b {branch}",
        cmd2=f'cd {dest} && git add -A && git commit -m "[PATCH] Upstream patch" && git push origin {branch} -o merge_request.create -o merge_request.target=master',
        cmd3=f'cd {dest} && git checkout master && git branch -d {branch}'
    )
    ps_execute(cmd)

def ps_execute(cmd):

    for i in cmd.values():
        ps2 = subprocess.Popen(i, shell=True)
        ps2.communicate()
        ps2.wait()
        

parser = optparse.OptionParser()

parser.add_option("--src", dest="src_path")
parser.add_option("--dest", dest="dest_path")

options, args = parser.parse_args()
src = options.src_path
dest = options.dest_path

# branch = options.branch
branch = "master-upstream-patch"
if src and dest:
    if not os.path.exists(src):
        print(src, "\tpath does not exist!")
    elif not os.path.exists(dest):
        print(dest, "\tpath does not exist!")
    else:
        update_translation(src, dest)

else:
    print("\nInvalid Command!\nProvide 'Source' and 'Destination'.\n\n\t1) --src=/path/to/source\n\t2) --dest=/path/to/destination\n")
