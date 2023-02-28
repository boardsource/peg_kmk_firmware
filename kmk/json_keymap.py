import json
import gc
from kmk.keys import KC


class UsedModulesKeys:
    tap_dance_used = 'tap_dance_used'
    modtap_used = 'modtap_used'
    mouse_keys_used = 'mouse_keys_used'
    sticky_mod_used = 'sticky_mod_used'
    send_string_used = 'send_string_used'
    simple_key_sequence_used = 'simple_key_sequence_used'
    media_keys_used = 'media_keys_used'
    combos_used = 'combos_used'


class CombosKeys:
    chord = 'chord'
    sequence = 'sequence'
    send = 'send'


class PegOledDisplayKeys:
    corner_one = 'cornerOne'
    corner_two = 'cornerTwo'
    corner_three = 'cornerThree'
    corner_four = 'cornerFour'
    zero = '0'
    one = '1'
    to_display = 'toDisplay'
    flip = 'flip'


class PegRgbMatrixKeys:
    led_display = 'ledDisplay'
    split = 'split'
    right_side = 'rightSide'
    disable_auto_write = 'disableAutoWrite'


class DataKeys:
    used_modules = 'used_modules'
    used_modules_keys = UsedModulesKeys
    code_block = 'codeBlock'
    combos = 'combos'
    combos_keys = CombosKeys
    keymap = 'keymap'
    peg_rgb_matrix = 'pegRgbMatrix'
    peg_rgb_matrix_keys = PegRgbMatrixKeys
    peg_oled_display = 'pegOledDisplay'
    peg_oled_display_keys = PegOledDisplayKeys


class JsonMap:
    def __init__(self, json_path, keyboard=None):
        self._json_path = json_path
        if keyboard:
            self._keyboard = keyboard
        else:
            print('importing json kb')
            from kmk.json_keyboard import JsonKb

            self._keyboard = JsonKb(json_path)

        self.read_json()
        gc.collect()
        print('mem after gc and reading json', gc.mem_free())
        self.process_data()
        # self._keyboard.clean_up()
        gc.collect()
        print('mem after gc and process_data', gc.mem_free())

    def return_keyboard(self):
        return self._keyboard

    def read_json(self):
        try:
            f = open(self._json_path, 'r')
            keymap_string = f.read()
            f.close()
            keymap_dict = json.loads(keymap_string)
            self._data = keymap_dict['data']
        except:
            print('keymap file load failed')

    def process_data(self):
        self._scope = globals()
        self.add_imports()
        self.handle_code_block()
        for data in self._data:
            if data == DataKeys.keymap:
                self.handle_keymap(self._data[data])
            if data == DataKeys.peg_rgb_matrix:
                self.handle_peg_rgb_matrix(self._data[data])
            if data == DataKeys.peg_oled_display:
                self.handle_peg_oled_display(self._data[data])
            if data == DataKeys.combos:
                self.handle_combos(self._data[data])

    def handle_code_block(self):
        if DataKeys.code_block in self._data:
            code_block = self._data[DataKeys.code_block]
            for cb in code_block:
                try:
                    exec(cb, self._scope)
                except:
                    print('code block failed to run', cb)

    def handle_peg_oled_display(self, oled_data):
        try:
            from kmk.extensions.peg_oled_Display import (
                Oled,
                OledDisplayMode,
                OledData,
            )

            oled_ext = Oled()
            if (
                oled_data[DataKeys.peg_oled_display_keys.to_display]
                == OledDisplayMode.TXT
            ):
                oled_ext = Oled(
                    OledData(
                        corner_one={
                            0: oled_data[DataKeys.peg_oled_display_keys.corner_one][
                                DataKeys.peg_oled_display_keys.zero
                            ],
                            1: oled_data[DataKeys.peg_oled_display_keys.corner_one][
                                DataKeys.peg_oled_display_keys.one
                            ],
                        },
                        corner_two={
                            0: oled_data[DataKeys.peg_oled_display_keys.corner_two][
                                DataKeys.peg_oled_display_keys.zero
                            ],
                            1: oled_data[DataKeys.peg_oled_display_keys.corner_two][
                                DataKeys.peg_oled_display_keys.one
                            ],
                        },
                        corner_three={
                            0: oled_data[DataKeys.peg_oled_display_keys.corner_three][
                                DataKeys.peg_oled_display_keys.zero
                            ],
                            1: oled_data[DataKeys.peg_oled_display_keys.corner_three][
                                DataKeys.peg_oled_display_keys.one
                            ],
                        },
                        corner_four={
                            0: oled_data[DataKeys.peg_oled_display_keys.corner_four][
                                DataKeys.peg_oled_display_keys.zero
                            ],
                            1: oled_data[DataKeys.peg_oled_display_keys.corner_four][
                                DataKeys.peg_oled_display_keys.one
                            ],
                        },
                    ),
                    toDisplay=OledDisplayMode.TXT,
                    flip=oled_data[DataKeys.peg_oled_display_keys.flip],
                )
            elif (
                oled_data[DataKeys.peg_oled_display_keys.to_display]
                == OledDisplayMode.IMG
            ):
                pass
            self._keyboard.extensions.append(oled_ext)
        except:
            if self._keyboard.debug_enabled:
                print('error in parsing peg_oled_display_data')

    def handle_peg_rgb_matrix(self, rgb_data):
        try:
            from kmk.extensions.peg_rgb_matrix import Rgb_matrix

            rgb_ext = Rgb_matrix(
                ledDisplay=rgb_data[DataKeys.peg_rgb_matrix_keys.led_display],
                split=rgb_data[DataKeys.peg_rgb_matrix_keys.split],
                rightSide=rgb_data[DataKeys.peg_rgb_matrix_keys.right_side],
                disable_auto_write=rgb_data[
                    DataKeys.peg_rgb_matrix_keys.disable_auto_write
                ],
            )
            self._keyboard.extensions.append(rgb_ext)
        except:
            if self._keyboard.debug_enabled:
                print('error in parsing peg_rgb_matrix_data')

    def add_imports(self):
        if DataKeys.used_modules in self._data:
            used_modules = self._data[DataKeys.used_modules]
            for item in used_modules:
                if (
                    item == DataKeys.used_modules_keys.tap_dance_used
                    and used_modules[item]
                ):
                    from kmk.modules.tapdance import TapDance

                    self._keyboard.modules.append(TapDance())
                if (
                    item == DataKeys.used_modules_keys.modtap_used
                    and used_modules[item]
                ):
                    from kmk.modules.modtap import ModTap

                    self._keyboard.modules.append(ModTap())
                if (
                    item == DataKeys.used_modules_keys.mouse_keys_used
                    and used_modules[item]
                ):
                    from kmk.modules.mouse_keys import MouseKeys

                    self._keyboard.modules.append(MouseKeys())
                if (
                    item == DataKeys.used_modules_keys.media_keys_used
                    and used_modules[item]
                ):
                    from kmk.extensions.media_keys import MediaKeys

                    self._keyboard.extensions.append(MediaKeys())
                if (
                    item == DataKeys.used_modules_keys.send_string_used
                    and used_modules[item]
                ):
                    global send_string
                    from kmk.handlers.sequences import send_string
                if (
                    item == DataKeys.used_modules_keys.simple_key_sequence_used
                    and used_modules[item]
                ):
                    global simple_key_sequence
                    from kmk.handlers.sequences import simple_key_sequence
                if (
                    item == DataKeys.used_modules_keys.sticky_mod_used
                    and used_modules[item]
                ):
                    from kmk.modules.sticky_mod import StickyMod

                    self._keyboard.modules.append(StickyMod())
                if (
                    item == DataKeys.used_modules_keys.combos_used
                    and used_modules[item]
                ):
                    from kmk.modules.combos import Combos

                    combos = Combos()
                    self._keyboard.extensions.append(combos)
                    self._combos = combos

    def return_key(self, key):
        if isinstance(key, str):
            if key.startswith('KC.'):
                replacement = eval(key, self._scope)
                if replacement is None:
                    replacement = KC.NO
                    if self._keyboard.debug_enabled:
                        print(f'Failed replacing "{key}". Using KC.NO')
                return replacement
            else:
                replacement = KC.get(key)
                if replacement is None:
                    if key.startswith('send_string'):
                        from kmk.handlers.sequences import send_string
                    if key.startswith('simple_key_sequence'):
                        from kmk.handlers.sequences import simple_key_sequence
                    # global imports not workiing
                    replacement = eval(key, self._scope)
                    if replacement is None:
                        replacement = KC.NO
                        if self._keyboard.debug_enabled:
                            print(f'Failed replacing "{key}". Using KC.NO')
                elif self._keyboard.debug_enabled:
                    print(f'Replacing "{key}" with {replacement}')
                return replacement
        if self._keyboard.debug_enabled:
            print(f'key is not string returning no')
        return KC.NO

    def handle_combos(self, combos):
        from kmk.modules.combos import Chord, Sequence

        keymap_combos = []
        for type in combos:
            if type == DataKeys.combos_keys.chord:
                for chord in combos[type]:
                    combo_keys = tuple(
                        map(self.return_key, chord[DataKeys.combos_keys.chord])
                    )
                    keymap_combos.append(
                        Chord(
                            combo_keys,
                            self.return_key(chord[DataKeys.combos_keys.send]),
                        )
                    )
            if type == DataKeys.combos_keys.sequence:
                for sequence in combos[type]:
                    combo_keys = tuple(
                        map(self.return_key, sequence[DataKeys.combos_keys.sequence])
                    )
                    keymap_combos.append(
                        Sequence(
                            combo_keys,
                            self.return_key(sequence[DataKeys.combos_keys.send]),
                        )
                    )
        self._combos.combos = keymap_combos

    def handle_keymap(self, keymap):
        for _, layer in enumerate(keymap):
            for key_idx, key in enumerate(layer):
                layer[key_idx] = self.return_key(key)
        self._keyboard.keymap = keymap
