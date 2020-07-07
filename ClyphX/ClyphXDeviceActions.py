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
from _Generic.Devices import *
from consts import *
    
class ClyphXDeviceActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Device and Looper actions '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._looper_data = {}
	
	
    def disconnect(self):
	self._looper_data = {}
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass

	
    def set_all_params(self, device, track, xclip, ident, args):
	""" Set the value of all macros in a rack in one go. So don't need to use a whole string of DEV Px actions to do this. 
	Can also capture the values of macros and store them in X-Clip name if no values specified. """
	if device.class_name.endswith('GroupDevice'):
	    args = args.replace('SET', '', 1).strip()
	    if args:
		param_values = args.split(' ')
		if len(param_values) == 8:
		    for index in range(8):
			self._parent.do_parameter_adjustment(device.parameters[index + 1], param_values[index].strip())
	    else:
		if type(xclip) is Live.Clip.Clip:
		    assign_string = xclip.name + ' '
		    for param in device.parameters:
			if 'Macro' in param.original_name:
			    assign_string += str(int(param.value)) + ' '
		    xclip.name = assign_string
	

    def adjust_selected_chain(self, device, track, xclip, ident, args):
	""" Adjust the selected chain in a rack. """
	if IS_LIVE_9 and device.can_have_chains and device.chains:
	    args = args.replace('CSEL', '', 1).strip()
	    if args in ('<', '>'):
		factor = self._parent.get_adjustment_factor(args)
		new_index = list(device.chains).index(device.view.selected_chain) + factor
	    else:
		try: new_index = int(args) - 1
		except: new_index = list(device.chains).index(device.view.selected_chain)
	    if new_index in range(len(device.chains)):
		device.view.selected_chain = device.chains[new_index]
	
		    
    def adjust_best_of_bank_param(self, device, track, xclip, ident, args):
	""" Adjust device best-of-bank parameter """
	param = None
	name_split = args.split()
	if len(name_split) > 1:
	    param = self.get_bob_parameter(device, name_split[0])
	    if param and param.is_enabled:
		self._parent.do_parameter_adjustment(param, name_split[-1])
		    
		    
    def adjust_banked_param(self, device, track, xclip, ident, args):
	""" Adjust device banked parameter """
	param = None
	name_split = args.split()
	if len(name_split) > 2:
	    param = self.get_banked_parameter(device, name_split[0], name_split[1])
	    if param and param.is_enabled:
		self._parent.do_parameter_adjustment(param, name_split[-1])
	    
	    
    def adjust_chain_selector(self, device, track, xclip, ident, args):
	""" Adjust device chain selector parameter """
	param = self.get_chain_selector(device)
	name_split = args.split()
	if param and param.is_enabled and len(name_split) > 1:
	    self._parent.do_parameter_adjustment(param, name_split[-1])
	
	
    def randomize_params(self, device, track, xclip, ident, args):
	""" Randomize device parameters """
	name = self._parent.get_name(device.name)
	if not name.startswith(('NK RND', 'NK RST', 'NK CHAIN MIX', 'NK DR', 'NK LEARN', 'NK RECEIVER', 'NK TRACK', 'NK SIDECHAIN')):
	    for p in device.parameters:
		if p and p.is_enabled and not p.is_quantized and p.name != 'Chain Selector':
		    p.value = (((p.max - p.min) / 127) * Live.Application.get_random_int(0, 128)) + p.min   
		
		
    def reset_params(self, device, track, xclip, ident, args):
	""" Reset device parameters """
	name = self._parent.get_name(device.name)
	if not name.startswith(('NK RND', 'NK RST', 'NK CHAIN MIX', 'NK DR', 'NK LEARN', 'NK RECEIVER', 'NK TRACK', 'NK SIDECHAIN')):
	    for p in device.parameters:
		if p and p.is_enabled and not p.is_quantized and p.name != 'Chain Selector':
		    p.value = p.default_value
		
		
    def select_device(self, device, track, xclip, ident, args):
	""" Select device and bring it and the track it's on into view """
	if self.song().view.selected_track != track:
	    self.song().view.selected_track = track
	self.application().view.show_view('Detail')
	self.application().view.show_view('Detail/DeviceChain')
	self.song().view.select_device(device)
	
	
    def set_device_on_off(self, device, track, xclip, ident, value = None):
	""" Toggles or turns device on/off """
	on_off = self.get_device_on_off(device)
	if on_off and on_off.is_enabled:
	    if value in KEYWORDS:
		on_off.value = KEYWORDS[value]
	    else:
		on_off.value = not(on_off.value)
		
		
    def set_looper_on_off(self, track, xclip, ident, value = None):
	""" Toggles or turns looper on/off """
	self.get_looper(track)
	if self._looper_data and self._looper_data['Looper'] and self._looper_data['Device On'].is_enabled:
	    if value in KEYWORDS:
		self._looper_data['Device On'].value = KEYWORDS[value]
	    else:
		self._looper_data['Device On'].value = not(self._looper_data['Device On'].value) 
    
    
    def set_looper_rev(self, track, xclip, ident, value = None):
	""" Toggles or turns looper reverse on/off """
	self.get_looper(track)
	if self._looper_data and self._looper_data['Looper'] and self._looper_data['Reverse'].is_enabled:
	    if value in KEYWORDS:
		self._looper_data['Reverse'].value = KEYWORDS[value]
	    else:
		self._looper_data['Reverse'].value = not(self._looper_data['Reverse'].value) 
    
    
    def set_looper_state(self, track, xclip, ident, value = None):
	""" Sets looper state """
	self.get_looper(track)
	if self._looper_data and self._looper_data['Looper'] and value in LOOPER_STATES and self._looper_data['State'].is_enabled:
	    self._looper_data['State'].value = LOOPER_STATES[value]
	    
	    
    def dispatch_chain_action(self, device, track, xclip, ident, args):
	""" Handle actions related to device chains """
	if self._parent._can_have_nested_devices and device.can_have_chains and device.chains:
	    arg_list = args.split()
	    try: chain = device.chains[int(arg_list[0].replace('CHAIN', '')) - 1]
	    except: chain = None
	    if chain == None and IS_LIVE_9:
		chain = device.view.selected_chain
	    if chain:
		if len(arg_list) > 1 and arg_list[1] == 'MUTE':
		    if len(arg_list) > 2 and arg_list[2] in KEYWORDS:
			chain.mute = KEYWORDS[arg_list[2]]
		    else:
			chain.mute = not(chain.mute)
		elif len(arg_list) > 1 and arg_list[1] == 'SOLO':
		    if len(arg_list) > 2 and arg_list[2] in KEYWORDS:
			chain.solo = KEYWORDS[arg_list[2]]
		    else:
			chain.solo = not(chain.solo)
		elif len(arg_list) > 2 and arg_list[1] == 'VOL' and not device.class_name.startswith('Midi'):
		    self._parent.do_parameter_adjustment(chain.mixer_device.volume, arg_list[2].strip())
		elif len(arg_list) > 2 and arg_list[1] == 'PAN' and not device.class_name.startswith('Midi'):
		    self._parent.do_parameter_adjustment(chain.mixer_device.panning, arg_list[2].strip())
    
    
    def get_device_on_off(self, device):
	""" Get device on/off param """
	result = None
	for parameter in device.parameters:
	    if str(parameter.name).startswith('Device On'):
		result = parameter
		break
	return result
    
    
    def get_chain_selector(self, device):
	""" Get rack chain selector param """
	result = None
	if device.class_name.endswith('GroupDevice'):
	    for parameter in device.parameters:
		if str(parameter.original_name) == 'Chain Selector':
		    result = parameter
		    break
	return result
    
    
    def get_bob_parameter(self, device, param_string):
	""" Get best-of-bank parameter 1-8 for Live's devices 
	The param string should be composed of 'P' followed by the param index (like P5) """
	result = None
	if (device.class_name in DEVICE_BOB_DICT.keys()):
	    param_bank = DEVICE_BOB_DICT[device.class_name][0]
	    try:
		param_num = int(param_string[1])-1
		if param_num in range (8):
		    parameter = get_parameter_by_name(device, param_bank[param_num]) 
		    if parameter:
			result = parameter
	    except: pass
	return result
    
    
    def get_banked_parameter(self, device, bank_string, param_string):
	""" Get bank 1-8/parameter 1-8 for Live's devices 
	The bank string should be composed of 'B' followed by the bank index (like B2)
	The param string should be composed of 'P' followed by the param index (like P5)"""
	result = None
	if device.class_name in DEVICE_DICT.keys():
	    device_bank = DEVICE_DICT[device.class_name]
	    try: 
		bank_num = int(bank_string[1])-1		    
		param_num = int(param_string[1])-1
		if param_num in range (8) and bank_num in range (8) and bank_num <= number_of_parameter_banks(device):
		    param_bank = device_bank[bank_num]
		    parameter = get_parameter_by_name(device, param_bank[param_num]) 
		    if parameter:
			result = parameter
	    except: pass
	return result
    
    
    def get_looper(self, track):
	""" Get first looper device on track and its params """
	self._looper_data = {}
	for d in track.devices:
	    if d.class_name == 'Looper':
		self._looper_data['Looper'] = d
		for p in d.parameters: 
		    if p.name in ('Device On', 'Reverse', 'State'):
			self._looper_data[p.name] = p
		break
	    elif not self._looper_data and self._parent._can_have_nested_devices and d.can_have_chains and d.chains:
		for c in d.chains:
		    self.get_looper(c)
		
    
# local variables:
# tab-width: 4