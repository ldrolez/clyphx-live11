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
from consts import *
if IS_LIVE_9:
    from functools import partial
    
class ClyphXGlobalActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Global actions '    
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._last_gqntz = 4
	self._last_rqntz = 5
	self._repeat_enabled = False
	self._tempo_ramp_active = False
	self._tempo_ramp_settings = []
	self._last_beat = -1
	self.song().add_current_song_time_listener(self.on_time_changed)
	self.song().add_is_playing_listener(self.on_time_changed)
	if self.song().clip_trigger_quantization != 0:
	    self._last_gqntz = int(self.song().clip_trigger_quantization)
	if self.song().midi_recording_quantization != 0:
	    self._last_rqntz = int(self.song().midi_recording_quantization)
	self._last_scene_index = list(self.song().scenes).index(self.song().view.selected_scene)
	self._scenes_to_monitor = []
	self.setup_scene_listeners()
	
	
    def disconnect(self):
	self.remove_scene_listeners()
	self.song().remove_current_song_time_listener(self.on_time_changed)
	self.song().remove_is_playing_listener(self.on_time_changed)
	self._tempo_ramp_settings = []
	self._scenes_to_monitor = None
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
    
    
    def on_scene_triggered(self, index):
	self._last_scene_index = index
	
	
    def on_scene_list_changed(self):
	self.setup_scene_listeners()
	

    def make_instant_mapping_docs(self, *a):
        from InstantMappingMakeDoc import InstantMappingMakeDoc
        InstantMappingMakeDoc()

    def send_midi_message(self, track, xclip, ident, args):
	""" Send formatted note/cc/pc message or raw midi message. """
	status_values = {'NOTE': 144, 'CC': 176, 'PC': 192}
	message_to_send = []
	if args:
	    byte_array = args.split()
	    if len(byte_array) >= 2:
		if len(byte_array) >= 3 and byte_array[0] in status_values:
		    data_bytes = self.convert_strings_to_ints(byte_array[1:])
		    if data_bytes and data_bytes[0] in range(1, 17):
			message_to_send = [status_values[byte_array[0]] + data_bytes[0] - 1]
			for byte in data_bytes[1:]:
			    if byte in range(128):
				message_to_send.append(byte)
			if (byte_array[0] != 'PC' and len(message_to_send) != 3) or (byte_array[0] == 'PC' and len(message_to_send) != 2):
			    return
		else:
		    message_to_send = self.convert_strings_to_ints(byte_array)
		if message_to_send:
		    try: 
			self._parent._send_midi(tuple(message_to_send))
			if byte_array[0] == 'NOTE': #---send matching note off for note messages
			    message_to_send[-1] = 0
			    if IS_LIVE_9:
				self._parent.schedule_message(1, partial(self._parent._send_midi, tuple(message_to_send)))
			    else:
				self._parent.schedule_message(1, self._parent._send_midi, tuple(message_to_send))
		    except: pass
		
		    
    def convert_strings_to_ints(self, strings):
	""" Convert list of strings of ints into list of ints. """
	result = []
	try:
	    for string in strings:
		result.append(int(string))
	except: result = []
	return result
	
	
    def do_variable_assignment(self, track, xclip, ident, args):
	""" Creates numbered variables for the name given in args from the offset given in args and in the quantity given in args """
	args = args.strip()
	arg_array = args.split()
	if len(arg_array) == 3:
	    try:
		start = int(arg_array[1])
		length = int(arg_array[2])
		for index in range(length):
		    self._parent._user_variables[arg_array[0] + str(index + 1)] = str(index + start)
	    except: pass
	    
	    
    def create_audio_track(self, track, xclip, ident, value = None):
	""" Creates audio track at end of track list or at the specified index. """
	if IS_LIVE_9:
	    value = value.strip()
	    if value:
		try:
		    index = int(value) - 1
		    if index in range(len(self.song().tracks)):
			self.song().create_audio_track(index)
		except: pass
	    else:
		self.song().create_audio_track(-1)	
	
	    
    def create_midi_track(self, track, xclip, ident, value = None):
	""" Creates MIDI track at end of track list or at the specified index. """
	if IS_LIVE_9:
	    value = value.strip()
	    if value:
		try:
		    index = int(value) - 1
		    if index in range(len(self.song().tracks)):
			self.song().create_midi_track(index)
		except: pass
	    else:
		self.song().create_midi_track(-1)
	    
	    
    def create_return_track(self, track, xclip, ident, value = None):
	""" Creates return track at end of return list. """
	if IS_LIVE_9:
	    self.song().create_return_track()


    def insert_and_configure_audio_track(self, track, xclip, ident, value = None):
        """ Inserts an audio track next to the selected track routed from the
        selected track and armed. """
        self._insert_and_configure_track()
	    

    def insert_and_configure_midi_track(self, track, xclip, ident, value = None):
        """ Inserts a midi track next to the selected track routed from the
        selected track and armed. """
        self._insert_and_configure_track(True)


    def _insert_and_configure_track(self, is_midi=False):
        """ Handles inserting tracks and configuring them. This method will only
        work if the selected track has the appropriate output/input for the insertion. """
        if IS_LIVE_9:
            sel_track = self.song().view.selected_track
            if is_midi and not sel_track.has_midi_input:
                return
            if not is_midi and not sel_track.has_audio_output:
                return
            try:
                ins_index = list(self.song().tracks).index(sel_track) + 1
                create_method = getattr(self.song(), 'create_midi_track' if is_midi
                                        else 'create_audio_track')
                create_method(ins_index)
                new_track = self.song().tracks[ins_index]
                new_track.name = 'From %s' % sel_track.name
                new_track.current_input_routing = sel_track.name   
                new_track.arm = True
            except: pass
            
    
    def create_scene(self, track, xclip, ident, value = None):
	""" Creates scene at end of scene list or at the specified index. """
	if IS_LIVE_9:
	    current_name = None
	    if type(xclip) is Live.Clip.Clip:
		current_name = xclip.name
		xclip.name = ''
	    value = value.strip()
	    if value:
		try:
		    index = int(value) - 1
		    if index in range(len(self.song().scenes)):
			self.song().create_scene(index)
		except: pass
	    else:
		self.song().create_scene(-1)
	    if current_name:
		self._parent.schedule_message(4, partial(self.refresh_xclip_name, (xclip, current_name)))
	    	    
	    
    def duplicate_scene(self, track, xclip, ident, args):
	""" Duplicates the given scene. """
	if IS_LIVE_9:
	    current_name = None
	    if type(xclip) is Live.Clip.Clip and args:
		current_name = xclip.name
		xclip.name = ''
	    self.song().duplicate_scene(self.get_scene_to_operate_on(xclip, args.strip()))
	    if current_name:
		self._parent.schedule_message(4, partial(self.refresh_xclip_name, (xclip, current_name)))
		
		
    def refresh_xclip_name(self, clip_info):
	""" This is used for both dupe and create scene to prevent the action from getting triggered over and over again. """
	if clip_info[0]:
	    clip_info[0].name = clip_info[1]
	    
	    
    def delete_scene(self, track, xclip, ident, args):
	""" Deletes the given scene as long as it's not the last scene in the set. """
	if IS_LIVE_9 and len(self.song().scenes) > 1:
	    self.song().delete_scene(self.get_scene_to_operate_on(xclip, args.strip()))
	    
	
    def swap_device_preset(self, track, xclip, ident, args):
	""" Activates swapping for the selected device or swaps out the preset for the given device with the given preset or navigates forwards and back through presets. """
	if IS_LIVE_9:
	    device = track.view.selected_device
	    if device:
		if not args:
		    self.application().view.toggle_browse()
		else:
		    if self.application().view.browse_mode:
			self.application().view.toggle_browse()
		    tag_target = None
		    dev_name = device.class_display_name
		    args = args.strip()
		    if IS_LIVE_9_5:
			if device.type == Live.Device.DeviceType.audio_effect:
			    tag_target = self.application().browser.audio_effects
			elif device.type == Live.Device.DeviceType.midi_effect:
			    tag_target = self.application().browser.midi_effects
			elif device.type == Live.Device.DeviceType.instrument:
			    tag_target = self.application().browser.instruments
			if tag_target:
			    for dev in tag_target.children:
				if dev.name == dev_name:
				    self._handle_swapping(device, dev, args)
				    break
		    else:
			if device.type == Live.Device.DeviceType.audio_effect:
			    tag_target = 'Audio Effects'
			elif device.type == Live.Device.DeviceType.midi_effect:
			    tag_target = 'MIDI Effects'
			elif device.type == Live.Device.DeviceType.instrument:
			    tag_target = 'Instruments'
			if tag_target:
			    for main_tag in self.application().browser.tags:
				if main_tag.name == tag_target:
				    for dev in main_tag.children:
					if dev.name == dev_name:
					    self._handle_swapping(device, dev, args)
					    break
				    break

				
    def _handle_swapping(self, device, browser_item, args):
	dev_items = self._create_device_items(browser_item, [])
	if args in ('<', '>'):
	    factor = self._parent.get_adjustment_factor(args)
	    index = self._get_current_preset_index(device, dev_items)
	    new_index = index + factor
	    if new_index > len(dev_items) - 1:
		new_index = 0
	    elif new_index < 0:
		new_index = -1
	    self._load_preset(dev_items[new_index])
	else:
	    if device.can_have_chains:
		args = args + '.ADG'
	    else:
		args = args + '.ADV'
	    for item in dev_items:
		if item.name.upper() == args:
		    self._load_preset(item)
		    break
			
			
    def _get_current_preset_index(self, device, presets):
	""" Returns the index of the current preset (based on the device's name) in the presets list. Returns -1 if not found. """
	index = -1
	current_preset_name = device.name
	if device.can_have_chains:
	    current_preset_name = current_preset_name + '.adg'
	else:
	    current_preset_name = current_preset_name + '.adv'
	for item_index in range(len(presets)):
	    if presets[item_index].name == current_preset_name:
		index = item_index
		break
	return index
    
			
    def _load_preset(self, preset):
	""" Loads the given preset. """
	self.application().view.toggle_browse()
	self.application().browser.load_item(preset)
	self.application().view.toggle_browse()
		
	    
    def _create_device_items(self, device, item_array):
	""" Returns the array of loadable items for the given device and handles digging into sub-folders too. """
	for item in device.children:
	    if item.is_folder:
		self._create_device_items(item, item_array)
	    elif item.is_loadable:
		item_array.append(item)
	return item_array
	
	
    def load_device(self, track, xclip, ident, args):
	""" Loads one of Live's built-in devices onto the selected Track. """
	# using a similar method for loading plugins doesn't seem to work!
	if IS_LIVE_9:
	    args = args.strip()
	    tag_target = None
	    name = None
	    if IS_LIVE_9_5:
		if args in AUDIO_DEVS:
		    tag_target = self.application().browser.audio_effects
		    name = AUDIO_DEVS[args]
		elif args in MIDI_DEVS:
		    tag_target = self.application().browser.midi_effects
		    name = MIDI_DEVS[args]
		elif args in INS_DEVS:
		    tag_target = self.application().browser.instruments
		    name = INS_DEVS[args]
		if tag_target:
		    for dev in tag_target.children:
			if dev.name == name:
			    self.application().browser.load_item(dev)
			    break
	    else:
		if args in AUDIO_DEVS:
		    tag_target = 'Audio Effects'
		    name = AUDIO_DEVS[args]
		elif args in MIDI_DEVS:
		    tag_target = 'MIDI Effects'
		    name = MIDI_DEVS[args]
		elif args in INS_DEVS:
		    tag_target = 'Instruments'
		    name = INS_DEVS[args]
		if tag_target:
		    for main_tag in self.application().browser.tags:
			if main_tag.name == tag_target:
			    for dev in main_tag.children:
				if dev.name == name:
				    self.application().browser.load_item(dev)
				    break
			    break
	    

    def load_m4l(self, track, xclip, ident, args):
	""" Loads M4L device onto the selected Track. The .amxd should be omitted by the user. """
	if IS_LIVE_9:
	    args = args.strip() + '.AMXD'	    
	    found_dev = False
	    if IS_LIVE_9_5:
		for m in self.application().browser.max_for_live.children:
		    for device in m.children:
			if not found_dev:
			    if device.is_folder:
				for dev in device.children:
				    if dev.name.upper() == args:
					found_dev = True
					self.application().browser.load_item(dev)
					break
			    elif device.name.upper() == args:
				found_dev = True
				self.application().browser.load_item(device)
				break
			else:
			    break				
	    else:
		for main_tag in self.application().browser.tags:
		    if main_tag.name == 'Max for Live':
			for folder in main_tag.children:
			    if not found_dev:
				if folder.is_folder:
				    for dev in folder.children:
					if dev.name.upper() == args:
					    found_dev = True
					    self.application().browser.load_item(dev)
					    break
			    else:
				break				
			break
		
		    
    def set_session_record(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off session record """
	if IS_LIVE_9:
	    if value in KEYWORDS:
		self.song().session_record = KEYWORDS[value]
	    else:
		self.song().session_record = not(self.song().session_record)
	    
	    
    def trigger_session_record(self, track, xclip, ident, value = None):
	""" Triggers session record in all armed tracks for the specified fixed length. """
	if IS_LIVE_9 and value:
            # the below fixes an issue where Live will crash instead of creating a new
            # scene when triggered via an X-Clip
            if type(xclip) is Live.Clip.Clip:
                scene = list(xclip.canonical_parent.canonical_parent.clip_slots).index(xclip.canonical_parent)
                for t in self.song().tracks:
                    if t.can_be_armed and t.arm:
                        if not self._track_has_empty_slot(t, scene):
                            self.song().create_scene(-1)
                            break
            bar = (4.0 / self.song().signature_denominator) * self.song().signature_numerator
            try: length = float(value.strip()) * bar
	    except: length = bar
	    self.song().trigger_session_record(length)


    def _track_has_empty_slot(self, track, start):
        """ Returns whether the given track has an empty slot existing after the starting
        slot index. """
        for s in track.clip_slots[start:]:
            if not s.has_clip:
                return True
        return False


    def set_session_automation_record(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off session automation record """
	if IS_LIVE_9:
	    if value in KEYWORDS:
		self.song().session_automation_record = KEYWORDS[value]
	    else:
		self.song().session_automation_record = not(self.song().session_automation_record)
	    
		
    def retrigger_recording_clips(self, track, xclip, ident, value = None):
	""" Retriggers all clips that are currently recording. """
	for track in self.song().tracks:
	    if track.playing_slot_index >= 0:
		slot = track.clip_slots[track.playing_slot_index]
		if slot.has_clip and slot.clip.is_recording:
		    slot.fire()
    
	    
    def set_back_to_arrange(self, track, xclip, ident, value = None):
	""" Triggers back to arrange button """
	self.song().back_to_arranger = 0
	
	
    def set_overdub(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off overdub """
	if value in KEYWORDS:
	    self.song().overdub = KEYWORDS[value]
	else:
	    self.song().overdub = not(self.song().overdub)
	    
	    
    def set_metronome(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off metronome """
	if value in KEYWORDS:
	    self.song().metronome = KEYWORDS[value]
	else:
	    self.song().metronome = not(self.song().metronome)	
	    
	    
    def set_record(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off record """
	if value in KEYWORDS:
	    self.song().record_mode = KEYWORDS[value]
	else:
	    self.song().record_mode = not(self.song().record_mode)	
	    
	    
    def set_punch_in(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off punch in """
	if value in KEYWORDS:
	    self.song().punch_in = KEYWORDS[value]
	else:
	    self.song().punch_in = not(self.song().punch_in)	
	    
	    
    def set_punch_out(self, track, xclip, ident, value = None):
	""" Toggles or turns on/off punch out """
	if value in KEYWORDS:
	    self.song().punch_out = KEYWORDS[value]
	else:
	    self.song().punch_out = not(self.song().punch_out)	

	    
    def restart_transport(self, track, xclip, ident, value = None):
	""" Restarts transport to 0.0 """
	self.song().current_song_time = 0
	
	
    def set_stop_transport(self, track, xclip, ident, value = None):
	""" Toggles transport """
	self.song().is_playing = not(self.song().is_playing)
	
	
    def set_continue_playback(self, track, xclip, ident, value = None):
	""" Continue playback from stop point """
	self.song().continue_playing()
	
	
    def set_stop_all(self, track, xclip, ident, value = None):
	""" Stop all clips w/no quantization option for Live 9 """
	if IS_LIVE_9:
	    self.song().stop_all_clips(not value.strip() == 'NQ')
	else:
	    self.song().stop_all_clips()
	
	
    def set_tap_tempo(self, track, xclip, ident, value = None):
	""" Tap tempo """
	self.song().tap_tempo()
	
	
    def set_undo(self, track, xclip, ident, value = None):
	""" Triggers Live's undo """
	if self.song().can_undo:
	    self.song().undo()
	    
	    
    def set_redo(self, track, xclip, ident, value = None):
	""" Triggers Live's redo """
	if self.song().can_redo:
	    self.song().redo()
	    
	    
    def move_up(self, track, xclip, ident, value = None):
	""" Scroll up """
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(0), '', False) 
	    
	
    def move_down(self, track, xclip, ident, value = None):
	""" Scroll down """
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(1), '', False) 
	
	
    def move_left(self, track, xclip, ident, value = None):
	""" Scroll left """
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(2), '', False) 
	
	
    def move_right(self, track, xclip, ident, value = None):
	""" Scroll right """
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(3), '', False)  
	
	
    def move_to_first_device(self, track, xclip, ident, value = None):
	""" Move to the first device on the track and scroll the view """
	self.focus_devices()
	self.song().view.selected_track.view.select_instrument()
	
	
    def move_to_last_device(self, track, xclip, ident, value = None):
	""" Move to the last device on the track and scroll the view """
	self.focus_devices()
	if self.song().view.selected_track.devices:
	    self.song().view.select_device(self.song().view.selected_track.devices[len(self.song().view.selected_track.devices) - 1])
	    self.application().view.scroll_view(Live.Application.Application.View.NavDirection(3), 'Detail/DeviceChain', False)
	    self.application().view.scroll_view(Live.Application.Application.View.NavDirection(2), 'Detail/DeviceChain', False)

      
    def move_to_prev_device(self, track, xclip, ident, value = None):
	""" Move to the previous device on the track """
	self.focus_devices()
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(2), 'Detail/DeviceChain', False)
	
	
    def move_to_next_device(self, track, xclip, ident, value = None):
	""" Move to the next device on the track """
	self.focus_devices()
	self.application().view.scroll_view(Live.Application.Application.View.NavDirection(3), 'Detail/DeviceChain', False)
	
    
    def focus_devices(self):
	""" Make sure devices are in focus and visible """
	self.application().view.show_view('Detail')
	self.application().view.show_view('Detail/DeviceChain')
		
	
    def show_clip_view(self, track, xclip, ident, value = None):
	""" Show clip view """
	self.application().view.show_view('Detail')
	self.application().view.show_view('Detail/Clip')
	
	
    def show_track_view(self, track, xclip, ident, value = None):
	""" Show track view """
	self.application().view.show_view('Detail')
	self.application().view.show_view('Detail/DeviceChain')
	
	
    def show_detail_view(self, track, xclip, ident, value = None):
	""" Toggle between showing/hiding detail view """
	if self.application().view.is_view_visible('Detail'):
	    self.application().view.hide_view('Detail')
	else:
	    self.application().view.show_view('Detail')
	    
	    
    def toggle_browser(self, track, xclip, ident, value = None):
	""" Hide/show browser and move focus to or from browser """
	if self.application().view.is_view_visible('Browser'):
	    self.application().view.hide_view('Browser')
	    self.application().view.focus_view('')
	else:
	    self.application().view.show_view('Browser')
	    self.application().view.focus_view('Browser')
	    
	
    def toggle_detail_view(self, track, xclip, ident, value = None):
	""" Toggle between clip and track view """
	self.application().view.show_view('Detail')
	if self.application().view.is_view_visible('Detail/Clip'):
	    self.application().view.show_view('Detail/DeviceChain')
	else:
	    self.application().view.show_view('Detail/Clip')
	    
	    
    def toggle_main_view(self, track, xclip, ident, value = None):
	""" Toggle between session and arrange view """
	if self.application().view.is_view_visible('Session'):
	    self.application().view.show_view('Arranger')
	else:
	    self.application().view.show_view('Session')
	    
	    
    def focus_browser(self, track, xclip, ident, value = None):
	""" Move the focus to the browser, show browser first if necessary """
	if not self.application().view.is_view_visible('Browser'):
	    self.application().view.show_view('Browser')
	self.application().view.focus_view('Browser')
	
	
    def focus_detail(self, track, xclip, ident, value = None):
	""" Move the focus to the detail view, show detail first if necessary """
	if not self.application().view.is_view_visible('Detail'):
	    self.application().view.show_view('Detail')
	self.application().view.focus_view('Detail')
	
	
    def focus_main(self, track, xclip, ident, value = None):
	""" Move the focus to the main focus """
	self.application().view.focus_view('')
	
	
    def adjust_horizontal_zoom(self, track, xclip, ident, value):     
	""" Horizontally zoom in in Arrange the number of times specified in value. This can accept ALL, but doesn't have any bearing. """
	zoom_all = 'ALL' in value
	value = value.replace('ALL', '').strip()
	try: value = int(value)
	except: return
	direct = (value > 0) + 2
	for index in range(abs(value) + 1):
	    self.application().view.zoom_view(Live.Application.Application.View.NavDirection(direct), '', zoom_all)
	    
	                                  
    def adjust_vertical_zoom(self, track, xclip, ident, value):
	""" Vertically zoom in on the selected track in Arrange the number of times specified in value. This can accept ALL for zooming all tracks. """
	zoom_all = 'ALL' in value
	value = value.replace('ALL', '').strip()
	try: value = int(value)
	except: return
	direct = (value > 0)
	for index in range(abs(value) + 1):
	    self.application().view.zoom_view(Live.Application.Application.View.NavDirection(direct), '', zoom_all)
	
	    
    def adjust_tempo(self, track, xclip, ident, args):
	""" Adjust/set tempo or apply smooth synced ramp """
	self._tempo_ramp_active = False
	self._tempo_ramp_settings = []
	args = args.strip()
	if args.startswith(('<', '>')):
	    factor = self._parent.get_adjustment_factor(args, True)
	    self.song().tempo = max(20, min(999, (self.song().tempo + factor)))
	elif args.startswith('*'):
	    try: self.song().tempo = max(20, min(999, (self.song().tempo * float(args[1:]))))
	    except: pass
	elif args.startswith('RAMP') and IS_LIVE_9:
	    arg_array = args.split()
	    if len(arg_array) == 3:
		try:
		    ramp_factor = float("%.2f" % (int(arg_array[1]) * self.song().signature_numerator))
		    if arg_array[2].startswith('*'):
			target_tempo = max(20, min(999, (self.song().tempo * float(arg_array[2][1:]))))
		    else:
			target_tempo = float("%.2f" % float(arg_array[2]))
		    if target_tempo >= 20.0 and target_tempo <= 999.0:
			self._tempo_ramp_settings = [target_tempo, (target_tempo - self.song().tempo) / ramp_factor]
			self._tempo_ramp_active = True
		except: pass
	else:
	    try:
		self.song().tempo = float(args)
	    except: pass
	    
	    
    def on_time_changed(self):
	""" Smooth BPM changes synced to tempo """
	if self._tempo_ramp_active and self._tempo_ramp_settings and self.song().is_playing:
	    time = int(str(self.song().get_current_beats_song_time()).split('.')[2])
	    if self._last_beat != time:
		self._last_beat = time
		self._tasks.add(self.apply_tempo_ramp)
		
		
    def apply_tempo_ramp(self, arg=None):
	""" Apply tempo smoothing """
	target_reached = False
	if self._tempo_ramp_settings[1] > 0:
	    target_reached = self._tempo_ramp_settings[0] <= self.song().tempo
	else:
	    target_reached = self._tempo_ramp_settings[0] >= self.song().tempo
	if target_reached:
	    self.song().tempo = self._tempo_ramp_settings[0]
	    self._tempo_ramp_active = False
	    self._tasks.kill()
	    self._tasks.clear()
	else:
	    self.song().tempo += self._tempo_ramp_settings[1] 
	   
	    
    def adjust_groove(self, track, xclip, ident, args):
	""" Adjust/set global groove """
	args = args.strip()
	if args.startswith(('<', '>')):
	    factor = self._parent.get_adjustment_factor(args, True)
	    self.song().groove_amount = max(0.0, min(1.3125, (self.song().groove_amount + factor * float(1.3125 / 131.0))))
	else:
	    try:
		self.song().groove_amount = int(args) * float(1.3125 / 131.0)
	    except: pass
	    
	    
    def set_note_repeat(self, track, xclip, ident, args):
	""" Set/toggle note repeat """
	if IS_LIVE_9:
	    args = args.strip()
	    if args in REPEAT_STATES:
		if args == 'OFF':
		    self._parent._c_instance.note_repeat.enabled = False
		    self._repeat_enabled = False
		else:
		    self._parent._c_instance.note_repeat.repeat_rate = REPEAT_STATES[args]
		    self._parent._c_instance.note_repeat.enabled = True
		    self._repeat_enabled = True
	    else:
		self._repeat_enabled = not self._repeat_enabled
		self._parent._c_instance.note_repeat.enabled = self._repeat_enabled 
		
		    
    def adjust_swing(self, track, xclip, ident, args):
	""" Adjust swing amount for use with note repeat """
	if IS_LIVE_9:
	    args = args.strip()
	    if args.startswith(('<', '>')):
		factor = self._parent.get_adjustment_factor(args, True)
		self.song().swing_amount = max(0.0, min(1.0, (self.song().swing_amount + factor * 0.01)))
	    else:
		try:
		    self.song().swing_amount = int(args) * 0.01
		except: pass
	    

    def adjust_global_quantize(self, track, xclip, ident, args):
	""" Adjust/set/toggle global quantization """
	args = args.strip()
	if args in GQ_STATES:
	    self.song().clip_trigger_quantization = GQ_STATES[args]
	elif args in ('<', '>'):
	    factor = self._parent.get_adjustment_factor(args)
	    new_gq = self.song().clip_trigger_quantization + factor
	    if new_gq in range (14):
		self.song().clip_trigger_quantization = new_gq
	else:
	    if self.song().clip_trigger_quantization != 0:
		self._last_gqntz = int(self.song().clip_trigger_quantization)
		self.song().clip_trigger_quantization = 0
	    else:
		self.song().clip_trigger_quantization = self._last_gqntz
	    
	    
    def adjust_record_quantize(self, track, xclip, ident, args):
	""" Adjust/set/toggle record quantization """
	args = args.strip()
	if args in RQ_STATES:
	    self.song().midi_recording_quantization = RQ_STATES[args]
	elif args in ('<', '>'):
	    factor = self._parent.get_adjustment_factor(args)
	    new_rq = self.song().midi_recording_quantization + factor
	    if new_rq in range (9):
		self.song().midi_recording_quantization = new_rq
	else:
	    if self.song().midi_recording_quantization != 0:
		self._last_rqntz = int(self.song().midi_recording_quantization)
		self.song().midi_recording_quantization = 0
	    else:
		self.song().midi_recording_quantization = self._last_rqntz
	    
    	    
    def adjust_time_signature(self, track, xclip, ident, args):
	""" Adjust global time signature """
	if '/' in args:
	    name_split = args.split('/')
	    try:
		self.song().signature_numerator = int(name_split[0].strip())
		self.song().signature_denominator = int(name_split[1].strip())
	    except: pass
	    
	    
    def set_jump_all(self, track, xclip, ident, args): 
	""" Jump arrange position forward/backward """
	try: self.song().jump_by(float(args.strip()))
	except: pass
	
	
    def set_unarm_all(self, track, xclip, ident, args):
	""" Unarm all armable tracks """
	for t in self.song().tracks:
	    if t.can_be_armed and t.arm:
		t.arm = 0  
		
		
    def set_unmute_all(self, track, xclip, ident, args):
	""" Unmute all tracks """
	for t in (tuple(self.song().tracks) + tuple(self.song().return_tracks)):
	    if t.mute:
		t.mute = 0
		
		
    def set_unsolo_all(self, track, xclip, ident, args):
	""" Unsolo all tracks """
	for t in (tuple(self.song().tracks) + tuple(self.song().return_tracks)):
	    if t.solo:
		t.solo = 0
		
		
    def set_fold_all(self, track, xclip, ident, value):
	""" Toggle or turn/on fold for all tracks """
	state_to_set = None
	for t in self.song().tracks:
	    if t.is_foldable:
		if state_to_set == None:
		    state_to_set = not(t.fold_state)
		if value in KEYWORDS:
		    t.fold_state = KEYWORDS[value]
		else:
		    t.fold_state = state_to_set
		    
	
    def set_scene(self, track, xclip, ident, args):  
	""" Sets scene to play (doesn't launch xclip) """
	args = args.strip()	
	scene_to_launch = self.get_scene_to_operate_on(xclip, args)
	if args != '':
	    if 'RND' in args and len(self.song().scenes) > 1:#--Don't allow randomization unless more than 1 scene
		num_scenes = len(self.song().scenes)
		rnd_range = [0, num_scenes]
		if '-' in args:
		    rnd_range_data = args.replace('RND', '').split('-')
		    if len(rnd_range_data) == 2:
			new_min = 0
			new_max = num_scenes
			try: new_min = int(rnd_range_data[0]) - 1
			except: new_min = 0
			try: new_max = int(rnd_range_data[1])
			except: new_max = num_scenes
			if new_min in range(0, num_scenes) and new_max in range(0, num_scenes + 1) and new_min < new_max - 1:
			    rnd_range = [new_min, new_max]
		scene_to_launch = Live.Application.get_random_int(0, rnd_range[1] - rnd_range[0]) + rnd_range[0] 
		if scene_to_launch == self._last_scene_index:
		    while scene_to_launch == self._last_scene_index:
			scene_to_launch = Live.Application.get_random_int(0, rnd_range[1] - rnd_range[0]) + rnd_range[0]
	    elif args.startswith(('<', '>')) and len(self.song().scenes) > 1:#--Don't allow adjustment unless more than 1 scene
		factor = self._parent.get_adjustment_factor(args)
		if factor < len(self.song().scenes):
		    scene_to_launch = self._last_scene_index + factor
		    if scene_to_launch >= len(self.song().scenes):
			scene_to_launch -= len(self.song().scenes)
		    elif scene_to_launch < 0 and abs(scene_to_launch) >= len(self.song().scenes):
			scene_to_launch = -(abs(scene_to_launch) - len(self.song().scenes))
	self._last_scene_index = scene_to_launch
	for t in self.song().tracks:
	    if t.is_foldable or (t.clip_slots[scene_to_launch].has_clip and t.clip_slots[scene_to_launch].clip == xclip):
		pass
	    else:
		t.clip_slots[scene_to_launch].fire()
		
		
    def get_scene_to_operate_on(self, xclip, args):
	scene = list(self.song().scenes).index(self.song().view.selected_scene)
	if type(xclip) is Live.Clip.Clip:
	    scene = xclip.canonical_parent.canonical_parent.playing_slot_index
	if args != '':
	    if '"' in args:
		scene_name = args[args.index('"')+1:]
		if '"' in scene_name:
		    scene_name = scene_name[0:scene_name.index('"')]
		    for index in range(len(self.song().scenes)):
			if scene_name == self.song().scenes[index].name.upper():
			    scene = index
			    break
	    elif args == 'SEL':
		scene = list(self.song().scenes).index(self.song().view.selected_scene)
	    else:
		try:
		    if int(args) in range(len(self.song().scenes) + 1):
			scene = int(args)-1
		except: pass
	return scene
    
    
    def set_locator(self, track, xclip, ident, args):
	""" Set/delete a locator at the current playback position """
	self.song().set_or_delete_cue()
	
    
    def do_locator_loop_action(self, track, xclip, ident, args):
	""" Same as do_locator_action with name argument, but also sets arrangement loop start to pos of locator. """
	self.do_locator_action(track, xclip, ident, args, True)
	    		    
		    
    def do_locator_action(self, track, xclip, ident, args, move_loop_too=False): 
	""" Jump between locators or to a particular locator. Can also move loop start to pos of locator if specified. """
	args = args.strip()
	if args == '>' and self.song().can_jump_to_next_cue:
	    self.song().jump_to_next_cue()
	elif args == '<' and self.song().can_jump_to_prev_cue:
	    self.song().jump_to_prev_cue()
	else:
	    try:
		for cp in self.song().cue_points:
		    if self._parent.get_name(cp.name) == args:
			cp.jump()
			if move_loop_too:
			    self.song().loop_start = cp.time
			break
	    except: pass
	    
	    
    def do_loop_action(self, track, xclip, ident, args):
	""" Handle arrange loop actions """
	args = args.strip()
	if args == '' or args in KEYWORDS:
	    self.set_loop_on_off(args)
	else:
	    new_start = self.song().loop_start
	    new_length = self.song().loop_length
	    if args.startswith(('<', '>')):
		self.move_loop_by_factor(args)
		return()
	    elif args == 'RESET':
		new_start = 0
	    elif args.startswith('*'):
		try:
		    new_length = self.song().loop_length * float(args[1:])
		except: pass
	    else:
		try:
		    new_length = float(args) * ((4.0 / self.song().signature_denominator) * self.song().signature_numerator)
		except: pass
	    self.set_new_loop_position(new_start, new_length)
	
	    
    def set_loop_on_off(self, value = None):
	""" Toggles or turns on/off arrange loop """
	if value in KEYWORDS:
	    self.song().loop = KEYWORDS[value]
	else:
	    self.song().loop = not(self.song().loop)
	    
	    
    def move_loop_by_factor(self, args):
	""" Move arrangement loop by its length or by a specified factor """
	factor = self.song().loop_length
	if args == '<':
	    factor = -(factor)
	if len(args) > 1:
	    factor = self._parent.get_adjustment_factor(args, True)
	new_start = self.song().loop_start + factor
	if new_start < 0.0:
	    new_start = 0.0
	self.set_new_loop_position(new_start, self.song().loop_length)
	
	
    def set_new_loop_position(self, new_start, new_length):
	""" For use with other loop actions, ensures that loop settings are within range """
	if new_start >= 0 and new_length >= 0 and new_length <= self.song().song_length:
	    self.song().loop_start = new_start  
	    self.song().loop_length = new_length	
	    
	    
    def setup_scene_listeners(self):
	""" Setup listeners for all scenes in set and check that last index is in current scene range. """
	self.remove_scene_listeners()
	scenes = self.song().scenes
	if not self._last_scene_index in range(len(scenes)):
	    self._last_scene_index = list(self.song().scenes).index(self.song().view.selected_scene)
	for index in range(len(scenes)):
	    self._scenes_to_monitor.append(scenes[index])
	    listener = lambda index = index:self.on_scene_triggered(index)
	    if not scenes[index].is_triggered_has_listener(listener):
		scenes[index].add_is_triggered_listener(listener)
		
	
    def remove_scene_listeners(self):
	if self._scenes_to_monitor:
	    scenes = self._scenes_to_monitor
	    for index in range(len(scenes)):
		if scenes[index]:
		    listener = lambda index = index:self.on_scene_triggered(index)
		    if scenes[index].is_triggered_has_listener(listener):
			scenes[index].remove_is_triggered_listener(listener)
	self._scenes_to_monitor = []     
    
# local variables:
# tab-width: 4
