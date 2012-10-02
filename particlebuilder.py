import kivy
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.app import App
from cbl_gui_elements import RectangleWidget, TagItemContainer, TagItem



class VariationSelector(TagItemContainer):
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
    available_parameters = ['texture', 'lifetime', 'x', 'y', 'velocity_x', 'velocity_y', 'color_r', 'color_g', 'color_b', 'color_a', 'width', 'height']

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


class ValueEditor(Widget):
    def __init__(self,parameter,**kwargs):
        super(ValueEditor, self).__init__(**kwargs)


class EffectParameter():
    
    initial_value = 0

    #leave scatter as None to leave out of CBLP and thus accept default
    scatter = None

    interval_change = None

    def __init__(self,name):
        self.name = name



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
        self.value_editor = ValueEditor(None,size_hint = (1.,1.))
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
