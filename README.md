# emailAuttachments
> Progetto per gestire email automatiche e ricezione automatica e sistematica 
di allegati email

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-372/)[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FOxke%2FemailAuttachments.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FOxke%2FemailAuttachments?ref=badge_shield)

##
Potete usare questo progetto per controllare email di un certo tipo (si 
possono usare gli attributi di imaplib per selezionare le email in arrivo) e 
scaricare gli allegati in modo sistematico e ordinato.

Al primo avvio saranno da impostare molte delle possibili preferenze, ma già 
dalla seconda si può riutilizzare un set di preferenze chiamato 'settings 
file' salvato la prima volta con un nome a scelta.

I file settings sono salvati come `*.eaa` (EmailAuttachments -> 
EmailAuto-Attachments) e per una questione di sicurezza sono crittati, 
perciò, a meno che non si chieda l'help, verrà sempre chiesto di inserire 
una password. (Anche se è sconsigliabile, in casi di necessità di maggiore 
sicurezza è possibile usare per un file settings una diversa password)s

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
usage: main.py [-h] [-i] {[Main],Delete} ...

Programmino per gestire le auto email contenenti allegati. Se non si specifica
un subparser, verrà considerato il "Main", a meno che non si chiami l'help e
in questo modo si otterrà quello generale. Per ottenere l'help del "Main"
basterà quindi chiamare "python main.py Main -h"

positional arguments:
  {Main,Delete}  Possibili quattro diversi tipi di azione
    Main         Main action
    Delete       help for Delete

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

Infine il sottoparser "Delete" richiede solamente di inserire il nome della Raccolta da eliminare.

## Thirdy-part modules
Il programma necessita di:
* IMAPclient
* pyCryptoDome
* pyzmail

per poter funzionare

## License
Un progetto per selezionare e ordinare alcune mail ricevute
Copyright (C) 2019 Oxke

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
