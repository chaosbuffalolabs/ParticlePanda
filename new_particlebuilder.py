import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty, BoundedNumericProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder

class ParticleBuilder(Widget):
	pass

class ParticleParamsLayout(Widget):
	all_tabs = ListProperty(None)

	def create_tab(self, num_tab):
		th = TabbedPanelHeader(text = 'tab ' + str(num_tab))
		tab_content = self.get_content(num_tab)
		th.content = tab_content
		self.all_tabs.append(th)

	def add_tab_to_layout(self, num_tab):
		self.particle_tabs.add_widget(self.all_tabs[num_tab-1])

	def remove_tab_from_layout(self, num_tab):
		self.particle_tabs.remove_widget(self.all_tabs[num_tab-1])

	def get_current_tab(self):
		return self.current_tab

	def get_default_tab(self):
		default_content = Default_Particle_Panel()
		return default_content
	
	def get_content(self, num_tab):
		if num_tab == 1:
			s = ParticlePanel()
			return s
		if num_tab == 2:
			s = BehaviorPanel()
			return s
		if num_tab >= 3:
			s = ColorPanel()
			return s
		
class ParticleVariationLayout(Widget):
	num_variants = NumericProperty(0)
	
	def add_variant_button(self):
		if self.num_variants < 10:
			self.num_variants += 1
			num_tab = self.num_variants
			pbuilder = self.parent.parent
			ctx = {'text': 'Variant' + str(num_tab), 'group': 'PVar', 'pbuilder': pbuilder, 'num_tab': num_tab}
			button = Builder.template('VariantButton', **ctx)
			self.variation_layout.add_widget(button)
			pbuilder.params_layout.create_tab(num_tab)

class Default_Particle_Panel(Widget):
	pass

class ParticlePanel(Widget):
	max_num_particles = BoundedNumericProperty(200, min=0, max=1000)
	life_span = BoundedNumericProperty(2, min=0, max=10)
	life_span_variance = BoundedNumericProperty(0, min=0, max=10)
	start_size = BoundedNumericProperty(16, min=0, max=70)
	start_size_variance = BoundedNumericProperty(0, min=0, max=70)
	end_size = BoundedNumericProperty(16, min=0, max=70)
	end_size_variance = BoundedNumericProperty(0, min=0, max=70)
	emit_angle = BoundedNumericProperty(0, min=0, max=360)
	emit_angle_variance = BoundedNumericProperty(0, min=0, max=360)
	start_rotation = BoundedNumericProperty(0, min=0, max=360)
	start_rotation_variance = BoundedNumericProperty(0, min=0, max=360)
	end_rotation = BoundedNumericProperty(0, min=0, max=360)
	end_rotation_variance = BoundedNumericProperty(0, min=0, max=360)

class BehaviorPanel(Widget):
	pass

class ColorPanel(Widget):
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

Factory.register('ParticleBuilder', ParticleBuilder)
Factory.register('ParticleVariationLayout', ParticleVariationLayout)
Factory.register('ParticleParamsLayout', ParticleParamsLayout)
Factory.register('ParticlePanel', ParticlePanel)
Factory.register('BehaviorPanel', BehaviorPanel)
Factory.register('ColorPanel', ColorPanel)

class ParticleBuilderApp(App):
    def build(self):
    	pass

if __name__ == '__main__':
    ParticleBuilderApp().run()

