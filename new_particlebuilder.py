import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder

class ParticleBuilder(Widget):
	pass


class ParticleXY(Widget):
	pass

class ParticleColor(Widget):
	pass

class ParticleVariationLayout(Widget):
	num_variants = NumericProperty(0)
	
	def add_variant_button(self):
		if self.num_variants < 9:
			self.num_variants += 1
			ctx = {'text': 'Variant'.join(str(self.num_variants))}
			button = Builder.template('VariantButton', **ctx)
			self.variation_layout.add_widget(button)


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

Factory.register('ParticleColor', ParticleColor)
Factory.register('ParticleXY', ParticleXY)
Factory.register('Particle_Property', Particle_Property)
Factory.register('Particle_Pos_Prop', Particle_Pos_Prop)
Factory.register('ParticleBuilder', ParticleBuilder)
Factory.register('ParticleVariationLayout', ParticleVariationLayout)




class ParticleBuilderApp(App):
    def build(self):
    	pass

    def on_start(self, *largs):
  		win = self.root.get_parent_window()
  		print win.size

if __name__ == '__main__':
    ParticleBuilderApp().run()

