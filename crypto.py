#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
__license__ = "GNU GPLv3.0"  # Read the file LICENSE for more information
__project__ = "emailAuto"

import json
import os
import struct

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256


def encrypt_eaa(key, in_filename, data=None, out_filename=None,
                chunksize=64 * 1024):
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


def decrypt_eaa(key, in_filename, out_filename=None, chunksize=64 * 1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]
    key = SHA3_256.new().update(key.encode()).digest()

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
