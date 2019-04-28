#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
__license__ = "GNU GPLv3.0"  # Read the file LICENSE for more information
__project__ = "emailAuto"
"""Questa parte di programma è una sezione più user-friendly e serve a 
visualizzare e modificare le possibili preferenze del programma"""

import subprocess
import sys
from glob import glob
from pprint import pprint
from shutil import rmtree

from crypto import *
from main import including_root


def modify(ch):
    data = decrypt_eaa(fin_cf[int(ch[1]) - 1])
    tomod = input('Ci sono impostazioni in "email" (1) o "general" ('
                  '2) che vuoi modificare? (vuoto per continuare) -> ')
    while tomod != '':
        if tomod == '1':
            tomod2 = input("modificare 'email' (1), 'password' (2) o "
                           "niente (lasciare vuoto)? -> ")
            while tomod2 != '':
                tomod2 = {'1': 'email', '2': 'password'}[tomod2]
                data['email'][tomod2] = input(f'Inserire '
                                              f'la nuova {tomod2} -> ')
                tomod2 = ("modificare 'email' (1), 'password' (2) o "
                          "continuare (lasciare vuoto)? -> ")
        elif tomod == '2':
            tomod2 = input('''modificare:
1 - "def_key" = il nome della raccolta (includere "$" per indicare un numero)
2 - "imap_options" = le opzioni imap per la ricezione dei file
3 - "def_dest" = directory di destinazione degli allegati
4 - "def_number" = numero di mail attese
5 - "def_info" = se visualizzare o no le informazioni

scegliere o lasciare vuoto per annullare -> ''')
            while tomod2 != '':
                tomod2 = {
                    '1': 'def_key',
                    '2': 'imap_options',
                    '3': 'def_dest',
                    '4': 'def_number',
                    '5': 'def_info'
                }[tomod2]
                if tomod2 == 'def_info':
                    data['general']['def_info'] = not data['general'][
                        'def_info']
                    if data['general']['def_info']:
                        print('Ora le informazioni si vedranno')
                    else:
                        print('Ora le informazioni non si vedranno più')
                else:
                    data['general'][tomod2] = input(f'Inserire la nuova '
                                                    f'{tomod2} -> ')
                tomod2 = input('''modificare:
1 - "def_key" = il nome del file settings
2 - "imap_options" = le opzioni imap per la ricezione dei file
3 - "def_dest" = directory di destinazione degli allegati
4 - "def_number" = numero di mail attese
5 - "def_info" = se visualizzare o no le informazioni

scegliere se modificare altro o lasciare vuoto per continuare -> ''')
        tomod = input('Ci sono altre impostazioni in "email" (1) o '
                      '"general" (2) che vuoi modificare?'
                      ' (vuoto per continuare) -> ')
    return data


def choix1(ch1):
    ch2 = None
    if ch1 == '1':
        print()
        for file in fin_cf:
            fname = os.path.splitext(os.path.split(file)[-1])[0]
            print(f"{fin_cf.index(file) + 1} - {fname}")
        ch2 = input(f"""\
{len(fin_cf) + 1} - File settings di default
{len(fin_cf) + 2} - Torna Indietro

Se scrivi un numero corrispondente a un file, potrai visualizzare il loro 
contenuto e modificarlo, altrimenti tornare indietro -> """)
    elif ch1 == '2':
        print()
        for file in fin_dc:
            fname = os.path.splitext(os.path.split(file)[-1])[0]
            print(f"{fin_dc.index(file) + 1} - {fname}")
        ch2 = input(f"""\
{len(fin_dc) + 1} - Torna Indietro

Se scrivi un numero corrispondente a un file, potrai visualizzare il loro 
contenuto e modificarlo, altrimenti tornare indietro -> """)
    elif ch1 == '3':
        print('Allora arrivederci')
        input()
        exit()
    else:
        print()
        setup()
    print()
    choix2(ch1 + ch2)


def choix2(ch2):
    fsettings = None
    if ch2[0] == '1':
        if int(ch2[1]) == len(fin_cf) + 2:
            print()
            setup()
        elif int(ch2[1]) == len(fin_cf) + 1:
            with open(including_root('config_folder\\settings.json')) as fp:
                fsettings = json.load(fp)
        else:
            fsettings = decrypt_eaa(fin_cf[int(ch2[1]) - 1])
        pprint(fsettings)
        print("""
1 - Modifica
2 - Crea una nuova raccolta usando questo file settings di base
3 - Crea un nuovo file settings sulla base di questo
4 - Imposta come predefinito
5 - Elimina file settings
6 - Torna alla scelta del file settings
7 - Torna al menù principale
""")
    elif ch2[0] == '2':
        if int(ch2[1]) == len(fin_dc) + 1:
            print()
            setup()
        else:
            fsettings = decrypt_eaa(fin_dc[int(ch2[1]) - 1])
        pprint(fsettings)
        print("""
1 - Modifica folder (cartella di destinazione della Raccolta)
2 - Modifica key (nome della Raccolta)
3 - Modifica number (numero di email attese)
4 - Elimina Raccolta
5 - Torna alla scelta della Raccolta
6 - Torna al menù principale
""")
    else:
        print()
        setup()
    print()
    choix3(ch2 +
           input("Inserisci il numero corrispondente alla tua scelta -> "))


def choix3(ch3):
    global fin_cf, fin_dc
    if ch3[0] == '1':  # config_folder
        try:
            if ch3[2] == '1':  # Modifica
                data = modify(ch3)
                encrypt_eaa(fin_cf[int(ch3[1]) - 1][:-4], data=data)
                print()
                choix2(ch3[:2])
            elif ch3[2] == '2':  # Crea nuova raccolta con questo base setfile
                data = modify(ch3)
                pprint(data)
                args = [sys.executable, including_root('main.py')]
                if data['general']['def_info']:
                    args += ['-i']
                args += ['Main', '-em', data['email']['email'],
                         '-pwd', data['email']['password'],
                         '-o', " ".join(data['general']['imap_options']),
                         '-d', data['general']['def_dest'],
                         '-n', str(data['general']['def_number'])]
                pprint(args)
                subprocess.Popen(args,
                                 creationflags=subprocess.CREATE_NEW_CONSOLE)
                exit()
            elif ch3[2] == '3':  # Crea nuovo file settings sulla base di questo
                name = input("Come vuoi chiamare questo nuovo file settings ("
                             "lascia vuoto per annullare) -> ")
                if name != '':
                    data = modify(ch3)
                    encrypt_eaa(including_root(f'config_folder\\{name}.json'),
                                data=data)
                print()
                choix1(ch3[0])
            elif ch3[2] == '4':  # Imposta come predefinito
                with open(including_root('config_folder\\settings.json')) as fp:
                    data = json.load(fp)
                with open(including_root('config_folder\\settings.json'),
                          'w') as \
                        fp:
                    data['general']['settings'] = fin_cf[int(ch3[1]) - 1]
                    json.dump(data, fp)
                print('\nFatto! Ora Ti rimando al menù principale\n')
                setup()
            elif ch3[2] == '5':  # Elimina file settings
                if fin_cf[int(ch3[1]) - 1] != including_root(
                        'config_folder\\settings.json'):
                    if input(f'Sicuro di eliminare il file settings ? -> '
                             f'').lower() not in ['no', 'n']:
                        os.remove(fin_cf[int(ch3[1]) - 1])
                    fin_cf = glob(including_root('config_folder\\*.eaa'))
                    print()
                else:
                    print("\nERRORE! Impossibile Eliminare\n")
                choix2(ch3[:2])
            elif ch3[2] == '6':  # Torna alla scelta del file settings
                print()
                choix1(ch3[0])
            else:  # Torna al menù principale
                print()
                setup()
        except FileNotFoundError:
            print('Ma sei scemo? L\'hai appena eliminato, non ricordi?')
            choix1(ch3[0])

    if ch3[0] == '2':  # Raccolte (data_config)
        if ch3[2] == '1':  # Modifica folder
            data = decrypt_eaa(fin_dc[int(ch3[1]) - 1])
            data['folder'] = input('Inserisci la nuova folder -> ')
            encrypt_eaa(fin_dc[int(ch3[1]) - 1][:-4], data=data)
        elif ch3[2] == '2':  # Modifica key
            data = decrypt_eaa(fin_dc[int(ch3[1]) - 1])
            data['key'] = input('Inserisci la nuova key -> ')
            encrypt_eaa(fin_dc[int(ch3[1]) - 1][:-4], data=data)
        elif ch3[2] == '3':  # Modifica number
            data = decrypt_eaa(fin_dc[int(ch3[1]) - 1])
            data['number'] = input('Inserisci il nuovo number -> ')
            encrypt_eaa(fin_dc[int(ch3[1]) - 1][:-4], data=data)
        elif ch3[2] == '4':  # Elimina Raccolta
            data = decrypt_eaa(fin_dc[int(ch3[1]) - 1])
            if input(f'Sicuro di eliminare la Raccolta ? -> '
                     f'').lower() not in ['no', 'n']:
                rmtree(data['folder'])
                os.remove(fin_dc[int(ch3[1]) - 1])
                print('Eliminata!')
            choix1(ch3[0])
            fin_dc = glob(including_root('config_folder\\data_config\\*.eaa'))
        elif ch3[2] == '5':  # Torna alla scelta della Raccolta
            print()
            choix1(ch3[0])
        else:  # Torna al menù principale
            print()
            setup()
        print()
        choix2(ch3[:2])
    else:
        print()
        setup()


def setup():
    global fin_dc, fin_cf
    fin_cf = glob(including_root('config_folder\\*.eaa'))
    fin_dc = glob(including_root('config_folder\\data_config\\*.eaa'))
    ch1 = input("""\
1 - File settings
2 - Raccolte
3 - Arresta il programma

Scegli cosa vuoi visualizzare scrivendo il numero corrispondente -> """)
    choix1(ch1)


if __name__ == "__main__":
    setup()
