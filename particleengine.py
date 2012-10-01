import kivy
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.app import App
from kivy.graphics import Color, Rectangle, Callback
from kivy.graphics.instructions import InstructionGroup
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.vector import Vector
from kivy.atlas import Atlas
from random import random, randint, uniform
from collections import deque
from functools import partial
from cbl_gui_elements import CBL_DebugPanel
import re

def interpret_str(valuestr):
    if valuestr.startswith("'"):
        return valuestr.strip("'")
    elif valuestr.startswith('"'):
        return valuestr.strip('"')
    else:
        try:
            return float(valuestr)
        except:
            return valuestr

class Particle(InstructionGroup):
    refresh_time = .08
    frame = 0

    def __init__(self, initial_params, param_changes, parent = None, dormant = False, **kwargs):
        # these parameters are necessary for Rectangle
        super(Particle,self).__init__()
        self.rect = Rectangle(pos=(initial_params['x'],initial_params['y']),size=(initial_params['width'],initial_params['height']),texture=initial_params['texture'])
        self.add(self.rect)

        self.color_code = (1., 1., 1., 1.)
        self.color = Color(*self.color_code)
        self.insert(0, self.color)

        self.initial_params = initial_params
        self.param_changes = param_changes
        self.parent = parent
        self.dormant = dormant

        if not dormant:
            self.activate()


    def activate(self):
        self.rect.pos = (self.initial_params['x'],self.initial_params['y'])
        self.rect.size  = (self.initial_params['width'],self.initial_params['height'])
        self.rect.texture = self.initial_params['texture']

        self.change_color((self.initial_params['color_r']/255.,self.initial_params['color_g']/255.,self.initial_params['color_b']/255.,self.initial_params['color_a']/255.))

        self.dormant = False
        self.dx = self.refresh_time * self.initial_params['velocity_x']
        self.dy = self.refresh_time * self.initial_params['velocity_y']

        Clock.schedule_once(self.kill,self.initial_params['lifetime'])

        if 'width' in self.param_changes:
            self.width_gen = (x for x in self.param_changes['width'])
            self.update_width(None)
        if 'height' in self.param_changes:
            self.height_gen = (x for x in self.param_changes['height'])
            self.update_height(None)
        if 'texture' in self.param_changes:
            self.texture_gen = (x for x in self.param_changes['texture'])
            self.update_texture(None)
        if 'color_a' in self.param_changes:
            self.color_a_gen = (x for x in self.param_changes['color_a'])
            self.update_color_a(None)
        
        self.update_pos(None)


    def update_pos(self,dt):
        self.rect.pos = (self.rect.pos[0] + self.dx, self.rect.pos[1] + self.dy)
        Clock.schedule_once(self.update_pos,self.refresh_time)

    def update_width(self,dt):
        try:
            val, time = self.width_gen.next()
        except StopIteration:
            return False
        self.rect.size = (self.rect.size[0]+val, self.rect.size[1])
        Clock.schedule_once(self.update_width,time)

    def update_height(self,dt):
        try:
            val, time = self.height_gen.next()
        except StopIteration:
            return False
        self.rect.size = (self.rect.size[0], self.rect.size[1]+val)
        Clock.schedule_once(self.update_height,time)

    def update_texture(self,dt):
        try:
            val, time = self.texture_gen.next()
        except StopIteration:
            return False
        self.rect.texture = val
        Clock.schedule_once(self.update_texture,time)

    def update_color_a(self,dt):

        try:
            val, time = self.color_a_gen.next()
        except StopIteration:
            return False

        a = self.color_code[3]+(val/255.)
        if a < 0: a = 0
        self.change_color((self.color_code[0], self.color_code[1], self.color_code[2], a))
        Clock.schedule_once(self.update_color_a,time)

    def change_color(self,color_code):
        # is there not a faster way to do this that works?
        self.color_code = color_code
        index = self.indexof(self.color)
        self.remove(self.color)
        self.color = Color(*self.color_code)
        self.insert(index, self.color)

    def kill(self,dt):
        self.parent.reap_particle(self)

class ParticleEffect(Widget):

    def __init__(self, initial_params, param_changes, scatterdict, num_particles = 30, **kwargs):
        super(ParticleEffect,self).__init__(**kwargs)

        self.initial_params = initial_params
        self.param_changes = param_changes
        self.scatterdict = scatterdict
        self.num_particles = num_particles

    def start(self):

        self.slate = InstructionGroup()
        self.canvas.add(self.slate)

        self.emit_rate = self.initial_params['lifetime']/float(self.num_particles)
        if self.emit_rate < 0.02: self.emit_rate = 0.02

        self.stop_flag = False
        self.emit_particle(None)


    def stop(self):
        self.stop_flag = True

    def emit_particle(self, dt):
        if self.stop_flag: return False
        self.slate.add(Particle(self.randomize_params(),self.param_changes,parent=self))
        Clock.schedule_once(self.emit_particle,self.emit_rate)

    def reap_particle(self,particle):
        self.slate.remove(particle)

    def randomize_params(self):
        params = self.initial_params.copy()
        params['x'] = self.x
        params['y'] = self.y
        for key in params.keys():
            try:
                if key in self.scatterdict:
                    params[key] = params[key] * uniform(1-self.scatterdict[key],1+self.scatterdict[key]) if self.scatterdict[key] < 1 else params[key] + randint(int(-self.scatterdict[key]),int(self.scatterdict[key]))
                else:
                    params[key] *= uniform(0.9,1.1)
            except:
                pass

        return params

class CBLParticleEmitter(Widget):
    

    def __init__(self, cblp_filename, num_particles=30,**kwargs):
        self.particle_effects = []
        super(CBLParticleEmitter,self).__init__(**kwargs)
        self.num_particles = num_particles
        self.particle_effects = self.parse_cblp(cblp_filename)



    def start(self,*largs):
        for p in self.particle_effects:
            p.num_particles = int(self.num_particles*p.initial_params['frequency'])
            p.pos = self.pos
            self.add_widget(p)
            p.start()

    def on_pos(self,instance,value):
        for p in self.particle_effects:
            p.pos = value

    def stop(self,*largs):
        for p in self.particle_effects:
            p.stop()

    def parse_cblp(self,cblp_filename):
        """Parses the text file at cblp_filename and returns a list of ParticleEffect objects. 
        Needs to be rewritten using proper recursive parsing techniques for extensibility, but functions for now."""
        
        # read file into a list for easier processing. list format will be (tablevel, field, value)
        tab_re = re.compile(r'(\ *)[^\ ]*')
        arg_re = re.compile(r'\ *([-_a-zA-Z0-9]+):\ *(.*)')
        cblp_lines = []
        with open(cblp_filename,'r') as inf:
            for line in inf:
                if arg_re.match(line) is None: continue

                line_tablevel = len(tab_re.match(line).group(1))
                line_field = arg_re.match(line).group(1)
                line_value = interpret_str(arg_re.match(line).group(2))
                cblp_lines.append((line_tablevel,line_field,line_value))


        particle_effects = []
        param_args = {}
        prev_tablevel = 0

        for line in cblp_lines:

            if prev_tablevel == 12 and line[0] < 12:
                self.set_param(particle_effects[-1],active_param, param_field, args = param_args)
                param_args = {}
            # if this is unindented, it's a new variation, so create a new ParticleEffect
            if line[0] == 0:
                if 'variation' not in line: continue
                particle_effects.append(ParticleEffect({},{},{},0))
            # if it's first level, and there is a value after the colon, it's an initial value, so set it.
            elif line[0] == 4 and line[2] != '':
                particle_effects[-1].initial_params[line[1]]=line[2]
            elif line[0] == 4 and line[2] == '':
                active_param = line[1]
            elif line[0] == 8 and line[2] != '':
                self.set_param(particle_effects[-1],active_param, line[1], value = line[2])
            elif line[0] == 8 and line[2] == '':
                param_field = line[1]
            elif line[0] == 12 and line[2] != '':
                param_args[line[1]] = line[2]
            else:
                # needs to change to raise new ParseError
                assert True == False

            prev_tablevel = line[0]
        
        # get texture_list for all particle effects
        for p in particle_effects:
            texture_list = self.get_texture_list(p.initial_params['image_basename'],p.initial_params['atlas'])
            p.initial_params['texture'] = texture_list[0]
            if 'frame_rate' in p.initial_params:
                p.param_changes['texture'] = zip(texture_list[1:], [p.initial_params['frame_rate']]*len(texture_list[1:]))
        return particle_effects

    def set_param(self,particle_effect, param, field, args=None, value=None):
        if value is not None:
            if field in ['average','initial', 'init']:
                particle_effect.initial_params[param] = value
            elif field == 'scatter':
                particle_effect.scatterdict[param] = value
        elif args is not None: 
            if field == 'interval_change':
                particle_effect.param_changes[param] = [(args['amount'],args['rate'])] * int(args['max_iter'])

    def get_texture_list(self, image_basename, image_location):
        basename = image_basename
        atlas = Atlas(image_location)
        all_keys = atlas.textures.keys()
        wanted_keys = filter(lambda x: x.startswith(basename),all_keys)

        if len(wanted_keys) > 1:
            pattern = re.compile(r'[0-9]+$')
            wanted_keys.sort(key=lambda x: int(pattern.search(x).group()))

        return [atlas[key] for key in wanted_keys]



class ParticleEngineApp(App):
    def build(self):
        # 'atlas://VFX/smoke_particles/VFX_SmokeParticle'
        fl = FloatLayout(pos=(0,0),size=Window.size)
        db_panel = CBL_DebugPanel(pos=(0,0),size=(100,50),size_hint = (None,None))
        fl.add_widget(db_panel)

        p = CBLParticleEmitter('smoke.cblp', num_particles = 50, pos = (200,50), size_hint = (None,None), size = (128,128))
        # this is just to show how you start/stop it
        Clock.schedule_once(p.start)
        Clock.schedule_once(p.stop, 8.)
        fl.add_widget(p)

        q = CBLParticleEmitter('snow.cblp', num_particles = 80, pos = (400,600), size_hint = (None,None), size=(1,1))
        Clock.schedule_once(q.start)
        fl.add_widget(q)        

        return fl



if __name__ == '__main__':
    ParticleEngineApp().run()
