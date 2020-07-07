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
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class MacrobatParameterRackTemplate(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Template for Macrobat racks that control parameters in Live 8 '
    
    def __init__(self, parent, rack, track):
	self._parent = parent
        ControlSurfaceComponent.__init__(self)
	self._register_timer_callback(self.on_timer)
	self._has_timer = True
	self._on_off_param = []
	self._param_macros = {}
	self._update_macro = 0
	self._update_param = 0
	self._param_update_in_progress = True
	self._macro_update_in_progress = True
	self._parent.schedule_message(8, self.allow_macro_updates)
	self._parent.schedule_message(8, self.allow_param_updates)
	self._get_initial_value = False
	self._track = track
	self.setup_device(rack)
	
	
    def disconnect(self):
	self.remove_macro_listeners()
	if self._has_timer:
	    self._unregister_timer_callback(self.on_timer)
	self._has_timer = False
	self._on_off_param = []
	self._param_macros = {}
	self._track = None
	self._parent = None
	
	    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
	
	
    def setup_device(self, rack):
	""" Remove any current listeners and set up listener for on/off (used for resetting assigned params) """  
	self.remove_macro_listeners()
	if not rack.parameters[0].value_has_listener(self.on_off_changed):
	    self._on_off_param = [rack.parameters[0], rack.parameters[0].value]
	    rack.parameters[0].add_value_listener(self.on_off_changed)
	
	
    def macro_changed(self, index):
	""" Called on macro changes to update param values """
	if not self._update_macro and not self._macro_update_in_progress:
	    if self._param_macros.has_key(index) and self._param_macros[index][0] and self._param_macros[index][1]:
		scaled_value = self.scale_param_value_to_macro(self._param_macros[index][1])
		if scaled_value != self._param_macros[index][0].value:
		    self._update_param = index
		    self._param_update_in_progress = True
		    self._parent.schedule_message(8, self.allow_macro_updates)
		    
    
    def param_changed(self, index):
	""" Called on param changes to update macros """
	if not self._update_param and not self._param_update_in_progress:
	    if self._param_macros.has_key(index) and self._param_macros[index][0] and self._param_macros[index][1]:
		scaled_value = self.scale_macro_value_to_param(self._param_macros[index][0], self._param_macros[index][1])
		if scaled_value != self._param_macros[index][1].value:
		    self._update_macro = index
		    self._macro_update_in_progress = True
		    self._parent.schedule_message(8, self.allow_param_updates)
		    		    		    
		    
    def on_off_changed(self):
	""" On/off changed, schedule param reset """
	if self._on_off_param and self._on_off_param[0]: 
	    if self._on_off_param[0].value != self._on_off_param[1] and self._on_off_param[0].value == 1.0:
		self._parent.schedule_message(1, self.do_reset)
	    self._on_off_param[1] = self._on_off_param[0].value
   
	    
    def do_reset(self):
	""" Reset assigned params to default """
	self._update_param = False
	self._update_macro = False
	self._param_update_in_progress = False
	self._macro_update_in_progress = False
	for k, v in self._param_macros.items():
	    if v[1] and not v[1].is_quantized and v[1].name != 'Chain Selector':
		v[1].value = v[1].default_value
		v[0].value = self.scale_param_value_to_macro(v[1])
	
		    
    def on_timer(self):
	""" Handle updating values and getting initial values """
	if not self._get_initial_value:
	    if self._update_macro and not self._update_param:
		if self._param_macros.has_key(self._update_macro):
		    if self._param_macros[self._update_macro][0] and self._param_macros[self._update_macro][1]:
			self._param_macros[self._update_macro][0].value = self.scale_param_value_to_macro(self._param_macros[self._update_macro][1])
		self._update_macro = 0
		self._parent.schedule_message(8, self.allow_param_updates)
	    elif self._update_param and not self._update_macro:
		if self._param_macros.has_key(self._update_param):
		    if self._param_macros[self._update_param][0] and self._param_macros[self._update_param][1]:
			self._param_macros[self._update_param][1].value = self.scale_macro_value_to_param(self._param_macros[self._update_param][0], self._param_macros[self._update_param][1])
		self._update_param = 0
		self._parent.schedule_message(8, self.allow_macro_updates)
	else:
	    for index in range(1,9):
		if self._param_macros.has_key(index):
		    if self._param_macros[index][0] and self._param_macros[index][1]:
			if self._param_macros[index][0].value != self.scale_param_value_to_macro(self._param_macros[index][1]):
			    self._param_macros[index][0].value = self.scale_param_value_to_macro(self._param_macros[index][1])
	    self._get_initial_value = False
			
		
    def scale_macro_value_to_param(self, macro, param):
	return (((param.max - param.min) / 127.0) * macro.value) + param.min
	
    
    def scale_param_value_to_macro(self, param):
	return int(((param.value - param.min) / (param.max - param.min)) * 127.0)
    
    
    def allow_macro_updates(self):
	""" Used to prevent param change getting triggered while param update is in progress (new issue in 8.2.2) """
	if not self._update_param:
	    self._param_update_in_progress = False
	    
	    
    def allow_param_updates(self):
	""" Used to prevent macro change getting triggered while macro update is in progress (new issue in 8.2.2) """
	if not self._update_macro:
	    self._macro_update_in_progress = False
    
    
    def get_drum_rack(self):
	""" For use with DR racks, get drum rack to operate on as well as the params of any simplers/samplers in the rack """
	drum_rack = {}
	drum_rack['devs_by_index'] = {}
	drum_rack['devs_by_name'] = {}
	if self._track and self._track.devices:
	    for d in self._track.devices:
		if d.class_name == 'DrumGroupDevice':
		    drum_rack['rack'] = d
		    rack_devices_by_index = {}
		    rack_devices_by_name = {}
		    for chain_index in range (len(d.chains)):
			for device in d.chains[chain_index].devices:
			    if device.class_name in ('OriginalSimpler', 'MultiSampler'):
				current_params = {}
				for p in device.parameters:
				    current_params[str(p.name).upper()] = p
				rack_devices_by_index[str(chain_index + 1)] = current_params
				rack_devices_by_name[str(device.name)] = current_params
			    break
			drum_rack['devs_by_index'] = rack_devices_by_index
			drum_rack['devs_by_name'] = rack_devices_by_name
		    break
	return drum_rack
					
			
    def remove_macro_listeners(self):
	for index in range(1,9):
	    if self._param_macros.has_key(index):
		m_listener = lambda index = index:self.macro_changed(index)
		p_listener = lambda index = index:self.param_changed(index)
		if self._param_macros[index][0] and self._param_macros[index][0].value_has_listener(m_listener):
		    self._param_macros[index][0].remove_value_listener(m_listener)
		if self._param_macros[index][1] and self._param_macros[index][1].value_has_listener(p_listener):
		    self._param_macros[index][1].remove_value_listener(p_listener)
	self._param_macros = {}
	if self._on_off_param and self._on_off_param[0] and self._on_off_param[0].value_has_listener(self.on_off_changed):
	    self._on_off_param[0].remove_value_listener(self.on_off_changed)
	self._on_off_param = []    

		
# local variables:
# tab-width: 4