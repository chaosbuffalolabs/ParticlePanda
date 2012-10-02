import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader

class ParticleBuilder(Widget):
	def __init__(self, **kwargs):
		super(ParticleBuilder,self).__init__(**kwargs)
		Clock.schedule_once(self.setup_window)
		

	def setup_window(self, dt):
		tp = TabbedPanel()
		th = TabbedPanelHeader(text='Tab1')
		tp.pos = (100, 100)
		tp.size = (400,500)
		th.content = ParticleXY()
		tp.default_tab = TabbedPanelHeader(text='Default')
		tp.add_widget(th)
		th2 = TabbedPanelHeader(text='Tab2')
		th2.content = Blank()
		tp.add_widget(th2)
		self.add_widget(tp)

class Blank(FloatLayout):
	pass

class ParticleXY(Widget):
	pass

class Particle_Pos_Prop(BoxLayout):
	pos_type = StringProperty(None)
	scatter_minimum = NumericProperty(-100)
	scatter_maximum = NumericProperty(100)
	scatter_value = NumericProperty(0)

class Particle_Property(BoxLayout):
	prop_type = StringProperty(None)
	initial_minimum = NumericProperty(-100)
	initial_maximum = NumericProperty(100)
	initial_value = NumericProperty(0)
	scatter_minimum = NumericProperty(-100)
	scatter_maximum = NumericProperty(100)
	scatter_value = NumericProperty(0)
	rate_minimum = NumericProperty(0)
	rate_maximum = NumericProperty(5)
	rate_value = NumericProperty(.5)
	amount_minimum = NumericProperty(-100)
	amount_maximum = NumericProperty(100)
	amount_value = NumericProperty(0)
	iter_minimum = NumericProperty(0)
	iter_maximum = NumericProperty(10)
	iter_value = NumericProperty(1)


Factory.register('ParticleXY', ParticleXY)
Factory.register('Particle_Property', Particle_Property)
Factory.register('Particle_Pos_Prop', Particle_Pos_Prop)

class ParticleBuilderApp(App):
    def build(self):

        return ParticleBuilder()

if __name__ == '__main__':
    ParticleBuilderApp().run()

