import kivy

kivy.require('1.11.1')
#print(kivy.__version__)

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
)
import numpy as np
import os

#print(os.path.dirname(kivy.__file__))
#moop
class PressureSensor(Widget):
    
    data = StringProperty(10)

    def pull(self):
        newdat = 10 + np.random.randn()
        self.data = "{:.3f}".format(newdat)
        

class FrictionDisplay(Widget):

    ps1 = ObjectProperty(None)
    ps2 = ObjectProperty(None)
    font_size = NumericProperty(50)
    
    def update(self,dt):
        self.ps1.pull()
        self.ps2.pull()
    


class FrictionTrainerApp(App):

    def build(self):
        #print('\n\n\n*********building**********\n\n\n')
        display = FrictionDisplay()
        Clock.schedule_interval(display.update, 30.0/60.0)
        return display


if __name__ == '__main__':
    FrictionTrainerApp().run()
