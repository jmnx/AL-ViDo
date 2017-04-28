#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from alvido import Alvido


a = Alvido("res/")

# dieser Schritt ist nur zum aufbau der DB nötig .. also ggf nur ein mal
a.getAndProcessData()

a.setup()
