# URN Checker

Dieser Code beschreibt einen minimalen Ansatz zur Überwachung eigener URNs und den damit verknüpften URLs. 
Dieser kann manuell oder teilautomatisiert zu einen selbstbestimmten Zeitpunkt ausgeführt werden.

Benötigt werden Python3, der Paketmanager pip3 und das Framework [Scrapy](https://scrapy.org). 
Des Weiteren wird eine Liste mit URNs/URLs benötig, welche getestet werden sollen. Eine von dem URN-Service der DNB zur Verfügung gestellten CSV Liste aller URN/URLs ist beispielsweise `URN;URL;URN_ID` aufgebaut.
Benötigt werden: 
- Python 3
- pip3
- Scrapy

Der Code kann mittels `scrapy runspider urnChecker.py  --logfile spider.log`ausgeführt werden.

Die sogenannte Standardausgabe könnte mittel `>` in eine separate Datei umgeleitet werden. 

Zu beachten ist, dass das Schließen der Konsole die Ausführung der Software abbricht. Unter Unix Systemen kann hier beispielsweise das Tool screen eingesetzt werden, um den Prozess im Hintergrund weiterlaufen zu lassen oder beispw. ein `systemd` Dienst angelegt werden.

Zur Aufgabensteuerung kann `crontab` oder `systemd.timer` verwendet werden.

Wird das Programm gestartet, wird zuerst die Funktion start_requests ausgeführt. Diese öffnet eine Datei `urnFileFromDNB.csv` bzw. die `URN;URL;URN_ID` Liste, durchläuft diese zeilenweise und gibt die URLs an das Framework weiter. 

Ist eine URL aufrufbar wird, die Funktion `parse()` aufgerufen.
Hier könnte ebenfalls der Programmcode erweitert werden, wenn beispielsweise eine Soft-404(siehe unten) Prüfung durchgeführt werden soll. 

```python
audit = difflib.SequenceMatch(None,nonExistingWebsiteCode,WebsiteCode,autojunk=False)
```

Ebenfalls können in dieser Funktion die Anzahl, Gründe von Weiterleitungen und deren URLs ermittelt werden.

``` python
redirect_times = str(meta['redirect_times']) if 'redirect_times' in meta else ''
        redirect_urls = ' '.join(str(x) for x in meta['redirect_urls']) if 'redirect_urls' in meta \
            else '' # List of all redirected urls
        redirect_reasons = ' '.join(str(x) for x in meta['redirect_reasons']) if 'redirect_reasons' in meta \
            else '' # list of all redirected http statuscode reasons
```

Die relevante Funktion in diesem Szenario ist die `error_parse()` Funktion. Diese Funktion wurde dem scrapy.Request Generator als Callback Methode mitgegeben und wird aufgerufen, wenn für eine Anfrage ein anderer Statuscode als `200 ok` zurückgegeben wird. Hier wird zwischen `4XX` und `5XX` HTTP Statuscodes, DNS Lookup Fehlern und Timeout unterschieden. 

## Soft 404
Ziel ist es mit Hilfe einer Testabfrage einen `404 not found` Fehler zu provozieren, um zu erkennen, ob ein Server für Soft-404 anfällig ist. Liefert ein Server auf eine falsche Anfrage einen `200 ok` ist der Server als Soft-404 Fehler anfällig. Der Quelltext dieser falschen `200 Ok` Anfrage, kann dann mit anderen Anfragen verglichen werden. Stimmen diese zu über X Prozent überein, handelt es sich um einen Soft-404 Fehler.

[1] Tomkins, Andrew, Ziv Bar-Yossef, Andrei Z. Broder und Ravi Kumar (Jan. 2004). Sic Transit Gloria Telae: Towards an Understanding of the Web’s Decay. url: https://web.archive.org/web/20080127185404/http://www.tomkinshome.com/andrew/papers/decay/final/p444-baryossef.htms