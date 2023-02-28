import json
from kmk.kmk_keyboard import KMKKeyboard
from kmk.modules.layers import Layers


class ScannerType:
    MATRIX = 'MatrixScanner'
    KEYS = 'KeysScanner'
    SHIFTREGISTER = 'ShiftRegisterKeys'
    DIGITALIO = 'Digitalio_MatrixScanner'
    ROTARYIOENCODER = 'RotaryioEncoder'


class DevelopmentBoards:
    blok = 'blok'
    nice_nano = 'nice_nano'
    kb2040 = 'kb2040'
    promicro_rp2040 = 'promicro_rp2040'
    promicro = 'promicro'
    none = 'none'
    raw = 'raw'


class RgbRatrixKeys:
    led_count = 'led_count'
    num_pixels = 'num_pixels'
    max_brightness = 'max_brightness'
    brightness_limit = 'brightness_limit'
    rgb_pixel_pin = 'rgb_pixel_pin'
    layout = 'layout'
    led_key_pos = 'led_key_pos'


class OledKeys:
    sda_pin = 'sda_pin'
    scl_pin = 'scl_pin'


class SplitKeys:
    soft_serial_pin = 'soft_serial_pin'
    enabled = 'enabled'
    splitPico = 'splitPico'
    split_pico = 'split_pico'
    tx_pin = 'tx_pin'
    uart_flip = 'uart_flip'


class LayoutsKeys:
    coord_mapping = 'coord_mapping'


class EncoderKeys:
    rotary = 'rotary'
    pin_a = 'pin_a'
    pin_b = 'pin_b'


class MatrixPinsKeys:
    cols = 'cols'
    rows = 'rows'
    direct = 'direct'


class InfoKeys:
    rgb_matrix = 'rgb_matrix'
    rgb_matrix_keys = RgbRatrixKeys
    oled = 'oled'
    oled_keys = OledKeys
    split = 'split'
    split_keys = SplitKeys
    matrix_pins = 'matrix_pins'
    development_board = 'development_board'
    development_board_pin_names = 'development_board_pin_names'
    diode_direction = 'diode_direction'
    debug_enabled = 'debug_enabled'
    layouts = 'layouts'
    layouts_keys = LayoutsKeys
    encoder = 'encoder'
    encoder_keys = EncoderKeys
    matrix_pins = 'matrix_pins'
    matrix_pins_keys = MatrixPinsKeys
    scanner_type = 'scanner_type'
    shift_register_clock = 'shift_register_clock'
    shift_register_data = 'shift_register_data'
    shift_register_latch = 'shift_register_latch'
    shift_register_key_count = 'shift_register_key_count'


class JsonKb(KMKKeyboard):
    matrix = []
    modules = [Layers()]

    def __init__(self, json_path):
        self._json_path = json_path
        self.read_json()
        self.process_data()

    def read_json(self):
        try:
            f = open(self._json_path, 'r')
            keymap_string = f.read()
            f.close()
            keymap_dict = json.loads(keymap_string)
            self._info = keymap_dict['info']
        except:
            print('json file load failed')

    def process_data(self):
        self.extract_settings()
        info = self._info
        if InfoKeys.matrix_pins in info:
            self.matrix_pins(info[InfoKeys.matrix_pins])
        if InfoKeys.layouts in info:
            self.layouts(info[InfoKeys.layouts])
        if InfoKeys.encoder in info:
            self.encoder(info[InfoKeys.encoder])
        if InfoKeys.split in info:
            self.split(info[InfoKeys.split])
        if InfoKeys.oled in info:
            self.oled(info[InfoKeys.oled])
        if InfoKeys.rgb_matrix in info:
            self.rgb_matrix(info[InfoKeys.rgb_matrix])

    def rgb_matrix(self, rgb_matrix):
        for info in rgb_matrix:
            if (
                info == InfoKeys.rgb_matrix_keys.led_count
                or info == InfoKeys.rgb_matrix_keys.num_pixels
            ):
                self.rgb_num_pixels = rgb_matrix[info]
                self.num_pixels = rgb_matrix[info]
            if info == InfoKeys.rgb_matrix_keys.brightness_limit:
                self.brightness_limit = rgb_matrix[info]
            if info == InfoKeys.rgb_matrix_keys.max_brightness:
                self.brightness_limit = rgb_matrix[info] / 250
            if info == InfoKeys.rgb_matrix_keys.rgb_pixel_pin:
                self.rgb_pixel_pin = self.return_pin(rgb_matrix[info])
            if (
                info == InfoKeys.rgb_matrix_keys.led_key_pos
                or info == InfoKeys.rgb_matrix_keys.layout
            ):
                self.led_key_pos = rgb_matrix[info]

    def oled(self, oled):
        if InfoKeys.oled_keys.scl_pin in oled:
            self.SCL = self.return_pin(oled[InfoKeys.oled_keys.scl_pin])
        if InfoKeys.oled_keys.sda_pin in oled:
            self.SDA = self.return_pin(oled[InfoKeys.oled_keys.sda_pin])

    def split(self, split):
        if InfoKeys.split_keys.enabled in split and split[InfoKeys.split_keys.enabled]:
            self.data_pin = self.return_pin(split[InfoKeys.split_keys.soft_serial_pin])
            from kmk.modules.split import Split

            split_ext = Split()
            if (
                InfoKeys.split_keys.splitPico in split
                and split[InfoKeys.split_keys.splitPico]
            ) or (
                InfoKeys.split_keys.split_pico in split
                and split[InfoKeys.split_keys.split_pico]
            ):
                split_ext = Split(use_pio=True)
            elif (
                InfoKeys.split_keys.tx_pin in split
                and split[InfoKeys.split_keys.tx_pin]
                and InfoKeys.split_keys.uart_flip in split
            ):
                self.tx = self.return_pin(split[InfoKeys.split_keys.tx_pin])
                split_ext = Split(
                    data_pin=self.data_pin,
                    data_pin2=self.tx,
                    uart_flip=split[InfoKeys.split_keys.uart_flip],
                )
            self.modules.append(split_ext)

    def extract_settings(self):
        for info in self._info:
            if info == InfoKeys.development_board_pin_names:
                self.development_board_pin_names = self._info[info]
            if info == InfoKeys.development_board:
                self.development_board = self._info[info]
            if info == InfoKeys.debug_enabled:
                self.debug_enabled = self._info[info]

    def layouts(self, layouts):
        for layout in layouts:
            # keys = layouts[layout]['layout']
            # coord_mapping = [None] * len(keys)
            # for key in keys:
            #     index = key['x'] * key['y']
            #     pos = key['matrix'][0] + key['matrix'][1]
            #     coord_mapping[index] = pos
            # self.coord_mapping = coord_mapping
            if layout == InfoKeys.layouts_keys.coord_mapping:
                self.coord_mapping = layouts[layout]
                break

    def return_pin(self, pin):
        if self.development_board == DevelopmentBoards.blok:
            from kmk.quickpin.pro_micro.boardsource_blok import pinout as pins
        elif self.development_board == DevelopmentBoards.nice_nano:
            from kmk.quickpin.pro_micro.nice_nano import pinout as pins
        elif self.development_board == DevelopmentBoards.kb2040:
            from kmk.quickpin.pro_micro.kb2040 import pinout as pins
        elif self.development_board == DevelopmentBoards.promicro_rp2040:
            from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import pinout as pins

        if self.development_board_pin_names == DevelopmentBoards.promicro:
            from kmk.quickpin.pro_Micro.avr_promicro import translate as avr
        if self.development_board_pin_names == self.development_board:
            return pins[pin]
        elif (
            self.development_board_pin_names == DevelopmentBoards.raw
            and self.development_board == DevelopmentBoards.none
        ):
            import board

            return board[pin]
        else:
            return pins[avr[pin]]

    def encoder(self, encoder):
        if InfoKeys.encoder_keys.rotary in encoder:
            for encoder_pin_set in encoder[InfoKeys.encoder_keys.rotary]:
                # this workflow overrides pins on self need to find a deep copy
                self.pin_a = self.return_pin(
                    encoder_pin_set[InfoKeys.encoder_keys.pin_a]
                )
                self.pin_b = self.return_pin(
                    encoder_pin_set[InfoKeys.encoder_keys.pin_b]
                )
                self.setup_scanner(ScannerType.ROTARYIOENCODER)

    def matrix_pins(self, matrix_pins):
        def call_scanner():
            if hasattr(self, 'direct_pins'):
                self.setup_scanner(ScannerType.KEYS)
            elif hasattr(self, 'col_pins') and hasattr(self, 'row_pins'):
                if InfoKeys.scanner_type in self._info:
                    scanner_type = self._info[InfoKeys.scanner_type]
                    if scanner_type == ScannerType.DIGITALIO:
                        self.setup_scanner(ScannerType.DIGITALIO)
                    else:
                        self.setup_scanner(ScannerType.MATRIX)
                else:
                    self.setup_scanner(ScannerType.MATRIX)
            elif InfoKeys.scanner_type in self._info:
                scanner_type = self._info[InfoKeys.scanner_type]
                self.setup_scanner(scanner_type)

        for section in matrix_pins:
            section_pins = []
            for pin in matrix_pins[section]:
                section_pins.append(self.return_pin(pin))
            if section == InfoKeys.matrix_pins_keys.cols:
                self.col_pins = tuple(section_pins)
            if section == InfoKeys.matrix_pins_keys.rows:
                self.row_pins = tuple(section_pins)
            if section == InfoKeys.matrix_pins_keys.direct:
                self.direct_pins = tuple(section_pins)
        call_scanner()

    def set_diode_orientation(self):
        if self.diode_orientation == None:
            from kmk.scanners import DiodeOrientation

            if InfoKeys.diode_direction in self._info:
                if self._info[InfoKeys.diode_direction] == 'ROW2COL':
                    self.diode_orientation = DiodeOrientation.ROW2COL
                else:
                    self.diode_orientation = DiodeOrientation.COL2ROW
            else:
                self.diode_orientation = DiodeOrientation.COL2ROW

    def setup_scanner(self, type):
        if type == ScannerType.MATRIX:
            from kmk.scanners.keypad import MatrixScanner

            self.set_diode_orientation()
            scanner = MatrixScanner(
                column_pins=self.col_pins,
                row_pins=self.row_pins,
                columns_to_anodes=self.diode_orientation,
            )
            self.matrix.append(scanner)
        if type == ScannerType.KEYS:
            from kmk.scanners.keypad import KeysScanner

            scanner = KeysScanner(pins=self.direct_pins)
            self.matrix.append(scanner)
        if type == ScannerType.SHIFTREGISTER:
            from kmk.scanners.keypad import ShiftRegisterKeys

            scanner = ShiftRegisterKeys(
                clock=self.return_pin(self._info[InfoKeys.shift_register_clock]),
                data=self.return_pin(self._info[InfoKeys.shift_register_data]),
                latch=self.return_pin(self._info[InfoKeys.shift_register_latch]),
                key_count=self._info[InfoKeys.shift_register_key_count],
            )
            self.matrix.append(scanner)
        if type == ScannerType.DIGITALIO:
            from kmk.scanners.digitalio import MatrixScanner

            self.set_diode_orientation()

            scanner = MatrixScanner(
                cols=self.col_pins,
                rows=self.row_pins,
                diode_orientation=self.diode_orientation,
            )
            self.matrix.append(scanner)
        if type == ScannerType.ROTARYIOENCODER:
            from kmk.scanners.encoder import RotaryioEncoder

            scanner = RotaryioEncoder(
                pin_a=self.pin_a,
                pin_b=self.pin_b,
            )
            self.matrix.append(scanner)

    def clean_up(self):
        # del self.setup_scanner
        del self.process_data
        del self.matrix_pins
        del self.layouts
        del self.extract_settings
        del self.set_diode_orientation
        del self.read_json
        del self._info
        pass
