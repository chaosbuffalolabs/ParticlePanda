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
	all_tabs2 = ListProperty(None)
	
	def create_tab(self, num_tab):
		new_num_variants = num_tab
		th1 = TabbedPanelHeader(text = 'tab ' + str(num_tab) + '-1')
		th2 = TabbedPanelHeader(text = 'tab ' + str(num_tab) + '-2')
		th1_tab_content = self.get_particle_content(num_tab)
		th2_tab_content = self.get_behavior_content(num_tab)
		th1.content = th1_tab_content
		th2.content = th2_tab_content
		self.all_tabs.append(th1)
		self.all_tabs2.append(th2)

	def add_tab_to_layout(self, num_tab):
		self.particle_tabs.add_widget(self.all_tabs[num_tab-1])
		self.particle_tabs.add_widget(self.all_tabs2[num_tab-1])

	def remove_tab_from_layout(self, num_tab):
		self.particle_tabs.remove_widget(self.all_tabs[num_tab-1])
		self.particle_tabs.remove_widget(self.all_tabs2[num_tab-1])

	def get_current_tab(self):
		return self.current_tab

	def get_default_tab(self):
		default_content = Default_Particle_Panel()
		return default_content
	
	def get_particle_content(self, num_tab):
		return ParticlePanel()

	def get_behavior_content(self, num_tab):
		return BehaviorPanel()
		
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

class Particle_Property_Slider(Widget):
	slider_bounds_min = NumericProperty(0)
	slider_bounds_max = NumericProperty(100)
	slider_bounds_init_value = NumericProperty(0)
	slider_step = NumericProperty(1.0)

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
	emitter_type = NumericProperty(0)
	## Gravity Emitter Params
	emitter_x_variance = BoundedNumericProperty(0, min=0, max=1000)
	emitter_y_variance = BoundedNumericProperty(0, min=0, max=1000)
	gravity_x = BoundedNumericProperty(0, min=-500, max=500)
	gravity_y = BoundedNumericProperty(0, min=-500, max=500)
	speed = BoundedNumericProperty(0, min=0, max=500)
	speed_variance = BoundedNumericProperty(0, min=0, max=500)
	radial_acceleration = BoundedNumericProperty(100, min=-400, max=400)
	radial_acceleration_variance = BoundedNumericProperty(0, min=0, max=400)
	tangential_acceleration = BoundedNumericProperty(0, min=-500, max=500)
	tangential_acceleration_variance = BoundedNumericProperty(0, min=0, max=500)

	## Radial Emitter Params
	max_radius = BoundedNumericProperty(100, min=0, max=500)
	max_radius_variance = BoundedNumericProperty(0, min=0, max=500)
	min_radius = BoundedNumericProperty(0, min=0, max=500)
	rotate_per_second = BoundedNumericProperty(0, min=-360, max=360)
	rotate_per_second_variance = BoundedNumericProperty(0, min=0, max=360)

	def set_emitter_type(self, num_type):
		self.emitter_type = num_type

class ColorPanel(Widget):
	#all colors given as rgba
	start_color_r = BoundedNumericProperty(1., min=0, max=1.)
	start_color_r_variance = BoundedNumericProperty(.1, min=0, max=1.)
	start_color_g = BoundedNumericProperty(1., min=0, max=1.)
	start_color_g_variance = BoundedNumericProperty(.1, min=0, max=1.)
	start_color_b = BoundedNumericProperty(1., min=0, max=1.)
	start_color_b_variance = BoundedNumericProperty(.1, min=0, max=1.)
	start_color_a = BoundedNumericProperty(1., min=0, max=1.)
	start_color_a_variance = BoundedNumericProperty(.1, min=0, max=1.)
	end_color_r = BoundedNumericProperty(0, min=0, max=1.)
	end_color_r_variance = BoundedNumericProperty(.1, min=0, max=1.)
	end_color_g = BoundedNumericProperty(0, min=0, max=1.)
	end_color_g_variance = BoundedNumericProperty(.1, min=0, max=1.)
	end_color_b = BoundedNumericProperty(0, min=0, max=1.)
	end_color_b_variance = BoundedNumericProperty(.1, min=0, max=1.)
	end_color_a = BoundedNumericProperty(0, min=0, max=1.)
	end_color_a_variance = BoundedNumericProperty(.1, min=0, max=1.)



Factory.register('ParticleBuilder', ParticleBuilder)
Factory.register('ParticleVariationLayout', ParticleVariationLayout)
Factory.register('ParticleParamsLayout', ParticleParamsLayout)
Factory.register('ParticlePanel', ParticlePanel)
Factory.register('BehaviorPanel', BehaviorPanel)
Factory.register('ColorPanel', ColorPanel)
Factory.register('Particle_Property_Slider', Particle_Property_Slider)

class ParticleBuilderApp(App):
    def build(self):
    	pass

if __name__ == '__main__':
    ParticleBuilderApp().run()

