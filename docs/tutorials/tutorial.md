```package
iot-cube=github:Smartfeld/pxt-iot-cube#v1.1.2
sensors=github:Smartfeld/pxt-sensorikAktorikSmartfeld
```

# Alarmanlage

## Willkommen!
In diesem Tutorial entwickelst du eine Alarmanlage, die bei einem Diebstahl deines bewachten Objekts
einen Alarm abgibt und dich das über das Dashboard wissen lässt.

## Wichtig! @showdialog
Stecke den **Ultraschallsensor** am **Port J2** an.  

![Tutorialbild](https://github.com/kosta11111/SmartAlarmanlage/blob/master/docs/imgs/IoTCube.png?raw=true) 

Falls du **Probleme** beim Tutorial hast, kannst du beim Klicken auf der **Glühbirne** sehen,
wie der Code ausschauen soll.
![Tutorialbild](https://github.com/kosta11111/SmartAlarmanlage/blob/master/docs/imgs/Gl%C3%BChbirne.png?raw=true)

## Schritt 1

Als ersten Schritt **ziehen** wir eine ``||logic:Wenn-Abfrage||`` 
in den ``||basic:dauerhaft||`` Codeblock **rein**. Das ist wichtig, um zu prüfen,
ob unser Objekt noch da ist.

```blocks 
basic.forever(function () {
    if (true) {
    }
})
```

## Schritt 2

Jetzt wollen wir, dass der Cube einen Alarm schlägt, wenn der Ultraschallsensor
nichts in 10 cm Reichweite erkennt.

* **Ziehe** den ``||logic:Vergleichscodeblock||`` in das **Sechseck** der **Wenn-Abfrage** rein.
* **Benutze** den ``||smartfeldSensoren:Distanz in cm||`` Codeblock, um zu **prüfen**,
ob der gemessene Wert **größer als 10** ist.
* ``||music:spiele Ton||`` kommt in die Abfrage. Änder den Schlag auf 1/2, um einen
typischen Alarmsound zu bekommen

```blocks
basic.forever(function () {
    if (smartfeldSensoren.measureInCentimetersV2(DigitalPin.P1) > 10) {
        music.play(music.tonePlayable(262, music.beat(BeatFraction.Half)), music.PlaybackMode.UntilDone)
    } 
})
```
## Schritt 3

Der IoT-Cube funktioniert jetzt als eine Alarmanlage, aber man kann diese nicht deaktivieren.
Das Deaktivieren implementieren wir mit den A + B-Knöpfen.

* **Ziehe** den ``||input: Wenn Knopf A geklickt||`` **zweimal** in das Programm und **ändere** 
bei einem der beiden Codeblöcken **den Buchstaben** auf ein **B** um.
* Erstelle eine neue ``||Variables:Variable||`` namens **"aktiv"**. Setze sie mit 
den Codeblöcken der gleichen Kategorie beim Betätigen von **A** auf **1** und beim Klicken 
von **B** auf **0**.
* Füge den ``||loops:während||`` Codeblock in den ``||basic:dauerhaft||`` Block hinzu 
und ziehe den dort bereits stehenden Code **in die Schleife**.
* **Ziehe** in den **Parameter** der Schleife die neue Variable ``||Variables:aktiv||``
rein.

Drücke auf **A**, um die Alarmanlage einzuschalten und auf **B**, um sie zu deaktivieren.

```blocks
input.onButtonPressed(Button.A, function () {
    aktiv = 1
})

input.onButtonPressed(Button.B, function () {
    aktiv = 0
})

basic.forever(function () {
    while (aktiv) {
        if (smartfeldSensoren.measureInCentimetersV2(DigitalPin.P1) > 10) {
            music.play(music.tonePlayable(262, music.beat(BeatFraction.Half)), music.PlaybackMode.UntilDone)
        } 
    }
})
```
## Schritt 4

Jetzt haben wir zwar eine Alarmanlage, aber noch keine Verbindung mit der Claviscloud.
Das wollen wir jetzt ändern. 😉

* **Ziehe** den ``||IoTCube:LoRa Netzwerk-Verbindung||`` Block in den ``||basic:beim Start||``
Block **rein**.
* **Ziehe** danach den ``||loops:während||`` Block rein und in seinen **Parameter** den 
``||logic:nicht||`` Block rein. In die Schleife kommt der ``||IoTCube:Gerätstatus-Bit||``
Block, der auf **"Verbunden"** gestellt ist.
* Während der IoT-Cube noch **nicht verbunden** ist, sollen die LED's unter ``||basic:zeige Symbol||``
ein X zeigen, sonst einen **Haken**.

```blocks
IoTCube.LoRa_Join(
eBool.enable,
eBool.enable,
10,
8
)
while (!(IoTCube.getStatus(eSTATUS_MASK.JOINED))) {
    basic.showIcon(IconNames.No)
}
basic.showIcon(IconNames.Yes)
```
## Schritt 5

Nun bauen wir eine Funktion, mit der wir Daten an die Claviscloud und so zum Dashboard
schicken können. Davor erstellst du 3 ``||variables:Variablen |`` mit dem Namen
**spaeterSenden**, **sendeErlaubnis** und **msBeiLetztemSenden**, setzt
die ersten zwei auf **falsch**, während die letzte Variable den Wert ``||control:Millisekunden||``
hat und fügst alle beim Start hinzu.

```blocks
IoTCube.LoRa_Join(
eBool.enable,
eBool.enable,
10,
8
)
while (!(IoTCube.getStatus(eSTATUS_MASK.JOINED))) {
    basic.showIcon(IconNames.Pitchfork)
}
basic.showIcon(IconNames.Yes)
spaeterSenden = false
sendeErlaubnis = false
msBeiLetztemSenden = control.millis()
```

## Schritt 6

Da wir unsere Variablen für die Funktion haben, erstellst du jetzt eine neue
``||functions:Funktion||`` mit dem namen **sendeDaten** mit 
einer Zahl als Parameter namens **status** und befolgst folgende Schritte.

* Zieh eine ``||logic:Wenn-Abfrage mit ansonsten||`` in die Funktion, die abfragt,
ob ``||control:Millisekunden||`` größer ist als die
``||variables: msBeiLetztemSenden |`` und addierst zur variable per 
``||math: + ||`` 5000, indem du den Matheblock in die rechte Seite der Abfrage ziehst.
* Zieh den ``||IoTCube:Wahrheitswert||`` Block mit **ID_0 = status** in die Abfrage rein
und sende mit dem ``||IoTCube:sende Daten||`` Block die Daten zur Claviscloud
* Setze danach ``||variables: spaeterSenden |`` auf falsch und die
``||variables: msBeiLetztemSenden |`` auf ``||control:Millisekunden||``. In
ansonsten setzt du ``||variables: spaeterSenden |`` auf wahr.

```blocks
function sendeDaten (status: number) {
    if (control.millis() > msBeiLetztemSenden + 5000) {
        IoTCube.addBinary(eIDs.ID_0, status)
        IoTCube.SendBufferSimple()
        spaeterSenden = false
        msBeiLetztemSenden = control.millis()
    } else {
        spaeterSenden = true
    }
}
```
## Schritt 7

Da du jetzt weißt, wie man ``||functions:Funktion||`` erstellt, machen wir zwei neue
mit dem Namen **objektSicher** und **objektGeklaut**.

* Wir machen eine neue ``||variables: Variable |`` namens **objektVorhanden**
und setzen sie in ``||functions:objektSicher||`` auf **1**, während wir sie in
``||functions:objektGeklaut||`` auf **0** setzen.
* In **beiden Funktionen** ziehst du den ``||functions:Aufruf sendeDaten||`` rein und ziehst
in den **Parameter** die ``||variables: objektVorhanden |`` Variable rein.

```blocks
function objektSicher () {
    objektVorhanden = 1
    sendeDaten(objektVorhanden)
}
function objektGeklaut () {
    objektVorhanden = 0
    sendeDaten(objektVorhanden)
}
```

## Schritt 8

Nun haben wir unsere zwei Funktionen, welche unserem Dashboard Bescheid geben,
ob unser Objekt vom Ultraschallsensor erfasst wird oder geklaut wurde.

* **Füge** den ``||functions:Aufruf objektSicher||`` in den **Start** hinzu, um
beim Starten den Programms das Dashboard auf den richtigen Zustand zu aktuallisieren.
* **Füge** den ``||functions:Aufruf objektGeklaut||`` in die ``||logic:Wenn-Abfrage||`` 
von dauerhaft **hinzu**, drücke auf das **Plus der Abfrage** und füge dann in  **ansonsten** den
``||functions:Aufruf objektSicher||`` hinzu.

```blocks
IoTCube.LoRa_Join(
eBool.enable,
eBool.enable,
10,
8
)
while (!(IoTCube.getStatus(eSTATUS_MASK.JOINED))) {
    basic.showIcon(IconNames.No)
}
basic.showIcon(IconNames.Yes)
spaeterSenden = false
sendeErlaubnis = false
msBeiLetztemSenden = control.millis()
objektSicher()

basic.forever(function () {
    if (smartfeldSensoren.measureInCentimetersV2(DigitalPin.P1) > 10) {
        music.play(music.tonePlayable(262, music.beat(BeatFraction.Half)), music.PlaybackMode.UntilDone)
        objektGeklaut()
    } else {
        objektSicher()
    }
})
```
## Schritt 9

Um sicherzugehen, dass die Daten verlässlich gesendet wurden, machen wir eine Schleife
die prüft, ob die Daten beim Aufrufen der Funktion geschickt wurden.

* **Ziehe** den Block ``||loops: alle 500ms ||`` ins **Programm**.
* **Ziehe** den ``||logic: wenn dann ||`` Block in die **Schleife**.
* **Ziehe** die Variable ``||variables: spaeterSenden |`` ins leere Feld
der **Wenn-Abfrage**.
* **Rufe** die Funktion ``||functions: sendeDaten(objektVorhanden) ||`` in der **Schleife** auf.

```blocks
loops.everyInterval(500, function () {
    if (spaeterSenden) {
        sendeDaten(objektVorhanden)
    }
})
```
## Glückwunsch🤩

Du hast eine Alarmanlage programmiert! Gehe auf 
[Claviscloud](https://iot.claviscloud.ch/), um dein IoT-Cube mit dem 
Alarmanlagen-Widget zu verbinden und schau, ob sich der Status des Widgets richtig
ändert. Was passiert, wenn du einen Gegenstand vor den Ultraschallsensor hinlegst?
Was passiert, wenn du diesen dann wegnimmst?
