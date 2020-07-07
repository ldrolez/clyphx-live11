"""
# Copyright (C) 2013-2017 Stray <stray411@hotmail.com>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# For questions regarding this module contact
# Stray <stray411@hotmail.com>
"""

# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from consts import *
if IS_LIVE_9:
    from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class MacrobatSidechainRack(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Macros sidechain to track output '    

    def __init__(self, parent, rack, track):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._last_meter_left_val = -1
	self._last_meter_right_val = -1
	self._last_midi_meter_val = -1
	self._track = track
	self._rack = rack
	self.setup_device()
	
	
    def disconnect(self):
	if self._track:
	    if self._track.has_audio_output and self._track.output_meter_left_has_listener(self.audio_left_changed):
		self._track.remove_output_meter_left_listener(self.audio_left_changed)
	    if self._track.has_audio_output and self._track.output_meter_right_has_listener(self.audio_right_changed):
		self._track.remove_output_meter_right_listener(self.audio_right_changed)
	    if self._track.has_midi_output and self._track.output_meter_level_has_listener(self.midi_changed):
		self._track.remove_output_meter_level_listener(self.midi_changed)
	self._track = None
	self._rack = None
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
	
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass

	
    def setup_device(self):
	""" - Rack name needs to start with 'nK Sidechain'
	    - Macro names needs to start with '[SC]'
	    - Macro names can be changed dynamically with this rack
	    - Dev On/Off turns sidechain on/off 
	    - IMPORTANT NOTE: This will hose undo history since each macro movement is undoable """
	if self._track.has_audio_output:
	    if not self._track.output_meter_left_has_listener(self.audio_left_changed):
		self._track.add_output_meter_left_listener(self.audio_left_changed)
	    if not self._track.output_meter_right_has_listener(self.audio_right_changed):
		self._track.add_output_meter_right_listener(self.audio_right_changed)
	if self._track.has_midi_output and not self._track.output_meter_level_has_listener(self.midi_changed):
	    self._track.add_output_meter_level_listener(self.midi_changed)
			
			
    def audio_left_changed(self):
	""" Audio left changed, update macro (1 tick delay)"""
	val = int(self._track.output_meter_left * 127)
	if val != self._last_meter_left_val:
	    self._last_meter_left_val = val
	    if IS_LIVE_9:
		self._parent.schedule_message(1, partial(self.update_macros, val))
	    else:
		self._parent.schedule_message(1, self.update_macros, val)
	    
	        
    def audio_right_changed(self):
	""" Audio right changed, update macro (1 tick delay) """
	val = int(self._track.output_meter_right * 127)
	if val != self._last_meter_right_val:
	    self._last_meter_right_val = val
	    if IS_LIVE_9:
		self._parent.schedule_message(1, partial(self.update_macros, val))
	    else:
		self._parent.schedule_message(1, self.update_macros, val)
		    
		    
    def midi_changed(self):
	""" Midi output changed, update macro (1 tick delay) """
	val = int(self._track.output_meter_level * 127)
	if val != self._last_midi_meter_val:
	    self._last_midi_meter_val = val
	    if IS_LIVE_9:
		self._parent.schedule_message(1, partial(self.update_macros, val))
	    else:
		self._parent.schedule_message(1, self.update_macros, val)
	    
	    
    def update_macros(self, val):
	""" Update macros based on track output as long as rack is on """
	if self._rack:
	    for p in self._rack.parameters:
		name = self._parent.get_name(p.name)
		if name.startswith('DEVICE'):
		    if p.value == 0.0:
			return()
		if name.startswith('[SC]') and p.is_enabled:
		    if (self._track.has_audio_output and self._track.output_meter_right == 0.0 and self._track.output_meter_left == 0.0) or self._track.output_meter_level == 0.0:
			val = 0.0
		    p.value = val
		    if self._track.has_midi_output:
			self._parent.schedule_message(4, self.midi_changed)
    
# local variables:
# tab-width: 4
		