def objektSicher():
    global objektVorhanden
    objektVorhanden = 1
    sendeDaten(objektVorhanden)
def objektGeklaut():
    global objektVorhanden
    objektVorhanden = 0
    sendeDaten(objektVorhanden)

def on_button_pressed_a():
    global aktiv
    aktiv = 1
input.on_button_pressed(Button.A, on_button_pressed_a)

def sendeDaten(status: number):
    global spaeterSenden, msBeiLetztemSenden
    if control.millis() > msBeiLetztemSenden + 5000:
        IoTCube.add_binary(eIDs.ID_0, status)
        IoTCube.send_buffer_simple()
        spaeterSenden = False
        msBeiLetztemSenden = control.millis()
    else:
        spaeterSenden = True

def on_button_pressed_b():
    global aktiv
    aktiv = 0
input.on_button_pressed(Button.B, on_button_pressed_b)

aktiv = 0
objektVorhanden = 0
msBeiLetztemSenden = 0
spaeterSenden = False
IoTCube.LoRa_Join(eBool.ENABLE, eBool.ENABLE, 10, 8)
while not (IoTCube.get_status(eSTATUS_MASK.JOINED)):
    basic.show_icon(IconNames.NO)
basic.show_icon(IconNames.YES)
spaeterSenden = False
msBeiLetztemSenden = control.millis()
objektSicher()

def on_every_interval():
    if spaeterSenden:
        sendeDaten(objektVorhanden)
loops.every_interval(500, on_every_interval)

def on_forever():
    while aktiv:
        if smartfeldSensoren.measure_in_centimeters_v2(DigitalPin.P1) > 10:
            music.play(music.tone_playable(262, music.beat(BeatFraction.HALF)),
                music.PlaybackMode.UNTIL_DONE)
            objektGeklaut()
        else:
            objektSicher()
basic.forever(on_forever)
