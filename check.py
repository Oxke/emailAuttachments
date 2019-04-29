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
import subprocess

__author__ = "Oxke"
__license__ = "GNU GPLv3.0"  # Read the file LICENSE for more information
__project__ = "emailAuto"

import argparse
import datetime
import re
import smtplib
from pathlib import Path

import imapclient
import pyzmail

from crypto import *

SENT = []
with open(including_root('nomehost.json')) as filenomehost:
    NOMEHOST = json.load(filenomehost)


def get_project_root() -> str:
    """Returns project root folder."""
    return Path(__file__).parent


def sendmail(args, email):
    with smtplib.SMTP(*NOMEHOST[email[0].split('@')[1]]['smtp']) as s:
        s.ehlo()
        s.starttls()
        s.login(*email)
        s.sendmail(*args)


def arg():
    global SENT
    config_folder = os.path.join(get_project_root(),
                                 "config_folder\\data_config")
    parser = argparse.ArgumentParser(description='Programmino per gestire le '
                                                 'auto email dalla classe ('
                                                 'principalmente)')
    parser.add_argument("key", help='chiave usata per filtrare le email '
                                    'classe ESABAC H')
    parser.add_argument("-d", "--destination", help='where to download '
                                                    'attachments')
    parser.add_argument("-f", "--folder", help='in which folder?')
    parser.add_argument("-n", "--number", help="number emails to receive",
                        type=int)
    parser.add_argument("-o", "--options", help="add imap options")
    parser.add_argument('-em', '--email', help='user_email_address')
    parser.add_argument('-pwd', '--password', help='user password')
    args = parser.parse_args()
    # noinspection PyUnresolvedReferences
    args.options = [option.strip() for option in args.options.split(' ')] if \
        args.options else []
    if args.folder is None:
        folder = os.path.join(args.destination, args.key)
    else:
        folder = os.path.join(args.destination, args.folder)

    if os.path.exists(os.path.join(config_folder, f'{args.key}.eaa')):
        data = decrypt_eaa(os.path.join(config_folder, f'{args.key}.eaa'))
        folder = data['folder']
        sent = glob(folder + "/*")
        sent = [os.path.split(path)[1] for path in sent]
        for file in sent:
            if not re.search('^\[.+]-([A-Z])([A-Z][a-z]+) (.+)', file):
                sent.remove(file)
        SENT += [file[file.index('-') + 1:file.index(' ')] for file in sent]

    else:
        try:
            os.mkdir(folder)
        except FileExistsError:
            in1 = input('Probabilmente avevi già creato il '
                        'progetto. Lo elimino (1) o lo apro in Esplora Risorse '
                        'per fartene vedere il contenuto più facilmente? (2) '
                        '-> ')
            if in1 == 1:
                shutil.rmtree(folder)
                os.mkdir(folder)
            elif in1 == 2:
                subprocess.run(['C:\\Windows\\explorer.exe', folder])
                input('Elimina Manualmente tutti i file che sono presenti in '
                      'quella cartella e poi premi invio, io creerò la nuova')
                if os.path.exists(folder):
                    shutil.rmtree(folder)
                os.mkdir(folder)

        data = {"key": args.key,
                "folder": folder,
                "number": args.number,
                "creationDate": str(datetime.date.today())}
        encrypt_eaa(os.path.join(config_folder, f'{args.key}.json'),
                    data=data)

    return data['key'], data['folder'], data['number'], args.options, (
        args.email,
        args.password)


def nhost(dominio):
    def chiedi(domin):
        imap = input('Non conosco questo dominio, sapresti dirmi qual è il '
                     'server imap? -> ')
        smtp = input('E quello smtp? -> ')
        NOMEHOST[domin] = {'imap': imap, 'smtp': smtp}
        with open(including_root('nomehost.json')) as fp:
            json.dump(NOMEHOST, fp)
        return nhost(domin)

    return NOMEHOST.get(dominio, chiedi(dominio))


def main(key, folder, number, imap_options, email):
    global msg, SENT
    print(f'Avanzamento della raccolta "{key}"')
    identifier_regex = re.compile(f'^\[{key}] (([A-Z])[a-z]+ ([A-Z][a-z]+))')
    with imapclient.IMAPClient(nhost(email[0].split('@')[1])['imap'],
                               ssl=True, use_uid=True) as imap_obj:
        imap_obj.login(*email)
        while len(SENT) < number:
            print(f'\r{len(SENT)}/{number}   {len(SENT) * 100 / number}%',
                  end="")
            imap_obj.select_folder("INBOX")
            uids = imap_obj.search([*imap_options,
                                    u"UNSEEN",
                                    u"SUBJECT", key])
            if uids:
                raw_messages = imap_obj.fetch(uids, 'BODY[]')
                for uid in uids:
                    message = pyzmail.PyzMessage.factory(
                        raw_messages[uid][b'BODY[]'])
                    res = identifier_regex.search(message.get_subject())
                    if res:
                        mex = f'Subject: Re: {message.get_subject()}\n{nofile}'
                        # noinspection PyUnresolvedReferences
                        for part in message.walk():
                            if part.get_content_maintype() == 'multipart':
                                continue
                            if part.get_content_disposition() is None:
                                continue
                            filename = f'[{key}]-{res.group(2) + res.group(3)} \
{part.get_filename()}'
                            if filename:
                                filepath = os.path.join(folder, filename)
                                if not os.path.isfile(filepath):
                                    with open(filepath, 'wb') as fp:
                                        fp.write(part.get_payload(decode=True))
                                mex = f'Subject: Re: ' \
                                    f'{message.get_subject()}\n{msg}'
                                SENT.append(res.group(3))

                    else:
                        print(f'NUOVA MAIL ILLEGALE da '
                              f'{message.get_addresses("from")}')
                        mex = error + f'"[{key}] Nome Cognome".\n\nGrazie per' \
                            f' l\'attenzione (anche lei dovrebbe ringraziare ' \
                            f'me a dirla tutta...) e arrivederci\n\nemailAuto'
                    mex = mex.encode('latin')
                    if (not re.search('^\[.+] [A-Z][a-z]+ [A-Z][a-z]+',
                                      message.get_subject())) or mex[9] != 'E':
                        sendmail((email[0], message.get_addresses('from')[0][1],
                                  mex), email)
                        imap_obj.delete_messages(uid)
                        imap_obj.expunge()

    print(f'\r{len(SENT)}/{number}   {len(SENT) * 100 / number}%',
          end="")
    print('\tRaccolta completata! Tutti hanno mandato il file!')
    input()


if __name__ == "__main__":
    msg = 'Ciao,\nGrazie per aver mandato correttamente ' \
          'l\'allegato, che è appena stato ricevuto e salvato ' \
          'automaticamente.\n\nGrazie e arrivederci\n\nemailAuto'
    error = "Subject: ERRORE! Non capisci niente!\nBuongiorno,\nmi spiace per" \
            " il disagio ma ci tengo a dirle che la sua mail non è stata " \
            "ricevuta correttamente a causa di un SUO errore nella " \
            "formattazione dell'oggetto, che mi ha impedito di riconoscerne " \
            "la corretta appartenenza. Ordunque, le consiglio di inviare di " \
            "nuovo la mail con l'oggetto che inizi in questo formato: "
    nofile = 'Ciao,\nGrazie per aver mandato correttamente la mail con ' \
             'l\'oggetto indicato nel modo corretto.\nLa informo però che io ' \
             'son pensato per gestire e scaricare gli allegati e inoltre non ' \
             'leggo mai il testo della mail. Quindi La informo che non ho ' \
             'trovato alcun allegato nella sua mail e che la mail non verrà ' \
             'letta né da un essere umano né tantomeno da me.\n\nDistinti ' \
             'Saluti in attesa di allegati\n\nemailAuto'
    main(*arg())
