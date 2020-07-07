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

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SessionComponent import SessionComponent
from consts import IS_LIVE_9_5
SessionRingComponent = None
if IS_LIVE_9_5:
    from ableton.v2.control_surface.components.session_ring import SessionRingComponent
    
class Push_APC_Combiner(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Class that syncs Push and APC40 session grids for proper emulation. '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._push = None
	self._push_session = None
	self._apc = None
	self._apc_session = None
	
	
    def disconnect(self):
	self._remove_listeners()
	self._push = None
	self._push_session = None
	self._apc = None
	self._apc_session = None
	self._parent = None
	ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass
    
    
    def set_up_scripts(self, scripts):
	""" Remove current listeners, get Push/APC scripts, set up listeners and also set feedback delay on APC+Push encoders. """
	self._remove_listeners()
	for script in scripts:
	    script_name = script.__class__.__name__ 
	    if script_name == 'Push':
		self._push = script
		self._push_session = self._get_session_component(script)
		if self._push_session:
		    for c in script.controls:
			if c.__class__.__name__ == 'TouchEncoderElement':
			    c.set_feedback_delay(-1)
	    elif script_name == 'APC40':
		self._apc = script
		self._apc_session = self._get_session_component(script)
		if self._apc_session:
		    for c in script.controls:
			if c.__class__.__name__ == 'RingedEncoderElement':
			    c.set_feedback_delay(-1)
		    self._apc_session.add_offset_listener(self._on_apc_offset_changed)
		    self._on_apc_offset_changed()

	    
    def _get_session_component(self, script):
	""" Get the session component for the given script. """
	comp = None
	if script and script._components:
	    for c in script.components:
		if isinstance (c, SessionComponent):
		    comp = c
		    break
	if comp is None:
            if hasattr(script, '_session_ring'):
                return script._session_ring
	return comp
    
    
    def _on_apc_offset_changed(self):
	""" Update Push offset on APC offset changed and suppress its highlight. """
	if self._push_session and self._apc_session:
	    self._push_session.set_offsets(self._apc_session.track_offset(), self._apc_session.scene_offset())
	    if IS_LIVE_9_5:
		self._push_session._session_ring.hide_highlight()
	    else:
		self._push._set_session_highlight(-1, -1, -1, -1, False)
    
    
    def _remove_listeners(self):
	if self._apc_session and self._apc_session.offset_has_listener(self._on_apc_offset_changed):
	    self._apc_session.remove_offset_listener(self._on_apc_offset_changed)
    
    
# local variables:
# tab-width: 4