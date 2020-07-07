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
from ActionList import ActionList
from consts import *
if IS_LIVE_9:
    from functools import partial

class ClyphXControlComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Control component for ClyphX '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._control_list = {}
	self._xt_scripts = []
	
	
    def disconnect(self):
	self._control_list = {}
	self._xt_scripts = []
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)

	    
    def on_enabled_changed(self):
        pass
        

    def update(self):    
        pass
	
	
    def connect_script_instances(self, instanciated_scripts):
	""" Try to connect to ClyphX_XT instances """
	ClyphX_XT = None
	for i in range (5):
	    try:
		if i == 0:
		    from ClyphX_XTA.ClyphX_XT import ClyphX_XT
		elif i == 1:
		    from ClyphX_XTB.ClyphX_XT import ClyphX_XT
		elif i == 2:
		    from ClyphX_XTC.ClyphX_XT import ClyphX_XT
		elif i == 3:
		    from ClyphX_XTD.ClyphX_XT import ClyphX_XT
		elif i == 4:
		    from ClyphX_XTE.ClyphX_XT import ClyphX_XT
	    except: pass
	    if ClyphX_XT:
		for i in instanciated_scripts:
		    if isinstance(i, ClyphX_XT) and not i in self._xt_scripts:
			self._xt_scripts.append(i)
			break
		
	
    def assign_new_actions(self, string):
	""" Assign new actions to controls via xclips """
	if self._xt_scripts:
	    for x in self._xt_scripts:
		x.assign_new_actions(string)
 	ident = string[string.index('[')+2:string.index(']')].strip()
	actions = string[string.index(']')+2:].strip()
	for c, v in self._control_list.items():
	    if ident == v['ident']:
		new_actions = actions.split(',')
		on_action = '[' + ident + '] ' + new_actions[0]
		off_action = None
		if on_action and len(new_actions) > 1:
		    if new_actions[1].strip() == '*':
			off_action = on_action
		    else:
			off_action = '[' + ident + '] ' + new_actions[1]
		if on_action:
		    v['on_action'] = on_action    
		    v['off_action'] = off_action
		break
		
	    
    def receive_midi(self, bytes):
	""" Receive user-defined midi messages """
	if self._control_list:
	    ctrl_data = None
	    if bytes[2] == 0 or bytes[0] < 144:
		if (bytes[0], bytes[1]) in self._control_list.keys() and self._control_list[(bytes[0], bytes[1])]['off_action']:
		    ctrl_data = self._control_list[(bytes[0], bytes[1])]
		elif (bytes[0] + 16, bytes[1]) in self._control_list.keys() and self._control_list[(bytes[0] + 16, bytes[1])]['off_action']:
		    ctrl_data = self._control_list[(bytes[0] + 16, bytes[1])]
		if ctrl_data:
		    ctrl_data['name'].name = ctrl_data['off_action']	
	    elif bytes[2] != 0 and (bytes[0], bytes[1]) in self._control_list.keys():
		ctrl_data = self._control_list[(bytes[0], bytes[1])]
		ctrl_data['name'].name = ctrl_data['on_action']
	    if ctrl_data:
		self._parent.handle_action_list_trigger(self.song().view.selected_track, ctrl_data['name'])
	    
		
    def get_user_control_settings(self, data, midi_map_handle):
	""" Receives control data from user settings file and builds control dictionary """
	self._control_list = {}
	for d in data:
	    status_byte = None
	    channel = None
	    ctrl_num = None
	    on_action = None
	    off_action = None
	    d = d.split('=')
	    ctrl_name = d[0].strip()
	    new_ctrl_data = d[1].split(',')
	    try:
		if new_ctrl_data[0].strip() == 'NOTE':
		    status_byte = 144
		elif new_ctrl_data[0].strip() == 'CC':
		    status_byte = 176
		if int(new_ctrl_data[1].strip()) in range(1,17):
		    channel = int(new_ctrl_data[1].strip()) - 1
		if int(new_ctrl_data[2].strip()) in range(128):
		    ctrl_num = int(new_ctrl_data[2].strip())
		on_action = '[' + ctrl_name + '] ' + new_ctrl_data[3]
		if on_action and len(new_ctrl_data) > 4:
		    if new_ctrl_data[4].strip() == '*':
			off_action = on_action
		    else:
			off_action = '[' + ctrl_name + '] ' + new_ctrl_data[4]
	    except: pass
	    if status_byte and channel != None and ctrl_num != None and on_action:
		self._control_list[(status_byte + channel, ctrl_num)] = {'ident' : ctrl_name, 'on_action' : on_action, 'off_action' : off_action, 'name' : ActionList(on_action)}
		if status_byte == 144:
		    Live.MidiMap.forward_midi_note(self._parent._c_instance.handle(), midi_map_handle, channel, ctrl_num)
		else:
		    Live.MidiMap.forward_midi_cc(self._parent._c_instance.handle(), midi_map_handle, channel, ctrl_num)
		    
		    
    def rebuild_control_map(self, midi_map_handle):
	""" Called from main when build_midi_map is called. """
	for key in self._control_list.keys():
	    if key[0] >= 176:
		Live.MidiMap.forward_midi_cc(self._parent._c_instance.handle(), midi_map_handle, key[0] - 176, key[1])
	    else:
		Live.MidiMap.forward_midi_note(self._parent._c_instance.handle(), midi_map_handle, key[0] - 144, key[1])
    
	
class ClyphXTrackComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Track component that monitors play slot index and calls main script on changes '
    
    def __init__(self, parent, track):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._track = track
	self._clip = None  
	self._loop_count = 0  
	self._track.add_playing_slot_index_listener(self.play_slot_index_changed)
	self._register_timer_callback(self.on_timer)
	self._last_slot_index = -1
	self._triggered_clips = []
	self._triggered_lseq_clip = None
	
	
    def disconnect(self):
	self.remove_loop_jump_listener()
	self._unregister_timer_callback(self.on_timer)
	if self._track and self._track.playing_slot_index_has_listener(self.play_slot_index_changed):
	    self._track.remove_playing_slot_index_listener(self.play_slot_index_changed)
	self._track = None
	self._clip = None  
	self._triggered_clips = []
	self._triggered_lseq_clip = None
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
	
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
	
	
    def play_slot_index_changed(self):
	""" Called on track play slot index changes to set up clips to trigger (on play and stop) and set up loop listener for LSEQ. """
	self.remove_loop_jump_listener()
	new_clip = self.get_xclip(self._track.playing_slot_index)
	prev_clip = self.get_xclip(self._last_slot_index)
	self._last_slot_index = self._track.playing_slot_index
	if new_clip and prev_clip and new_clip == prev_clip:
	    self._triggered_clips.append(new_clip)
	elif new_clip:
	    if prev_clip:
		self._triggered_clips.append(prev_clip)
	    self._triggered_clips.append(new_clip)
	elif prev_clip:
	    self._triggered_clips.append(prev_clip)
	self._clip = new_clip
	if self._clip and '(LSEQ)' in self._clip.name.upper() and not self._clip.loop_jump_has_listener(self.on_loop_jump):
	    self._clip.add_loop_jump_listener(self.on_loop_jump)
	  	
	
    def get_xclip(self, slot_index):
	""" Get the xclip associated with slot_index or None. """
	clip = None
	if self._track and slot_index in xrange(len(self._track.clip_slots)):
	    slot = self._track.clip_slots[slot_index]
	    if slot.has_clip and not slot.clip.is_recording and not slot.clip.is_triggered:
		clip_name = slot.clip.name
		if len(clip_name) > 2 and clip_name[0] == '[' and ']' in clip_name:
		    clip = slot.clip
	return clip

    
    def on_loop_jump(self):
	""" Called on loop changes to increment loop count and set clip to trigger. """
	self._loop_count += 1
	if self._clip:
	    self._triggered_lseq_clip = self._clip
    
    
    def on_timer(self):
	""" Continuous timer, calls main script if there are any triggered clips. """
	if self._track and (not self._track.mute or self._parent._process_xclips_if_track_muted):
	    if self._triggered_clips:
		for clip in self._triggered_clips:
		    self._parent.handle_action_list_trigger(self._track, clip)  
		self._triggered_clips = []
	    if self._triggered_lseq_clip:
		self._parent.handle_loop_seq_action_list(self._triggered_lseq_clip, self._loop_count)
		self._triggered_lseq_clip = None
	    

    def remove_loop_jump_listener(self):
	self._loop_count = 0
	if self._clip and self._clip.loop_jump_has_listener(self.on_loop_jump):
	    self._clip.remove_loop_jump_listener(self.on_loop_jump)
	        
    
class ClyphXCueComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Cue component that monitors cue points and calls main script on changes '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self.song().add_current_song_time_listener(self.arrange_time_changed)
	self.song().add_is_playing_listener(self.arrange_time_changed)
	self.song().add_cue_points_listener(self.cue_points_changed)
	self._x_points = {}
	self._x_point_time_to_watch_for = -1
	self._last_arrange_position = -1
	self._sorted_times = []
	self.cue_points_changed()
	
	
    def disconnect(self):
	self.remove_cue_point_listeners()
	self.song().remove_current_song_time_listener(self.arrange_time_changed)
	self.song().remove_is_playing_listener(self.arrange_time_changed)
	self.song().remove_cue_points_listener(self.cue_points_changed)
	self._x_points = {}
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
    	
	    
    def cue_points_changed(self):
	""" Called on cue point changes to set up points to watch, cue points can't be named via the API so cue points can't perform any actions requiring naming """
	self.remove_cue_point_listeners()
	self._sorted_times = []
	for cp in self.song().cue_points:
	    if not cp.time_has_listener(self.cue_points_changed):
		cp.add_time_listener(self.cue_points_changed)
	    if not cp.name_has_listener(self.cue_points_changed):
		cp.add_name_listener(self.cue_points_changed)
	    name = self._parent.get_name(cp.name)
	    if len(name) > 2 and name[0] == '[' and name.count('[') == 1 and name.count(']') == 1:
		cue_name = name.replace(name[name.index('['):name.index(']')+1].strip(), '')
		self._x_points[cp.time] = cp
	self._sorted_times = sorted(self._x_points.keys())
	self.set_x_point_time_to_watch()

	
    def arrange_time_changed(self):
	""" Called on arrange time changed and schedules actions where necessary """
	if self.song().is_playing:
	    if self._x_point_time_to_watch_for != -1 and self._last_arrange_position < self.song().current_song_time:
		if self.song().current_song_time >= self._x_point_time_to_watch_for and self._x_point_time_to_watch_for < self._last_arrange_position:
		    if IS_LIVE_9:
			self._parent.schedule_message(1, partial(self.schedule_x_point_action_list, self._x_point_time_to_watch_for))
		    else:
			self._parent.schedule_message(1, self.schedule_x_point_action_list, self._x_point_time_to_watch_for)
		    self._x_point_time_to_watch_for = -1
	    else:
		self.set_x_point_time_to_watch()
	self._last_arrange_position = self.song().current_song_time
	    
	    
    def set_x_point_time_to_watch(self):
	""" Determine which cue point time to watch for next """
	if self._x_points:
	    if self.song().is_playing:
		for t in self._sorted_times:
		    if t >= self.song().current_song_time:
			self._x_point_time_to_watch_for = t
			break
	    else:
		self._x_point_time_to_watch_for = -1
		
		
    def schedule_x_point_action_list(self, point):
	self._parent.handle_action_list_trigger(self.song().view.selected_track, self._x_points[point])
	    
    
    def remove_cue_point_listeners(self):
	for cp in self.song().cue_points:
	    if cp.time_has_listener(self.cue_points_changed):
		cp.remove_time_listener(self.cue_points_changed)
	    if cp.name_has_listener(self.cue_points_changed):
		cp.remove_name_listener(self.cue_points_changed)
	self._x_points = {}
	self._x_point_time_to_watch_for = -1
	
    
# local variables:
# tab-width: 4
