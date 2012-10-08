import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy_particle import *
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty, BoundedNumericProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder

class ParticleBuilder(Widget):
    demo_particles = ListProperty(None)
    demo_particle = ObjectProperty(ParticleSystem)

    def __init__(self, **kwargs):
        super(ParticleBuilder, self).__init__(**kwargs)
        
    def create_particle_system(self):
        texture = Image('media/particle.png').texture
        demo_particle = ParticleSystem(texture, None)
        self.demo_particles.append(demo_particle)

    def add_demo_particle_system(self, num_tab):
        self.demo_particle = self.demo_particles[num_tab-1]
        self.demo_particle.emitter_x = self.particle_window.pos[0] + self.particle_window.width *.5
        self.demo_particle.emitter_y = self.particle_window.pos[1] + self.particle_window.height *.5
        self.add_widget(self.demo_particle)
        self.demo_particle.start()

    def remove_demo_particle_system(self):
        self.demo_particle.stop()
        self.remove_widget(self.demo_particle)

    def on_touch_down(self, touch):
        super(ParticleBuilder, self).on_touch_down(touch)
        if self.particle_window.collide_point(touch.x, touch.y):
            self.demo_particle.emitter_x = touch.x
            self.demo_particle.emitter_y = touch.y

    def on_touch_move(self, touch):
        super(ParticleBuilder, self).on_touch_move(touch)
        if self.particle_window.collide_point(touch.x, touch.y):
            self.demo_particle.emitter_x = touch.x
            self.demo_particle.emitter_y = touch.y


class ParticleParamsLayout(Widget):
    all_tabs = ListProperty(None)
    all_tabs2 = ListProperty(None)
    all_tabs3 = ListProperty(None)

    def create_tab(self, num_tab):
        if num_tab == 1:
            self.particle_tabs.default_tab = TabbedPanelHeader(text='new tab')
            default = TabbedPanelHeader(text='Hello')
            default.content = self.get_default_tab()
            self.particle_tabs.add_widget(default)
            self.particle_tabs.switch_to(self.particle_tabs.tab_list[0])
        new_num_variants = num_tab
        th1 = TabbedPanelHeader(text = 'Particle' + str(num_tab))
        th2 = TabbedPanelHeader(text = 'Behavior' + str(num_tab))
        th3 = TabbedPanelHeader(text = 'Color' + str(num_tab))
        th1_tab_content = self.get_particle_content()
        th2_tab_content = self.get_behavior_content()
        th3_tab_content = self.get_color_content()
        th1.content = th1_tab_content
        th2.content = th2_tab_content
        th3.content = th3_tab_content
        self.parent.parent.create_particle_system()
        self.all_tabs.append(th1)
        self.all_tabs2.append(th2)
        self.all_tabs3.append(th3)

    def add_tab_to_layout(self, num_tab):
        try:
            self.particle_tabs.remove_widget(self.particle_tabs.tab_list[0])
        except: 
            print 'no tab to remove'

        self.particle_tabs.add_widget(self.all_tabs[num_tab-1])
        self.particle_tabs.add_widget(self.all_tabs2[num_tab-1])
        self.particle_tabs.add_widget(self.all_tabs3[num_tab-1])
        self.parent.parent.add_demo_particle_system(num_tab)
        self.particle_tabs.switch_to(self.particle_tabs.tab_list[2])

    def remove_tab_from_layout(self, num_tab):
        self.particle_tabs.remove_widget(self.all_tabs[num_tab-1])
        self.particle_tabs.remove_widget(self.all_tabs2[num_tab-1])
        self.particle_tabs.remove_widget(self.all_tabs3[num_tab-1])
        default = TabbedPanelHeader(text='Hello')
        default.content = self.get_default_tab()
        self.parent.parent.remove_demo_particle_system()
        self.particle_tabs.add_widget(default)
        self.particle_tabs.switch_to(self.particle_tabs.tab_list[0])

    def get_current_tab(self):
        return self.current_tab

    def get_default_tab(self):
        default_content = Default_Particle_Panel()
        return default_content
    
    def get_particle_content(self):
        pbuilder = self.parent
        return ParticlePanel(pbuilder)

    def get_behavior_content(self):
        pbuilder = self.parent
        return BehaviorPanel(pbuilder)

    def get_color_content(self):
        pbuilder = self.parent
        return ColorPanel(pbuilder)
        
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

class Particle_Color_Sliders(Widget):
    color_r = BoundedNumericProperty(1., min=0, max=1.)
    color_g = BoundedNumericProperty(1., min=0, max=1.)
    color_b = BoundedNumericProperty(1., min=0, max=1.)
    color_a = BoundedNumericProperty(1., min=0, max=1.)

class ParticlePanel(Widget):
    particle_builder = ObjectProperty(None)
    max_num_particles = BoundedNumericProperty(200, min=1, max=500)
    life_span = BoundedNumericProperty(2, min=.01, max=10)
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

    def __init__(self, pbuilder, **kwargs):
        super(ParticlePanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent

    def on_max_num_particles(self, instance, value):
        self.particle_builder.demo_particle.max_num_particles = value

    def on_life_span(self, instance, value):
        self.particle_builder.demo_particle.life_span = value

    def on_life_span_variance(self, instance, value):
        self.particle_builder.demo_particle.life_span_variance = value

    def on_start_size(self, instance, value):
        self.particle_builder.demo_particle.start_size = value

    def on_start_size_variance(self, instance, value):
        self.particle_builder.demo_particle.start_size_variance = value

    def on_end_size(self, instance, value):
        self.particle_builder.demo_particle.end_size = value

    def on_end_size_variance(self, instance, value):
        self.particle_builder.demo_particle.end_size_variance = value

    def on_emit_angle(self, instance, value):
        self.particle_builder.demo_particle.emit_angle = value

    def on_emit_angle_variance(self, instance, value):
        self.particle_builder.demo_particle.emit_angle_variance = value

    def on_start_rotation(self, instance, value):
        self.particle_builder.demo_particle.start_rotation = value

    def on_start_rotation_variance(self, instance, value):
        self.particle_builder.demo_particle.start_rotation_variance = value

    def on_end_rotation(self, instance, value):
        self.particle_builder.demo_particle.end_rotation = value

    def on_end_rotation_variance(self, instance, value):
        self.particle_builder.demo_particle.end_rotation_variance = value


class BehaviorPanel(Widget):
    particle_builder = ObjectProperty(None)
    emitter_type = NumericProperty(0)
    ## Gravity Emitter Params
    emitter_x_variance = BoundedNumericProperty(0, min=0, max=100)
    emitter_y_variance = BoundedNumericProperty(0, min=0, max=100)
    gravity_x = BoundedNumericProperty(0, min=-100, max=100)
    gravity_y = BoundedNumericProperty(0, min=-100, max=100)
    speed = BoundedNumericProperty(0, min=0, max=100)
    speed_variance = BoundedNumericProperty(0, min=0, max=100)
    radial_acceleration = BoundedNumericProperty(100, min=-400, max=400)
    radial_acceleration_variance = BoundedNumericProperty(0, min=0, max=400)
    tangential_acceleration = BoundedNumericProperty(0, min=-500, max=500)
    tangential_acceleration_variance = BoundedNumericProperty(0, min=0, max=500)

    ## Radial Emitter Params
    max_radius = BoundedNumericProperty(100, min=0, max=250)
    max_radius_variance = BoundedNumericProperty(0, min=0, max=250)
    min_radius = BoundedNumericProperty(0, min=0, max=250)
    rotate_per_second = BoundedNumericProperty(0, min=-180, max=180)
    rotate_per_second_variance = BoundedNumericProperty(0, min=0, max=180)

    def __init__(self, pbuilder, **kwargs):
        super(BehaviorPanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent

    def set_emitter_type(self, num_type):
        self.emitter_type = num_type

    def on_emitter_type(self, instance, value):
        self.particle_builder.demo_particle.emitter_type = value

    def on_emitter_x_variance(self, instance, value):
        self.particle_builder.demo_particle.emitter_x_variance = value

    def on_emitter_y_variance(self, instance, value):
        self.particle_builder.demo_particle.emitter_y_variance = value

    def on_gravity_x(self, instance, value):
        self.particle_builder.demo_particle.gravity_x = value

    def on_gravity_y(self, instance, value):
        self.particle_builder.demo_particle.gravity_y = value

    def on_speed(self, instance, value):
        self.particle_builder.demo_particle.speed = value

    def on_speed_variance(self, instance, value):
        self.particle_builder.demo_particle.speed_variance = value

    def on_radial_acceleration(self, instance, value):
        self.particle_builder.demo_particle.radial_acceleration = value

    def on_radial_acceleration_variance(self, instance, value):
        self.particle_builder.demo_particle.tangential_acceleration_variance = value

    def on_tangential_acceleration(self, instance, value):
        self.particle_builder.demo_particle.tangential_acceleration = value

    def on_tangential_acceleration_variance(self, instance, value):
        self.particle_builder.demo_particle.tangential_acceleration_variance = value

    def on_max_radius(self, instance, value):
        self.particle_builder.demo_particle.max_radius = value

    def on_max_radius_variance(self, instance, value):
        self.particle_builder.demo_particle.max_radius_variance = value

    def on_min_radius(self, instance, value):
        self.particle_builder.demo_particle.min_radius = value

    def on_rotate_per_second(self, instance, value):
        self.particle_builder.demo_particle.rotate_per_second = value

    def on_rotate_per_second_variance(self, instance, value):
        self.particle_builder.demo_particle.rotate_per_second_variance = value

class ColorPanel(Widget):
    particle_builder = ObjectProperty(None)
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

    def __init__(self, pbuilder, **kwargs):
        super(ColorPanel, self).__init__(**kwargs)
        self.particle_builder = pbuilder.parent

    def on_start_color_r(self, instance, value):
        self.particle_builder.demo_particle.start_color[0] = self.start_color_r

    def on_start_color_g(self, instance, value):
        self.particle_builder.demo_particle.start_color[1] = self.start_color_g

    def on_start_color_b(self, instance, value):
        self.particle_builder.demo_particle.start_color[2] = self.start_color_b

    def on_start_color_a(self, instance, value):
        self.particle_builder.demo_particle.start_color[3] = self.start_color_a

    def on_start_color_r_variance(self, instance, value):
        self.particle_builder.demo_particle.start_color_variance[0] = self.start_color_r_variance

    def on_start_color_g_variance(self, instance, value):
        self.particle_builder.demo_particle.start_color_variance[1] = self.start_color_g_variance

    def on_start_color_b_variance(self, instance, value):
        self.particle_builder.demo_particle.start_color_variance[2] = self.start_color_b_variance

    def on_start_color_a_variance(self, instance, value):
        self.particle_builder.demo_particle.start_color_variance[3] = self.start_color_a_variance

    def on_end_color_r(self, instance, value):
        self.particle_builder.demo_particle.end_color[0] = self.end_color_r

    def on_end_color_g(self, instance, value):
        self.particle_builder.demo_particle.end_color[1] = self.end_color_g

    def on_end_color_b(self, instance, value):
        self.particle_builder.demo_particle.end_color[2] = self.end_color_b

    def on_end_color_a(self, instance, value):
        self.particle_builder.demo_particle.end_color[3] = self.end_color_a

    def on_end_color_r_variance(self, instance, value):
        self.particle_builder.demo_particle.end_color_variance[0] = self.end_color_r_variance

    def on_end_color_g_variance(self, instance, value):
        self.particle_builder.demo_particle.end_color_variance[1] = self.end_color_g_variance

    def on_end_color_b_variance(self, instance, value):
        self.particle_builder.demo_particle.end_color_variance[2] = self.end_color_b_variance

    def on_end_color_a_variance(self, instance, value):
        self.particle_builder.demo_particle.end_color_variance[3] = self.end_color_a_variance

Factory.register('ParticleBuilder', ParticleBuilder)
Factory.register('ParticleVariationLayout', ParticleVariationLayout)
Factory.register('ParticleParamsLayout', ParticleParamsLayout)
Factory.register('ParticlePanel', ParticlePanel)
Factory.register('BehaviorPanel', BehaviorPanel)
Factory.register('ColorPanel', ColorPanel)
Factory.register('Particle_Property_Slider', Particle_Property_Slider)
Factory.register('Particle_Color_Sliders', Particle_Color_Sliders)

class ParticleBuilderApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    ParticleBuilderApp().run()

