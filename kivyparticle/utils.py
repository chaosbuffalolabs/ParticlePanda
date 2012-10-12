# -*- coding: utf-8 -*-

import random

__all__ = ['random_variance', 'random_color_variance']


def random_variance(base, variance):
    return base + variance * (random.random() * 2.0 - 1.0)


def random_color_variance(base, variance):
    return [min(max(0.0, (random_variance(base[i], variance[i]))), 1.0) for i in range(4)]
