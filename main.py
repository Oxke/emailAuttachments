#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#  Un progetto per selezionare e ordinare alcune mail ricevute
#  Copyright (C) 2019 Oxke
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
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
__project__ = "emailAuto"
__version__ = "v2.2.1"
__date__ = "2019-02-03"

import argparse
import datetime
import json
import os
import pprint
import subprocess
import sys
from pathlib import Path
from shutil import rmtree


def including_root(path) -> str:
    """Return absolute path"""
    return os.path.join(Path(__file__).parent, path)


def arg():
    with open(including_root('config_folder\\settings.json')) as def_sett_file:
        def_settings = json.load(def_sett_file)
    with open(including_root(def_settings['general']["settings"])) as sett_file:
        dati = json.load(sett_file)
    parser = argparse.ArgumentParser(description='Programmino per gestire le '
                                                 'auto email contenenti '
                                                 'allegati')
    parser.add_argument('-i', '--info', help='prima di iniziare il programma '
                                             'stampa le impostazioni',
                        action='store_true')
    subparsers = parser.add_subparsers(help='Possibili quattro '
                                            'diversi tipi di azione',
                                       dest='command')
    parser1 = subparsers.add_parser('Main', help='Main action')
    parser1.add_argument("-s", "--settings", help='choose settings file')
    parser1.add_argument("-d", "--destination", help='where to download '
                                                     'attachments')
    parser1.add_argument("-f", "--folder", help='in which folder?')
    parser1.add_argument("-n", "--number", help="number emails to receive")
    parser1.add_argument('-k', "--key", help='chiave usata per filtrare le '
                                             'email')
    parser1.add_argument('-o', '--options', help='imap options for selecting '
                                                 'emails')
    parser1.add_argument('-em', '--email', help='user_email_address')
    parser1.add_argument('-pwd', '--password', help='user password')
    parser1.add_argument("-ss", "--setsettings", help='create new file '
                                                      'settings')
    parser2 = subparsers.add_parser('Delete', help='help for Delete')
    parser2.add_argument('delete', help='distrugge tutto')
    args = parser.parse_args()
    if args.command == 'Main':
        if args.settings:
            with open(including_root(f'config_folder\\{args.settings}.json')) \
                    as setf:
                dati = json.load(setf)
        numb = 1
        def_key = dati['general']['def_key'].replace('$', str(numb))
        while os.path.exists(including_root(f'config_folder\\data_config\\'
                                            f'data_config_{def_key}.json')):
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
    else:
        raise argparse.ArgumentError('False Command')


if __name__ == "__main__":
    key, act, command = arg()
    config_f = including_root(f"config_folder\\data_config\\data_c"
                              f"onfig_{key}.json")
    if os.path.exists(config_f):
        with open(config_f) as jsn:
            data = json.load(jsn)
    else:
        data = {
            'creationDate': str(datetime.date.today()),
            'key': key,
            'folder': os.path.join(act[1]['general']['def_dest'], key),
            'number': act[1]['general']['def_number'],
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
        if input(f'Vuoi che il file settings {name} diventi di default? -> '
                 f'').lower() not in ('no', 'n'):
            with open(including_root('config_folder\\settings.json')) as sf:
                d = json.load(sf)
            with open(including_root('config_folder\\settings.json'),
                      'w') as sf:
                d['general']['settings'] = f'config_folder\\{name}.json'
                json.dump(d, sf)
        with open(including_root(f'config_folder\\{name}.json'), 'w') as sf:
            json.dump(setting, sf)
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
                     act[1]['email']['password'], data['key']]
        if len(act[1]['general']['imap_options']) != 0:
            argscheck += ['-o', " ".join(act[1]['general']['imap_options'])]
        subprocess.Popen(argscheck, creationflags=subprocess.CREATE_NEW_CONSOLE)
        print(*argscheck)
