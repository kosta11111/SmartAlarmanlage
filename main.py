def objektSicher():
    global objektVorhanden
    objektVorhanden = 1
    sendeDaten(objektVorhanden)
def objektGeklaut():
    global objektVorhanden
    objektVorhanden = 0
    sendeDaten(objektVorhanden)
def sendeDaten(status: number):
    global spaeterSenden, msBeiLetztemSenden
    if control.millis() > msBeiLetztemSenden + 10000:
        IoTCube.add_binary(eIDs.ID_0, status)
        IoTCube.send_buffer_simple()
        spaeterSenden = False
        msBeiLetztemSenden = control.millis()
    else:
        spaeterSenden = True
objektVorhanden = 0
msBeiLetztemSenden = 0
spaeterSenden = False
IoTCube.LoRa_Join(eBool.ENABLE, eBool.ENABLE, 10, 8)
while not (IoTCube.get_status(eSTATUS_MASK.JOINED)):
    basic.show_icon(IconNames.PITCHFORK)
basic.show_icon(IconNames.YES)
sendeErlaubnis = False
spaeterSenden = False
msBeiLetztemSenden = control.millis()
objektSicher()

def on_every_interval():
    if spaeterSenden:
        sendeDaten(objektVorhanden)
loops.every_interval(500, on_every_interval)

def on_forever():
    if smartfeldSensoren.measure_in_centimeters_v2(DigitalPin.P1) > 10:
        music.play(music.tone_playable(262, music.beat(BeatFraction.HALF)),
            music.PlaybackMode.UNTIL_DONE)
        objektGeklaut()
    else:
        objektSicher()
basic.forever(on_forever)