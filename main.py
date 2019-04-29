#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Un progetto per selezionare e ordinare alcune mail ricevute
#  Copyright (C) 2019 Oxke
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3 of the License.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#  If you want to contact me, -> oseaetobia@gmail.com
__author__ = "Oxke"
__contact__ = "oseaetobia@gmail.com"
__copyright__ = "Copyright (C) 2019, Oxke"
__license__ = "GNU GPLv3.0"  # Read the file LICENSE for more information
__project__ = "emailAuttachments"
__version__ = "v3.0.3"
__date__ = "2019-02-03"

import argparse
import datetime
import pprint
import subprocess
import sys
from pathlib import Path
from shutil import rmtree

import settings
from crypto import *


def including_root(path):
    """Return absolute path"""
    return os.path.join(Path(__file__).parent, path)


def arg():
    try:
        with open(including_root(
                'config_folder\\settings.json')) as def_sett_file:
            def_settings = json.load(def_sett_file)
        dati = decrypt_eaa(including_root(def_settings['general']['settings']))
        if def_settings['general']['settings'] == \
                'config_folder\\settings.json':
            del dati['general']['settings']
    except Exception as e:
        if '-h' not in sys.argv[1:]:
            raise e
        else:
            dati = None
    parser = argparse.ArgumentParser(description='Programmino per gestire le '
                                                 'auto email contenenti '
                                                 'allegati. Se non si '
                                                 'specifica un subparser, '
                                                 'verrà considerato il '
                                                 '"Main", a meno che non si '
                                                 'chiami l\'help e in questo '
                                                 'modo si otterrà quello '
                                                 'generale. Per ottenere '
                                                 'l\'help del "Main" basterà '
                                                 'quindi chiamare "python '
                                                 'main.py Main -h"',
                                     usage='main.py [-h] [-i]'
                                           ' {[Main],Delete} ...')
    parser.add_argument('-i', '--info', help='prima di iniziare il programma '
                                             'stampa le impostazioni',
                        action='store_true')
    subparsers = parser.add_subparsers(help='Possibili quattro '
                                            'diversi tipi di azione',
                                       dest='command')
    parser1 = subparsers.add_parser('Main', help='Main action',
                                    usage="main.py [Main -h] [-s SETTINGS] [-d "
                                          "DESTINATION] [-f FOLDER] "
                                          "[-n NUMBER] [-o OPTIONS] "
                                          "[-em EMAIL] [-pwd PASSWORD] "
                                          "[-ss SETSETTINGS] [key]")
    parser1.add_argument("-s", "--settings", help='choose settings file')
    parser1.add_argument("-d", "--destination", help='where to download '
                                                     'attachments')
    parser1.add_argument("-f", "--folder", help='in which folder?')
    parser1.add_argument("-n", "--number", help="number emails to receive")
    parser1.add_argument("key", help='chiave usata per filtrare le '
                                     'email', nargs='?', default=None)
    parser1.add_argument('-o', '--options', help='imap options for selecting '
                                                 'emails')
    parser1.add_argument('-em', '--email', help='user_email_address')
    parser1.add_argument('-pwd', '--password', help='user password')
    parser1.add_argument("-ss", "--setsettings", help='create new file '
                                                      'settings')
    parser2 = subparsers.add_parser('Delete', help='help for Delete')
    parser2.add_argument('delete', help='distrugge tutto')
    # noinspection PyUnusedLocal
    parser3 = subparsers.add_parser('Settings', help='Settings made easy')
    args = parser.parse_args(sys.argv[1:])
    if args.command == 'Main':
        if args.settings:
            dati = decrypt_eaa(including_root(f'config'
                                              f'_folder\\{args.settings}.eaa'))
        numb = 1
        def_key = dati['general']['def_key'].replace('$', str(numb))
        while os.path.exists(including_root(f'config_folder\\data_config\\'
                                            f'{def_key}.eaa')):
            numb += 1
            def_key = dati['general']['def_key'].replace('$', str(numb))
        dati['general']['def_key'] = args.key if args.key else def_key
        dati['general']['def_dest'] = args.destination if args.destination \
            else dati['general']['def_dest']
        dati['general']['def_number'] = args.number if args.number else dati[
            'general']['def_number']
        dati['general']['def_info'] = args.info if args.info else dati[
            'general']['def_info']
        dati['general']['imap_options'] = dati['general']['imap_options'] + [
            option.strip() for option in args.options.split(' ')] \
            if args.options else dati['general']['imap_options']
        dati['email']['email'] = args.email if args.email else dati['email'][
            'email']
        dati['email']['password'] = args.password if args.password else dati[
            'email']['password']
        return dati['general']['def_key'], (args.info, dati,
                                            args.setsettings), 'Main'
    elif args.command == 'Delete':
        dati['general']['def_key'] = args.delete
        return dati['general']['def_key'], (args.info, dati,
                                            args.delete), 'Delete'
    elif args.command == 'Settings':
        settings.setup()
        arg()
    return dati['general']['def_key'], (None, None, None), 'Main'


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.argv += ['Main']
    if '-h' not in sys.argv:
        if sys.argv[1] not in ['Main', 'Delete', 'Settings']:
            if sys.argv[1] == '-i':
                if len(sys.argv) == 2:
                    sys.argv = sys.argv[:2] + ['Main'] + sys.argv[2:]
                elif sys.argv[2] not in ['Main', 'Delete', 'Settings']:
                    sys.argv = sys.argv[:2] + ['Main'] + sys.argv[2:]
            else:
                sys.argv = sys.argv[:1] + ['Main'] + sys.argv[1:]
    key, act, command = arg()
    config_f = including_root(f"config_folder\\data_config\\{key}.eaa")
    if os.path.exists(config_f):
        data = decrypt_eaa(config_f)
    else:
        data = {
            'creationDate': str(datetime.date.today()),
            'key': key,
            'folder': os.path.join(act[1]['general']['def_dest'], key),
            'number': act[1]['general']['def_number'],
            'email': act[1]['email']['email'],
            'imap_options': act[1]['general']['imap_options'],
        }
    if act[0]:
        pprint.pprint(data)
        input()
    if command == 'Delete':
        if input(f'Eliminare la raccolta "{key}"? -> ').lower() not in ('no',
                                                                        'n'):
            try:
                rmtree(data['folder'])
                os.remove(config_f)

                print('Eliminata!')
            except Exception as ex:
                print("C'è stato un errore:", ex, sep=' ')
            finally:
                input()
    elif act[2]:
        name = act[2]
        setting = act[1]
        pprint.pprint(setting)
        if '$' not in setting['general']['def_key']:
            setting['general']['def_key'] += '$'
        if input(f'Vuoi che il file settings "{name}" diventi di default? -> '
                 f'').lower() not in ('no', 'n'):
            with open(including_root('config_folder\\settings.json')) as fp:
                d = json.load(fp)
            with open(including_root('config_folder\\settings.json'), 'w') as \
                    fp:
                json.dump(d, fp)
        encrypt_eaa(including_root(f'config_folder\\{name}.json'),
                    data=setting)
    else:
        dest = os.path.split(data['folder'])[0]
        name_folder = os.path.split(data['folder'])[1]
        num = str(data['number'])
        subprocess.Popen([sys.executable, including_root(".\\printSent.py"),
                          "-k", data['key'], '-n', num, data['folder']],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
        argscheck = [sys.executable, including_root("check.py"), "-d",
                     dest, "-f", name_folder, "-n", num,
                     '-em', act[1]['email']['email'], '-pwd',
                     act[1]['email']['password']]
        if len(act[1]['general']['imap_options']) != 0:
            argscheck += ['-o', " ".join(act[1]['general']['imap_options'])]
        argscheck += [data['key']]
        subprocess.Popen(argscheck, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(*argscheck)
