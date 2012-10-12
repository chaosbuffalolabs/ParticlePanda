# -*- coding: utf-8 -*-

import kivy
kivy.require('1.4.1')

__title__ = 'kivyparticle'
__version__ = '0.1'
__author__ = 'Alexis Couronne'
__all__ = ['ParticleSystem', 'EMITTER_TYPE_GRAVITY', 'EMITTER_TYPE_RADIAL']

from .engine import ParticleSystem, EMITTER_TYPE_GRAVITY, EMITTER_TYPE_RADIAL
