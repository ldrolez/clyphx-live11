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

MAX_SCROLL_POS = 28 
    
class ClyphXDRActions9(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = 'Drum Rack actions '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	
	
    def disconnect(self):
	self._parent = None
	ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
	
	
    def scroll_selector(self, dr, track, xclip, ident, args):
	""" Scroll Drum Rack selector up/down """
	args = args.replace('SCROLL', '').strip()
	if args.startswith(('<', '>')):
	    factor = self._parent.get_adjustment_factor(args)
	    pos = dr.view.drum_pads_scroll_position
	    if factor > 0:
		if pos < MAX_SCROLL_POS - factor:
		    dr.view.drum_pads_scroll_position = pos + factor
		else:
		    dr.view.drum_pads_scroll_position = MAX_SCROLL_POS
	    else:
		if pos + factor > 0:
		    dr.view.drum_pads_scroll_position = pos + factor
		else:
		    dr.view.drum_pads_scroll_position = 0
		    
		    
    def unmute_all(self, dr, track, xclip, ident, args):
	""" Unmute all pads in the Drum Rack """
	for pad in dr.drum_pads:
	    pad.mute = False
	    
	    
    def unsolo_all(self, dr, track, xclip, ident, args):
	""" Unsolo all pads in the Drum Rack """
	for pad in dr.drum_pads:
	    pad.solo = False
	   	
	    
    def dispatch_pad_action(self, dr, track, xclip, ident, args):
	""" Dispatches pad-based actions """
	arg_split = args.split()
	if len(arg_split) > 1:
	    pads = self._get_pads_to_operate_on(dr, arg_split[0].replace('PAD', '').strip())
	    if pads:
		action = arg_split[1]
		action_arg = None
		if len(arg_split) > 2:
		    action_arg = arg_split[2]
		if arg_split[1] == 'MUTE':
		    self._mute_pads(pads, action_arg)
		elif arg_split[1] == 'SOLO':
		    self._solo_pads(pads, action_arg)	
		elif arg_split[1] == 'SEL':
		    dr.view.selected_drum_pad = pads[-1]
		elif arg_split[1] == 'VOL' and action_arg:
		    self._adjust_pad_volume(pads, action_arg)
		elif arg_split[1] == 'PAN' and action_arg:
		    self._adjust_pad_pan(pads, action_arg)
		elif 'SEND' in arg_split[1] and len(arg_split) > 3:
		    self._adjust_pad_send(pads, arg_split[3], action_arg)
			
			
    def _mute_pads(self, pads, action_arg):
	""" Toggles or turns on/off pad mute """
	for pad in pads:
	    if action_arg in KEYWORDS:
		pad.mute = KEYWORDS[action_arg]
	    else:
		pad.mute = not pad.mute
		
		
    def _solo_pads(self, pads, action_arg):
	""" Toggles or turns on/off pad solo """
	for pad in pads:
	    if action_arg in KEYWORDS:
		pad.solo = KEYWORDS[action_arg]
	    else:
		pad.solo = not pad.solo
		
		
    def _adjust_pad_volume(self, pads, action_arg):
	""" Adjust/set pad volume """
	for pad in pads:
	    if pad.chains:
		self._parent.do_parameter_adjustment(pad.chains[0].mixer_device.volume, action_arg)
		
		
    def _adjust_pad_pan(self, pads, action_arg):
	""" Adjust/set pad pan """
	for pad in pads:
	    if pad.chains:
		self._parent.do_parameter_adjustment(pad.chains[0].mixer_device.panning, action_arg)
		
		
    def _adjust_pad_send(self, pads, action_arg, send):
	""" Adjust/set pad send """
	try: 
	    for pad in pads:
		if pad.chains:
		    param = pad.chains[0].mixer_device.sends[ord(send) - 65]
		    self._parent.do_parameter_adjustment(param, action_arg)
	except: pass
	
	
    def _get_pads_to_operate_on(self, dr, pads):
	""" Get the Drum Rack pad or pads to operate on """
	pads_to_operate_on = [dr.view.selected_drum_pad]
	if pads == 'ALL':
	    pads_to_operate_on = dr.visible_drum_pads
	elif pads:
	    try: 
		index = int(pads) - 1
		if index in range(16):
		    pads_to_operate_on = [dr.visible_drum_pads[index]]
	    except: pass
	return pads_to_operate_on
    
    
# local variables:
# tab-width: 4