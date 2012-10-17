import kivy
from kivy.clock import Clock
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.factory import Factory
from kivy.uix.boxlayout import BoxLayout
from kivy.core.image import Image
from kivy.uix.image import Image as ImageWidget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivyparticle.engine import *
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty, BoundedNumericProperty
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelHeader
from kivy.lang import Builder
import os

from time import sleep
from xml.dom.minidom import Document
import xml.dom.minidom

class ParticleBuilder(Widget):
    demo_particles = ListProperty(None)
    demo_particle = ObjectProperty(ParticleSystem)
    active = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(ParticleBuilder, self).__init__(**kwargs)
        
    def create_particle_system(self):
        texture = Image('media/particle.png').texture
        demo_particle = ParticleSystem(None)
        demo_particle.texture = texture
        self.demo_particles.append(demo_particle)

    def add_demo_particle_system(self, num_tab):
        self.demo_particle = self.demo_particles[num_tab-1]
        self.demo_particle.emitter_x = self.particle_window.pos[0] + self.particle_window.width *.5
        self.demo_particle.emitter_y = self.particle_window.pos[1] + self.particle_window.height *.5
        self.add_widget(self.demo_particle)
        self.demo_particle.start()
        self.active = True

    def remove_demo_particle_system(self):
        if not self.active: return
        self.demo_particle.stop()
        self.remove_widget(self.demo_particle)
        self.active = False

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
    current_tab = NumericProperty(0)

    def create_tab(self, num_tab):
        if num_tab == 1:
            self.particle_tabs.default_tab = TabbedPanelHeader(text='new tab')
            default = TabbedPanelHeader(text='Hello')
            default.content = self.get_default_tab()
            self.particle_tabs.add_widget(default)
            self.particle_tabs.switch_to(self.particle_tabs.tab_list[0])
        new_num_variants = num_tab
        th1 = TabbedPanelHeader(text = 'Particle ' + str(num_tab))
        th2 = TabbedPanelHeader(text = 'Behavior ' + str(num_tab))
        th3 = TabbedPanelHeader(text = 'Color ' + str(num_tab))
        th1.content = self.get_particle_content()
        th2.content = self.get_behavior_content()
        th3.content = self.get_color_content()
        self.parent.parent.create_particle_system()
        self.all_tabs.append(th1)
        self.all_tabs2.append(th2)
        self.all_tabs3.append(th3)

    def add_tab_to_layout(self, num_tab):
        try:
            self.particle_tabs.remove_widget(self.particle_tabs.tab_list[0])
            print 'removed hello tab'
        except: 
            print 'no tab to remove'

        self.particle_tabs.add_widget(self.all_tabs[num_tab-1])
        self.particle_tabs.add_widget(self.all_tabs2[num_tab-1])
        self.particle_tabs.add_widget(self.all_tabs3[num_tab-1])
        self.parent.parent.add_demo_particle_system(num_tab)
        self.current_tab = num_tab
        self.particle_tabs.switch_to(self.particle_tabs.tab_list[2])

    def remove_tab_from_layout(self, num_tab):
        self.particle_tabs.remove_widget(self.all_tabs[num_tab-1])
        self.particle_tabs.remove_widget(self.all_tabs2[num_tab-1])
        self.particle_tabs.remove_widget(self.all_tabs3[num_tab-1])
        self.current_tab = 0
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
    
    def add_variant(self):
        if self.num_variants < 10:
            self.num_variants += 1
            num_tab = self.num_variants
            pbuilder = self.parent.parent
            ctx = {'text': 'Variant' + str(num_tab), 'group': 'PVar', 'pbuilder': pbuilder, 'num_tab': num_tab}
            button = Builder.template('VariantButton', **ctx)
            self.variation_layout.add_widget(button)
            pbuilder.params_layout.create_tab(num_tab)

    def reset_variants(self):
        for v in self.variation_layout.children:
            if v.state == 'down': v.state = 'normal'

        self.variation_layout.clear_widgets()
        self.num_variants = 0


    def on_num_variants(self, instance, value):
        print "num variants changed to ", value

class ParticleLoadSaveLayout(Widget):
    new_particle = ObjectProperty(None)

    def __init__(self,**kwargs):
        super(ParticleLoadSaveLayout,self).__init__(**kwargs)


    def save_particle(self):
        name = "C:\Users\Kerby\CBLParticleSystem\SavedParticles"

        new_particle = Document()
        particle_panel_values = new_particle.createElement("ParticleProperties")
        new_particle.appendChild(particle_panel_values)
        # particle_behavior_values = new_particle.createElement("ParticleBehaviorProperties")
        # new_particle.appendChild(particle_behavior_values)
        # particle_color_values = new_particle.createElement("ParticleColorProperties")
        # new_particle.appendChild(particle_color_values)

        thefile = open("name","w")
        new_particle.writexml(thefile)
        thefile.close()
    
    # def write_to_file(doc, name="C:\Users\Kerby\CBLParticleSystem\SavedParticles\particle.xml"):
        # new_particle = Document()
        # new_element = new_particle.createElement('saved_particle')
        # new_particle.appendChild(new_element)
        # thefile = open("name","w")
        # new_particle.writexml(thefile)
        # thefile.close()

        # f = open('file.xml','wb')
        # doc.writexml(f,encoding='utf-8')
        # f.close()

        # print 'save'

    def load_particle(self,name='templates/fire.pex'):
        pbuilder = self.parent.parent
        vl = pbuilder.variation_layout
        pl = pbuilder.params_layout
        vl.reset_variants()

        # removing 'hello' tab
        try:
            pl.particle_tabs.remove_widget(pl.particle_tabs.tab_list[0])
        except: 
            print 'no tab to remove'

        new_particle = ParticleSystem(name)
        pbuilder.demo_particles = [new_particle]

        pl.all_tabs = []
        pl.all_tabs2 = []
        pl.all_tabs3 = []

        vl.add_variant()
        vl.variation_layout.children[0].state = 'down'

        pl.all_tabs[-1].content.get_values_from_particle()
        pl.all_tabs2[-1].content.get_values_from_particle()
        pl.all_tabs3[-1].content.get_values_from_particle()
        print pl.all_tabs2
        


class Default_Particle_Panel(Widget):
    pass

class ImageChooserCell(Widget):
    image_location = StringProperty("None")
    image_chooser = ObjectProperty(None)

    def cell_press(self):
        self.image_chooser.select(self.image_location)


class ImageChooserPopupContent(GridLayout):
    def __init__(self, image_chooser = None, **kwargs):
        super(ImageChooserPopupContent,self).__init__(rows = 8, cols = 8, col_force_default = True, row_force_default = True, row_default_height = 64, col_default_width = 64, **kwargs)
        self.image_chooser = image_chooser
        png_files = self.get_all_images('.', '.png')
        # atlasses = self.get_all_images('.', '.atlas')
        for i in png_files:
            self.add_widget(ImageChooserCell(image_location=i, image_chooser = self.image_chooser))
        

    def get_all_images(self,dir_name,extension):
        outputList = []
        for root, dirs, files in os.walk(dir_name):
            for fl in files:
                if fl.endswith(extension): outputList.append(os.path.join(root,fl))
        return outputList

    # # not yet implemented:
    # def get_image_urls_from_atlas(self,atlas_file):
    #     pass

class ImageChooser(Widget):
    button_text = StringProperty("Choose a texture...")
    image_location = StringProperty('media/particle.png')
    
    def __init__(self,**kwargs):
        image_chooser_popup_content = ImageChooserPopupContent(image_chooser = self)
        self.image_chooser_popup = Popup(title="Images", content=image_chooser_popup_content, size_hint = (None,None), size=(512,512))
        super(ImageChooser,self).__init__(**kwargs)

    def button_callback(self,):
        self.image_chooser_popup.open()

    def select(self,image_location):
        self.image_location = image_location
        self.image_chooser_popup.dismiss()

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
    texture_location = StringProperty("media/particle.png")
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
        print dir(self)
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

    def on_texture_location(self,instance,value):
        self.particle_builder.demo_particle.texture = Image(value).texture

    def get_values_from_particle(self):
        properties = ['max_num_particles', 'life_span', 'life_span_variance', 'start_size', 'start_size_variance', 
                    'end_size', 'end_size_variance', 'emit_angle', 'emit_angle_variance', 'start_rotation', 
                    'start_rotation_variance', 'end_rotation', 'end_rotation_variance']
    
        for p in properties:
            setattr(self,p,getattr(self.particle_builder.demo_particle,p))

class BehaviorPanel(Widget):
    particle_builder = ObjectProperty(None)
    emitter_type = NumericProperty(0)

    ## Gravity Emitter Params
    emitter_x_variance = BoundedNumericProperty(0, min=0, max=200)
    emitter_y_variance = BoundedNumericProperty(0, min=0, max=200)
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

    def get_values_from_particle(self):
        properties = ['emitter_x_variance', 'emitter_y_variance', 'gravity_x', 'gravity_y', 'speed', 'speed_variance',
                     'radial_acceleration', 'radial_acceleration_variance', 'tangential_acceleration', 
                     'tangential_acceleration_variance', 'max_radius', 'max_radius_variance', 'min_radius', 
                     'rotate_per_second', 'rotate_per_second_variance']

        for p in properties:
            setattr(self,p,getattr(self.particle_builder.demo_particle,p))



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

    def get_values_from_particle(self):
        print self.start_color_r, self.start_color_g, self.start_color_b, self.start_color_a
        

        self.start_color_r = self.particle_builder.demo_particle.start_color[0]
        self.start_color_g = self.particle_builder.demo_particle.start_color[1]
        self.start_color_b = self.particle_builder.demo_particle.start_color[2]
        self.start_color_a = self.particle_builder.demo_particle.start_color[3]
        self.start_color_r_variance = self.particle_builder.demo_particle.start_color_variance[0]
        self.start_color_g_variance = self.particle_builder.demo_particle.start_color_variance[1]
        self.start_color_b_variance = self.particle_builder.demo_particle.start_color_variance[2]
        self.start_color_a_variance = self.particle_builder.demo_particle.start_color_variance[3]
        self.end_color_r = self.particle_builder.demo_particle.end_color[0]
        self.end_color_g = self.particle_builder.demo_particle.end_color[1]
        self.end_color_b = self.particle_builder.demo_particle.end_color[2]
        self.end_color_a = self.particle_builder.demo_particle.end_color[3]
        self.end_color_r_variance = self.particle_builder.demo_particle.end_color_variance[0]
        self.end_color_g_variance = self.particle_builder.demo_particle.end_color_variance[1]
        self.end_color_b_variance = self.particle_builder.demo_particle.end_color_variance[2]
        self.end_color_a_variance = self.particle_builder.demo_particle.end_color_variance[3]

        print self.start_color_r, self.start_color_g, self.start_color_b, self.start_color_a

Factory.register('ParticleBuilder', ParticleBuilder)
Factory.register('ParticleVariationLayout', ParticleVariationLayout)
Factory.register('ParticleLoadSaveLayout', ParticleLoadSaveLayout)
Factory.register('ParticleParamsLayout', ParticleParamsLayout)
Factory.register('ParticlePanel', ParticlePanel)
Factory.register('BehaviorPanel', BehaviorPanel)
Factory.register('ColorPanel', ColorPanel)
Factory.register('Particle_Property_Slider', Particle_Property_Slider)
Factory.register('Particle_Color_Sliders', Particle_Color_Sliders)
Factory.register('ImageChooser', ImageChooser)

class ParticleBuilderApp(App):
    def build(self):
        pass

if __name__ == '__main__':
    ParticleBuilderApp().run()

