# -*- coding: utf-8 -*-
# !/usr/bin/python3

import logging
import os
import sys
import time
import shutil
import subprocess
# import codecs
import traceback

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)-8s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)

FLECTRA_VERSION = 2
ODOO_VERSION = 14

_help = '''#######################################################################################################
Run command  : python odoo_flectra.py <path> [--copy/-c] [--help/-h]

@param -> odoo_flectra.py : to convert odoo modules to flectra
@param -> <path>         : give a path where your module is located
@param -> --copy OR -C   : this is an option parameter, pass if you want to make a copy before converting

@example> For Help       : python odoo_flectra.py [-h]
@example> Without Copy   : python odoo_flectra.py /home/<system_user>/<module_name>
@example> With Copy      : python odoo_flectra.py /home/<system_user>/<module_name> --copy

**Note ::
- If you execute this script on migrated module then there is possibility that you can get following kind of strings:
    -- "flectra, flectra",
    -- "odoo, flectra, flecta" 
- So do not use multiple times on migrated module.
- In case you get any error during execution, the best way, use --copy flag on your module,
so you can have a backup of your real data.

#######################################################################################################'''

if '--help' in sys.argv or '-H' in sys.argv or '-h' in sys.argv:
    print(_help)
    os._exit(1)

if len(sys.argv) < 2:
    logging.error(
        'Directory path is required, please follow below instructions.')
    print(_help)
    os._exit(1)
else:
    odoo_path = sys.argv[1]
    if not os.path.isdir(odoo_path) and not os.path.exists(odoo_path):
        logging.error(
            'Directory does not exist. Please check for path : %s' % odoo_path)
        print(_help)
        os._exit(1)

suffix = "/"
win_suffix = "\\"
while odoo_path.endswith(suffix, len(odoo_path) - 1) or odoo_path.endswith(
        win_suffix, len(odoo_path) - 1):
    odoo_path = odoo_path[:len(odoo_path) - 1]
path_join = os.path.join
logging.info("You Directory is : %s" % odoo_path)

if '--copy' in sys.argv or '-C' in sys.argv or '-c' in sys.argv:
    logging.info('Please wait, copy is being process.')
    shutil.copytree(odoo_path, odoo_path + time.strftime("%Y-%m-%d %H:%M:%S"))

replacements = {
    'odoo': 'flectra',
    'Odoo': 'Flectra',
    'ODOO': 'FLECTRA',
    '8069': '7073',
    # 'Part of Odoo.': 'Part of Odoo, Flectra.',
    # 'openerp': 'flectra',
    # 'Openerp': 'Flectra',
    # 'OpenERP': 'Flectra',
    # 'OpenErp': 'Flectra',
    # 'OPENERP': 'FLECTRA',
    # 'Part of Openerp.': 'Part of Openerp, Flectra.',
}

xml_replacements = {
    'odoo': 'flectra',
    'Odoo': 'Flectra',
    'ODOO': 'FLECTRA',
    # 'Part of Odoo.': 'Part of Odoo, Flectra.',
    '<openerp>': '<flectra>',
    '</openerp>': '</flectra>',
    # 'openerp': 'flectra',
    # 'Openerp': 'Flectra',
    # 'OpenERP': 'Flectra',
    # 'OpenErp': 'Flectra',
    # 'OPENERP': 'FLECTRA',

    # '<openerp>': '<flectra>',
    # '</openerp>': '</flectra>',
    # '<Openerp>': '<Flectra>',
    # '<OpenERP>': '<Flectra>',
    # '<OpenErp>': '<Flectra>',
    # '<OPENERP>': '<FLECTRA>',
    # 'Part of OpenERP.': 'Part of OpenERP, Flectra.',
}

# New ###################################################################
rng_replacement = {
    'odoo': 'flectra',
    'openerp': 'flectra',
}
#########################################################################

init_replacements = {
    # 'Odoo.': 'Odoo, Flectra.',
    'odoo': 'flectra',
    # 'openerp': 'flectra',
    # 'Openerp': 'Flectra',
    # 'OpenERP': 'Flectra',
    # 'OpenErp': 'Flectra',
}

manifest_replacements = {
    # 'Odoo.': 'Odoo, Flectra.',
    'odoo': 'flectra',
    # 'openerp': 'flectra',
    # 'Openerp': 'Flectra',
    # 'OpenERP': 'Flectra',
    # 'OpenErp': 'Flectra',
}

re_replacements = {
    # 'Odoo.': 'Odoo, Flectra.',
    # 'openerp': 'openerp, flectra',
    # 'Openerp': 'Openerp, Flectra',
    # 'OpenERP': 'OpenERP, Flectra',
    # 'OpenErp': 'OpenErp, Flectra',
}

ignore_dir = [
    'cla',
    'doc',
]

ignore_files = [
    'LICENSE',
    'COPYRIGHT',
    'README.md',
    'CONTRIBUTING.md',
    'Makefile',
    'MANIFEST.in'
]

ignore_words = [
    'OpenERPSession',
    'provider_openerp'
]

website_replacements = {
    'https://www.odoo.com': 'https://flectrahq.com',
    'www.odoo.com': 'https://flectrahq.com',
    'https://www.openerp.com': 'https://flectrahq.com',
    'www.opernerp.com': 'https://flectrahq.com',
}

replace_email = {
    'info@odoo.com': 'info@flectrahq.com',
    'info@openerp.com': 'info@flectrahq.com',
}

replace_website = {
    'www.odoo.com': 'www.flectrahq.com',
    'www.openerp.com': 'www.flectrahq.com'
}

def init_files(root):
    infile = open(path_join(root, '__init__.py'), 'r').read()
    for i in init_replacements.keys():
        infile = infile.replace(i, init_replacements[i])
    out = open(path_join(root, '__init__.py'), 'w')
    out.write(infile)
    out.close()

def manifest_files(root):
    temp = {}
    infile = open(path_join(root, '__manifest__.py'), 'r').read()
    temp.update(replace_email)
    temp.update(website_replacements)
    out = open(path_join(root, '__manifest__.py'), 'w')
    for i, j in temp.items():
        infile = infile.replace(i, j)
    out.write(infile)
    out.close()
    content_replacements(root, '__manifest__.py', manifest_replacements)

def xml_csv_json_files(root, name):
    infile = open(path_join(root, name), 'r',
                  encoding='utf-8', errors='replace').read()
    for i in replace_email.keys():
        infile = infile.replace(i, replace_email[i])
    out = open(path_join(root, name), 'w', encoding='utf-8', errors='replace')
    out.write(infile)
    out.close()
    content_replacements(root, name, xml_replacements)

def python_files(root, name):
    infile = open(path_join(root, name), 'r').read()
    out = open(path_join(root, name), 'w')
    for i in replace_email.keys():
        infile = infile.replace(i, replace_email[i])
    out.write(infile)
    out.close()
    content_replacements(root, name, replacements)


def content_replacements(root, name, replace_dict):
    infile = open(path_join(root, name), 'r').readlines()
    ignore_key = ['payment_odoo_by_adyen']
    multilist = []
    if infile:
        for line in infile:
            words = line.split(' ')
            single_line = []
            for word in words:
                if word.startswith('info@') or word.startswith("'info@") or word.startswith('"info@'):
                    single_line.append(word)
                    continue
                for i in replace_dict.keys():
                    if i in ignore_key:
                        pass
                    else:
                        must_replace = True
                        for ing_word in ignore_words:
                            if ing_word in word:
                                must_replace = False
                        if must_replace:
                            word = word.replace(i, replace_dict[i])
                single_line.append(word)
            multilist.append(single_line)
    with open('temp', 'a') as temp_file:
        for lines in multilist:
            for word in lines:
                word = word if word.endswith(
                    '\n') else word + ' ' if word else ' '
                temp_file.write(word)
    shutil.copy('temp', path_join(root, name))
    os.remove('temp')


def rename_files(root, items):
    for name in items:
        logging.info(path_join(root, name))
        if name in ignore_files:
            continue
        if name == '__openerp__.py':
            shutil.copy(path_join(root, name),
                        path_join(root, '__manifest__.py'))
            os.remove(path_join(root, name))
            name = '__manifest__.py'
        if name == '__init__.py':
            init_files(root)
        elif name == '__manifest__.py':
            # manifest_files(root)
            continue
        else:
            sp_name = name.split('.')
            if len(sp_name) >= 2 and sp_name[-1] in ['xml', 'csv', 'json', 'html']:
                xml_csv_json_files(root, name)
            elif sp_name[-1] in ['py', 'css', 'less', 'js', 'yml']:
                python_files(root, name)
                # continue
        try:
            for i in replacements.keys():
                if name != (name.replace(i, replacements[i])):
                    logging.info('Rename With :: ' + name +
                                 ' -> ' + (name.replace(i, replacements[i])))
                    shutil.copy(path_join(root, name), path_join(
                        root, name.replace(i, replacements[i])))
                    os.remove(path_join(root, name))

        except OSError as e:
            pass


def rename_dir(root, items):
    for folder in items:
        if folder in ignore_dir:
            continue
        for in_root, dirs, files in os.walk(root + folder, topdown=True):
            if files:
                rename_files(in_root, files)
            if dirs:
                rename_dir(in_root, dirs)


def replace_rng():
    try:
        path = sys.argv[1]
        line_to_find = "<rng:name>openerp</rng:name>"
        line_to_replace = "<rng:name>flectra</rng:name>"
        odoo = "odoo"
        flectra = "flectra"
        dirs = os.listdir(path)
        for i in dirs:
            if i == 'flectra':
                continue
            if i == 'odoo':
                os.rename('{}/odoo/'.format(path), '{}/flectra/'.format(path))
        dir_name = "flectra"

        rng_file_path = os.path.join(
            str(path), str(dir_name) + "/import_xml.rng")
        init_file_path = os.path.join(
            str(path) + "/flectra-bin")

        try:
            init_file = open(init_file_path).readlines()

            f = open(rng_file_path).readlines()

            ftemp = open("rng_temp.txt", "w")
            for line in f:
                line = line.replace(line_to_find, line_to_replace)
                ftemp.write(line)
            os.rename("rng_temp.txt", rng_file_path)

            itemp = open("init_temp.txt", "w")
            for line in init_file:
                line = line.replace(odoo, flectra)
                itemp.write(line)
            os.rename("init_temp.txt", init_file_path)

            # replace_images()
            replace_addons()
        except FileNotFoundError:
            pass
    except:
        pass

def replace_addons():
    try:
        path = sys.argv[1]
        dirs = os.listdir(path + '/addons')
        for i in dirs:
            if 'odoo_referral' in i:
                print(i)
                temp = i.replace('odoo', 'flectra')
                subprocess.run(
                    ['mv', '-T', '{}/addons/{}'.format(path, i), '{}/addons/{}'.format(path, temp)])
    except:
        pass

def replace_images():
    path = sys.argv[1]
    image_to_replace = {
        'images/favicon.ico': "addons/web/static/src/img",
        # 'images/db_manager.png': "doc/setup/enterprise/db_manager.png",
        # 'images/devmode.png': "doc/howtos/web",
        'images/flectra.png': "addons/web/tests/flectra.png",
        'images/flectrabot.png': "addons/mail/static/src/img/flectrabot.png",
        'images/flectrabot_transparent.png': "addons/mail/static/src/img/flectrabot_transparent.png",
        # 'images/flectra_icon.png': "addons/payment_odoo_by_adyen/static/src/img/flectra_icon.png",
        # 'images/flectra_logo_rgb.png': "doc/_extensions/odoo_ext/static/img/flectra_logo_rgb.png",
        'images/flectra_logo_tiny.png': "addons/web/static/src/img/flectra_logo_tiny.png",
        'images/flectra_o.png': "addons/mail/static/src/img/flectra_o.png",
        'images/logo.png': "addons/web/static/src/img/logo.png",
        'images/logo2.png': "addons/web/static/src/img/logo2.png",
        'images/logo3.png': "addons/web/static/src/img/nologo.png",
        'images/logo_white.png': "flectra/addons/base/static/img/logo_white.png",
        'images/main_partner-image.png': "flectra/addons/base/static/img/main_partner-image.png",
        'images/openerp_gold_partner.png': "addons/sale_management/static/src/img/openerp_gold_partner.png",
        'images/partners.png': "addons/website_google_map/static/src/img",
        'images/speaker.png': "addons/website_event/static/src/img/speaker.png",
        'images/Attendances.png': "addons/hr_attendance/static/description/icon.png",
        'images/CRM.png': "addons/crm/static/description/icon.png",
        'images/blog.png': "addons/website_blog/static/description/icon.png",
        'images/calendar.png': "addons/calendar/static/description/icon.png",
        'images/contacts.png': "addons/contacts/static/description/icon.png",
        'images/dashboards.png': "addons/board/static/description/icon.png",
        'images/discuss.png': "addons/mail/static/description/icon.png",
        'images/e-commerce.png': "addons/website_sale/static/description/icon.png",
        'images/elearning.png': "addons/website_slides/static/description/icon.png",
        'images/email-marketing.png': "addons/mass_mailing/static/description/icon.png",
        # 'images/employee-contracts.png': "addons/hr_contract/static/description/icon.png",
        'images/employees.png': "addons/hr/static/description/icon.png",
        'images/events.png': "addons/website_event/static/description/icon.png",
        'images/expenses.png': "addons/hr_expense/static/description/icon.png",
        'images/Fleet.png': "addons/fleet/static/description/icon.png",
        'images/forum.png': "addons/website_forum/static/description/icon.png",
        'images/Inventory.png': "addons/stock/static/description/icon.png",
        'images/invoicing.png': "addons/account/static/description/icon.png",
        'images/livechat.png': "addons/im_livechat/static/description/icon.png",
        'images/lunch.png': "addons/lunch/static/description/icon.png",
        'images/maintenance.png': "addons/maintenance/static/description/icon.png",
        'images/Manufacturing.png': "addons/mrp/static/description/icon.png",
        'images/notes.png': "addons/note/static/description/icon.png",
        'images/online_job.png': "addons/website_hr_recruitment/static/description/icon.png",
        'images/Point_of_Sale.png': "addons/point_of_sale/static/description/icon.png",
        'images/Project.png': "addons/project/static/description/icon.png",
        'images/Purchase.png': "addons/purchase/static/description/icon.png",
        'images/Recruitment.png': "addons/hr_recruitment/static/description/icon.png",
        'images/repairs.png': "addons/repair/static/description/icon.png",
        'images/Sales.png': "addons/sale_management/static/description/icon.png",
        'images/skills-management.png': "addons/hr_skills/static/description/icon.png",
        'images/sms-marketing.png': "addons/mass_mailing_sms/static/description/icon.png",
        'images/time-off.png': "addons/hr_holidays/static/description/icon.png",
        'images/website.png': "addons/website/static/description/icon.png",
        'images/Survey.png': "addons/survey/static/description/icon.png",
        'images/apps.png': "flectra/addons/base/static/description/modules.png",
        'images/setting.png': "flectra/addons/base/static/description/settings.png",
        'images/flectra2.png': "flectra/addons/base/tests/flectra.png",
        'images/events-organization.png': "addons/event/static/description/icon.png",
        'images/dashboards2.png': "flectra/addons/base/static/description/board.png",
        'images/members.png': 'addons/membership/static/description/icon.png',
        'images/timesheets.png': 'addons/hr_timesheet/static/description/icon.png',
        'images/timesheets2.png': 'addons/hr_timesheet/static/description/icon_timesheet.png',
        'images/link_tracker.png': 'addons/utm/static/description/icon.png',
        # 'images/logo2.png': 'addons/web/static/src/img/logo.png',
        'images/flectra_icon.png': 'addons/web/static/src/img/nologo.png',
        'images/logo_inverse.png': 'addons/web/static/src/img/logo_inverse_white_206px.png',
        'images/logo4.png': 'addons/web/tests/flectra.png',
        'images/whitelogo.png': 'addons/point_of_sale/static/src/img/logo.png',
        'images/flectra_logo_tiny_2.png': 'addons/mass_mailing/static/src/img/theme_basic/s_default_image_logo.png',

    }
    
    try:
        for key, value in image_to_replace.items():
            shutil.copy(key, os.path.join(path, value))
            print(key, os.path.join(path, value))
    except Exception:
            traceback.print_exc()

def replace_content(root, items):

    ignore_files = ['png', 'jpg', 'pyc']  # 'po', 'pot'
    replace_items = {
        'flectra.com': 'flectrahq.com',
        'odoo.com': 'flectrahq.com',
        # 'http://www.flectra.com': 'http://www.flectrahq.com',
        # 'https://iap.flectra.com': 'https://iap.flectrahq.com',
        # 'https://nightly.flectra.com': 'https://nightly.flectrahq.com',
        # 'https://www.odoo.com/page/': 'https://flectrahq.com/',
        'Odoo': 'Flectra',
        'Flectra.com': 'flectrahq.com',
        'flectra.com': 'flectrahq.com',
        'Flectra S.A': 'FlectraHQ Inc., Odoo S.A',
        'Flectra SA': 'FlectraHQ Inc.',
        'id1272543640': 'id1561830563',
        'com.odoo.mobile':'com.flectra.flectrahq',
        'com.flectra.mobile':'com.flectra.flectrahq',
        'Part of Flectra.': 'Part of Odoo, Flectra.',
        'https://apps.flectrahq.com': 'https://store.flectrahq.com',
        'payment_flectra_by_adyen': 'payment_odoo_by_adyen',
        '#875A7B': '#009EFB',
        '#875a7b': '#2496f6',
        '127.0.0.1:8072': '127.0.0.1:7072',
        'Flectra Server 14.0': 'Flectra Server 2.0',
        'my_default=8072': 'my_default=7072',
        'https://www.flectrahq.com/documentation/user/14.0': 'https://doc.flectrahq.com/2.0',
        'https://www.flectrahq.com/documentation/14.0': 'https://doc.flectrahq.com/2.0',

    }

    temp_file = None
    for key, value in replace_items.items():
        for files in items:
            try:
                if files[-2:] in ignore_files or files[-3:] in ignore_files:
                    continue
                else:
                    logging.info(path_join(root, files))
                    file_path = os.path.join(root, files)
                    logging.info(file_path)
                    temp_file = open(
                        file_path, 'r+', encoding='utf-8')
                    temp_file_write = open('temp_file', 'w', encoding='utf-8')
                    for i in temp_file.readlines():
                        line = i.replace(key, value)
                        temp_file_write.write(line)
                    os.rename(temp_file.name, file_path)
                    os.remove('temp_file')
                    temp_file.close()
                    temp_file_write.close()
            except UnicodeDecodeError:
                pass


def delete_svg():
    try:
        path = sys.argv[1] + '/addons'
        base_path = sys.argv[1] + '/flectra/addons'
        dirs = os.listdir(path)
        svg_icons = ['board.svg', 'modules.svg', 'settings.svg']
        for i in dirs:
            try:
                os.remove(f"{path}/{i}/static/description/icon.svg")
            except FileNotFoundError:
                pass
        for i in svg_icons:
            os.remove(f"{base_path}/base/static/description/{i}")
    except:
        pass

def replace_manifest():
    path = sys.argv[1]
    dirs = os.listdir(f"{path}/addons")

    for i in dirs:
        if 'flectra' in i:
            manifest_path = f"{path}/addons/{i}"
            manifest = os.listdir(manifest_path)
            if "__manifest__.py" in manifest:
                f = open(f"{manifest_path}/__manifest__.py").readlines()
                ftemp = open("/tmp/manifest.txt", "w")
                for line in f:
                    line = line.replace('Odoo', 'Flectra')
                    ftemp.write(line)
                os.rename("/tmp/manifest.txt",
                        f"{manifest_path}/__manifest__.py")

def change_release():
    try:
        path = os.path.join(sys.argv[1], "flectra/release.py")
        # line_to_find = ("version_info = (" + str(ODOO_VERSION), )
        line_to_replace = (("version_info = (" + str(ODOO_VERSION), "version_info = (" + str(FLECTRA_VERSION)), ("author = 'OpenERP S.A.'", "author = 'FlectraHQ, OpenERP S.A.'"))

        logging.info(path)
        for replace in line_to_replace:
            temp_file = open(
                path, 'r+', encoding='utf-8')
            temp_file_write = open('temp_file', 'w', encoding='utf-8')
            for i in temp_file.readlines():
                line = i.replace(replace[0], replace[1])
                temp_file_write.write(line)
            os.rename('temp_file', path)
            temp_file.close()
            temp_file_write.close()
    except:
        pass

start_time = time.strftime("%Y-%m-%d %H:%M:%S")
if os.path.isdir(odoo_path):
    for root, dirs, files in os.walk(odoo_path, topdown=True):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        rename_files(root, files)
        rename_dir(root, dirs)
    replace_rng()
    replace_images()
    for root, dirs, files in os.walk(odoo_path, topdown=True):
        files = [f for f in files if not f[0] == '.']
        dirs[:] = [d for d in dirs if not d[0] == '.']
        replace_content(root, files)
    change_release()
    delete_svg()

else:
    rename_files('', [odoo_path])
end_time = time.strftime("%Y-%m-%d %H:%M:%S")
logging.info('Execution Log :::: ')
logging.info('Start Time ::: %s' % start_time)
logging.info('End Time   ::: %s' % end_time)
