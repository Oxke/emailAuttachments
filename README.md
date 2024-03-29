# emailAuttachments
> Progetto per gestire email automatiche e ricezione automatica e sistematica 
di allegati email

[![GitHub release](https://img.shields.io/github/release/Oxke/emailAuttachments.svg)](https://GitHub.com/Oxke/emailAuttachments/releases/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-372/)
[![GitHub license](https://img.shields.io/github/license/Oxke/emailAuttachments.svg)](https://github.com/Oxke/emailAuttachments/blob/master/LICENSE)
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FOxke%2FemailAuttachments.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FOxke%2FemailAuttachments?ref=badge_shield)

##
Potete usare questo progetto per controllare email di un certo tipo (si 
possono usare gli attributi di imaplib per selezionare le email in arrivo) e 
scaricare gli allegati in modo sistematico e ordinato.

Al primo avvio saranno da impostare molte delle possibili preferenze, ma già 
dalla seconda si può riutilizzare un set di preferenze chiamato 'settings 
file' salvato la prima volta con un nome a scelta.

I file settings sono salvati come `.eaa` (EmailAuttachments -> 
EmailAuto-Attachments) e per una questione di sicurezza sono crittati, perciò
bisognerà ogni volta che si crea un progetto scrivere la password di 
crittatura, che verrà salvata da keyring. Per comodità, esiste una 
MasterPassword impostabile e che può essere applicata a un file quando si sta
 creando una nuova raccolta scrivendo come password '' (ossia lasciando 
 vuoto). La prima volta che lo si fa chiederà di inserire una MasterPassword.

Viene chiamata "Raccolta" tutta l'operazione di controllo e salvataggio degli 
allegati.
  
#### Boot
Il modo più consigliato di avviare il programma è creando un file `.bat` che
avvii il main.py ed eseguirlo (su windows anche dalla _run dialog box_). Il 
main avvierà gli altri due programmi. Si può anche avviare direttamente il 
file check.py ma è sconsigliabile perché:
1. A differenza del main.py nel check e nel printSent è necessario scrivere da 
riga di comando tutte le informazioni necessario e non possono essere 
importati i file di impostazioni.
2. Il programmma è pensato per poter sempre vedere in contemporanea la 
finestra di quanti hanno risposto in percentuale (che è la finestra che 
lavora sincronizzandosi) e di che file sono arrivati.

## Screenshot
![Screenshot](http://oxke.altervista.org/screenshots/Capture.PNG)

## Documentation
Questo l'help di argparse (ottenibile con il comando `python main.py -h`):
  ```
usage: main.py [-h] [-i] {[Main], Delete, Settings} ...

Programmino per gestire le auto email contenenti allegati. Se non si specifica
un subparser, verrà considerato il "Main", a meno che non si chiami l'help e
in questo modo si otterrà quello generale. Per ottenere l'help del "Main"
basterà quindi chiamare "python main.py Main -h"

positional arguments:
  {Main,Delete,Settings}  Possibili quattro diversi tipi di azione
    Main                  Main action
    Delete                help for Delete
    Settings              Settings made easy

optional arguments:
  -h, --help     show this help message and exit
  -i, --info     prima di iniziare il programma stampa le impostazioni
```

Per il main riscrivo i vari argomenti in una tabella:

Comando | Funzione
------- | --------
-s {settings}| Scegli il file settings da cui importare le impostazioni
-d {destinazione}| Scegli la directory dove creare la cartella dove salverai gli allegati email
-f {folder}| Scegli il nome della cartella dove salvare gli allegati email
-n {number}| Il numero di mail da ricevere per dire terminata una Raccolta
-o {opzioni}| Aggiungi opzioni imaplib
-em {email}| Scrivi il tuo indirizzo email
-pwd {password}| Scrivi la password del tuo account
-ss {settings}| Usate questo comando per salvare la configurazione delle preferenze corrente
key | Unico comando posizionale, è il nome che la nuova Raccolta dovrà avere. 
Può anche essere omessa, in questo caso verrà generato un nome in base alle 
impostazioni del file settings di default.

Il sottoparser "Delete" richiede solamente di inserire il nome della Raccolta
 da eliminare.
 
 Il subparser "Settings", invece, permette di visualizzare tutti i file 
 settings e tutte le raccolte e di gestirle, ma essendo molto più 
 user-friendly, non mi soffermerò a descriverne i contenuti, che si possono 
 facilmente capire dal programma stesso.

## Thirdy-part modules
Il programma necessita di:
* IMAPclient
* pyCryptoDome
* pyzmail36
* keyring

per poter funzionare

#### Installation
Per installare i moduli di terze parti richiesti è possibile semplicemente 
scrivere da linea di comando dalla cartella dove è salvato il programma "py 
setup.py install" e installerà tutti i moduli richiesti. Successivamente si 
potrà semplicemente avviare il file main.py.

## License
Un progetto per selezionare e ordinare alcune mail ricevute
Copyright (C) 2019 Oxke

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
