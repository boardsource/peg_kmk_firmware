from kmk.scanners import Scanner
import digitalio
from keypad import Event as KeyEvent


def intify_coordinate(row, col):
    return row << 8 | col


class SquareMatrixScanner(Scanner):
    def __init__(self, pins,        offset=0):
        self.offset = offset
        self.len_pins = len(pins)
        self.pins = [
            x if x.__class__.__name__ == "DigitalInOut" else digitalio.DigitalInOut(x)
            for x in pins
        ]
        # self.live_pin_index = 0
        # self.pins[self.live_pin_index].switch_to_output()
        self.translate_coords = True
        for i, pin in enumerate(self.pins):
            # if i != self.live_pin_index:
            pin.switch_to_input(pull=digitalio.Pull.DOWN)

        self._key_count = self.len_pins * self.len_pins
        self.state = bytearray(self.key_count)
        self.rollover_cols_every_rows = self.len_pins

    @property
    def key_count(self):
        return self._key_count

    def scan_for_changes(self):
        ba_idx = 0
        any_changed = False

        # self.pins[self.live_pin_index].value = True
        for oidx, opin in enumerate(self.pins):
            opin.switch_to_output()
            opin.value = True
            for iidx, ipin in enumerate(self.pins):
                if iidx != oidx:
                    new_val = int(ipin.value)
                    old_val = self.state[ba_idx]
                    if old_val != new_val:
                        col = oidx
                        row = iidx

                        self.state[ba_idx] = new_val

                        any_changed = True

                        pressed = new_val
                        break

                    ba_idx += 1

            opin.value = False
            opin.switch_to_input(pull=digitalio.Pull.DOWN)

            if any_changed:
                break

        if any_changed:
            key_number = self.len_pins*row + col+self.offset
            return KeyEvent(key_number, pressed)
