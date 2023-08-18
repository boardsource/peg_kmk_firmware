from kmk.extensions import Extension
from kmk.keys import make_key
import simpleio

class StartUpSong(Extension):
    _song_list=[
                [ 262,  # C4
                    294,  # D4
                    330,  # E4
                    349,  # F4
                    392,  # G4
                    440,  # A4
                    494 ] # B4
                    ]
    _pin=None
    def __init__(self,pin,song=0):
        self._pin=pin
        for i in range(len(self._song_list[song])):
            simpleio.tone(pin, self._song_list[song][i], duration=0.5)



    def on_runtime_enable(self, sandbox):
        return

    def on_runtime_disable(self, sandbox):
        return

    def during_bootup(self, sandbox):
        return

    def before_matrix_scan(self, sandbox):
        return

    def after_matrix_scan(self, sandbox):
        return

    def before_hid_send(self, sandbox):
        return

    def after_hid_send(self, sandbox):
        return

    def on_powersave_enable(self, sandbox):
        return

    def on_powersave_disable(self, sandbox):
        return
