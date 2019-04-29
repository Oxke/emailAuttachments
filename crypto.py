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

import getpass
import json
import os
import shutil
import struct
from glob import glob

import keyring
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256

from main import including_root


def encrypt_eaa(in_filename, data=None, out_filename=None, chunksize=64 * 1024):
    key_pwd = os.path.splitext(os.path.split(in_filename)[-1])[0]
    service = os.path.split(os.path.split(in_filename)[-2])[-1]
    key = getpass.getpass(f'Quale vuoi che sia la password per '
                          f'"{os.path.split(in_filename)[-1]}"? '
                          f'(lascia vuoto e imposterò questa '
                          f'password come la MasterPassword)-> ')
    if key == '':
        key = keyring.get_password('emauto', 'master')
        if key is None:
            key = getpass.getpass('Impostare la MasterPassword -> ')
            keyring.set_password('emauto', 'master', key)
    keyring.set_password(service, key_pwd, key)
    if in_filename[-5:] != '.json':
        in_filename += '.json'
    if data:
        with open(in_filename, 'w') as fp:
            json.dump(data, fp)
    if not out_filename:
        out_filename = in_filename[:-5] + '.eaa'
    key = SHA3_256.new().update(key.encode()).digest()
    iv = Random.new().read(AES.block_size)
    encryptor = AES.new(key, AES.MODE_CBC, IV=iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % AES.block_size != 0:
                    chunk += b' ' * (AES.block_size - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))

    os.remove(in_filename)


def decrypt_eaa(in_filename, key=None, out_filename=None, chunksize=64 * 1024):
    key_pwd = os.path.splitext(os.path.split(in_filename)[-1])[0]
    service = os.path.split(os.path.split(in_filename)[-2])[-1]
    key = key if key else keyring.get_password(service, key_pwd)
    if key is None:
        key = getpass.getpass(f'Non conosco la password per '
                              f'"{os.path.split(in_filename)[-1]}", '
                              f'inseriscila (se lasci vuoto, provo a usare la '
                              f'MasterPassword)-> ')
        if key == '':
            key = keyring.get_password('emauto', 'master')
            if key is None:
                key = getpass.getpass('Impostare la MasterPassword -> ')
                keyring.set_password('emauto', 'master', key)
        keyring.set_password(service, key_pwd, key)

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    key = SHA3_256.new().update(key.encode()).digest()
    try:
        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, IV=iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    decd = decryptor.decrypt(chunk)
                    n = len(decd)
                    if origsize > n:
                        outfile.write(decd)
                    else:
                        outfile.write(decd[:origsize])
                    origsize -= n

            with open(out_filename) as fp:
                data = json.load(fp)
        os.remove(out_filename)
        return data
    except UnicodeDecodeError:
        k_m = getpass.getpass('Mi spiace, la password o il nome del file '
                              'risultano errati! Provare a reinserire la '
                              'password, altrimenti scrivi "pescegatto" per '
                              'avviare la rimozione forzata (lasciando '
                              'vuoto invece proverò ad usare la '
                              'MasterPassword)--> ')
        keyring.delete_password(service, key_pwd)
        if k_m == 'pescegatto':
            for file_settings in glob(including_root('config_folder\\*.*')):
                if file_settings == including_root(
                        'config_folder\\settings.json'):
                    with open(file_settings) as fp:
                        d = json.load(fp)
                    f = d['general']['def_dest']
                else:
                    f = decrypt_eaa(file_settings)['general']['def_dest']
                if key_pwd in map(lambda x: os.path.split(x)[-1],
                                  next(os.walk(f))[1]):
                    print('Trovata la cartella di destinazione del file')
                    shutil.rmtree(os.path.join(f, key_pwd))
                    break
            else:
                a = input('Non ho trovato la Raccolta negli indirizzi scritti '
                          'nei '
                          'file settings, tu sai dov\'è? (1 per dirmi la path),'
                          ' oppure me ne frego altamente ed elimino solo il '
                          'data_config? (2) -> ')
                if a == 1:
                    f = a
                    if key_pwd in map(lambda x: os.path.split(x)[-1],
                                      next(os.walk(f))[1]):
                        shutil.rmtree(os.path.join(f, key_pwd))
                    else:
                        print('Ahahah no. Bello prendermi in giro ma quella '
                              'non è la cartella dove sono immagazzinati gli '
                              'allegati')
                        f = input('Riscrivimi la path della cartella '
                                  'corretta, stavolta, altrimenti io elimino '
                                  'solo il data_config e poi son cavoli tuoi '
                                  'se mentre fai altre raccolte trovi errori')
                        if key_pwd in map(lambda x: os.path.split(x)[-1],
                                          next(os.walk(f))[1]):
                            shutil.rmtree(os.path.join(f, key_pwd))
            os.remove(in_filename)
            print('Raccolta eliminata...')
            input()
            exit()

        elif k_m == '':
            decrypt_eaa(in_filename, key=keyring.get_password('emauto',
                                                              'master'))
        else:
            keyring.set_password(service, key_pwd, k_m)
            decrypt_eaa(in_filename, key=k_m)


def keyringdel(in_filename):
    key_pwd = os.path.splitext(os.path.split(in_filename)[-1])[0]
    service = os.path.split(os.path.split(in_filename)[-2])[-1]
    keyring.delete_password(service, key_pwd)
