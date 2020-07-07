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

class ExtraPrefs(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = " Extra prefs component for ClyphX "

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
	self._parent = parent
        self._show_highlight = True
        self._exclusive_arm = False
        self._exclusive_fold = False
        self._clip_record = False
	self._clip_record_slot = None
        self._midi_clip_length = False
        self._midi_clip_length_slot = None
        self._last_track = self.song().view.selected_track
	self.on_selected_track_changed()
	
	
    def disconnect(self):
	self.remove_listeners()
	self._last_track = None
	self._clip_record_slot = None
        self._midi_clip_length_slot = None
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
	
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
	       
        
    def get_user_settings(self, data): 
        """ Get user settings from config file and make sure they are in proper range """
	for d in data:
	    d = d.split('=')
	    if 'NAVIGATION_HIGHLIGHT' in d[0]:
		self._show_highlight = 'ON' in d[1]
	    elif 'EXCLUSIVE_ARM_ON_SELECT' in d[0] and 'ON' in d[1]:
		self._exclusive_arm = True
	    elif 'EXCLUSIVE_SHOW_GROUP_ON_SELECT' in d[0] and 'ON' in d[1]:
		self._exclusive_fold = True
	    elif 'CLIP_RECORD_LENGTH_SET_BY_GLOBAL_QUANTIZATION' in d[0] and 'ON' in d[1]:
		self._clip_record = True
	    elif 'DEFAULT_INSERTED_MIDI_CLIP_LENGTH' in d[0]:
		try:
		    if int(d[1].strip()) in range (2,17):
			self._midi_clip_length = int(d[1].strip())
		except: pass
	    self.on_selected_track_changed()
                                
    
    def on_selected_track_changed(self):
        """ Handles navigation highlight, triggering exclusive arm/fold functions and removes/sets up listeners for clip-related functions """
        ControlSurfaceComponent.on_selected_track_changed(self)
        track = self.song().view.selected_track
	clip_slot = self.song().view.highlighted_clip_slot
	self.remove_listeners()
        if self._show_highlight:
	    tracks = list(tuple(self.song().visible_tracks) + tuple(self.song().return_tracks))
	    tracks.append(self.song().master_track)
	    if self.song().view.selected_track in tracks:
		self._parent._set_session_highlight(tracks.index(self.song().view.selected_track), list(self.song().scenes).index(self.song().view.selected_scene), 1, 1, True)
	else:
	    self._parent._set_session_highlight(-1, -1, -1, -1, False)
        if self._exclusive_arm and track != self._last_track:
	    if IS_LIVE_9:
		self._parent.schedule_message(1, partial(self.do_exclusive_arm, track))
	    else:
		self._parent.schedule_message(1, self.do_exclusive_arm, track)
        if self._exclusive_fold and track != self._last_track:
	    if IS_LIVE_9:
		self._parent.schedule_message(1, partial(self.do_exclusive_fold, track))
	    else:
		self._parent.schedule_message(1, self.do_exclusive_fold, track)
        if self._clip_record:
	    if track.can_be_armed and not clip_slot.has_clip:
		self._clip_record_slot = clip_slot
		if not self._clip_record_slot.has_clip_has_listener(self.clip_record_slot_changed):
		    self._clip_record_slot.add_has_clip_listener(self.clip_record_slot_changed)
        if self._midi_clip_length:
	    if track.has_midi_input and not clip_slot.has_clip and not track.is_foldable:
		self._midi_clip_length_slot = clip_slot
		if not self._midi_clip_length_slot.has_clip_has_listener(self.midi_clip_length_slot_changed):
		    self._midi_clip_length_slot.add_has_clip_listener(self.midi_clip_length_slot_changed)
        self._last_track = track
	
     
    def do_exclusive_fold(self, track):
        """ Called on track change.  Collapses all group tracks except for the current group track """
        if (track.is_foldable):
            for t in self.song().tracks:
                if (t.is_foldable):
                    if t == track:
                        t.fold_state = 0
                    else:
                        t.fold_state = 1 
                        
                
    def do_exclusive_arm(self, track): 
        """ Called on track change.  Disarams all tracks except for the current track """
        for t in self.song().tracks:
            if (t.can_be_armed):
                if t == track:
                    t.arm = True
                else:
                    t.arm = False
		    
		    
    def clip_record_slot_changed(self):
	""" Called on slot has clip changed.  Checks if clip is recording and retriggers it if so """
	track = self.song().view.selected_track
	if self.song().clip_trigger_quantization != 0 and track.arm:
	    clip = self._clip_record_slot.clip
	    if clip and clip.is_recording:
		clip.fire()
		
	
    def midi_clip_length_slot_changed(self):
	"""Called on slot has clip changed to trigger set length function.  Checks if clip is not playing/triggered, is 1-bar in length, has no name and no notes."""
	clip = self._midi_clip_length_slot.clip
	if clip and not clip.is_playing and not clip.is_triggered:
	    one_bar = (4.0 / self.song().signature_denominator) * self.song().signature_numerator
	    if clip.length == one_bar and clip.name == '':
		clip.select_all_notes()
		all_notes = clip.get_selected_notes()
		clip.deselect_all_notes()
		if not all_notes:
		    if IS_LIVE_9:
			self._parent.schedule_message(1, partial(self.do_midi_clip_set_length, (clip, one_bar)))
		    else:
			self._parent.schedule_message(1, self.do_midi_clip_set_length, (clip, one_bar))


    def do_midi_clip_set_length(self, clip_params):
	""" Sets clip length and loop end to user-defined length """
	clip = clip_params[0]
	new_length = clip_params[1] * self._midi_clip_length
	clip.loop_end = new_length
	clip.looping = False
	clip.loop_end = new_length
	clip.looping = True
		    
                    
    def remove_listeners(self):
	""" Remove parameter listeners. """
	if self._clip_record_slot:
	    if self._clip_record_slot.has_clip_has_listener(self.clip_record_slot_changed):
		self._clip_record_slot.remove_has_clip_listener(self.clip_record_slot_changed)
	self._clip_record_slot = None
	if self._midi_clip_length_slot:
	    if self._midi_clip_length_slot.has_clip_has_listener(self.midi_clip_length_slot_changed):
		self._midi_clip_length_slot.remove_has_clip_listener(self.midi_clip_length_slot_changed)
	self._midi_clip_length_slot = None
	
    
    def on_selected_scene_changed(self):
        ControlSurfaceComponent.on_selected_scene_changed(self)
        self.on_selected_track_changed()
                           
    
# local variables:
# tab-width: 4
