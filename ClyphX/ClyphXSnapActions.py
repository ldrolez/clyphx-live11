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
import math
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from consts import *
if IS_LIVE_9:
    from functools import partial

class ClyphXSnapActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Snapshot-related actions '    

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._current_tracks = {}
	self._parameters_to_smooth = {}
	self._rack_parameters_to_smooth = {}
	self._smoothing_active = False
	self._synced_smoothing_active = False
	self._rack_smoothing_active = False
	self._smoothing_speed = 7 
	self._smoothing_count = 0
	self._last_beat = -1
	self._control_rack = None
	self._snap_id = None
	self._is_control_track = False
	self._include_nested_devices = False
	self._parameter_limit = 500	
	self._register_timer_callback(self.on_timer)
	self._has_timer = True
	self.song().add_current_song_time_listener(self.on_time_changed)
	self.song().add_is_playing_listener(self.on_time_changed)
	
	
    def disconnect(self): 
	if self._has_timer:
	    self._unregister_timer_callback(self.on_timer)
	self.remove_control_rack()
	self.remove_track_listeners()
	self.song().remove_current_song_time_listener(self.on_time_changed)
	self.song().remove_is_playing_listener(self.on_time_changed)
	self._current_tracks = {}
	self._parameters_to_smooth = {}
	self._rack_parameters_to_smooth = {}
	self._control_rack = None
	self._snap_id = None
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
	
    
    def store_track_snapshot(self, track_list, xclip, ident, action, args):
	""" Store snapshot of track params """
	param_count = 0
	if not type(xclip) is Live.Clip.Clip:
	    return()
	snap_data = {}
	if track_list:
	    for track in track_list:
		track_name = self._parent.get_name(track.name)
		if not track_name.startswith('CLYPHX SNAP') and not snap_data.has_key(track.name):
		    track_data = [[], [], None, {}]
		    if args == '' or 'MIX' in args: 
			if not 'MIXS' in args:
			    mix_vals = [track.mixer_device.volume.value, track.mixer_device.panning.value]
			else:
			    mix_vals = [-1, -1]
			if not 'MIX-' in args:
			    mix_vals.extend([s.value for s in track.mixer_device.sends])
			param_count += len(mix_vals)
			track_data[0] = mix_vals
			if ('MIX+' in args or 'MIX-' in args) and track != self.song().master_track:
			    track_data[1] = [int(track.mute), int(track.solo), track.mixer_device.crossfade_assign]
			    param_count += 3
		    if 'PLAY' in args and track in self.song().tracks:
			track_data[2] = track.playing_slot_index
			param_count += 1
		    if (args == '' or 'DEV' in args) and track.devices:
			dev_range = self.get_snap_device_range(args, track)
			if dev_range:
			    track_devices = {}
			    for dev_index in range (dev_range[0], dev_range[1]):
				if dev_index < (len(track.devices)):
				    current_device = track.devices[dev_index]
				    if not track_devices.has_key(current_device.name):
					track_devices[current_device.name] = [[p.value for p in current_device.parameters], []]
					param_count += len(current_device.parameters)
					if self._include_nested_devices and self._parent._can_have_nested_devices and current_device.can_have_chains:
					    nested_devices = self.get_nested_devices(current_device, [], 0)
					    if nested_devices:
						track_devices[current_device.name][1] = nested_devices[0]
						param_count += nested_devices[1]
			    if track_devices:
				track_data[3] = track_devices
		    snap_data[track.name] = track_data
	    if snap_data:
		if param_count <= self._parameter_limit:
		    xclip.name = str(ident) + ' || ' + repr(snap_data)
		else:
		    current_name = xclip.name
		    xclip.name = 'Too many parameters to store!'
		    if IS_LIVE_9:
			self._parent.schedule_message(8, partial(self.refresh_xclip_name, (xclip, current_name)))
		    else:
			self._parent.schedule_message(8, self.refresh_xclip_name, (xclip, current_name))
			
		    
    def refresh_xclip_name(self, xclip_data):
	""" Refreshes xclip's previous name in cases where a snap is asking to store too many params """
	xclip_data[0].name = xclip_data[1]
		    
						
    def get_nested_devices(self, rack, nested_list, parameter_count):
	""" Get list of nested devices and count of parameters """
	if rack.chains:
	    for c in rack.chains:
		for d in c.devices:
		    new_device_entry = [[p.value for p in d.parameters], []]
		    parameter_count += len(d.parameters)
		    if not rack.class_name.startswith('Midi') and list(c.devices).index(d) == 0:
			new_device_entry[1] = [c.mixer_device.volume.value, c.mixer_device.panning.value, c.mixer_device.chain_activator.value]
			parameter_count += 3
			sends = c.mixer_device.sends
			if sends:
			    for s in sends:
				new_device_entry[1].append(s.value)
			    parameter_count += len(sends)
		    nested_list.append(new_device_entry)
		    if d.can_have_chains and d.chains:
			self.get_nested_devices(d, nested_list, parameter_count)
	    return [nested_list, parameter_count]
			
			
    def recall_track_snapshot(self, name, xclip):
	""" Recall snapshot of track params """
	self._smoothing_count = 0
	self._snap_id = xclip.name[xclip.name.index('['):xclip.name.index(']')+1].strip().upper() 
	track_name = self._parent.get_name(xclip.canonical_parent.canonical_parent.name)
	snap_data = eval(str(xclip.name)[len(self._snap_id) + 3:])
	self._smoothing_active = False
	self._rack_smoothing_active = False
	self._synced_smoothing_active = False
	self._parameters_to_smooth = {}
	self._rack_parameters_to_smooth = {}
	self._is_control_track = track_name.startswith('CLYPHX SNAP')
	is_synced = False
	if self._is_control_track:
	    self.setup_control_rack(xclip.canonical_parent.canonical_parent)
	    self._smoothing_speed = 8
	    new_speed = 8
	    if 'SP:' in self._snap_id:
		speed = self._snap_id[self._snap_id.index(':')+1:self._snap_id.index(']')].strip()
		is_synced = 'S' in speed		
		try: new_speed = int(speed.replace('S', ''))
		except: new_speed = 8
	    else:
		if '[' and ']' in track_name:
		    speed = track_name[track_name.index('[')+1:track_name.index(']')].strip()
		    is_synced = 'S' in speed
		    try: new_speed = int(speed.replace('S', ''))
		    except: new_speed = 8
	    if is_synced:
		new_speed *= self.song().signature_numerator
	    if new_speed in range(501):
		self._smoothing_speed = new_speed
	for track, param_data in snap_data.items():
	    if self._current_tracks.has_key(track):
		track = self._current_tracks[track]
		if param_data[0]:
		    if track.mixer_device.volume.is_enabled and param_data[0][0] != -1:
			self.get_parameter_data_to_smooth(track.mixer_device.volume, param_data[0][0])
		    if track.mixer_device.panning.is_enabled and param_data[0][1] != -1:
			self.get_parameter_data_to_smooth(track.mixer_device.panning, param_data[0][1])
		    if track is not self.song().master_track:
			for index in range (len(param_data[0])-2):
			    if index <= len(track.mixer_device.sends)-1 and track.mixer_device.sends[index].is_enabled:
				self.get_parameter_data_to_smooth(track.mixer_device.sends[index], param_data[0][2+index])
		if param_data[1] and track is not self.song().master_track:
		    track.mute = param_data[1][0]
		    track.solo = param_data[1][1]
		    track.mixer_device.crossfade_assign =  param_data[1][2]
		if param_data[2] != None and not track.is_foldable and track is not self.song().master_track:
		    if param_data[2] < 0:
			track.stop_all_clips()
		    else:
			if track.clip_slots[param_data[2]].has_clip and track.clip_slots[param_data[2]].clip != xclip:
			    track.clip_slots[param_data[2]].fire()
		if param_data[3]:
		    for device in track.devices:
			if param_data[3].has_key(device.name):
			    self.recall_device_snap(device, param_data[3][device.name][0])
			    if self._include_nested_devices and self._parent._can_have_nested_devices and device.can_have_chains and param_data[3][device.name][1]:
				self.recall_nested_device_snap(device, param_data[3][device.name][1])
			    del param_data[3][device.name]
	if self._is_control_track and self._parameters_to_smooth:
	    if not self._control_rack or (self._control_rack and not self._control_rack.parameters[0].value == 1.0):
		self._smoothing_active = not is_synced
		self._synced_smoothing_active = is_synced
	    else:
		self._parent.schedule_message(1, self.refresh_control_rack)
	    
	    
    def recall_device_snap(self, device, device_data):
	""" Recall device snap """
	if device and len(device.parameters) == len(device_data):
	    for index in range (len(device.parameters)):
		if device.parameters[index].is_enabled:
		    self.get_parameter_data_to_smooth(device.parameters[index], device_data[index])
			
			
    def recall_nested_device_snap(self, rack, device_data):
	""" Recall snaps of nested devices """
	if rack.chains and device_data: 
	    for c in rack.chains:
		combined_data = zip(c.devices, device_data)
		if combined_data:
		    for cd in combined_data:
			device_data.remove(cd[1])
			self.recall_device_snap(cd[0], cd[1][0])
			if not cd[0].class_name.startswith('Midi') and cd[1][1]:
			    if c.mixer_device.volume.is_enabled:
				self.get_parameter_data_to_smooth(c.mixer_device.volume, cd[1][1][0])
			    if c.mixer_device.panning.is_enabled:
				self.get_parameter_data_to_smooth(c.mixer_device.panning, cd[1][1][1])
			    if c.mixer_device.chain_activator.is_enabled:
				self.get_parameter_data_to_smooth(c.mixer_device.chain_activator, cd[1][1][2])
			    sends = c.mixer_device.sends
			    if sends:
				for i in range(len(cd[1][1]) - 3):
				    if i < len(sends) and sends[i].is_enabled:
					self.get_parameter_data_to_smooth(sends[i], cd[1][1][3 + i])
		    if cd[0].can_have_chains:
			self.recall_nested_device_snap(cd[0], device_data)
		    
		    
    def setup_control_rack(self, track):
	""" Setup rack to use for morphing between current vals and snapped vals """
	self.remove_control_rack()
	for dev in track.devices:
	    dev_name = self._parent.get_name(dev.name)
	    if dev.class_name.endswith('GroupDevice') and dev_name.startswith('CLYPHX SNAP'):
		self._control_rack = dev
		break
    
		
    def refresh_control_rack(self):
	""" Refresh rack name and macro value on snap triggered.  If triggered when rack off, clear snap id from rack name """
	if self._control_rack and self._snap_id:
	    if self._control_rack.parameters[0].value == 1.0:
		self._control_rack.name = 'ClyphX Snap ' + str(self._snap_id)
		self._control_rack.parameters[1].value = 0.0
		self._rack_smoothing_active = True
		if not self._control_rack.parameters[1].value_has_listener(self.control_rack_macro_changed):
		    self._control_rack.parameters[1].add_value_listener(self.control_rack_macro_changed)
	    else:
		self._control_rack.name = 'ClyphX Snap'
	    
	
    def control_rack_macro_changed(self): 
	""" Get param values to set based on macro value and build dict """
	if self._rack_smoothing_active and self._parameters_to_smooth and self._control_rack.parameters[0].value == 1.0:
	    self._rack_parameters_to_smooth = {}
	    macro_value = self._control_rack.parameters[1].value
	    new_dict = {}
	    for p, v in self._parameters_to_smooth.items():
		param_value = v[2] + (macro_value * v[0])
		if p.is_quantized:
		    if macro_value < 63 and p.value != v[2]:
			param_value = v[2]
		    elif macro_value > 63 and p.value != v[1]:
			param_value = v[1]
		    else:
			param_value = None
		if param_value != None:
		    new_dict[p] = param_value
	    self._rack_parameters_to_smooth = new_dict
	    
		    
    def on_timer(self):
	""" Smooth parameter value changes via timer """
	if self._smoothing_active and self._parameters_to_smooth:
	    self.apply_timed_smoothing()
	if self._rack_smoothing_active and self._rack_parameters_to_smooth:
	    for p, v in self._rack_parameters_to_smooth.items():
		p.value = v
		del self._rack_parameters_to_smooth[p] 
	    		    
		
    def on_time_changed(self):
	""" Smooth parameter value changes synced to playback """
	if self._synced_smoothing_active and self._parameters_to_smooth and self.song().is_playing:
	    time = int(str(self.song().get_current_beats_song_time()).split('.')[2])
	    if self._last_beat != time:
		self._last_beat = time
		self._tasks.add(self.apply_timed_smoothing)
		
		
    def apply_timed_smoothing(self, arg=None):
	""" Apply smoothing for either timer or sync """
	self._smoothing_count += 1
	for p, v in self._parameters_to_smooth.items():
	    param_value = v[2] + (self._smoothing_count * v[0])
	    if p.is_quantized:
		p.value = v[1]
		del self._parameters_to_smooth[p]
	    elif param_value == v[1] or self._smoothing_count >= self._smoothing_speed:
		del self._parameters_to_smooth[p]
		p.value = v[1]
	    else:
		p.value = param_value
	
	
    def get_parameter_data_to_smooth(self, parameter, new_value): 
	""" Get parameter data to smooth and return list of smoothing value, target value and current value """ 
	factor = self._smoothing_speed
	if self._is_control_track and self._control_rack and self._control_rack.parameters[0].value == 1.0:
	    factor = 127
	if factor and self._is_control_track:
	    difference = new_value - parameter.value
	    if difference and (factor == 127 or (factor != 127 and abs(difference) > 0.01)):
		if parameter.is_quantized:
		    factor = 1
		param_data = [(new_value - parameter.value) / factor, new_value, parameter.value]  
		if difference < 0.0:
		    param_data = [((parameter.value - new_value) / factor) * -1, new_value, parameter.value]  
		self._parameters_to_smooth[parameter] = param_data
	    else:
		parameter.value = new_value
	else:
	    parameter.value = new_value
    			
		    		
    def get_snap_device_range(self, args, track):
	""" Get range of devices to snapshot """
	dev_args = args.replace('MIX', '')
	dev_args = dev_args.replace('PLAY', '')
	dev_args = dev_args.replace('DEV', '')
	dev_args = dev_args.replace('IO', '')
	start = 0
	end = start + 1
	if dev_args:
	    if 'ALL' in dev_args:
		start = 0
		end = len(track.devices)
	    elif '-' in dev_args:
		try:
		    name_split = dev_args.split('-')
		    start = int(name_split[0].strip()) - 1
		    end = int(name_split[1].strip())
		except: pass
	    else:
		try: 
		    start = int(dev_args) - 1
		    end = start + 1
		except: pass
	if start > len(track.devices) or start < 0 or end > len(track.devices) or end < start:
	    return()
	return (start, end)
    
    
    def setup_tracks(self):  
	""" Store dictionary of tracks by name """
	self._current_tracks = {}
	self.remove_track_listeners()
	for track in (tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)):
	    if not track.name_has_listener(self.setup_tracks):
		track.add_name_listener(self.setup_tracks)
	    name = self._parent.get_name(track.name)
	    if not self._current_tracks.has_key(track.name) and not name.startswith('CLYPHX SNAP'):
		self._current_tracks[track.name] = track
	    
    
    def remove_control_rack(self):
	""" Remove control rack listeners """
	if self._control_rack:
	    self._control_rack.name = 'ClyphX Snap'
	    if self._control_rack.parameters[1].value_has_listener(self.control_rack_macro_changed):
		self._control_rack.parameters[1].remove_value_listener(self.control_rack_macro_changed)
	self._control_rack = None
	
	
    def remove_track_listeners(self): 
	""" Remove track name listeners """
	for track in (tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)):
	    if track.name_has_listener(self.setup_tracks):
		track.remove_name_listener(self.setup_tracks)
		       					
    
# local variables:
# tab-width: 4