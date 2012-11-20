# -*- coding: utf-8 -*-

from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Callback, Rotate, PushMatrix, PopMatrix, Translate, Quad
from kivy.graphics.opengl import glBlendFunc, GL_SRC_ALPHA, GL_ONE, GL_ZERO, GL_SRC_COLOR, GL_ONE_MINUS_SRC_COLOR, GL_ONE_MINUS_SRC_ALPHA, GL_DST_ALPHA, GL_ONE_MINUS_DST_ALPHA, GL_DST_COLOR, GL_ONE_MINUS_DST_COLOR
from kivy.core.image import Image
from xml.dom.minidom import parse as parse_xml
from .utils import random_variance, random_color_variance
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, StringProperty, ObjectProperty, BoundedNumericProperty

import sys
import math
import os

__all__ = ['EMITTER_TYPE_GRAVITY', 'EMITTER_TYPE_RADIAL', 'Particle', 'ParticleSystem']


EMITTER_TYPE_GRAVITY = 0
EMITTER_TYPE_RADIAL = 1

BLEND_FUNC = {0: GL_ZERO,
            1: GL_ONE,
            0x300: GL_SRC_COLOR,
            0x301: GL_ONE_MINUS_SRC_COLOR,
            0x302: GL_SRC_ALPHA,
            0x303: GL_ONE_MINUS_SRC_ALPHA,
            0x304: GL_DST_ALPHA,
            0x305: GL_ONE_MINUS_DST_ALPHA,
            0x306: GL_DST_COLOR,
            0x307: GL_ONE_MINUS_DST_COLOR
}


class Particle(object):
    x, y, rotation, current_time = -256, -256, 0, 0
    scale, total_time = 1.0, 0.
    color = [1.0, 1.0, 1.0, 1.0]
    color_delta = [0.0, 0.0, 0.0, 0.0]
    start_x, start_y, velocity_x, velocity_y = 0, 0, 0, 0
    radial_acceleration, tangent_acceleration = 0, 0
    emit_radius, emit_radius_delta = 0, 0
    emit_rotation, emit_rotation_delta = 0, 0
    rotation_delta, scale_delta = 0, 0


class ParticleSystem(Widget):
    max_num_particles = NumericProperty(200)
    life_span = NumericProperty(2)
    texture = ObjectProperty(None)
    texture_path = StringProperty(None)
    life_span_variance = NumericProperty(0)
    start_size = NumericProperty(16)
    start_size_variance = NumericProperty(0)
    end_size = NumericProperty(16)
    end_size_variance = NumericProperty(0)
    emit_angle = NumericProperty(0)
    emit_angle_variance = NumericProperty(0)
    start_rotation = NumericProperty(0)
    start_rotation_variance = NumericProperty(0)
    end_rotation = NumericProperty(0)
    end_rotation_variance = NumericProperty(0)
    emitter_x_variance = NumericProperty(100)
    emitter_y_variance = NumericProperty(100)
    gravity_x = NumericProperty(0)
    gravity_y = NumericProperty(0)
    speed = NumericProperty(0)
    speed_variance = NumericProperty(0)
    radial_acceleration = NumericProperty(100)
    radial_acceleration_variance = NumericProperty(0)
    tangential_acceleration = NumericProperty(0)
    tangential_acceleration_variance = NumericProperty(0)
    max_radius = NumericProperty(100)
    max_radius_variance = NumericProperty(0)
    min_radius = NumericProperty(50)
    rotate_per_second = NumericProperty(0)
    rotate_per_second_variance = NumericProperty(0)
    start_color = ListProperty([1.,1.,1.,1.])
    start_color_variance = ListProperty([1.,1.,1.,1.])
    end_color = ListProperty([1.,1.,1.,1.])
    end_color_variance = ListProperty([1.,1.,1.,1.])
    blend_factor_source = NumericProperty(770)
    blend_factor_dest = NumericProperty(1)
    emitter_type = NumericProperty(0)

    def __init__(self, config, **kwargs):
        super(ParticleSystem, self).__init__(**kwargs)
        self.capacity = 0
        self.particles = list()
        self.particles_dict = dict()
        self.emission_time = 0.0
        self.frame_time = 0.0
        self.num_particles = 0

        if config is not None: self._parse_config(config)
        self.emission_rate = self.max_num_particles / self.life_span
        self.initial_capacity = self.max_num_particles
        self.max_capacity = self.max_num_particles
        self._raise_capacity(self.initial_capacity)

        with self.canvas.before:
            Callback(self._set_blend_func)
        with self.canvas.after:
            Callback(self._reset_blend_func)

        Clock.schedule_interval(self._update, 1.0 / 60.0)

    def start(self, duration=sys.maxint):
        if self.emission_rate != 0:
            self.emission_time = duration

    def stop(self, clear=False):
        self.emission_time = 0.0
        if clear:
            self.num_particles = 0
            self.particles_dict = dict()
            self.canvas.clear()

    def on_max_num_particles(self, instance, value):
        self.max_capacity = value
        if self.capacity < value:
            self._raise_capacity(self.max_capacity - self.capacity)
        elif self.capacity > value:
            self._lower_capacity(self.capacity - self.max_capacity)
        self.emission_rate = self.max_num_particles/self.life_span

    def on_texture(self,instance,value):
        for p in self.particles:
            try:
                self.particles_dict[p]['rect'].texture = self.texture
            except KeyError:
                # if particle isn't initialized yet, you can't change its texture.
                pass

    def on_life_span(self,instance,value):
        self.emission_rate = self.max_num_particles/value

    def _set_blend_func(self, instruction):
        #glBlendFunc(self.blend_factor_source, self.blend_factor_dest)
        #glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE)

    def _reset_blend_func(self, instruction):
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def _parse_config(self, config):
        self._config = parse_xml(config)
        self.texture_path = self._parse_data('texture', 'name')
        self.texture = Image(self.texture_path).texture
        # self.emitter_x = float(self._parse_data('sourcePosition', 'x'))
        # self.emitter_y = float(self._parse_data('sourcePosition', 'y'))
        self.emitter_x_variance = float(self._parse_data('sourcePositionVariance', 'x'))
        self.emitter_y_variance = float(self._parse_data('sourcePositionVariance', 'y'))
        self.gravity_x = float(self._parse_data('gravity', 'x'))
        self.gravity_y = float(self._parse_data('gravity', 'y'))
        self.emitter_type = int(self._parse_data('emitterType'))
        self.max_num_particles = int(self._parse_data('maxParticles'))
        self.life_span = max(0.01, float(self._parse_data('particleLifeSpan')))
        self.life_span_variance = float(self._parse_data('particleLifespanVariance'))
        self.start_size = float(self._parse_data('startParticleSize'))
        self.start_size_variance = float(self._parse_data('startParticleSizeVariance'))
        self.end_size = float(self._parse_data('finishParticleSize'))
        self.end_size_variance = float(self._parse_data('FinishParticleSizeVariance'))
        self.emit_angle = math.radians(float(self._parse_data('angle')))
        self.emit_angle_variance = math.radians(float(self._parse_data('angleVariance')))
        self.start_rotation = math.radians(float(self._parse_data('rotationStart')))
        self.start_rotation_variance = math.radians(float(self._parse_data('rotationStartVariance')))
        self.end_rotation = math.radians(float(self._parse_data('rotationEnd')))
        self.end_rotation_variance = math.radians(float(self._parse_data('rotationEndVariance')))
        self.speed = float(self._parse_data('speed'))
        self.speed_variance = float(self._parse_data('speedVariance'))
        self.radial_acceleration = float(self._parse_data('radialAcceleration'))
        self.radial_acceleration_variance = float(self._parse_data('radialAccelVariance'))
        self.tangential_acceleration = float(self._parse_data('tangentialAcceleration'))
        self.tangential_acceleration_variance = float(self._parse_data('tangentialAccelVariance'))
        self.max_radius = float(self._parse_data('maxRadius'))
        self.max_radius_variance = float(self._parse_data('maxRadiusVariance'))
        self.min_radius = float(self._parse_data('minRadius'))
        self.rotate_per_second = math.radians(float(self._parse_data('rotatePerSecond')))
        self.rotate_per_second_variance = math.radians(float(self._parse_data('rotatePerSecondVariance')))
        self.start_color = self._parse_color('startColor')
        self.start_color_variance = self._parse_color('startColorVariance')
        self.end_color = self._parse_color('finishColor')
        self.end_color_variance = self._parse_color('finishColorVariance')
        self.blend_factor_source = self._parse_blend('blendFuncSource')
        self.blend_factor_dest = self._parse_blend('blendFuncDestination')

    def _parse_data(self, name, attribute='value'):
        return self._config.getElementsByTagName(name)[0].getAttribute(attribute)

    def _parse_color(self, name):
        return [float(self._parse_data(name, 'red')), float(self._parse_data(name, 'green')), float(self._parse_data(name, 'blue')), float(self._parse_data(name, 'alpha'))]

    def _parse_blend(self, name):
        value = int(self._parse_data(name))
        return BLEND_FUNC[value]

    def _update(self, dt):
        self._advance_time(dt)
        self._render()

    def _create_particle(self):
        return Particle()

    def _init_particle(self, particle):
        life_span = random_variance(self.life_span, self.life_span_variance)
        if life_span <= 0.0:
            return

        particle.current_time = 0.0
        particle.total_time = life_span

        particle.x = random_variance(self.emitter_x, self.emitter_x_variance)
        particle.y = random_variance(self.emitter_y, self.emitter_y_variance)
        particle.start_x = self.emitter_x
        particle.start_y = self.emitter_y

        angle = random_variance(self.emit_angle, self.emit_angle_variance)
        speed = random_variance(self.speed, self.speed_variance)
        particle.velocity_x = speed * math.cos(angle)
        particle.velocity_y = speed * math.sin(angle)

        particle.emit_radius = random_variance(self.max_radius, self.max_radius_variance)
        particle.emit_radius_delta = (self.max_radius - self.min_radius) / life_span

        particle.emit_rotation = random_variance(self.emit_angle, self.emit_angle_variance)
        particle.emit_rotation_delta = random_variance(self.rotate_per_second, self.rotate_per_second_variance)

        particle.radial_acceleration = random_variance(self.radial_acceleration, self.radial_acceleration_variance)
        particle.tangent_acceleration = random_variance(self.tangential_acceleration, self.tangential_acceleration_variance)

        start_size = random_variance(self.start_size, self.start_size_variance)
        end_size = random_variance(self.end_size, self.end_size_variance)

        start_size = max(0.1, start_size)
        end_size = max(0.1, end_size)

        particle.scale = start_size / self.texture.width
        particle.scale_delta = ((end_size - start_size) / life_span) / self.texture.width

        # colors
        start_color = random_color_variance(self.start_color, self.start_color_variance)
        end_color = random_color_variance(self.end_color, self.end_color_variance)

        particle.color_delta = [(end_color[i] - start_color[i]) / life_span for i in range(4)]
        particle.color = start_color

        # rotation
        start_rotation = random_variance(self.start_rotation, self.start_rotation_variance)
        end_rotation = random_variance(self.end_rotation, self.end_rotation_variance)
        particle.rotation = start_rotation
        particle.rotation_delta = (end_rotation - start_rotation) / life_span

    def _advance_particle(self, particle, passed_time):
        passed_time = min(passed_time, particle.total_time - particle.current_time)
        particle.current_time += passed_time

        if self.emitter_type == EMITTER_TYPE_RADIAL:
            particle.emit_rotation += particle.emit_rotation_delta * passed_time
            particle.emit_radius -= particle.emit_radius_delta * passed_time
            particle.x = self.emitter_x - math.cos(particle.emit_rotation) * particle.emit_radius
            particle.y = self.emitter_y - math.sin(particle.emit_rotation) * particle.emit_radius

            if particle.emit_radius < self.min_radius:
                particle.current_time = particle.total_time

        else:
            distance_x = particle.x - particle.start_x
            distance_y = particle.y - particle.start_y
            distance_scalar = math.sqrt(distance_x * distance_x + distance_y * distance_y)
            if distance_scalar < 0.01:
                distance_scalar = 0.01

            radial_x = distance_x / distance_scalar
            radial_y = distance_y / distance_scalar
            tangential_x = radial_x
            tangential_y = radial_y

            radial_x *= particle.radial_acceleration
            radial_y *= particle.radial_acceleration

            new_y = tangential_x
            tangential_x = -tangential_y * particle.tangent_acceleration
            tangential_y = new_y * particle.tangent_acceleration

            particle.velocity_x += passed_time * (self.gravity_x + radial_x + tangential_x)
            particle.velocity_y += passed_time * (self.gravity_y + radial_y + tangential_y)

            particle.x += particle.velocity_x * passed_time
            particle.y += particle.velocity_y * passed_time

        particle.scale += particle.scale_delta * passed_time
        particle.rotation += particle.rotation_delta * passed_time

        particle.color = [particle.color[i] + particle.color_delta[i] * passed_time for i in range(4)]

    def _raise_capacity(self, by_amount):
        old_capacity = self.capacity
        new_capacity = min(self.max_capacity, self.capacity + by_amount)
        
        for i in range(int(new_capacity - old_capacity)):
            self.particles.append(self._create_particle())

        self.num_particles = int(new_capacity)
        self.capacity = new_capacity

    def _lower_capacity(self, by_amount):
        old_capacity = self.capacity
        new_capacity = max(0, self.capacity - by_amount)
        
        for i in range(int(old_capacity - new_capacity)):
            try:
                self.canvas.remove(self.particles_dict[self.particles.pop()]['rect'])
            except: 
                pass

        self.num_particles = int(new_capacity)
        self.capacity = new_capacity


    def _advance_time(self, passed_time):
        particle_index = 0

        # advance existing particles
        while particle_index < self.num_particles:
            particle = self.particles[particle_index]
            if particle.current_time < particle.total_time:
                self._advance_particle(particle, passed_time)
                particle_index += 1
            else:
                if particle_index != self.num_particles - 1:
                    next_particle = self.particles[self.num_particles - 1]
                    self.particles[self.num_particles - 1] = particle
                    self.particles[particle_index] = next_particle
                self.num_particles -= 1
                if self.num_particles == 0:
                    print 'COMPLETE'

        # create and advance new particles
        if self.emission_time > 0:
            time_between_particles = 1.0 / self.emission_rate
            self.frame_time += passed_time

            while self.frame_time > 0:
                if self.num_particles < self.max_capacity:
                    if self.num_particles == self.capacity:
                        self._raise_capacity(self.capacity)

                    particle = self.particles[self.num_particles]
                    self.num_particles += 1
                    self._init_particle(particle)
                    self._advance_particle(particle, self.frame_time)

                self.frame_time -= time_between_particles

            if self.emission_time != sys.maxint:
                self.emission_time = max(0.0, self.emission_time - passed_time)

    def _render(self):
        if self.num_particles == 0:
            return
        for i in range(self.num_particles):
            particle = self.particles[i]
            size = (self.texture.size[0] * particle.scale, self.texture.size[1] * particle.scale)
            if particle not in self.particles_dict:
                self.particles_dict[particle] = dict()
                color = particle.color[:]
                with self.canvas:
                    self.particles_dict[particle]['color'] = Color(color[0], color[1], color[2], color[3])
                    PushMatrix()
                    self.particles_dict[particle]['translate'] = Translate()
                    self.particles_dict[particle]['rotate'] = Rotate()
                    self.particles_dict[particle]['rotate'].set(particle.rotation, 0, 0, 1)
                    self.particles_dict[particle]['rect'] = Quad(texture=self.texture, points=(-size[0] * 0.5, -size[1] * 0.5, 
                        size[0] * 0.5,  -size[1] * 0.5, size[0] * 0.5,  size[1] * 0.5, 
                        -size[0] * 0.5,  size[1] * 0.5))    
                    self.particles_dict[particle]['translate'].xy = (particle.x, particle.y)
                    PopMatrix()
                    
            else:
                self.particles_dict[particle]['rotate'].angle = particle.rotation
                self.particles_dict[particle]['translate'].xy = (particle.x, particle.y)
                self.particles_dict[particle]['color'].rgba = particle.color
