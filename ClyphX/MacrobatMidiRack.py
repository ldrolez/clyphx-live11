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
from MacrobatUserConfig import *
from consts import IS_LIVE_9

class MacrobatMidiRack(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Macros To Midi CCs + PCs + SysEx '    

    def __init__(self, parent, rack, name):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._macro_to_cc = []
	self._macro_to_pc = []
	self._macro_to_sysex = []
	self._sysex_list = []
	self.build_sysex_list()
	self.setup_device(rack, name)
	
	
    def disconnect(self):
	self.remove_macro_listeners()
	self._macro_to_cc = []
	self._macro_to_pc = []
	self._macro_to_sysex = []
	self._sysex_list = []
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
		
	    
    def on_enabled_changed(self):
        pass
        

    def update(self):    
        pass
	
		
    def setup_device(self, rack, name):
	""" - Rack name needs to start with 'nK MIDI'
	    - Default channel is 0. Can change with '[CHn]' in rack name
	    - Macro names needs to start with = functions:
	      * [CCn] = Where n is the CC# to send 
	      * [PC] = Program Change 
	      * SysEx_identifier = Identifier specified in SysEx List in user config """
	self.remove_macro_listeners()
	channel = self.check_for_channel(name)
	for p in rack.parameters:
	    if p.is_enabled:
		name = self._parent.get_name(p.name)
		if name.startswith('[CC') and not p.value_has_listener(self.do_cc):
		    cc_num = self.check_for_cc_num(name)
		    if cc_num != None:
			self._macro_to_cc.append((p, cc_num, -1, rack, channel))
			p.add_value_listener(self.do_cc)
		elif name.startswith('[PC]') and not p.value_has_listener(self.do_pc):  
		    self._macro_to_pc.append((p, -1, rack, channel))
		    p.add_value_listener(self.do_pc)
		else:
		    sysex_entry = self.check_sysex_list(name)
		    if sysex_entry and not p.value_has_listener(self.do_sysex):
			self._macro_to_sysex.append((p, sysex_entry, -1, rack))
			p.add_value_listener(self.do_sysex)

		    
    def do_cc(self):
	""" Send out CC on macro value change """
	if self._macro_to_cc:
	    for p in self._macro_to_cc:
		if int(p[0].value) != p[2]:
		    self._parent._send_midi((int(176 + p[4]), p[1], int(p[0].value)))
		    self._macro_to_cc[self._macro_to_cc.index(p)] = ((p[0], p[1], int(p[0].value), p[3], p[4]))
		    
		    
    def do_pc(self):
	""" Send out PC on macro value change """
	if self._macro_to_pc:
	    for p in self._macro_to_pc:
		if int(p[0].value) != p[1]:
		    self._parent._send_midi((int(192 + p[3]), int(p[0].value)))
		    self._macro_to_pc[self._macro_to_pc.index(p)] = ((p[0], int(p[0].value), p[2], p[3]))
	
    
    def do_sysex(self):
	""" Send out SysEx on macro value change """
	if self._macro_to_sysex:
	    for p in self._macro_to_sysex:
		if int(p[0].value) != p[2]:
		    new_string = []
		    send_new_val = True
		    for byte in p[1][0]:
			if byte == -1:
			    new_val = int((((p[1][2] - p[1][1]) / 127.0) * int(p[0].value)) + p[1][1])
			    if int((((p[1][2] - p[1][1]) / 127.0) * p[2]) + p[1][1]) != new_val:
				new_string.append(new_val)
			    else:
				send_new_val = False
			else:
			    new_string.append(byte)
		    if send_new_val:
			self._parent._send_midi(tuple(new_string))
		self._macro_to_sysex[self._macro_to_sysex.index(p)] = ((p[0], p[1], int(p[0].value), p[3]))
				
		
    def build_sysex_list(self):
	""" Build SysEx list (in decimal) based on user-defined list """
	self._sysex_list = []
	if SYSEX_LIST:
	    for s in SYSEX_LIST:
		if len(s) == 4:
		    bytes = s[1].split()
		    current_entry = []
		    if bytes[0] == 'F0' and bytes[-1] == 'F7' and s[2] in range (128) and s[3] in range (128):
			for byte in bytes:
			    if byte == 'nn':
				current_entry.append(-1)
			    else:
				if int(byte, 16) in range (248):
				    current_entry.append(int(byte, 16))
			self._sysex_list.append((s[0], current_entry, s[2], s[3]))
			
		    
    def check_sysex_list(self, name_string):
	""" Check that SysEx list exists and identifier exists in list """
	result = None
	if self._sysex_list:
	    for entry in self._sysex_list:
		if self._parent.get_name(entry[0]) == name_string:
		    result = [entry[1], entry[2], entry[3]]
	return result
    
	
    def check_for_channel(self, name):
	""" Check for user-specified channel in rack name """
	result = 0
	if '[CH' in name and ']' in name and not name.count('[') > 1 and not name.count(']') > 1:
	    try:
		get_ch = int(name[name.index('[')+3:name.index(']')])
		if get_ch in range (1, 17):
		    result = get_ch - 1
	    except:
		pass
	return result
    
    
    def check_for_cc_num(self, name):
	""" Check for user-specified CC# in macro name """
	result = None
	if '[CC' in name and ']' in name and not name.count('[') > 1 and not name.count(']') > 1:
	    try:
		get_cc = int(name[name.index('[')+3:name.index(']')])
		if get_cc in range (128):
		    result = get_cc
	    except:
		pass
	return result

    	
    def remove_macro_listeners(self):
	""" Remove listeners """
	if self._macro_to_cc:
	    for p in self._macro_to_cc:
		if p[3] and p[0].value_has_listener(self.do_cc):
		    p[0].remove_value_listener(self.do_cc)
	self._macro_to_cc = []
	if self._macro_to_pc:
	    for p in self._macro_to_pc:
		if p[2] and p[0].value_has_listener(self.do_pc):
		    p[0].remove_value_listener(self.do_pc)
	self._macro_to_pc = []
	if self._macro_to_sysex:
	    for p in self._macro_to_sysex:
		if p[3] and p[0].value_has_listener(self.do_sysex):
		    p[0].remove_value_listener(self.do_sysex)
	self._macro_to_sysex = []
	
		
# local variables:
# tab-width: 4