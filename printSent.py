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

import argparse
import glob
import os
import re
import time


def arg():
    parser = argparse.ArgumentParser(description='check SENT')
    parser.add_argument('folder', help='folder')
    parser.add_argument('-k', '--key', help='key')
    parser.add_argument('-n', '--number', type=int, help='number', default=20)
    args = parser.parse_args()
    key = os.path.split(args.folder)[1] if args.key is None else args.key
    return args.folder, key, args.number


def main(folder, key, number):
    regex = re.compile('^\[.+]-([A-Z])([A-Z][a-z]+) (.+)')
    sent = {}
    while len(sent) < number:
        os.system('cls')
        print(f'Persone che hanno inviato l\'allegato per la raccolta "{key}"')
        sent = glob.glob(folder + "/*")
        sent = [os.path.split(path)[1] for path in sent]
        resses = []
        for file in sent:
            res = regex.search(file)
            if res:
                resses.append(res)
        sent = {f'{res.group(1)}. {res.group(2)}': res.group(3) for res in
                resses}
        for who, what in sent.items():
            print(f"{who} - {what}")
        print()
        for i in range(9, 0, -1):
            print(f'\rAggiornamento tra {i}', end='')
            time.sleep(1)
        wheel = '/-\\|'
        for i in range(20):
            print(f'\rAggiornamento{"." * (i % 4) + " " * (3 - (i % 4))}'
                  f'  {wheel[i % 4]}', end='')
            time.sleep(0.1)
    print("\rTutti hanno mandato il file!")
    input()


if __name__ == '__main__':
    main(*arg())
