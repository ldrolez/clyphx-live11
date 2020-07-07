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
import _Framework.Task
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

MAX_CHARS = 52
FULL_SEGMENT = 26
FULL_SEGMENT_OFFSETS = (0, 28)

class ClyphXMXTActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Actions related to the MXT-Live control surface '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._script = None
	self._seq_comp = None
	self._encoders = None
	self._message_display_line = None
	
	
    def disconnect(self):
	self._script = None
	self._seq_comp = None
	self._encoders = None
	self._message_display_line = None
	self._parent = None
	ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass    
    
    def set_script(self, mxt_script):
	""" Set the MXT script to connect to and get necessary components. """
	self._script = mxt_script
	if self._script and self._script._components:
	    self._message_display_line = self._script._display_lines[0]
	    for c in self._script.components:
		comp_name = c.__class__.__name__
		if 'NoteSeqComponent' in comp_name:
		    self._seq_comp = c
		elif 'EncModeSelector' in comp_name:
		    self._encoders = c._encoders
	
	
    def dispatch_action(self, track, xclip, ident, action, args):
	""" Dispatch action to proper action group handler. """
	if self._script:
	    if args.startswith('MSG'):
		self._display_message(args, xclip)
	    elif args.startswith('ENC'):
		self._handle_encoder_action(args.replace('ENC', '').strip())
	    elif args.startswith('SEQ') and self._seq_comp:
		self._handle_seq_action(args.replace('SEQ', '').strip(), xclip, ident)
		
		
    def _handle_seq_action(self, args, xclip, ident):
	""" Handle note actions related to the note currently being sequenced. """
	comp = self._seq_comp
	clip = comp._midi_clip
	if clip:
	    note = comp._note_lane_component._note
	    start = comp._position_component._start_position
	    end = comp._position_component._end_position
	    self._parent._clip_actions.do_clip_note_action(clip, None, None, '', 'NOTES' + str(note) + ' @' + str(start) + '-' + str(end) + ' ' + args)	
	    
	    
    def _handle_encoder_action(self, args):
	""" Reset or randomize the values of the parameters the encoders are controlling. """
	if self._encoders:
	    randomize = args == 'RND'
	    for enc in self._encoders:
		if enc:
		    p = enc.mapped_parameter()
		    if p and p.is_enabled and not p.is_quantized:
			if randomize:
			    p.value = (((p.max - p.min) / 127) * Live.Application.get_random_int(0, 128)) + p.min
			else:
			    p.value = p.default_value
			    
			    
    def _display_message(self, args, xclip):
	""" Temporarily displays a message in Maschine's display. """
	if self._message_display_line:
	    msg = args.replace('MSG', '', 1).strip()
	    if len(msg) > MAX_CHARS:
		msg = msg[:MAX_CHARS]
	    num_segments = 2 if len(msg) > FULL_SEGMENT else 1
	    for i in range(num_segments):
		offset = FULL_SEGMENT_OFFSETS[i]
		self._message_display_line.write_momentary(offset, FULL_SEGMENT, msg[offset:offset+FULL_SEGMENT], True)
	    self._tasks.add(_Framework.Task.sequence(_Framework.Task.delay(15), self._revert_display))
	    
	
    def _revert_display(self, args=None):
	""" Reverts the display after showing temp message. """
	self._message_display_line.revert()
    
# local variables:
# tab-width: 4