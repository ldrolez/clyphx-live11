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

HAS_PXT = False
try: 
    from _NKFW.ClipUtils import SEQ_RESOLUTIONS
    from _NKFW.Scales import SCALE_TYPES
    from _NKFW.ScalesComponent import EDITABLE_SCALE
    HAS_PXT = True
except: pass

UNWRITABLE_INDEXES = (17, 35, 53)
FULL_SEGMENT = 17
FULL_SEGMENT_OFFSETS = (0, 17, 34, 51)
    
class ClyphXPXTActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Actions related to the PXT-Live/PXT-Live Plus control surface '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._script = None
	self._mono_seq_mode = None
	self._poly_seq_mode = None
	self._encoders = None
	self._message_display_line = None
	
	
    def disconnect(self):
	self._script = None
	self._mono_seq_mode = None
	self._poly_seq_mode = None
	self._encoders = None
	self._message_display_line = None
	self._parent = None
	ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass    
    
    
    def set_script(self, pxt_script):
	""" Set the PXT script to connect to and get necessary components. """
	self._script = pxt_script
	if self._script and self._script._components:
	    self._message_display_line = self._script._display_lines[2]
	    for c in self._script.components:
		comp_name = c.__class__.__name__
		if 'MatrixModeSelector' in comp_name:
		    self._mono_seq_mode = c._mono_seq_mode
		    self._poly_seq_mode = c._poly_seq_mode
		elif 'EncModeSelector' in comp_name:
		    self._encoders = c._encoders
	
	
    def dispatch_action(self, track, xclip, ident, action, args):
	""" Dispatch action to proper action group handler. """
	if self._script:
	    if args.startswith('MSG'):
		self._display_message(args, xclip)
	    elif args.startswith('ENC'):
		self._handle_encoder_action(args.replace('ENC', '').strip())
	    elif args.startswith('MSEQ') and self._mono_seq_mode and self._mono_seq_mode.is_enabled():
		self._handle_mono_seq_action(args.replace('MSEQ', '').strip(), xclip, ident)
	    elif args.startswith('PSEQ') and self._poly_seq_mode and self._poly_seq_mode.is_enabled():
		self._handle_poly_seq_action(args.replace('PSEQ', '').strip(), xclip, ident)
		
		
    def _handle_mono_seq_action(self, args, xclip, ident):
	""" Handle note actions related to the note currently being sequenced in mono seq mode or capture mono seq mode settings. """
	comp = self._mono_seq_mode
	clip = comp._midi_clip
	if clip:
	    if args == 'CAP':
		self._capture_seq_settings(xclip, ident, comp, True)
	    elif args.startswith('CAP'):
		self._recall_seq_settings(args.replace('MSEQ', ''), comp)
	    else:
		note = comp._note_lane_components[comp._selected_lane_index]._note
		start = comp._position_component._start_position
		end = comp._position_component._end_position
		self._parent._clip_actions.do_clip_note_action(clip, None, None, '', 'NOTES' + str(note) + ' @' + str(start) + '-' + str(end) + ' ' + args)	
	    
	    
    def _handle_poly_seq_action(self, args, xclip, ident):
	""" Handle note actions related to the notes currently being sequenced in poly seq mode or capture poly seq mode settings. """
	comp = self._poly_seq_mode
	clip = comp._midi_clip
	if clip:
	    if args == 'CAP':
		self._capture_seq_settings(xclip, ident, comp, False)
	    elif args.startswith('CAP'):
		self._recall_seq_settings(args.replace('PSEQ', ''), comp)
	    else:
		start = comp._position_component._start_position
		end = comp._position_component._end_position
		notes = None
		if 'ALL' in args:
		    notes = str(comp._note_lane_components[0]._note) + '-' + str(comp._note_lane_components[-1]._note)
		    args = args.replace('ALL', '')
		else:
		    lane_spec = args.split()[0]
		    try:
			lane_num = int(lane_spec) - 1
			if lane_num in range(comp._num_note_lanes):
			    notes = str(comp._note_lane_components[lane_num]._note)
			args = args.replace(lane_spec, '')
		    except: pass
		if notes:
		    start = comp._position_component._start_position
		    end = comp._position_component._end_position
		    self._parent._clip_actions.do_clip_note_action(clip, None, None, '', 'NOTES' + str(notes) + ' @' + str(start) + '-' + str(end) + ' ' + args)	
		
		
    def _capture_seq_settings(self, xclip, ident, comp, is_mono):
	""" Capture the settings of the given seq comp and store them in the given xclip. """
	if type(xclip) is Live.Clip.Clip and HAS_PXT:
	    settings = ''
	    # res settings
	    settings += str(SEQ_RESOLUTIONS.index(comp._resolution_component._resolution)) + ' '
	    # velo settings
	    velo_comp = comp._velocity_component
	    settings += str(velo_comp._fixed_velocity) + ' '
	    settings += str(velo_comp._velocity_type) + ' '
	    # scale settings
	    scl_comp = comp._scales_component
	    settings += str(scl_comp._scale_index) + ' '
	    settings += str(scl_comp._root_note) + ' '
	    settings += str(scl_comp._octave_offset) + ' '
	    settings += str(scl_comp._offset_within_octave)
	    xclip.name = ident + ' PXT ' + ('MSEQ' if is_mono else 'PSEQ') + ' CAP ' + settings
    
    
    def _recall_seq_settings(self, args, comp):
	""" Recall the settings for the given seq comp. """
	arg_array = args.replace('CAP', '').strip().split()
	if len(arg_array) >= 7:
	    # res settings
	    res_comp = comp._resolution_component
	    if res_comp._resolution_buttons:
		res_btn = res_comp._resolution_buttons[int(arg_array[0])]
		res_comp._on_resolution_button_value(127, res_btn)
	    # velo settings
	    velo_comp = comp._velocity_component
	    velo_comp._fixed_velocity = int(arg_array[1])
	    velo_comp._velocity_type = int(arg_array[2])
	    velo_comp.update()
	    # scale settings
	    scl_comp = comp._scales_component
	    scl_index = int(arg_array[3])
	    scl_comp._scale_index = scl_index
	    scl_comp._root_note = int(arg_array[4])
	    scl_comp._octave_offset = int(arg_array[5])
	    scl_comp._offset_within_octave = int(arg_array[6])
	    scl_comp._scale = EDITABLE_SCALE if scl_index == -1 else SCALE_TYPES[scl_index]
	    scl_comp._set_current_notes()
    
    
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
	""" Temporarily displays a message in Push's display
	Uses special handling to ensure that empty display spaces aren't written to. """
	if self._message_display_line:
	    note_as_caps = args.replace('MSG', '', 1).strip()
	    note_len = len(note_as_caps)
	    start_index = xclip.name.upper().find(note_as_caps)
	    note_at_og_case = xclip.name[start_index:note_len+start_index]
	    for i in UNWRITABLE_INDEXES:
		if len(note_at_og_case) > i and note_at_og_case[i] != ' ':
		    note_at_og_case = note_at_og_case[0:i] + ' ' + note_at_og_case[i:note_len]
		    note_len += 1
	    new_len = len(note_at_og_case)
	    num_segments = (new_len / FULL_SEGMENT) + 1
	    for i in range(num_segments):
		offset = FULL_SEGMENT_OFFSETS[i]
		self._message_display_line.write_momentary(offset, FULL_SEGMENT, note_at_og_case[offset:offset+FULL_SEGMENT], True)
	    self._tasks.add(_Framework.Task.sequence(_Framework.Task.delay(15), self._revert_display))
	    
	    
    def _revert_display(self, args=None):
	""" Reverts the display after showing temp message. """
	self._message_display_line.revert()
    
# local variables:
# tab-width: 4