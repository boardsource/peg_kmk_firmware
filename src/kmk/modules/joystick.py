import analogio

from kmk.keys import AX

from kmk.kmktime import PeriodicTimer
from kmk.modules import Module
# from kmk.modules.mouse_keys import PointingDevice
from kmk.keys import make_key

class JoyStick(Module):
    def __init__(self,layer,speed=1.5):
        self.layer=layer
        self.pot_min = 0.00
        self.pot_max = 3.29
        self.step = (self.pot_max - self.pot_min) / 20.0
        # self.pointing_device = PointingDevice()
        self.polling_interval = 100
        self.scroll_mode=False
        self.default_layer=0
        self.speed=speed
        make_key(
            names=('JOY_MODE',),
            on_press=self._joy_mode_press,
            on_release=self._joy_mode_press,
        )


    def get_voltage(self, pin):
        raw_value= int((pin.value * 3.3) / 10000)
    
        if raw_value>11:
            return raw_value-10
        if raw_value<9:
            return -10+raw_value
        if raw_value==10:
            return 0
        return 0
 

    def _joy_mode_press(self, key, keyboard, *args, **kwargs):
        self.scroll_mode = not self.scroll_mode


    def during_bootup(self, keyboard):
        self.y_axis = analogio.AnalogIn(keyboard.joy_y)
        self.x_axis = analogio.AnalogIn(keyboard.joy_x)
        self.swap_x=keyboard.swap_x
        self.swap_y=keyboard.swap_y
        self._timer = PeriodicTimer(self.polling_interval)
        self._debug= keyboard.debug_enabled

    
    def swap_layers_start(self,keyboard):
        if keyboard.active_layers[-1]!=self.layer:
            self.default_layer=keyboard.active_layers[-1]
        keyboard.active_layers[-1]=self.layer
    def swap_layers_end(self,keyboard):
        keyboard.active_layers[-1]=self.default_layer
        self.scroll_mode=False
    def handel_swap(self,flag,value):
        if flag:
            if value<0:
                return abs(value)
            if value >0:
                return -abs(value)
            else:
                return value
        else:
            return value
    def adjust_speed(self,value):
        if value>7:
            return int(value*self.speed)
        if value<-7:
            return int(value*self.speed)
        else: 
            return value

    def before_matrix_scan(self, keyboard):
    
        raw_x=self.get_voltage(self.x_axis)
        raw_y=self.get_voltage(self.y_axis)

        x = self.handel_swap(self.swap_x,self.adjust_speed(raw_x))
        y = self.handel_swap(self.swap_y,self.adjust_speed(raw_y))
        AX.X.move(keyboard, x)
        AX.Y.move(keyboard, y)
        if keyboard.debug_enabled:
            print("x:",x,"y:",y)



       

    def after_matrix_scan(self, keyboard):
        return None

    def before_hid_send(self, keyboard):
        return None
    def _clear_pending_hid(self):
        pass

    def after_hid_send(self, keyboard):
        pass


    def on_powersave_enable(self, keyboard):
        return None

    def on_powersave_disable(self, keyboard):
        return None
