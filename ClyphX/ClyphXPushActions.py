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

from __future__ import with_statement
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from consts import *

UNWRITABLE_INDEXES = (17, 35, 53)

MATRIX_MODES = {'SESSION': 'session',
                'NOTE': 'note'}
TRACK_MODES = {'STOP': 'stop',
               'SOLO': 'solo',
               'MUTE': 'mute'}
MAIN_MODES = {'VOLUME': 'volumes',
              'PAN': 'pan_sends',
              'TRACK': 'track',
              'CLIP': 'clip',
              'DEVICE': 'device'}
P2_MAIN_MODES = {'DEVICE': 'device',
                 'MIX': 'mix',
                 'CLIP': 'clip'}


class ClyphXPushActions(ControlSurfaceComponent):
    """ Actions related to Push/Push2 ???? control surface script. """

    def __init__(self, parent):
        super(ClyphXPushActions, self).__init__()
        self._parent = parent
        self._script = None
        self._ins_component = None
        self._note_editor = None
        self._scales_component = None
        self._is_push2 = False

    def disconnect(self):
        self._script = None
        self._ins_component = None
        self._note_editor = None
        self._scales_component = None
        self._parent = None
        super(ClyphXPushActions, self).disconnect()

    def set_script(self, push_script, is_push2=False):
        """ Set the Push script to connect to and get necessary components. """
        self._script = push_script
        self._is_push2 = is_push2
        if self._script and self._script._components:
            for c in self._script._components:
                comp_name = c.__class__.__name__
                if comp_name == 'InstrumentComponent':
                    self._ins_component = c
                elif comp_name.endswith('NoteEditorComponent'):
                    self._note_editor = c
                elif comp_name == 'ScalesComponent':
                    self._scales_component = c
            if not self._is_push2:
                s_mode = self._script._scales_enabler._mode_map['enabled'].mode
                if hasattr(s_mode, '_component'):
                    self._scales_component = s_mode._component
                else:
                    self._scales_component = s_mode._enableable

    def handle_session_offset(self, session, last_pos, args, parser):
        """  Special offset handling for use with 9.5. """
        try:
            new_track = session.track_offset
            new_scene = session.scene_offset
            if args.strip() == 'LAST':
                if last_pos:
                    session.set_offsets(last_pos[0], last_pos[1])
                return None
            return_val = (new_track, new_scene)		
            new_track, args = parser('T', args, new_track, self.song().tracks)
            new_scene, args = parser('S', args, new_scene, self.song().scenes)
            if new_track == -1 or new_scene == -1:
                return
            session.set_offsets(new_track, new_scene)
            return return_val
        except: pass

    def get_session_offsets(self, session):
        return session.track_offset, session.scene_offset

    def get_session_dimensions(self, session):
        return session.num_tracks, session.num_scenes

    def dispatch_action(self, track, xclip, ident, action, args):
        """ Dispatch action to proper action group handler. """
        if self._script:
            if args.startswith('SCL') and self._ins_component:
                self._handle_scale_action(args.replace('SCL', '').strip(), xclip, ident)
            elif args.startswith('SEQ') and self._note_editor:
                self._handle_sequence_action(args.replace('SEQ', '').strip())
            elif args == 'DRINS' and self.song().view.selected_track.has_midi_input:
                with self._script.component_guard():
                    with self._script._push_injector:
                        self._script._note_modes.selected_mode = 'instrument'
            elif args.startswith('MSG'):
                self._display_message(args, xclip)
            elif args.startswith('MODE'):
                self._handle_mode_selection(args.replace('MODE', '').strip())

    def _handle_mode_selection(self, mode_name):
        """ Handles switching to one of Push's mode if possible. """
        mode_component = None
        mode_dict = None
        if mode_name in MATRIX_MODES:
            mode_component = self._script._matrix_modes
            mode_dict = MATRIX_MODES
        elif mode_name in TRACK_MODES:
            if self._is_push2:
                main = self._script._mute_solo_stop
                mode = getattr(main, '_%s_button_handler' % TRACK_MODES[mode_name])
                main._mute_button_handler._unlock_mode()
                main._solo_button_handler._unlock_mode()
                main._stop_button_handler._unlock_mode()
                mode._allow_released_immediately_action = False
                mode._track_list_component.push_mode(mode._mode)
                mode._lock_mode()
                return
            mode_component = self._script._track_modes
            mode_dict = TRACK_MODES
        elif ((not self._is_push2 and mode_name in MAIN_MODES)
                or (self._is_push2 and mode_name in P2_MAIN_MODES)):
            mode_component = self._script._main_modes
            mode_dict = P2_MAIN_MODES if self._is_push2 else MAIN_MODES
        if mode_component and mode_dict:
            if mode_component.selected_mode != mode_dict[mode_name]:
                with self._script.component_guard():
                    with self._script._push_injector:
                        mode_component.selected_mode = mode_dict[mode_name]

    def _display_message(self, args, xclip):
        """ Temporarily displays a message in Push's display.  Uses special handling to
        ensure that empty display spaces aren't written to. """
        note_as_caps = args.replace('MSG', '', 1).strip()
        note_len = len(note_as_caps)
        start_index = xclip.name.upper().find(note_as_caps)
        note_at_og_case = xclip.name[start_index:note_len+start_index]
        if not self._is_push2:
            for i in UNWRITABLE_INDEXES:
                if len(note_at_og_case) > i and note_at_og_case[i] != ' ':
                    note_at_og_case = note_at_og_case[0:i] + ' ' + note_at_og_case[i:note_len]
                    note_len += 1
        self._script.show_notification(note_at_og_case)

    def _handle_scale_action(self, args, xclip, ident):
        """ Handles actions related to scale settings. """
        if args:
            arg_array = args.split()
            array_len = len(arg_array)
            if arg_array[0] == 'INKEY':
                self._handle_in_key(arg_array)
            elif arg_array[0] == 'FIXED':
                self._handle_fixed(arg_array)
            elif arg_array[0] == 'ROOT' and array_len == 2:
                self._handle_root_note(arg_array)    
            elif arg_array[0] == 'TYPE' and array_len >= 2:
                self._handle_scale_type(arg_array, args)
            elif arg_array[0] == 'OCT' and array_len >= 2 and arg_array[1] in ('<', '>'):
                self._handle_octave(arg_array)
            elif array_len == 6:
                self._recall_scale_settings(arg_array)
            self._update_scale_display_and_buttons()
        else:
            self._capture_scale_settings(xclip, ident)

    def _handle_in_key(self, arg_array):
        if len(arg_array) == 2 and arg_array[1] in KEYWORDS:
            self._ins_component._note_layout.is_in_key = KEYWORDS[arg_array[1]]
        else:
            self._ins_component._note_layout.is_in_key =\
                not self._ins_component._note_layout.is_in_key

    def _handle_fixed(self, arg_array):
        if len(arg_array) == 2 and arg_array[1] in KEYWORDS:
            self._ins_component._note_layout.is_fixed = KEYWORDS[arg_array[1]]
        else:
            self._ins_component._note_layout.is_fixed =\
                not self._ins_component._note_layout.is_fixed

    def _handle_root_note(self, arg_array):
        if arg_array[1] in NOTE_NAMES:
            self._ins_component._note_layout.root_note = NOTE_NAMES.index(arg_array[1])
        elif arg_array[1] in ('<', '>'):
            new_root = (self._parent.get_adjustment_factor(arg_array[1])
                        + self._ins_component._note_layout.root_note)
            if new_root in range(12):
                self._ins_component._note_layout.root_note = new_root

    def _handle_octave(self, arg_array):
        if arg_array[1] == '<':
            self._ins_component._slider.scroll_page_down()
        else:
            self._ins_component._slider.scroll_page_up()

    def _handle_scale_type(self, arg_array, args):
        if arg_array[1] in ('<', '>'):
            factor = self._parent.get_adjustment_factor(arg_array[1])
            if self._is_push2:
                idx = self._scales_component.selected_scale_index + factor
                self._scales_component._set_selected_scale_index(idx)
            else:
                scale_list = self._scales_component._scale_list.scrollable_list
                if factor < 0:
                    for index in range(abs(factor)):
                        scale_list.scroll_up()
                else:
                    for index in range(factor):
                        scale_list.scroll_down()
        else:
            scale_type = args.replace('TYPE', '').strip()
            if self._is_push2:
                for i, s in enumerate(self._scales_component.scale_names):
                    if s.upper() == scale_type:
                        self._scales_component._set_selected_scale_index(i)
                        break
            else:
                scale_list = self._scales_component._scale_list.scrollable_list
                for index in range(len(scale_list.items)):
                    modus = scale_list.items[index]
                    if modus.content.name.upper() == scale_type:
                        scale_list._set_selected_item_index(index)
                        break

    def _capture_scale_settings(self, xclip, ident):
        """ Captures scale settings and writes them to X-Clip's name. """
        if type(xclip) is Live.Clip.Clip:
            root = str(self._ins_component._note_layout.root_note)
            if self._is_push2:
                scl_type = self._scales_component.selected_scale_index
            else:
                scl_type = str(self._scales_component._scale_list.scrollable_list
                               .selected_item_index)
            octave = '0'
            fixed = str(self._ins_component._note_layout.is_fixed)
            inkey = str(self._ins_component._note_layout.is_in_key)
            orient = '0'
            xclip.name = '%s Push SCL %s %s %s %s %s %s' % (ident, root, scl_type, octave,
                                                            fixed, inkey, orient)

    def _recall_scale_settings(self, arg_array):
        """ Recalls scale settings from X-Trigger name. """
        try:
            self._ins_component._note_layout.root_note = int(arg_array[0])
            if self._is_push2:
                self._scales_component._set_selected_scale_index(int(arg_array[1]))
            else:
                self._scales_component._scale_list.scrollable_list.selected_item_index =\
                    int(arg_array[1])
            self._ins_component._note_layout.is_fixed = arg_array[3] == 'TRUE'
            self._ins_component._note_layout.is_in_key = arg_array[4] == 'TRUE'
        except: pass
        
    def _update_scale_display_and_buttons(self):
        """ Updates Push's scale display and buttons to indicate current settings. """
        if not self._is_push2:
            self._scales_component._update_data_sources()
            self._scales_component.update()

    def _handle_sequence_action(self, args):
        """ Handle note actions related to the note currently being sequenced. """
        c = self.song().view.detail_clip
        clip = c if c and c.is_midi_clip else None
        note = self._script._drum_component.selected_note
        if clip and note != None:
            self._parent._clip_actions.do_clip_note_action(clip, None, None, '',
                                                           'NOTES%s %s' % (note, args))
