import json
from kmk.json_keyboard import InfoKeys,DevelopmentBoards
class FeaturesKeys:
    features="features"
    name="name"
    split="split"
    rightSide="rightSide"
    serial_write="serial_write"
class JsonBoot:
    storage_mode=True
    boot_loader=False
    need_to_rename=True
    drive_name="KEYBOARD"
    row_pins=None
    col_pins=None
    direct_pins=None

    def __init__(self, json_path):
        self._json_path = json_path
        self.read_json()
        self.process_data()

    def read_json(self):
        try:
            f = open(self._json_path, 'r')
            keymap_string = f.read()
            f.close()
            self._keymap_dict = json.loads(keymap_string)
        except:
            print('json file load failed')

    def process_data(self):
        self.extract_settings()
        self.handle_rename()
        info = self._keymap_dict['info']
        if InfoKeys.matrix_pins in info:
            self.matrix_pins(info[InfoKeys.matrix_pins])
        if InfoKeys.diode_direction in info:
            self.diode_orientation=info[InfoKeys.diode_direction]
        else:
             self.diode_orientation="COL2ROW"
        self.look_at_pressed_keys()
        self.handle_setup()
    
    def extract_settings(self):
        data_info = self._keymap_dict['info']

        for info in data_info:
            if info == InfoKeys.development_board_pin_names:
                self.development_board_pin_names = data_info[info]
            if info == InfoKeys.development_board:
                self.development_board = data_info[info]
            if info == InfoKeys.debug_enabled:
                self.debug_enabled = data_info[info]

    def handle_rename(self):
        from storage import getmount
        current_name=str(getmount('/').label)
        if current_name.endswith('PYTHON'):
            self.need_to_rename=True
            self.get_keyboard_name()
        else:
            self.need_to_rename=False




    def get_keyboard_name(self):
        self.drive_name="KEYBOARD"
        if FeaturesKeys.features in self._keymap_dict:
            features=self._keymap_dict[FeaturesKeys.features]
            if FeaturesKeys.name in features:
                self.drive_name=features[FeaturesKeys.name].upper()
            if FeaturesKeys.split in features and features[FeaturesKeys.split]:
                if FeaturesKeys.rightSide in features and features[FeaturesKeys.rightSide]:
                    self.drive_name=self.drive_name+"R"
                else:
                    self.drive_name=self.drive_name+"L"
                
                
        
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
        elif (
            self.development_board_pin_names == DevelopmentBoards.raw
            and self.development_board == DevelopmentBoards.none
        ):
            import board

            return getattr(board,pin)
        else:
            return pins[avr[pin]]
    
    def matrix_pins(self, matrix_pins):
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

    def look_at_pressed_keys(self):
        import digitalio
        if self.row_pins and self.col_pins:
            col = digitalio.DigitalInOut(self.col_pins[0])
            row1 = digitalio.DigitalInOut(self.row_pins[0])
            row2 = digitalio.DigitalInOut(self.row_pins[1])

            if self.diode_orientation == "COL2ROW":
                col.switch_to_output(value=True)
                row1.switch_to_input(pull=digitalio.Pull.DOWN)
                row1.switch_to_input(pull=digitalio.Pull.DOWN)

            else:
                col.switch_to_input(pull=digitalio.Pull.DOWN)
                row1.switch_to_output(value=True)
                row2.switch_to_output(value=True)


            self.storage_mode=row2.value
            self.boot_loader=row1.value

            row1.deinit()
            row2.deinit()
            col.deinit()
        elif self.direct_pins:
            switch1 = digitalio.DigitalInOut(self.direct_pins[0])
            switch1.direction = digitalio.Direction.INPUT
            switch1.pull = digitalio.Pull.UP
            switch2 = digitalio.DigitalInOut(self.direct_pins[1])
            switch2.direction = digitalio.Direction.INPUT
            switch2.pull = digitalio.Pull.UP
            self.storage_mode=switch2.value
            self.boot_loader=switch1.value

            
    def handle_setup(self):
        if self.boot_loader:
            import microcontroller
            microcontroller.on_next_reset(microcontroller.RunMode.UF2)
            microcontroller.reset()
            return
        if self.need_to_rename:
            import storage
            storage.remount("/", readonly=False)
            m = storage.getmount("/")
            m.label = self.drive_name
            storage.remount("/", readonly=True)
            storage.enable_usb_drive()
        if not self.storage_mode:
            import storage
            storage.disable_usb_drive()
            storage.remount("/",  False)
        


