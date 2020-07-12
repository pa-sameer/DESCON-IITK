import kivy 
kivy.require('1.11.1')

from kivy.app import App
#from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
#from kivy.properties import ObjectProperty
#import math
#import os
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import AsyncImage, Image
from kivy.core.window import Window
#from kivy.app import runTouchApp
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from sympy.physics.continuum_mechanics.beam import Beam
from sympy import symbols
from kivy.uix.togglebutton import ToggleButton
from sympy.plotting import plot
import os
import sys
from kivy.app import runTouchApp
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window




class Toggle_btn(GridLayout):
    def __init__(self, **kwargs):
        super(Toggle_btn, self).__init__(**kwargs)
        self.cols = 2

        self.tb1 = ToggleButton(text = 'DOWN', group = 'dir',state = 'down')
        self.add_widget(self.tb1)

        self.tb2 = ToggleButton(text = 'UP', group = 'dir')
        self.add_widget(self.tb2)

    def get_state(self):
        return [self.tb1.state, self.tb2.state]


class Toggle_btn_moment(GridLayout):
    def __init__(self, **kwargs):
        super(Toggle_btn_moment, self).__init__(**kwargs)
        self.cols = 2

        self.tb1 = ToggleButton(text = 'CLOCK', group = 'dir',state = 'down')
        self.add_widget(self.tb1)

        self.tb2 = ToggleButton(text = 'ANTI-CLOCK', group = 'dir')
        self.add_widget(self.tb2)

    def get_state(self):
        return [self.tb1.state, self.tb2.state]


class Panel(FloatLayout):

    def __init__(self, **kwargs):
        super(Panel, self).__init__(**kwargs)

        self.lay_shear = BoxLayout(orientation = 'vertical', size_hint_y = None, height = int(Window.size[1] * 0.8), spacing = 5)
        self.lay_bending = BoxLayout(orientation = 'vertical', size_hint_y=None, height = int(Window.size[1] * 0.8), spacing = 5)
        self.lay_slope = BoxLayout(orientation = 'vertical', size_hint_y = None, height = int(Window.size[1] * 0.8), spacing = 5)
        self.lay_deflection = BoxLayout(orientation = 'vertical', size_hint_y=None, height = int(Window.size[1] * 0.8), spacing = 5)
        self.lay_loading = BoxLayout(orientation = 'vertical', size_hint_y = None, height = int(Window.size[1] * 0.8), spacing = 5)

        self.btn_ht = int(Window.size[1])

        self.bind(size = self.set_btn_ht)

        col = (0, 0, .7, .8)

        self.E = "20"
        self.I = "40"
        self.Len = '10'
        self.reaction_vars = []
        self.BEAM = Beam(self.Len, self.E, self.I)

        self.d = None
        self.shear_plot_cnt = 0
        self.slope_plot_cnt = 0
        self.bending_plot_cnt = 0
        self.deflection_plot_cnt = 0
        self.loading_plot_cnt = 0

        self.analysis_started = False

        if os.path.exists('shear.png'):
            os.remove('shear.png')

        if os.path.exists('bending_moment.png'):
            os.remove('bending_moment.png')

        if os.path.exists('slope.png'):
            os.remove('slope.png')

        if os.path.exists('deflection.png'):
            os.remove('deflection.png')

        layout = GridLayout(cols=1, spacing=10, size_hint_y=None, size_hint_x = 1)

        layout.bind(minimum_height = layout.setter('height'))

        self.sign_conv = Button(text = '[b]SIGN CONVENTION[/b]', markup = True, text_size = self.size, halign = 'center', valign = 'middle', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.sign_conv)
        self.sign_conv.bind(on_press = self.popup_sign_conv)

        self.default_val = Button(text = 'SET E, I AND L', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.default_val)
        self.default_val.bind(on_press = self.popup_default_value)

        self.supports = Label(text = '[b]SUPPORTS[/b]', markup = True, size_hint_y=None, height=40)
        layout.add_widget(self.supports)

        self.Fix = Button(text = 'FIXED', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Fix)
        self.Fix.bind(on_press = self.popup_fix)

        self.Roller = Button(text = 'ROLLER', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Roller)
        self.Roller.bind(on_press = self.popup_roller)

        self.Pin = Button(text = 'PIN', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Pin)
        self.Pin.bind(on_press = self.popup_pin)

        self.loads = Label(text = '[b]LOADS[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7)
        layout.add_widget(self.loads)

        self.conc = Label(text = '[b]CONCENTRATED[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7)
        layout.add_widget(self.conc)

        self.pt_load = Button(text = 'POINT LOAD', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.pt_load)
        self.pt_load.bind(on_press = self.popup_vertical)

        self.Moment = Button(text = 'MOMENT', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Moment)
        self.Moment.bind(on_press = self.popup_moment)

        self.dist = Label(text = '[b]DISTRIBUTED[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7)
        layout.add_widget(self.dist)

        self.const_p = Button(text = 'CONSTANT PRESSURE', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.const_p)
        self.const_p.bind(on_press = self.popup_linear)

        self.Lramp = Button(text = 'LINEAR RAMP', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Lramp)
        self.Lramp.bind(on_press = self.popup_linear_ramp)

        self.Pramp = Button(text = 'PARABOLIC RAMP', markup = True, size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Pramp)
        self.Pramp.bind(on_press = self.popup_parabolic_ramp)

        self.Plot = Label(text = '[b]PLOT[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7)
        layout.add_widget(self.Plot)

        self.Shear = Button(text = 'SHEAR FORCE DIAGRAM', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Shear)
        self.Shear.bind(on_press = self.popup_shear)

        self.Bending = Button(text = 'BENDING MOMENT DIAGRAM', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Bending)
        self.Bending.bind(on_press = self.popup_bending)

        self.Slope = Button(text = 'SLOPE DIAGRAM', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Slope)
        self.Slope.bind(on_press = self.popup_slope)

        self.Deflection = Button(text = 'DEFLECTION DIAGRAM', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Deflection)
        self.Deflection.bind(on_press = self.popup_deflection)

        self.loading = Button(text = 'LOADING DIAGRAM', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.loading)
        self.loading.bind(on_press = self.popup_loading)

        self.Reaction = Button(text = 'REACTION LOADS', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.Reaction)
        self.Reaction.bind(on_press = self.popup_reaction)

        self.sup_and_load = Button(text = 'SUPPORTS AND LOADS', size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.sup_and_load)
        self.sup_and_load.bind(on_press = self.popup_sup_and_load)

        self.NewBeam = Button(text = '[b]NEW BEAM[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7, background_color = col)
        layout.add_widget(self.NewBeam)
        self.NewBeam.bind(on_press = self.popup_newbeam)

        self.close_app = Button(text = '[b]EXIT APP[/b]', markup = True, size_hint_y=None, height = self.btn_ht / 7, background_color = (1, 0, 0, 1))
        layout.add_widget(self.close_app)
        self.close_app.bind(on_press = self.exit_app)

        MakeBeam = ScrollView(size_hint=(.3, 1))
        MakeBeam.add_widget(layout)
        self.add_widget(MakeBeam)       

        #---------------plots------------scroll----------------------

        self.scroll_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, size_hint_x = 1)

        self.scroll_layout.bind(minimum_height = self.scroll_layout.setter('height'))

        self.show_plots = ScrollView(size_hint=(.7, 1), pos_hint = {'x' : 0.3, 'y' : 0})
        self.show_plots.add_widget(self.scroll_layout)
        self.add_widget(self.show_plots)

        #---------------------support&load button----------------

        self.sup = BoxLayout(orientation = 'vertical')
        self.load = BoxLayout(orientation = 'vertical')

    def set_btn_ht(self, *kwargs):
        self.sign_conv.height = int(Window.size[1]) / 7
        self.default_val.height = int(Window.size[1]) / 7
        self.supports.height = int(Window.size[1]) / 7
        self.Fix.height = int(Window.size[1]) / 7
        self.Roller.height = int(Window.size[1]) / 7
        self.Pin.height = int(Window.size[1]) / 7
        self.loads.height = int(Window.size[1]) / 7
        self.conc.height = int(Window.size[1]) / 7
        self.pt_load.height = int(Window.size[1]) / 7
        self.Moment.height = int(Window.size[1]) / 7
        self.dist.height = int(Window.size[1]) / 7
        self.const_p.height = int(Window.size[1]) / 7
        self.Lramp.height = int(Window.size[1]) / 7
        self.Pramp.height = int(Window.size[1]) / 7
        self.NewBeam.height = int(Window.size[1]) / 7
        self.Shear.height = int(Window.size[1]) / 7
        self.Bending.height = int(Window.size[1]) / 7
        self.Slope.height = int(Window.size[1]) / 7
        self.Deflection.height = int(Window.size[1]) / 7
        self.close_app.height = int(Window.size[1]) / 7
        self.loading.height = int(Window.size[1]) / 7
        self.Reaction.height = int(Window.size[1]) / 7
        self.sup_and_load.height = int(Window.size[1]) / 7
        self.lay_shear.height = int(Window.size[1] * 0.8)
        self.lay_bending.height = int(Window.size[1] * 0.8)
        self.lay_slope.height = int(Window.size[1] * 0.8)
        self.lay_deflection.height = int(Window.size[1] * 0.8)
        self.lay_loading.height = int(Window.size[1] * 0.8)
        #print(Window.size)

    def exit_app(self, instance):

        if os.path.exists('shear.png'):
            os.remove('shear.png')

        if os.path.exists('bending_moment.png'):
            os.remove('bending_moment.png')

        if os.path.exists('slope.png'):
            os.remove('slope.png')

        if os.path.exists('deflection.png'):
            os.remove('deflection.png')
        #sys.exit("< Beam Solver closed >")
        beam.stop()

    def popup_sign_conv(self, instance):
        layout = GridLayout(cols = 1)

        layout.add_widget(Label(text = 'UPWARD DIRECTION AND ANTI-CLOCKWISE\nSENSE IS CONSIDERED AS POSITIVE\nIN PRODUCING RESULTS'))

        btn2 = Button(text = 'CLOSE')
        layout.add_widget(btn2)
        btn2.bind(on_press = self.popup_dismiss)

        self.popup = Popup(title = 'SIGN CONVENTION', content = layout, size_hint = (.5, .5), pos_hint = {'center_x' : .5, 'center_y' : .5})
        self.popup.open()




    def popup_default_value(self, instance):
        #layout = BoxLayout(orientation = 'vertical')

        #layout1 is our child wiget of layout and is GridLayout with coloumn = 2
        layout1 = GridLayout(cols = 2)

        #layout1's child widget Label
        layout1.add_widget(Label(text = 'E = '))

        #layout1's child widget having value of E
        self.E_text = TextInput(text = self.E,multiline = False)
        layout1.add_widget(self.E_text)

        #layout1's child widget Label
        layout1.add_widget(Label(text = 'I = '))

        #layout1's another child widget having value of E
        self.I_text = TextInput(text = self.I,multiline = False)
        layout1.add_widget(self.I_text)

        #layout1's child widget Label
        layout1.add_widget(Label(text = 'LENGTH (m) = '))

        #layout1's another child widget having value of length of beam
        self.len_text = TextInput(text = self.Len,multiline = False)
        layout1.add_widget(self.len_text)

        #Button to save the changes done
        btn = Button(text = 'SAVE')
        layout1.add_widget(btn)
        btn.bind(on_press = self.set_E_I_Len)

        #Button to accept the default values and close the popup
        btn2 = Button(text = 'CLOSE')
        layout1.add_widget(btn2)
        btn2.bind(on_press = self.popup_dismiss)

        #layout.add_widget(layout1)

        #Instantiating the Popup
        self.popup = Popup(title = 'SET E, I  AND LENGTH FOR BEAM', content = layout1, size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
        self.popup.open()


    def popup_fix(self, instance):

         layout = GridLayout(cols = 2)

         layout.add_widget(Label(text = 'X (m) = '))

         self.fix_text = TextInput(multiline = False)
         layout.add_widget(self.fix_text)


         btn = Button(text = 'SAVE')
         layout.add_widget(btn)
         btn.bind(on_press = self.add_fix)

         btn2 = Button(text = 'CLOSE')
         layout.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         self.popup = Popup(title = 'FIXED SUPPPORT ', content = layout, size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
         self.popup.open()

    def popup_roller(self, instance):


         layout = GridLayout(cols = 2)

         layout.add_widget(Label(text = 'X (m) = '))

         self.roller_text = TextInput(multiline = False)
         layout.add_widget(self.roller_text)

         btn = Button(text = 'SAVE')
         layout.add_widget(btn)
         btn.bind(on_press = self.add_roller)

         btn2 = Button(text = 'CLOSE')
         layout.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         self.popup = Popup(title = 'ROLLER SUPPORT ', content = layout, size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
         self.popup.open()

    def popup_pin(self, instance):

         layout = GridLayout(cols = 2)

         layout.add_widget(Label(text = 'X (m) = '))

         self.pin_text = TextInput(multiline = False)
         layout.add_widget(self.pin_text)

         btn = Button(text = 'SAVE')
         layout.add_widget(btn)
         btn.bind(on_press = self.add_pin)

         btn2 = Button(text = 'CLOSE')
         layout.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         self.popup = Popup(title = 'PIN SUPPORT ', content = layout, size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
         self.popup.open()

    def popup_vertical(self, instance):

         layout = BoxLayout(orientation = 'vertical')

         layout1 = GridLayout(cols = 2)

         layout1.add_widget(Label(text = 'X (m) = '))

         self.vertical_load_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.vertical_load_pos_text)

         layout1.add_widget(Label(text = 'LOAD (kN) = '))

         self.vertical_load_mag_text = TextInput(multiline = False)
         layout1.add_widget(self.vertical_load_mag_text)

         layout.add_widget(layout1)

         self.load_dir = Toggle_btn()
         layout.add_widget(self.load_dir)

         layout2 = GridLayout(cols = 2)

         btn = Button(text = 'SAVE')
         layout2.add_widget(btn)
         btn.bind(on_press = self.add_vertical_load)

         btn2 = Button(text = 'CLOSE')
         layout2.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         layout.add_widget(layout2)

         self.popup = Popup(title = 'POINT LOAD ', content = layout, size_hint = (.5, .5), pos_hint = {'center_x' : .5, 'center_y' : .5})

         self.popup.open()

    def popup_moment(self, instance):
         layout = BoxLayout(orientation = 'vertical')

         layout1 = GridLayout(cols = 2)

         layout1.add_widget(Label(text = 'X (m) = '))

         self.moment_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.moment_pos_text)

         layout1.add_widget(Label(text = 'MOMENT (kN * m)= '))

         self.moment_mag_text = TextInput(multiline = False)
         layout1.add_widget(self.moment_mag_text)

         layout.add_widget(layout1)

         self.moment_dir = Toggle_btn_moment()
         layout.add_widget(self.moment_dir)

         layout2 = GridLayout(cols = 2)

         btn = Button(text = 'SAVE')
         layout2.add_widget(btn)
         btn.bind(on_press = self.add_moment)

         btn2 = Button(text = 'CLOSE')
         layout2.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         layout.add_widget(layout2)

         self.popup = Popup(title = 'MOMENT MAG. ', content = layout, size_hint = (.5, .5), pos_hint = {'center_x' : .5, 'center_y' : .5})
         self.popup.open()

    def popup_linear(self, instance):

         self.ramp_order = 0

         layout = BoxLayout(orientation = 'vertical')

         layout1 = GridLayout(cols = 2)

         layout1.add_widget(Label(text = 'X1 (m) = '))

         self.starting_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.starting_pos_text)

         layout1.add_widget(Label(text = 'X2 (m) = '))

         self.ending_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.ending_pos_text)

         layout1.add_widget(Label(text = 'LOAD (kN) = '))

         self.load_per_m_text = TextInput(multiline = False)
         layout1.add_widget(self.load_per_m_text)

         layout.add_widget(layout1)

         self.load_dir_linear = Toggle_btn()
         layout.add_widget(self.load_dir_linear)

         layout2 = GridLayout(cols = 2)

         btn = Button(text = 'SAVE')
         layout2.add_widget(btn)
         btn.bind(on_press = self.add_linear_load)

         btn2 = Button(text = 'CLOSE')
         layout2.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         layout.add_widget(layout2)

         self.popup = Popup(title = 'DISTRIBUTED LINEAR LOAD ', content = layout, size_hint = (.6, .6), pos_hint = {'center_x' : .5, 'center_y' : .5})

         self.popup.open()


    def popup_linear_ramp(self, instance):
        
         self.ramp_order = 1

         layout = BoxLayout(orientation = 'vertical')

         layout1 = GridLayout(cols = 2)

         layout1.add_widget(Label(text = 'X1 (m) = '))

         self.starting_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.starting_pos_text)

         layout1.add_widget(Label(text = 'X2 (m) = '))

         self.ending_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.ending_pos_text)

         layout1.add_widget(Label(text = 'LOAD (kN/m/m) = '))

         self.load_per_m_text = TextInput(multiline = False)
         layout1.add_widget(self.load_per_m_text)

         layout.add_widget(layout1)

         self.load_dir_linear = Toggle_btn()
         layout.add_widget(self.load_dir_linear)

         layout2 = GridLayout(cols = 2)

         btn = Button(text = 'SAVE')
         layout2.add_widget(btn)
         btn.bind(on_press = self.add_linear_load)

         btn2 = Button(text = 'CLOSE')
         layout2.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         layout.add_widget(layout2)

         self.popup = Popup(title = 'LINEAR RAMP LOAD ', content = layout, size_hint = (.6, .6), pos_hint = {'center_x' : .5, 'center_y' : .5})

         self.popup.open()


    def popup_parabolic_ramp(self, instance):

         self.ramp_order = 2
        
         layout = BoxLayout(orientation = 'vertical')

         layout1 = GridLayout(cols = 2)

         layout1.add_widget(Label(text = 'X1 (m) = '))

         self.starting_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.starting_pos_text)

         layout1.add_widget(Label(text = 'X2 (m) = '))

         self.ending_pos_text = TextInput(multiline = False)
         layout1.add_widget(self.ending_pos_text)

         layout1.add_widget(Label(text = 'LOAD (kN/m/m/m) = '))

         self.load_per_m_text = TextInput(multiline = False)
         layout1.add_widget(self.load_per_m_text)

         layout.add_widget(layout1)

         self.load_dir_linear = Toggle_btn()
         layout.add_widget(self.load_dir_linear)

         layout2 = GridLayout(cols = 2)

         btn = Button(text = 'SAVE')
         layout2.add_widget(btn)
         btn.bind(on_press = self.add_linear_load)

         btn2 = Button(text = 'CLOSE')
         layout2.add_widget(btn2)
         btn2.bind(on_press = self.popup_dismiss)

         layout.add_widget(layout2)

         self.popup = Popup(title = 'PARABOLIC RAMP LOAD ', content = layout, size_hint = (.6, .6), pos_hint = {'center_x' : .5, 'center_y' : .5})

         self.popup.open()


    def popup_shear(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.shear_plot_cnt > 0:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "ALREADY PLOTTED"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "SCROLL BELOW !!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.shear_plot_cnt += 1
            #lay_shear = BoxLayout(orientation = 'vertical', size_hint_y=None, height = 300, spacing = 5)
            self.lay_shear.add_widget(Label(text = 'SHEAR FORCE DIAGRAM', size_hint = (1,.05)))
            graph = plot(self.BEAM.shear_force(), show = False, label = 'Shear')
            graph.save('./cache/shear.png')
            img = Image(source='./cache/shear.png')
            self.lay_shear.add_widget(img)
            self.scroll_layout.add_widget(self.lay_shear)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()
            else:
                self.shear_plot_cnt += 1
                self.d =  self.BEAM.reaction_loads
                #self.lay_shear = BoxLayout(orientation = 'vertical', size_hint_y = None, height = int(Window.size[1] * 0.8), spacing = 5)
                self.lay_shear.add_widget(Label(text = 'SHEAR FORCE DIAGRAM', size_hint = (1,.05)))
                graph = plot(self.BEAM.shear_force(), show = False, label = 'Shear')
                graph.save('./chache/shear.png')
                img = Image(source='./chache/shear.png')
                self.lay_shear.add_widget(img)
                self.scroll_layout.add_widget(self.lay_shear)


    def popup_bending(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.bending_plot_cnt > 0:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "MAY NEED TO SCROLL DOWN"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "ALREADY PLOTTED !!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.bending_plot_cnt += 1
            #lay_bending = BoxLayout(orientation = 'vertical', size_hint_y=None, height = 300, spacing = 5)
            self.lay_bending.add_widget(Label(text = 'BENDING MOMENT DIAGRAM', size_hint = (1,.05)))
            graph = plot(self.BEAM.bending_moment(), show = False)
            graph.save('./chache/bending.png')
            img = Image(source = './chache/bending.png', size_hint = (1, .95))
            self.lay_bending.add_widget(img)
            self.scroll_layout.add_widget(self.lay_bending)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()
            else:
                self.bending_plot_cnt += 1
                self.d =  self.BEAM.reaction_loads
                #lay_bending = BoxLayout(orientation = 'vertical', size_hint_y = None, height = 300, spacing = 5)
                self.lay_bending.add_widget(Label(text = 'BENDING MOMENT DIAGRAM', size_hint = (1,.05)))
                graph = plot(self.BEAM.bending_moment(), show = False)
                graph.save('./chache/bending.png')
                img = Image(source='./chache/bending.png', size_hint=(1, .95))
                self.lay_bending.add_widget(img)
                self.scroll_layout.add_widget(self.lay_bending)



    def popup_slope(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.slope_plot_cnt > 0:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "MAY NEED TO SCROLL DOWN"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "ALREADY PLOTTED !!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.slope_plot_cnt += 1
            #lay_slope = BoxLayout(orientation = 'vertical', size_hint_y=None, height = 300, spacing = 5)
            self.lay_slope.add_widget(Label(text = 'SLOPE DIAGRAM', size_hint = (1,.05)))
            graph = plot(self.BEAM.slope(), show = False)
            graph.save('./chache/slope.png')
            img = Image(source='./chache/slope.png', size_hint=(1, .95))
            self.lay_slope.add_widget(img)
            self.scroll_layout.add_widget(self.lay_slope)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()
            else:
                self.slope_plot_cnt += 1
                self.d =  self.BEAM.reaction_loads
                #lay_slope = BoxLayout(orientation = 'vertical', size_hint_y = None, height = 300, spacing = 5)
                self.lay_slope.add_widget(Label(text = 'SLOPE DIAGRAM', size_hint = (1,.05)))
                graph = plot(self.BEAM.slope(), show = False)
                graph.save('./chache/slope.png')
                img = Image(source = './chache/slope.png', size_hint = (1, .95))
                self.lay_slope.add_widget(img)
                self.scroll_layout.add_widget(self.lay_slope)

    
    def popup_deflection(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.deflection_plot_cnt > 0:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "MAY NEED TO SCROLL DOWN"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "ALREADY PLOTTED !!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.deflection_plot_cnt += 1
            #lay_deflection = BoxLayout(orientation = 'vertical', size_hint_y=None, height = 300, spacing = 5)
            self.lay_deflection.add_widget(Label(text = 'DEFLECTION DIAGRAM', size_hint = (1,.05)))
            graph = plot(self.BEAM.deflection(), show = False)
            graph.save('./chache/deflection.png')
            img = Image(source = './chache/deflection.png', size_hint = (1, .95))
            self.lay_deflection.add_widget(img)
            self.scroll_layout.add_widget(self.lay_deflection)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()
            else:
                self.deflection_plot_cnt += 1
                self.d =  self.BEAM.reaction_loads
                #lay_deflection = BoxLayout(orientation = 'vertical', size_hint_y = None, height = 300, spacing = 5)
                self.lay_deflection.add_widget(Label(text = 'DEFLECTION DIAGRAM', size_hint = (1,.05)))
                graph = plot(self.BEAM.deflection(), show = False)
                graph.save('./chache/deflection.png')
                img = Image(source = './chache/deflection.png', size_hint = (1, .95))
                self.lay_deflection.add_widget(img)
                self.scroll_layout.add_widget(self.lay_deflection)
                    
    
    def popup_loading(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.loading_plot_cnt > 0:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "MAY NEED TO SCROLL DOWN"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "ALREADY PLOTTED !!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()
            return

        if self.d:
            self.loading_plot_cnt += 1
            #lay_loading = BoxLayout(orientation = 'vertical', size_hint_y=None, height = 300, spacing = 5)
            self.lay_loading.add_widget(Label(text = 'LOADING DIAGRAM', size_hint = (1,.05)))
            graph = plot(self.BEAM.load, show = False)
            graph.save('./chache/loading.png')
            img = Image(source='./chache/loading.png', size_hint=(1, .95))
            self.lay_loading.add_widget(img)
            self.scroll_layout.add_widget(self.lay_loading)
        else:

            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)

            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()
            else:
                self.loading_plot_cnt += 1
                self.d =  self.BEAM.reaction_loads
                #lay_loading = BoxLayout(orientation = 'vertical', size_hint_y = None, height = 300, spacing = 5)
                self.lay_loading.add_widget(Label(text = 'LOADING DIAGRAM', size_hint = (1,.05)))
                graph = plot(self.BEAM.load, show = False)
                graph.save('./chache/loading.png')
                img = Image(source='./chache/loading.png', size_hint=(1, .95))
                self.lay_loading.add_widget(img)
                self.scroll_layout.add_widget(self.lay_loading)
                


    def popup_reaction(self, instance):

        if self.analysis_started == False:
            self.default_val.disabled = True
            self.Fix.disabled = True
            self.Roller.disabled = True
            self.Pin.disabled = True
            self.pt_load.disabled = True
            self.Moment.disabled = True
            self.const_p.disabled = True
            self.Lramp.disabled = True
            self.Pramp.disabled = True

            self.analysis_started = True
        
        else:
            pass

        if self.d:
            layout_react = BoxLayout(orientation = 'vertical')
            for i, j in self.d.items():
                alphabet, distance = str(i).split('_')
                if alphabet == 'R':
                    text1 = 'Reaction Force at x = {} m is {} kN'.format(distance, j)
                elif alphabet == 'M':
                    text1 = 'Reaction Moment at x = {} m is {} kN*m'.format(distance, j)

                layout_react.add_widget(Label(text = text1))
            btn = Button(text = 'CLOSE')
            layout_react.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "SUPPPORT REACTIONS",content = layout_react , size_hint = (.8, .8), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()

        else:
            try:
                self.BEAM.solve_for_reaction_loads(*self.reaction_vars)
            except:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "INSUFFICIENT DATA GIVEN!!"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "BEAM UNSTABLE!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5}, )
                self.popup_in_popup.open()
            else:
                layout_react = BoxLayout(orientation = 'vertical')
                self.d = self.BEAM.reaction_loads
                for i, j in self.d.items():
                    alphabet, distance = str(i).split('_')
                    if alphabet == 'R':
                        text1 = 'Reaction Force at x = {} m is {} kN'.format(distance, j)
                    elif alphabet == 'M':
                        text1 = 'Reaction Moment at x = {} m is {} kN*m'.format(distance, j)

                    layout_react.add_widget(Label(text = text1))
                btn = Button(text = 'CLOSE')
                layout_react.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "SUPPPORT REACTIONS", content = layout_react , size_hint = (.8, .8), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()


    def popup_sup_and_load(self, instance):

        
        self.mlayout = BoxLayout(orientation = 'vertical')
        self.head = GridLayout(cols = 2, size_hint = (1, .1))
        self.head.add_widget(Label(text = "SUPPORTS"))
        self.head.add_widget(Label(text = "LOADS"))
        self.mlayout.add_widget(self.head)
        self.layout = GridLayout(cols = 2, size_hint = (1, .8))
        self.layout.add_widget(self.sup)
        self.layout.add_widget(self.load)
        self.mlayout.add_widget(self.layout)
        btn = Button(text = 'CLOSE', size_hint = (1, .1))
        self.mlayout.add_widget(btn)
        btn.bind(on_press = self.dismiss_pop_sup_and_load)
        self.popup_sl = Popup(title = "SUPPORTS AND LOADS",content = self.mlayout , size_hint = (.98, .98), pos_hint = {'center_x' : .5, 'center_y' : .5})
        self.popup_sl.open()
        
        pass

    def dismiss_pop_sup_and_load(self, instance):
        self.layout.remove_widget(self.sup)
        self.layout.remove_widget(self.load)
        self.popup_sl.dismiss()

    def popup_newbeam(self, instance):
        del self.BEAM
        self.E = "20"
        self.I = "40"
        self.Len = '10'
        self.reaction_vars = []
        self.d = None
        self.shear_plot_cnt = 0
        self.slope_plot_cnt = 0
        self.bending_plot_cnt = 0
        self.deflection_plot_cnt = 0
        self.loading_plot_cnt = 0

        if self.analysis_started != False:
            self.default_val.disabled = False
            self.Fix.disabled = False
            self.Roller.disabled = False
            self.Pin.disabled = False
            self.pt_load.disabled = False
            self.Moment.disabled = False
            self.const_p.disabled = False
            self.Lramp.disabled = False
            self.Pramp.disabled = False

            self.analysis_started = False
        
        else:
            pass

        self.BEAM = Beam(self.Len, self.E, self.I)

        self.scroll_layout.clear_widgets()

        if os.path.exists('shear.png'):
            os.remove('shear.png')

        if os.path.exists('bending_moment.png'):
            os.remove('bending_moment.png')

        if os.path.exists('slope.png'):
            os.remove('slope.png')

        if os.path.exists('deflection.png'):
            os.remove('deflection.png')
        """
        layout = BoxLayout(orientation = 'vertical')
        layout.add_widget(Label(text = "ANALYSE A NEW BEAM NOW!!!"))
        btn = Button(text = 'CLOSE')
        layout.add_widget(btn)
        btn.bind(on_press = self.popup_in_popup_dismiss)
        self.popup_in_popup = Popup(title = "!!NEW!!",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
        self.popup_in_popup.open()
        """

    def set_E_I_Len(self, instance):

        self.E = self.E_text.text
        self.I = self.I_text.text
        self.Len = self.len_text.text

        self.BEAM = Beam(self.Len, self.E, self.I)

        self.popup.dismiss()

    def add_fix(self, instance):
        if self.fix_text.text:
            if int(self.fix_text.text) >= 0 and int(self.fix_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.fix_text.text)))
                self.reaction_vars.append(symbols('M_{}'.format(self.fix_text.text)))
                self.BEAM.apply_support(self.fix_text.text, 'fixed')
                self.BEAM.bc_deflection.append((self.fix_text.text, 0))
                self.BEAM.bc_slope.append((self.fix_text.text, 0))

                self.sup.add_widget(Label(text = f"Fixed support at {self.fix_text.text} m"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "YOU HAVEN'T ENTERED POSITION"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "NOTHING TO SAVE",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()

    def add_roller(self, instance):

        if self.roller_text.text:

            if int(self.roller_text.text) >= 0 and int(self.roller_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.roller_text.text)))
                self.BEAM.apply_support(self.roller_text.text, 'roller')
                self.BEAM.bc_deflection.append((self.roller_text.text, 0))

                self.sup.add_widget(Label(text = f"Roller support at {self.roller_text.text} m"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "YOU HAVEN'T ENTERED POSITION"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "NOTHING TO SAVE",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()


    def add_pin(self, instance):

        if self.pin_text.text:

            if int(self.pin_text.text) >= 0 and int(self.pin_text.text) <= int(self.Len):

                self.reaction_vars.append(symbols('R_{}'.format(self.pin_text.text)))
                self.BEAM.apply_support(self.pin_text.text, 'pin')
                self.BEAM.bc_deflection.append((self.pin_text.text, 0))

                self.sup.add_widget(Label(text = f"Pin support at {self.pin_text.text} m"))

                self.popup.dismiss()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "YOU HAVEN'T ENTERED POSITION"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "NOTHING TO SAVE",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()


    def add_vertical_load(self, instance):
        if self.vertical_load_mag_text.text != '' and self.vertical_load_pos_text.text != '':

            if int(self.vertical_load_pos_text.text) >= 0 and int(self.vertical_load_pos_text.text) <= int(self.Len):

                states = self.load_dir.get_state()
                print(states)
                if (states[0] == 'normal' and states[1] == 'down') or (states[0] == 'down' and states[1] == 'normal'):

                    if states[0] == 'normal' and states[1] == 'down':

                        self.BEAM.apply_load(self.vertical_load_mag_text.text, self.vertical_load_pos_text.text, -1)

                        self.load.add_widget(Label(text = f"Upward Point load of {self.vertical_load_mag_text.text} kN at {self.vertical_load_pos_text.text} m"))

                        self.popup.dismiss()
                    else:
                        self.BEAM.apply_load('-' + self.vertical_load_mag_text.text, self.vertical_load_pos_text.text, -1)

                        self.load.add_widget(Label(text = f"Downward Point load of {self.vertical_load_mag_text.text} kN at {self.vertical_load_pos_text.text} m"))

                        self.popup.dismiss()


                else:
                    layout = BoxLayout(orientation = 'vertical')
                    layout.add_widget(Label(text = "YOU MUST CHOOSE ONE DIRECTION"))
                    btn = Button(text = 'CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press = self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title = "IN WHICH DIR. DO I APPLY LOAD ?",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "ENTER BOTH LOAD MAG. AND POS."))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "INSUFFICIENT INFO !",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()

    def add_moment(self, instance):

        if self.moment_pos_text.text != '' and self.moment_mag_text.text != '':
            if int(self.moment_pos_text.text) >= 0 and int(self.moment_pos_text.text) <= int(self.Len):


                states = self.moment_dir.get_state()
                print(states)
                if (states[0] == 'normal' and states[1] == 'down') or (states[0] == 'down' and states[1] == 'normal'):

                    if states[0] == 'normal' and states[1] == 'down':

                        self.BEAM.apply_load(self.moment_mag_text.text, self.moment_pos_text.text, -2)

                        self.load.add_widget(Label(text = f"Anticlockwise moment of {self.moment_mag_text.text} kN-m at {self.moment_pos_text.text} m"))

                        self.popup.dismiss()
                    else:
                        self.BEAM.apply_load('-' + self.moment_mag_text.text, self.moment_pos_text.text, -2)

                        self.load.add_widget(Label(text = f"Clockwise moment of {self.moment_mag_text.text} kN-m at {self.moment_pos_text.text} m"))

                        self.popup.dismiss()


                else:
                    layout = BoxLayout(orientation = 'vertical')
                    layout.add_widget(Label(text = "YOU MUST CHOOSE ONE DIRECTION"))
                    btn = Button(text = 'CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press = self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title = "IN WHICH DIR. DO I APPLY MOMENT ?",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "ENTER BOTH MOMENT MAG. AND POS."))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "INSUFFICIENT INFO !",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()


    def add_linear_load(self, instance):

        if self.starting_pos_text.text != '' and self.ending_pos_text.text != '' and self.load_per_m_text.text != '':

            if int(self.starting_pos_text.text) >= 0 and int(self.starting_pos_text.text) <= int(self.Len) and int(self.ending_pos_text.text) >= 0 and int(self.ending_pos_text.text) <= int(self.Len):
                
                if int(self.starting_pos_text.text) != int(self.ending_pos_text.text):

                    states = self.load_dir_linear.get_state()
                    print(states)
                    if (states[0] == 'normal' and states[1] == 'down') or (states[0] == 'down' and states[1] == 'normal'):

                        if self.ramp_order == 0: 
                            dload_type = "constant pressure"
                            unit = "kN/m"
                        elif self.ramp_order == 1: 
                            dload_type = "linear ramp"
                            unit = "kN/m/m"
                        elif self.ramp_order == 2: 
                            dload_type = "prabolic ramp"
                            unit = "kN/m/m/m"

                        if states[0] == 'normal' and states[1] == 'down':

                            self.BEAM.apply_load(self.load_per_m_text.text, self.starting_pos_text.text, self.ramp_order, int(self.ending_pos_text.text))

                            self.load.add_widget(Label(text = f"Upward {dload_type} of {self.load_per_m_text.text} {unit} from {self.starting_pos_text.text} m to {self.ending_pos_text.text} m"))

                            self.popup.dismiss()
                        else:
                            self.BEAM.apply_load('-' + self.load_per_m_text.text, self.starting_pos_text.text, self.ramp_order, int(self.ending_pos_text.text))

                            self.load.add_widget(Label(text = f"Downward {dload_type} of {self.load_per_m_text.text} {unit} from {self.starting_pos_text.text} m to {self.ending_pos_text.text} m"))

                            self.popup.dismiss()


                    else:
                        layout = BoxLayout(orientation = 'vertical')
                        layout.add_widget(Label(text = "YOU MUST CHOOSE ONE DIRECTION"))
                        btn = Button(text = 'CLOSE')
                        layout.add_widget(btn)
                        btn.bind(on_press = self.popup_in_popup_dismiss)
                        self.popup_in_popup = Popup(title = "IN WHICH DIR. DO I APPLY THE LOAD ?",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                        self.popup_in_popup.open()

                else:

                    layout = BoxLayout(orientation = 'vertical')
                    layout.add_widget(Label(text = "STARTING AND ENDING POSITIONS\nCAN'T BE SAME !"))
                    btn = Button(text = 'CLOSE')
                    layout.add_widget(btn)
                    btn.bind(on_press = self.popup_in_popup_dismiss)
                    self.popup_in_popup = Popup(title = "INVALID ENTRY !",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                    self.popup_in_popup.open()

            else:
                layout = BoxLayout(orientation = 'vertical')
                layout.add_widget(Label(text = "ENTER POSITION ON THE BEAM"))
                btn = Button(text = 'CLOSE')
                layout.add_widget(btn)
                btn.bind(on_press = self.popup_in_popup_dismiss)
                self.popup_in_popup = Popup(title = "INVALID POSTION",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
                self.popup_in_popup.open()

        else:
            layout = BoxLayout(orientation = 'vertical')
            layout.add_widget(Label(text = "ENTER ALL START, END AND LOAD"))
            btn = Button(text = 'CLOSE')
            layout.add_widget(btn)
            btn.bind(on_press = self.popup_in_popup_dismiss)
            self.popup_in_popup = Popup(title = "INSUFFICIENT INFO !",content = layout , size_hint = (.4, .4), pos_hint = {'center_x' : .5, 'center_y' : .5})
            self.popup_in_popup.open()


    def popup_dismiss(self, instance):
        self.popup.dismiss()


    def popup_in_popup_dismiss(self, instance):
        self.popup_in_popup.dismiss()


class FirstPage(FloatLayout):
    def __init__(self, **kwargs):
        super(FirstPage, self).__init__(**kwargs)

        Window.clearcolor = (.234, .456, .678, .8)
        
        self.name = Label(text = "[b]BEAM SOLVER[/b]",
                     markup = True,
                     font_size = 110,
                     color = (1, 1, 1, 1),
                     pos_hint = {'center_x' : .5, 'center_y' : .6},
                     size_hint = (1, .4)
                     )
        self.add_widget(self.name)
        self.start = Button(text = '[b][i]New Beam[/i][/b]',
                            markup = True,
                            size_hint = (.3, .1),
                            pos_hint = {'x' : .35, 'y' : .3},
                            background_color = (0, 0, .7, .8),
                            color = (1, 1, 1, 1),
                            font_size = 20
                            )
        self.start.bind(on_press = self.main_page)
        self.add_widget(self.start)

    def main_page(self, instance):

        beam.screen_manager.current = 'Main Page'

        
class BApp(App):
    def build(self):

        self.screen_manager = ScreenManager()

        self.fpage = FirstPage()
        screen = Screen(name = 'First Page')
        screen.add_widget(self.fpage)
        self.screen_manager.add_widget(screen)

        self.panel = Panel()
        screen = Screen(name = 'Main Page')
        screen.add_widget(self.panel)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == "__main__":
    beam = BApp()
    beam.run()