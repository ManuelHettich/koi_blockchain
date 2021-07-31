# blockchain_project
Blockchain Server and Client for Netzwerkprogrammierung (SS 2021)

Dieses Projekt stellt eine Interpretation eines Blockchain-Netzwerks dar. Es besteht aus einem Server und einem Client,
welche miteinander kommunizieren können. Der Client kann Dateien (Texte, Bilder, etc.) einlesen, in einzelne
Blöcke unterteilen und diese an den Server schicken. Der Server kann diese Blöcke empfangen, ihren Erhalt bestätigen
und sie nicht-transient in einer kontinuierlichen Liste (Chain) abspeichern. Der Client kann zudem beim Server anfragen, 
ob einzelne Dateien bereits abgespeichert worden sind. Diese Anfragen werden vom Server geprüft und beantwortet. Beim
Empfang von Blöcken einer Datei gibt der Server auch immer an, ob diese Datei für ihn neu ist.

Die Blöcke bilden auf dem Server eine kontinuierliche Liste, indem sie jeweils den vorherigen Block anhand seines
individuellen Hashes referenzieren. Außerdem enthält jeder Block den Hash der originalen Datei, die Anzahl der 
Blöcke, die zu dieser Datei gehören, und einen 500 byte großen Abschnitt der originalen Datei. Bei der Aufspaltung
einer neuen Datei fragt der Client immer zuerst beim Server den Hash des dort zuletzt vorhandenen Blockes an, um
an diesem richtig anzuknüpfen.

_Optionale Zusatzfunktionalität_: Der Server kann außerdem feststellen, ob die Integrität der Chain noch erhalten ist.
Dafür beginnt er bei dem ersten Block und hangelt sich von diesem zu dem jeweils folgenden, bis das Ende der Chain
erreicht wurde und jeder Block korrekterweise den jeweils vorherigen Block mittels des spezifischen Block-Hashes 
referenziert.


## Starten des Servers
Server starten, wenn man sich im Hauptordner des Projekts befindet:

`$ python3 -m src.server`


## Starten & Verwendung des Clients
Client starten, wenn man sich im Hauptordner des Projekts befindet:

`$ python3 -m src.client 127.0.0.1 8000`

Anschließend können Dateien zu dem verbundenen Server gesendet werden und es kann geprüft werden,
ob einzelne Dateien bereits auf dem Server gespeichert worden sind. Dafür können die Befehle `send` bzw. `check`
mit der Angabe des relativen Pfads der jeweiligen Datei verwendet werden. Nach jedem Befehl wird die Antwort des Servers ausgegeben.
Nachfolgend ist ein beispielhafter Programmablauf angegeben:

```
[send] / [check] a local file (relative path from root folder), check the [integrity] of the server chain or [quit]
> send test_files/isaac-martin-61d2hT57MAE-unsplash.jpg
Response from Server: {'success': True, 'new_file': True, 'hash': '45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12', 'index_all': 5285}
> check test_files/isaac-martin-61d2hT57MAE-unsplash.jpg
Response from Server: {'check': True, 'hash': '45f293033312d42815155e871f37b56b4de9b925c07d4a5f6262320c1627db12'}
> check test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg
Response from Server: {'check': False, 'hash': '415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9'}
> send test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg
Response from Server: {'success': True, 'new_file': True, 'hash': '415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9', 'index_all': 1704}
> send test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg
Response from Server: {'success': True, 'new_file': False, 'hash': '415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9', 'index_all': 1704}
> check test_files/debashis-rc-biswas-3U4gGsGNsMY-unsplash.jpg
Response from Server: {'check': True, 'hash': '415d4f66e1b8b9083014dcdca5ddd7d1dcca3f5a4a120603169b951b1c5fa0c9'}
> integrity
Response from Server: {'integrity_check': True}
```


## Tests
Alle Tests der wichtigsten Funktionen werden mit pytest anhand des folgenden Befehlsaufrufs im Hauptordner
des Projekts durchgeführt: 

`$ pytest`


## Importierte Third-Party Packages
* **fastapi**: Web framework for building APIs with Python 3.6+ based on standard Python type hints
* **uvicorn**: Notwendig, um den Server mit FastAPI zu starten
* **python-multipart**: Notwendig, um große Dateien als Teil eines POST-Requests zu versenden
* **requests**: Notwendig, um HTTP-Anfragen an den Server zu schicken (REST-API)
* **pytest**: Notwendig, um die Tests in Python durchzuführen

Alle importierten packages sind in requirements.txt aufgelistet und sind ggf. Dependencies der hier aufgelisteten packages.