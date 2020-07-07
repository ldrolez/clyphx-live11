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
from MacrobatMidiRack import MacrobatMidiRack
from MacrobatRnRRack import MacrobatRnRRack
from MacrobatSidechainRack import MacrobatSidechainRack
from MacrobatParameterRacks import MacrobatLearnRack, MacrobatChainMixRack, MacrobatDRMultiRack, MacrobatDRRack, MacrobatReceiverRack, MacrobatTrackRack
from consts import IS_LIVE_9, IS_LIVE_9_5
if IS_LIVE_9_5:
    from MacrobatPushRack import MacrobatPushRack
if IS_LIVE_9:
    from MacrobatParameterRacks9 import MacrobatChainSelectorRack, MacrobatDRPadMixRack

class Macrobat(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = " Macrobat script component for ClyphX "

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
	self._parent = parent
	self._current_tracks = []
	
	
    def disconnect(self):
	self._current_tracks = []
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
	
    def on_enabled_changed(self):
        pass
        

    def update(self):    
        pass
	
	
    def setup_tracks(self, track):
	""" Setup component tracks on ini and track list changes """
	if not track in self._current_tracks:
	    self._current_tracks.append(track)
	    MacrobatTrackComponent(track, self._parent)
        
    
class MacrobatTrackComponent(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Track component that monitors track devices '
    
    def __init__(self, track, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._track = track
	self._track.add_devices_listener(self.setup_devices)
	self._current_devices = []
	self._update_in_progress = False
	self._has_learn_rack = False
	self.setup_devices()
	
	
    def disconnect(self):
	self.remove_listeners()
	if self._track:
	    if self._track.devices_has_listener(self.setup_devices):
		self._track.remove_devices_listener(self.setup_devices)
	    self.remove_devices(self._track.devices)
	self._track = None
	self._current_devices = []
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	
	
    def update(self):    
	if self._track and self.song().view.selected_track == self._track:
	    self.setup_devices()
    
		    
    def on_enabled_changed(self):
	pass
	
	
    def reallow_updates(self):
	""" Reallow device updates, used to prevent updates happening in quick succession """
	self._update_in_progress = False
		
	
    def setup_devices(self):
	""" Get devices on device/chain list and device name changes """
	if self._track and not self._update_in_progress:
	    self._update_in_progress = True
	    self._has_learn_rack = False
	    self.remove_listeners()
	    self.get_devices(self._track.devices)
	    self._parent.schedule_message(5, self.reallow_updates)
	
	
    def remove_listeners(self):
	""" Disconnect Macrobat rack components """
	for d in self._current_devices:
	    d[0].disconnect()
	self._current_devices = []
		
	
    def get_devices(self, dev_list):
	""" Go through device and chain lists and setup Macrobat racks """
	for d in dev_list:
	    self.setup_macrobat_rack(d)
	    if not d.name_has_listener(self.setup_devices):
		d.add_name_listener(self.setup_devices)
	    if self._parent._can_have_nested_devices and d.can_have_chains:
		if not d.chains_has_listener(self.setup_devices):
		    d.add_chains_listener(self.setup_devices)
		for c in d.chains:
		    if not c.devices_has_listener(self.setup_devices):
			c.add_devices_listener(self.setup_devices)
		    self.get_devices(c.devices)
		    
    
    def setup_macrobat_rack(self, rack):
	""" Setup Macrobat rack if meets criteria """
	if rack.class_name.endswith('GroupDevice'):
	    name = self._parent.get_name(rack.name)
	    m = None
	    if name.startswith('NK RECEIVER'):
		m = MacrobatReceiverRack(self._parent, rack, self._track) 
	    elif name.startswith('NK TRACK') and not self._track.has_midi_output: 
		m = MacrobatTrackRack(self._parent, rack, self._track) 
	    elif name.startswith('NK DR MULTI') and self._parent._can_have_nested_devices:
		m = MacrobatDRMultiRack(self._parent, rack, self._track)
	    elif name.startswith('NK DR PAD MIX') and IS_LIVE_9_5:
		m = MacrobatDRPadMixRack(self._parent, rack, self._track) 
	    elif name.startswith('NK CHAIN MIX') and self._parent._can_have_nested_devices:
		m = MacrobatChainMixRack(self._parent, rack, self._track) 
	    elif name.startswith('NK DR') and self._parent._can_have_nested_devices:
		m = MacrobatDRRack(self._parent, rack, self._track) 
	    elif name.startswith('NK LEARN') and self._parent._can_have_nested_devices and self._track == self.song().master_track and not self._has_learn_rack:
		m = MacrobatLearnRack(self._parent, rack, self._track) 
		self._has_learn_rack = True
	    elif name.startswith('NK MIDI'): 
		m = MacrobatMidiRack(self._parent, rack, name) 
	    elif name.startswith(('NK RST', 'NK RND')): 
		m = MacrobatRnRRack(self._parent, rack, name, self._track) 
	    elif name.startswith('NK SIDECHAIN'): 
		m = MacrobatSidechainRack(self._parent, rack, self._track) 
	    elif name.startswith('NK SCL') and IS_LIVE_9_5:
		m = MacrobatPushRack(self._parent, rack)
	    elif name.startswith('NK CS') and IS_LIVE_9:
		m = MacrobatChainSelectorRack(self._parent, rack, self._track)
	    if m:
		self._current_devices.append((m, rack))
	    
	    
    def remove_devices(self, dev_list):
	""" Remove all device listeners """
	for d in dev_list:
	    if d.name_has_listener(self.setup_devices):
		d.remove_name_listener(self.setup_devices)
	    if self._parent._can_have_nested_devices and d.can_have_chains:
		if d.chains_has_listener(self.setup_devices):
		    d.remove_chains_listener(self.setup_devices)
		for c in d.chains:
		    if c.devices_has_listener(self.setup_devices):
			c.remove_devices_listener(self.setup_devices)
		    self.remove_devices(c.devices)
		    
		    
    def on_selected_track_changed(self):
	self.update()
		    
        
# local variables:
# tab-width: 4