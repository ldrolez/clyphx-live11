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
import pickle
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from consts import *
if IS_LIVE_9:
    from functools import partial
    
""" The positions of the main categories in the snap data array. """
MIX_STD_SETTINGS_POS = 0
MIX_EXT_SETTINGS_POS = 1
PLAY_SETTINGS_POS = 2
DEVICE_SETTINGS_POS = 3

""" The positions of standard mix settings within the associated array. """
MIX_VOL_POS = 0
MIX_PAN_POS = 1
MIX_SEND_START_POS = 2

""" The positions of extended mix settings within the associated array. """
MIX_MUTE_POS = 0
MIX_SOLO_POS = 1
MIX_CF_POS = 2

""" The positions of chain mix settings within the associated array. """
CHAIN_VOL_POS = 0
CHAIN_PAN_POS = 1
CHAIN_MUTE_POS = 2
CHAIN_SEND_START_POS = 3

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
	self._register_timer_callback(self._on_timer)
	self._has_timer = True
	self.song().add_current_song_time_listener(self._on_time_changed)
	self.song().add_is_playing_listener(self._on_time_changed)
	
	
    def disconnect(self): 
	if self._has_timer:
	    self._unregister_timer_callback(self._on_timer)
	self._remove_control_rack()
	self._remove_track_listeners()
	self.song().remove_current_song_time_listener(self._on_time_changed)
	self.song().remove_is_playing_listener(self._on_time_changed)
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
	
    
    def store_track_snapshot(self, track_list, xclip, ident, action, args, force=False):
	""" Stores snapshot of track params """
	param_count = 0
	if not type(xclip) is Live.Clip.Clip and not force:
	    return()
	snap_data = {}
	if track_list:
	    for track in track_list:
		track_name = self._parent.get_name(track.name)
		if not track_name.startswith('CLYPHX SNAP') and not snap_data.has_key(track.name):
		    self._current_track_data = [[], [], None, {}]
		    if args == '' or 'MIX' in args:
			param_count += self._store_mix_settings(track, args)
		    if 'PLAY' in args and track in self.song().tracks:
			self._current_track_data[PLAY_SETTINGS_POS] = track.playing_slot_index
			param_count += 1
		    if (args == '' or 'DEV' in args) and track.devices:
			param_count += self._store_device_settings(track, args)
		    snap_data[track.name] = self._current_track_data
	    if snap_data:
		if param_count <= self._parameter_limit:
		    xclip.name = str(ident) + ' || ' + pickle.dumps(snap_data)
		else:
		    current_name = xclip.name
		    xclip.name = 'Too many parameters to store!'
		    if IS_LIVE_9:
			self._parent.schedule_message(8, partial(self._refresh_xclip_name, (xclip, current_name)))
		    else:
			self._parent.schedule_message(8, self._refresh_xclip_name, (xclip, current_name))
			
			
    def _store_mix_settings(self, track, args):
	""" Stores mixer related settings and returns the number of parameters that were stored. """
	param_count = 0
	if not 'MIXS' in args:
	    mix_vals = [track.mixer_device.volume.value, track.mixer_device.panning.value]
	else:
	    mix_vals = [-1, -1]
	if not 'MIX-' in args:
	    mix_vals.extend([s.value for s in track.mixer_device.sends])
	param_count += len(mix_vals)
	self._current_track_data[MIX_STD_SETTINGS_POS] = mix_vals
	if ('MIX+' in args or 'MIX-' in args) and track != self.song().master_track:
	    self._current_track_data[MIX_EXT_SETTINGS_POS] = [int(track.mute), int(track.solo), track.mixer_device.crossfade_assign]
	    param_count += 3
	return param_count
    
    	
    def _store_device_settings(self, track, args):
	""" Stores device related settings and returns the number of parameters that were stored. """
	param_count = 0
	dev_range = self._get_snap_device_range(args, track)
	if dev_range:
	    track_devices = {}
	    for dev_index in range (dev_range[0], dev_range[1]):
		if dev_index < (len(track.devices)):
		    current_device = track.devices[dev_index]
		    if not track_devices.has_key(current_device.name):
			track_devices[current_device.name] = {'params' : [p.value for p in current_device.parameters]}
			param_count += len(current_device.parameters)
			if self._include_nested_devices and self._parent._can_have_nested_devices and current_device.can_have_chains:
			    param_count += self._get_nested_devices(current_device, track_devices[current_device.name], 0)
	    if track_devices:
		self._current_track_data[DEVICE_SETTINGS_POS] = track_devices
	return param_count
		
		
    def _get_nested_devices(self, rack, nested_devs, parameter_count):
	""" Creates recursive dict of nested devices and returns count of parameters """
	if rack.chains:
	    nested_devs['chains'] = {}
	    for chain_index, c in enumerate(rack.chains):
		nested_devs['chains'][chain_index] = {'devices' : {}}
		for device_index, d in enumerate(c.devices):
		    nested_devs['chains'][chain_index]['devices'][device_index] = {'params' : [p.value for p in d.parameters]}
		    parameter_count += len(d.parameters)
		    if not rack.class_name.startswith('Midi'):
			mix_settings = [c.mixer_device.volume.value, c.mixer_device.panning.value, c.mixer_device.chain_activator.value]
			parameter_count += 3
			sends = c.mixer_device.sends
			if sends:
			    for s in sends:
				mix_settings.append(s.value)
			    parameter_count += len(sends)
			nested_devs['chains'][chain_index]['mixer'] = mix_settings
		    if d.can_have_chains and d.chains:
			self._get_nested_devices(d, nested_devs['chains'][chain_index]['devices'][device_index], parameter_count)
	return parameter_count
		
			
    def recall_track_snapshot(self, name, xclip, disable_smooth=False):
	""" Recalls snapshot of track params """
	self._snap_id = xclip.name[xclip.name.index('['):xclip.name.index(']')+1].strip().upper() 
	snap_data = pickle.loads(str(xclip.name)[len(self._snap_id) + 4:])
	self._parameters_to_smooth = {}
	self._rack_parameters_to_smooth = {}
	is_synced = False if disable_smooth else self._init_smoothing(xclip)
	for track, param_data in snap_data.items():
	    if self._current_tracks.has_key(track):
		track = self._current_tracks[track]
		self._recall_mix_settings(track, param_data)
		if param_data[PLAY_SETTINGS_POS] != None and not track.is_foldable and track is not self.song().master_track:
		    if param_data[PLAY_SETTINGS_POS] < 0:
			track.stop_all_clips()
		    else:
			if track.clip_slots[param_data[PLAY_SETTINGS_POS]].has_clip and track.clip_slots[param_data[PLAY_SETTINGS_POS]].clip != xclip:
			    track.clip_slots[param_data[PLAY_SETTINGS_POS]].fire()
		if param_data[DEVICE_SETTINGS_POS]:
		    self._recall_device_settings(track, param_data)
	if self._is_control_track and self._parameters_to_smooth:
	    if not self._control_rack or (self._control_rack and not self._control_rack.parameters[0].value == 1.0):
		self._smoothing_active = not is_synced
		self._synced_smoothing_active = is_synced
	    else:
		self._parent.schedule_message(1, self._refresh_control_rack)
		
		
    def _recall_mix_settings(self, track, param_data):
	""" Recalls mixer related settings. """
	if param_data[MIX_STD_SETTINGS_POS]:
	    pan_value = param_data[MIX_STD_SETTINGS_POS][MIX_PAN_POS]
	    if track.mixer_device.volume.is_enabled and param_data[MIX_STD_SETTINGS_POS][MIX_VOL_POS] != -1:
		self._get_parameter_data_to_smooth(track.mixer_device.volume, param_data[MIX_STD_SETTINGS_POS][MIX_VOL_POS])
	    if track.mixer_device.panning.is_enabled and not isinstance(pan_value, int):
		self._get_parameter_data_to_smooth(track.mixer_device.panning, param_data[MIX_STD_SETTINGS_POS][MIX_PAN_POS])
	    if track is not self.song().master_track:
		for index in range (len(param_data[MIX_STD_SETTINGS_POS])-MIX_SEND_START_POS):
		    if index <= len(track.mixer_device.sends)-1 and track.mixer_device.sends[index].is_enabled:
			self._get_parameter_data_to_smooth(track.mixer_device.sends[index], param_data[MIX_STD_SETTINGS_POS][MIX_SEND_START_POS+index])
	if param_data[1] and track is not self.song().master_track:
	    track.mute = param_data[MIX_EXT_SETTINGS_POS][MIX_MUTE_POS]
	    track.solo = param_data[MIX_EXT_SETTINGS_POS][MIX_SOLO_POS]
	    track.mixer_device.crossfade_assign =  param_data[MIX_EXT_SETTINGS_POS][MIX_CF_POS]
	    
	    
    def _recall_device_settings(self, track, param_data):
	""" Recalls device related settings. """
	for device in track.devices:
	    if param_data[DEVICE_SETTINGS_POS].has_key(device.name):
		self._recall_device_snap(device, param_data[DEVICE_SETTINGS_POS][device.name]['params'])
		if self._include_nested_devices and self._parent._can_have_nested_devices and device.can_have_chains and param_data[DEVICE_SETTINGS_POS][device.name].has_key('chains'):
		    self._recall_nested_device_snap(device, param_data[DEVICE_SETTINGS_POS][device.name]['chains'])
		del param_data[DEVICE_SETTINGS_POS][device.name]
		
		
    def _recall_device_snap(self, device, stored_params):
	""" Recalls the settings of a single device """
	if device and len(device.parameters) == len(stored_params):
	    for index, param in enumerate(device.parameters):
		if param.is_enabled:
		    self._get_parameter_data_to_smooth(param, stored_params[index])

		    
    def _recall_nested_device_snap(self, rack, stored_params):
	""" Recalls the settings and mixer settings of nested devices """
	if rack.chains and stored_params: 
	    num_chains = len(rack.chains)
	    for chain_key in stored_params.keys():
		if chain_key < num_chains:  
		    chain = rack.chains[chain_key]
		    chain_devices = chain.devices
		    num_chain_devices = len(chain_devices)
		    stored_chain = stored_params[chain_key]
		    stored_devices = stored_chain['devices']
		    for device_key in stored_devices.keys():
			if device_key < num_chain_devices:
			    self._recall_device_snap(chain_devices[device_key], stored_devices[device_key]['params'])
			    if chain_devices[device_key].can_have_chains and stored_devices[device_key].has_key('chains'):
				self._recall_nested_device_snap(chain_devices[device_key], stored_devices[device_key]['chains'])
		    if not rack.class_name.startswith('Midi') and stored_chain.has_key('mixer'):
			if chain.mixer_device.volume.is_enabled:
			    self._get_parameter_data_to_smooth(chain.mixer_device.volume, stored_chain['mixer'][CHAIN_VOL_POS])
			if chain.mixer_device.panning.is_enabled:
			    self._get_parameter_data_to_smooth(chain.mixer_device.panning, stored_chain['mixer'][CHAIN_PAN_POS])
			if chain.mixer_device.chain_activator.is_enabled:
			    self._get_parameter_data_to_smooth(chain.mixer_device.chain_activator, stored_chain['mixer'][CHAIN_MUTE_POS])
			sends = chain.mixer_device.sends
			if sends:
			    num_sends = len(sends)
			    for i in range(len(stored_chain['mixer']) - CHAIN_SEND_START_POS):
				if i < num_sends and sends[i].is_enabled:
				    self._get_parameter_data_to_smooth(sends[i], stored_chain['mixer'][CHAIN_SEND_START_POS + i])
				    
			
    def _init_smoothing(self, xclip):
	""" Initializes smoothing and returns whether or not smoothing is synced to tempo or not. """
	self._smoothing_count = 0
	self._smoothing_active = False
	self._rack_smoothing_active = False
	self._synced_smoothing_active = False
	is_synced = False
	track_name = self._parent.get_name(xclip.canonical_parent.canonical_parent.name)
	self._is_control_track = track_name.startswith('CLYPHX SNAP')
	if self._is_control_track:
	    self._setup_control_rack(xclip.canonical_parent.canonical_parent)
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
	return is_synced
    
    
    def _setup_control_rack(self, track):
	""" Sets up rack to use for morphing between current vals and snapped vals """
	self._remove_control_rack()
	for dev in track.devices:
	    dev_name = self._parent.get_name(dev.name)
	    if dev.class_name.endswith('GroupDevice') and dev_name.startswith('CLYPHX SNAP'):
		self._control_rack = dev
		break
    
		
    def _refresh_control_rack(self):
	""" Refreshes rack name and macro value on snap triggered.  If triggered when rack off, clear snap id from rack name """
	if self._control_rack and self._snap_id:
	    if self._control_rack.parameters[0].value == 1.0:
		self._control_rack.name = 'ClyphX Snap ' + str(self._snap_id)
		self._control_rack.parameters[1].value = 0.0
		self._rack_smoothing_active = True
		if not self._control_rack.parameters[1].value_has_listener(self._control_rack_macro_changed):
		    self._control_rack.parameters[1].add_value_listener(self._control_rack_macro_changed)
	    else:
		self._control_rack.name = 'ClyphX Snap'
	    
	
    def _control_rack_macro_changed(self): 
	""" Returns param values to set based on macro value and build dict """
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
	    
		    
    def _on_timer(self):
	""" Smoothes parameter value changes via timer """
	if self._smoothing_active and self._parameters_to_smooth:
	    self._apply_timed_smoothing()
	if self._rack_smoothing_active and self._rack_parameters_to_smooth:
	    for p, v in self._rack_parameters_to_smooth.items():
		p.value = v
		del self._rack_parameters_to_smooth[p] 
	    		    
		
    def _on_time_changed(self):
	""" Smoothes parameter value changes synced to playback """
	if self._synced_smoothing_active and self._parameters_to_smooth and self.song().is_playing:
	    time = int(str(self.song().get_current_beats_song_time()).split('.')[2])
	    if self._last_beat != time:
		self._last_beat = time
		if IS_LIVE_9:
		    self._tasks.add(self._apply_timed_smoothing)
		else:
		    self._parent.schedule_message(1, self._apply_timed_smoothing)
		    
		
    def _apply_timed_smoothing(self, arg=None):
	""" Applies smoothing for either timer or sync """
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
	
	
    def _get_parameter_data_to_smooth(self, parameter, new_value): 
	""" Returns parameter data to smooth and return list of smoothing value, target value and current value """ 
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
    			
		    		
    def _get_snap_device_range(self, args, track):
	""" Returns range of devices to snapshot """
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
	""" Stores dictionary of tracks by name """
	self._current_tracks = {}
	self._remove_track_listeners()
	for track in (tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)):
	    if not track.name_has_listener(self.setup_tracks):
		track.add_name_listener(self.setup_tracks)
	    name = self._parent.get_name(track.name)
	    if not self._current_tracks.has_key(track.name) and not name.startswith('CLYPHX SNAP'):
		self._current_tracks[track.name] = track
		
		
    def _refresh_xclip_name(self, xclip_data):
	""" Refreshes xclip's previous name in cases where a snap is asking to store too many params """
	xclip_data[0].name = xclip_data[1]
		    	    
    
    def _remove_control_rack(self):
	""" Removes control rack listeners """
	if self._control_rack:
	    self._control_rack.name = 'ClyphX Snap'
	    if self._control_rack.parameters[1].value_has_listener(self._control_rack_macro_changed):
		self._control_rack.parameters[1].remove_value_listener(self._control_rack_macro_changed)
	self._control_rack = None
	
	
    def _remove_track_listeners(self): 
	""" Removes track name listeners """
	for track in (tuple(self.song().tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)):
	    if track.name_has_listener(self.setup_tracks):
		track.remove_name_listener(self.setup_tracks)
		       					
    
# local variables:
# tab-width: 4
