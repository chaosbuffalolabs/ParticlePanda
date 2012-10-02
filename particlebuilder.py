import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.app import App
from cbl_gui_elements import RectangleWidget, TagItemContainer, TagItem



class VariationSelector(TagItemContainer):
    """Subclass of TagItemContainer, simply adds variations sequentially and calls main.change_variation when one is selected."""

    variation_count = NumericProperty(1)

    def __init__(self, main = None, **kwargs):
        super(VariationSelector,self).__init__(**kwargs)
        self.main = main
        self.items = ['Variation 1']

    def item_callback(self,instance):
        if instance.text == '[blank]':
            self.variation_count += 1
            self.add_item('Variation %s' %(self.variation_count,))
        else:
            self.main.change_variation(instance.text)

class ParameterEditor(TagItemContainer):
    """Subclass of TagItemContainer, allows user to add parameters from available_parameters. 
    When a parameter tag is touched, runs main.change_parameter() to tell the main widget to switch to the appropriate ValueEditor"""

    available_parameters = ['frequency','texture', 'lifetime', 'x', 'y', 'velocity_x', 'velocity_y', 'color_r', 'color_g', 'color_b', 'color_a', 'width', 'height']

    def __init__(self, main = None, **kwargs):
        super(ParameterEditor,self).__init__(**kwargs)
        self.main = main
        self.items = ['frequency', 'texture', 'frame_rate', 'lifetime', 'width', 'height']

    def item_callback(self,instance):
        if instance.text == '[blank]':
            pass
            # need a popup here that lets you select from those available_parameters that are not already in self.items
        else:
            pass
            # needs to ask parent to switch to new instance of ValueEditor based on this parameter

class ValueSlider(Widget):
    value = NumericProperty(0)
    min = NumericProperty(0)
    max = NumericProperty(255)

class LabeledValueSlider(Widget):
    value = NumericProperty(0)
    min = NumericProperty(0)
    max = NumericProperty(255)
    labeltext = StringProperty('Slider')


class ValueEditor(BoxLayout):
    """This is the class with all the actual sliders and buttons that control the effects. 
    There will be one for each parameter -- the class takes an EffectParameter as input"""
    tb_initial_value = ObjectProperty(None)

    def __init__(self,parameter,**kwargs):
        super(ValueEditor, self).__init__(orientation='vertical', margins=5, spacing=5, **kwargs)
        self.parameter = parameter
        Clock.schedule_once(self.setup_window)

    def setup_window(self,dt):
        self.tb_initial_value = ToggleButton(text='Initial Value', height = 25, size_hint_y = None,)
        self.tb_initial_value.bind(state=self.toggle_initial_value_slider)
        self.slider_initial_value = ValueSlider(height=25, size_hint_y=None, min=self.parameter.initial_value_range[0], max=self.parameter.initial_value_range[1])
        
        self.tb_scatter = ToggleButton(text='Scatter', height = 25, size_hint_y = None, )
        self.tb_scatter.bind(state=self.toggle_scatter_slider)
        self.slider_scatter = ValueSlider(height=25, size_hint_y=None, min=self.parameter.initial_value_range[0], max=self.parameter.initial_value_range[1])
        
        self.tb_interval_change = ToggleButton(text='Interval Change', height = 25, size_hint_y = None, )
        self.tb_interval_change.bind(state=self.toggle_interval_change_sliders)
        self.slider_interval_change_rate = LabeledValueSlider(labeltext='Rate', height=50, size_hint_y=None, min=0.05, max=10.)
        self.slider_interval_change_amount = LabeledValueSlider(labeltext='Amount', height=50, size_hint_y=None, min=self.parameter.initial_value_range[0], max=self.parameter.initial_value_range[1])
        self.slider_interval_change_max_iter = LabeledValueSlider(labeltext='Iterations', height=50, size_hint_y=None, min=1, max=30)

        self.add_widget(self.tb_initial_value)
        self.add_widget(self.tb_scatter)
        self.add_widget(self.tb_interval_change)
        self.add_widget(Widget())


    def toggle_initial_value_slider(self,instance,value):
        if self.slider_initial_value in self.children:
            self.remove_widget(self.slider_initial_value)
        else:
            self.add_widget(self.slider_initial_value, self.children.index(self.tb_initial_value))

    def toggle_scatter_slider(self,instance,value):
        if self.slider_scatter in self.children:
            self.remove_widget(self.slider_scatter)
        else:
            self.add_widget(self.slider_scatter, self.children.index(self.tb_scatter))

    def toggle_interval_change_sliders(self,instance,value):
        tb_index = self.children.index(self.tb_interval_change)

        if self.slider_interval_change_rate in self.children:
            for x in [self.slider_interval_change_rate, self.slider_interval_change_amount, self.slider_interval_change_max_iter]:
                self.remove_widget(x)
        else:
            for idx, x in enumerate([self.slider_interval_change_rate, self.slider_interval_change_amount, self.slider_interval_change_max_iter]):
                self.add_widget(x, tb_index + idx)

class EffectParameter():
    _initial_value_range_lookup = {
            'frequency': (0,1),
            'lifetime': (0,25),
            'velocity_x': (-400,400),
            'velocity_y': (-400,400),
            'color_r': (0,255),
            'color_g': (0,255),
            'color_b': (0,255),
            'color_a': (0,255),
            'width': (0,255),
            'height': (0,255),
    }

    _scatter_range_lookup = {
            'lifetime': (0,25),
            'velocity_x': (0,400),
            'velocity_y': (0,400),
            'color_r': (0,255),
            'color_g': (0,255),
            'color_b': (0,255),
            'color_a': (0,255),
            'width': (0,255),
            'height': (0,255),
    }

    initial_value = 0
    #leave scatter as None to leave out of CBLP and thus accept default
    scatter = None
    interval_change = None

    def __init__(self,name):
        self.name = name
        self.initial_value_range = self._initial_value_range_lookup[name]
        self.scatter_range = self. _scatter_range_lookup[name]


class MainScreen(BoxLayout):
    def __init__(self,**kwargs):
        super(MainScreen,self).__init__(orientation='vertical', spacing = 10, padding = 10, **kwargs)
        Clock.schedule_once(self.setup_window)

    def setup_window(self,dt):
        controls_bl = BoxLayout(orientation='horizontal',size_hint=(1,.5))

        bl1 = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10, size_hint=(.25,1.))
        bl1.add_widget(Label(text='Particle Variations',height=15,size_hint_y=None))
        bl1.add_widget(RectangleWidget(color = (0,204,255), height = 3, size_hint_y = None))
        self.variation_selector = VariationSelector(main = self)
        bl1.add_widget(self.variation_selector)

        bl2 = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10, size_hint=(.25,1.))
        bl2.add_widget(Label(text='Parameters',height=15,size_hint_y=None))
        bl2.add_widget(RectangleWidget(color = (0,204,255), height = 3, size_hint_y = None))
        self.parameter_editor = ParameterEditor(main=self)
        bl2.add_widget(self.parameter_editor)
        
        bl3 = BoxLayout(orientation = 'vertical', spacing = 10, padding = 10, size_hint=(.5,1.))
        bl3.add_widget(Label(text='Values',height=15,size_hint_y=None))
        bl3.add_widget(RectangleWidget(color = (0,204,255), height = 3, size_hint_y = None))
        self.value_editor = ValueEditor(EffectParameter('lifetime'),size_hint = (1.,1.))
        bl3.add_widget(self.value_editor)

        self.preview_pane = FloatLayout(size_hint=(1,.5))

        controls_bl.add_widget(bl1)
        controls_bl.add_widget(bl2)
        controls_bl.add_widget(bl3)

        self.add_widget(self.preview_pane)
        self.add_widget(controls_bl)

    def change_variation(self,variation_id):
        pass
        # here we need code that switches the active parameter list to the new variation. we'll want a visual cue that this is happening too, like highlighting the active variation 

class ParticleBuilderApp(App):
    def build(self):
        # 'atlas://VFX/smoke_particles/VFX_SmokeParticle'
        fl = MainScreen(pos=(0,0),size=Window.size)
        return fl



if __name__ == '__main__':
    ParticleBuilderApp().run()
