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
from .ClyphXClipEnvCapture import ClyphXClipEnvCapture
from .consts import *
if IS_LIVE_9:
    import random

ENV_TYPES = ('IRAMP', 'DRAMP', 'IPYR', 'DPYR', 'SQR', 'SAW')
   
class ClyphXClipActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Clip-related actions '

    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
        self._env_capture = ClyphXClipEnvCapture()
        
        
    def disconnect(self):
        self._parent = None
        if IS_LIVE_9:
            ControlSurfaceComponent.disconnect(self)            
            
    
    def on_enabled_changed(self):
        pass
        

    def update(self):    
        pass
        
        
    def set_clip_name(self, clip, track, xclip, ident, args): 
        """ Set clip's name """
        args = args.strip()
        if args:
            clip.name = args

    def set_clip_color(self, clip, track, xclip, ident, args): 
        """ Set clip's color """
        args = args.strip()
        if args:
            clip.color = int(args,16)
                
        
    def set_clip_on_off(self, clip, track, xclip, ident, value = None):
        """ Toggles or turns clip on/off """
        if value in KEYWORDS:
            clip.muted = not(KEYWORDS[value])
        else:
            clip.muted = not(clip.muted)
            
            
    def set_warp(self, clip, track, xclip, ident, value = None):
        """ Toggles or turns clip warp on/off """
        if clip.is_audio_clip:
            value = value.strip()
            if value in KEYWORDS:
                clip.warping = KEYWORDS[value]
            else:
                clip.warping = not(clip.warping)
            
            
    def adjust_time_signature(self, clip, track, xclip, ident, args):
        """ Adjust clip's time signature """
        if '/' in args:
            name_split = args.split('/')
            try:
                clip.signature_numerator = int(name_split[0].strip())
                clip.signature_denominator = int(name_split[1].strip())
            except: pass
            
               
    def adjust_detune(self, clip, track, xclip, ident, args):
        """ Adjust/set audio clip detune """
        if clip.is_audio_clip:
            args = args.strip()
            if args.startswith(('<', '>')):
                factor = self._parent.get_adjustment_factor(args)
                clip.pitch_fine = clip.pitch_fine + factor
            else:
                try:
                    clip.pitch_fine = int(args)
                except: pass
                
                
    def adjust_transpose(self, clip, track, xclip, ident, args):
        """ Adjust audio or midi clip transpose, also set audio clip transpose """
        args = args.strip()
        if args.startswith(('<', '>')):
            factor = self._parent.get_adjustment_factor(args)
            if clip.is_audio_clip:
                clip.pitch_coarse = max(-48, min(48, (clip.pitch_coarse + factor)))
            elif clip.is_midi_clip:
                self.do_note_pitch_adjustment(clip, factor)
        else:
            if clip.is_audio_clip:
                try:
                    clip.pitch_coarse = int(args)
                except: pass
                
                
    def adjust_gain(self, clip, track, xclip, ident, args):
        """ Adjust/set clip gain for Live 9. For settings, range is 0 - 127. """
        if IS_LIVE_9 and clip.is_audio_clip:
            args = args.strip()
            if args.startswith(('<', '>')):
                factor = self._parent.get_adjustment_factor(args, True)
                clip.gain = max(0.0, min(1.0, (clip.gain + factor * float(1.0 / 127.0))))
            else:
                try:
                    clip.gain = int(args) * float(1.0 / 127.0)
                except: pass
            
            
    def adjust_start(self, clip, track, xclip, ident, args):
        """ Adjust/set clip start exclusively for Live 9. In Live 8, same as adjust_loop_start. """
        args = args.strip()
        if args.startswith(('<', '>')):
            factor = self._parent.get_adjustment_factor(args, True)
            if IS_LIVE_9 and clip.looping:
                clip.start_marker = max(0.0, min(clip.end_marker - factor, (clip.start_marker + factor)))
            else:
                clip.loop_start = max(0.0, min(clip.loop_end - factor, (clip.loop_start + factor)))
        else:
            try:
                if IS_LIVE_9 and clip.looping:
                    clip.start_marker = float(args)
                else:
                    clip.loop_start = float(args)
            except: pass
            
            
    def adjust_loop_start(self, clip, track, xclip, ident, args):
        """ Adjust/set clip loop start if loop is on or clip start otherwise. """
        args = args.strip()
        if args.startswith(('<', '>')):
            factor = self._parent.get_adjustment_factor(args, True)
            clip.loop_start = max(0.0, min(clip.loop_end - factor, (clip.loop_start + factor)))
        else:
            try:
                clip.loop_start = float(args)
            except: pass
            
            
    def adjust_end(self, clip, track, xclip, ident, args):
        """ Adjust/set clip end exclusively for Live 9. In Live 8, same as adjust_loop_end. """
        args = args.strip()
        if args.startswith(('<', '>')):
            factor = self._parent.get_adjustment_factor(args, True)
            if IS_LIVE_9 and clip.looping:
                clip.end_marker = max((clip.start_marker - factor), (clip.end_marker + factor))
            else:
                clip.loop_end = max((clip.loop_start - factor), (clip.loop_end + factor))
        else:
            try:
                if IS_LIVE_9 and clip.looping:
                    clip.end_marker = float(args)
                else:
                    clip.loop_end = float(args)
            except: pass
            
            
    def adjust_loop_end(self, clip, track, xclip, ident, args):
        """ Adjust/set clip loop end if loop is on or close end otherwise. """
        args = args.strip()
        if args.startswith(('<', '>')):
            factor = self._parent.get_adjustment_factor(args, True)
            clip.loop_end = max((clip.loop_start - factor), (clip.loop_end + factor))
        else:
            try:
                clip.loop_end = float(args)
            except: pass
            
            
    def adjust_cue_point(self, clip, track, xclip, ident, args):
        """ Adjust clip's start point and fire (also stores cue point if not specified). Will not fire xclip itself as this causes a loop """
        if clip.is_midi_clip or (clip.is_audio_clip and clip.warping):
            if args:
                args = args.strip()
                if args.startswith(('<', '>')):
                    factor = self._parent.get_adjustment_factor(args, True)
                    args = clip.loop_start + factor
                try:
                    clip.loop_start = float(args)
                    if clip.looping:
                        clip.looping = False
                        clip.loop_start = float(args)
                        clip.looping = True
                    if clip != xclip: 
                        clip.fire()
                except: pass
            else:
                if type(xclip) is Live.Clip.Clip:
                    xclip.name = xclip.name.strip() + ' ' + str(clip.loop_start)
                    
                    
    def adjust_warp_mode(self, clip, track, xclip, ident, args):
        """ Adjusts the warp mode of the clip. This cannot be applied if the warp mode is currently rex (5). """
        if IS_LIVE_9 and clip.is_audio_clip and clip.warping and not clip.warp_mode == 5:
            args = args.strip()
            if args in WARP_MODES:
                clip.warp_mode = WARP_MODES[args]
            elif args in ('<', '>'):
                factor = self._parent.get_adjustment_factor(args)
                new_mode = clip.warp_mode + factor
                if new_mode == 5 and '>' in args:
                    new_mode = 6
                elif new_mode == 5 and '<' in args:
                    new_mode = 4
                if new_mode in range(7) and new_mode != 5:
                    clip.warp_mode = new_mode
                    
                    
    def adjust_grid_quantization(self, clip, track, xclip, ident, args):
        """ Adjusts clip grid quantization. """
        if IS_LIVE_9:
            args = args.strip()
            if args in CLIP_GRID_STATES:
                clip.view.grid_quantization = CLIP_GRID_STATES[args]
                
                
    def set_triplet_grid(self, clip, track, xclip, ident, args):
        """ Toggles or turns triplet grid on or off. """
        if IS_LIVE_9:
            if args in KEYWORDS:
                clip.view.grid_is_triplet = KEYWORDS[args]
            else:
                clip.view.grid_is_triplet = not(clip.view.grid_is_triplet)
                
        
    def capture_to_envelope(self, clip, track, xclip, ident, args):
        if IS_LIVE_9_1:
            self._env_capture.capture(clip, track, args)
        
                    
    def insert_envelope(self, clip, track, xclip, ident, args):
        """ Inserts an envelope for the given parameter into the clip. 
        This doesn't apply to quantized parameters. 
        Requires 9.1 or later. """
        if IS_LIVE_9_1:
            args = args.strip()
            arg_array = args.split()
            if len(arg_array) > 1:
                # used to determine whether env_type is last arg...otherwise a range is specified
                last_arg_index = len(arg_array) - 1
                env_type_index = last_arg_index
                env_type = None
                for index in range(len(arg_array)):
                    if arg_array[index] in ENV_TYPES:
                        env_type_index = index
                        env_type = arg_array[index]
                        break   
                if env_type:
                    env_param_spec = ''
                    for index in range(env_type_index):
                        env_param_spec += arg_array[index] + ' '
                    param = self._get_envelope_parameter(track, env_param_spec)
                    if param and not param.is_quantized:
                        env_range = (param.min, param.max)
                        # calculate range if specified in args
                        if env_type_index != last_arg_index:
                            try: 
                                min_factor = int(arg_array[-2]) 
                                max_factor = int(arg_array[-1])
                                if min_factor in range(101) and max_factor in range(101) and min_factor < max_factor:
                                    env_range = ((min_factor / 100.0) * param.max, (max_factor / 100.0) * param.max)
                            except: pass
                        self.song().view.detail_clip = clip
                        clip.view.show_envelope()
                        clip.view.select_envelope_parameter(param)      
                        clip.clear_envelope(param)
                        clip.create_automation_envelope(param)
                        self._perform_envelope_insertion(clip, param, env_type, env_range)
                                                    
                         
    def _perform_envelope_insertion(self, clip, param, env_type, env_range):
        """ Performs the actual insertion of the envelope into the clip. """
        env = clip.automation_envelope(param)
        if env:
            median = ((clip.loop_end - clip.loop_start) / 2.0) + clip.loop_start
            num_beats = int(clip.loop_end - clip.loop_start) + 1
            start_beat = int(clip.loop_start)
            if env_type == 'IRAMP':   
                env.insert_step(clip.loop_start, 0.0, env_range[0])
                env.insert_step(clip.loop_end, 0.0, env_range[1])
            elif env_type == 'DRAMP':
                env.insert_step(clip.loop_start, 0.0, env_range[1])
                env.insert_step(clip.loop_end, 0.0, env_range[0])
            elif env_type == 'IPYR':
                env.insert_step(clip.loop_start, 0.0, env_range[0])
                env.insert_step(median, 0.0, env_range[1])
                env.insert_step(clip.loop_end, 0.0, env_range[0])
            elif env_type == 'DPYR':
                env.insert_step(clip.loop_start, 0.0, env_range[1])
                env.insert_step(median, 0.0, env_range[0])
                env.insert_step(clip.loop_end, 0.0, env_range[1])
            elif env_type == 'SAW':
                for b in range(num_beats):
                    beat = float(b + start_beat)
                    env.insert_step(beat, 0.0, env_range[1])
                    if beat < clip.loop_end:
                        env.insert_step(beat + 0.5, 0.0, env_range[0])
            elif env_type == 'SQR':
                for b in range(num_beats):
                    beat = float(b + start_beat)
                    if beat < clip.loop_end:
                        if b % 2 == 0:
                            env.insert_step(beat, 1.0, env_range[1])
                        else:
                            env.insert_step(beat, 1.0, env_range[0])
                        
                    
    def clear_envelope(self, clip, track, xclip, ident, args):
        """ Clears the envelope of the specified param or all envelopes from the given clip. """
        if IS_LIVE_9_1:
            if args:
                param = self._get_envelope_parameter(track, args.strip())
                if param:
                    clip.clear_envelope(param)
            else:
                clip.clear_all_envelopes()
            
            
    def show_envelope(self, clip, track, xclip, ident, args):
        """ Shows the clip's envelope view and a particular envelope if specified. 
        Requires 9.1 or later. """
        if IS_LIVE_9_1:
            self.song().view.detail_clip = clip
            clip.view.show_envelope()
            if args:
                param = self._get_envelope_parameter(track, args.strip())
                if param:
                    clip.view.select_envelope_parameter(param)                      
                            
                            
    def _get_envelope_parameter(self, track, args):
        """ Gets the selected, mixer or device parameter for envelope-related actions. """
        param = None
        if 'SEL' in args:
            param = self.song().view.selected_parameter
        elif 'VOL' in args:
            param = track.mixer_device.volume
        elif 'PAN' in args:
            param = track.mixer_device.panning
        elif 'SEND' in args:
            param = self._parent._track_actions.get_send_parameter(track, args.replace('SEND', '').strip())
        elif 'DEV' in args:
            arg_array = args.split()
            if len(arg_array) > 1:
                dev_array = self._parent.get_device_to_operate_on(track, arg_array[0], args.replace(arg_array[0], '').strip())
                if len(dev_array) == 2:
                    param_array = dev_array[1].strip().split()
                    param = None
                    if len(param_array) > 1:
                        param = self._parent._device_actions.get_banked_parameter(dev_array[0], param_array[0], param_array[1])
                    else:
                        param = self._parent._device_actions.get_bob_parameter(dev_array[0], param_array[0])
        return param
    
        
    def hide_envelopes(self, clip, track, xclip, ident, args):
        """ Hides the clip's envelope view. """
        if IS_LIVE_9_1:
            clip.view.hide_envelope()
            
            
    def quantize(self, clip, track, xclip, ident, args):
        """ 
        Quantizes notes or warp markers to the given quantization value, at the (optional) given strength and with the (optional) percentage of swing. 
        Can optionally be applied to specific notes or ranges of notes.
        """
        if IS_LIVE_9:
            args = args.strip()
            arg_array = args.split()
            array_offset = 0
            rate_to_apply = None
            # standard qntz to all
            if arg_array[0] in R_QNTZ_STATES:
                rate_to_apply = R_QNTZ_STATES[arg_array[0]]
            # qntz to specific note or note range
            elif arg_array[1] in R_QNTZ_STATES and clip.is_midi_clip:
                array_offset = 1
                rate_to_apply = R_QNTZ_STATES[arg_array[1]]
            if rate_to_apply:
                strength = 1.0
                swing_to_apply = 0.0
                current_swing = self.song().swing_amount
                if len(arg_array) > (1 + array_offset):
                    try: 
                        strength = float(arg_array[1 + array_offset]) / 100.0
                        if strength > 1.0 or strength < 0.0:
                            strength = 1.0
                    except: strength = 1.0
                if len(arg_array) > (2 + array_offset):
                    try: 
                        swing_to_apply = float(arg_array[2 + array_offset]) / 100.0
                        if swing_to_apply > 1.0 or swing_to_apply < 0.0:
                            swing_to_apply = 0.0
                    except: swing_to_apply = 0.0
                self.song().swing_amount = swing_to_apply
                # apply standard qntz to all
                if array_offset == 0:
                    clip.quantize(rate_to_apply, strength)
                # apply qntz to specific note or note range
                else:
                    note_range = self.get_note_range(arg_array[0])
                    for note in range(note_range[0], note_range[1]):
                        clip.quantize_pitch(note, rate_to_apply, strength)
                self.song().swing_amount = current_swing
                    
                
    def duplicate_clip_content(self, clip, track, xclip, ident, args):
        """ Duplicates all the content in a MIDI clip and doubles loop length. Will also zoom out to show entire loop if loop is on. """
        if IS_LIVE_9 and clip.is_midi_clip:
            try:
                clip.duplicate_loop()
            except: pass
            
            
    def delete_clip(self, clip, track, xclip, ident, args):
        """ Deletes the given clip. """
        if IS_LIVE_9:
            clip.canonical_parent.delete_clip()
                
            
    def duplicate_clip(self, clip, track, xclip, ident, args):
        """ Duplicates the given clip. This will overwrite clips if any exist in the slots used for duplication. """
        if IS_LIVE_9:
            try:
                track.duplicate_clip_slot(list(track.clip_slots).index(clip.canonical_parent))
            except: pass
            
            
    def chop_clip(self, clip, track, xclip, ident, args):
        """ Duplicates the clip the number of times specified and sets evenly distributed start points across all duplicates. This will overwrite clips if any exist in the slots used for duplication. """
        if IS_LIVE_9:
            args = args.strip()
            num_chops = 8       
            if args:
                try: num_chops = int(args)
                except: pass    
            slot_index = list(track.clip_slots).index(clip.canonical_parent)
            current_start = clip.start_marker
            chop_length = (clip.loop_end - current_start) / num_chops
            try:
                for index in range(num_chops - 1):
                    track.duplicate_clip_slot(slot_index + index)
                    dupe_start = (chop_length * (index + 1)) + current_start
                    dupe = track.clip_slots[slot_index + index + 1].clip
                    dupe.start_marker = dupe_start
                    dupe.loop_start = dupe_start
                    dupe.name = clip.name + '-' + str(index + 1)
            except: pass

                
    def split_clip(self, clip, track, xclip, ident, args):
        """ Duplicates the clip and sets each duplicate to have the length specified in args.  This will overwrite clips if any exist in the slots used for duplication. """
        if IS_LIVE_9:
            try:
                bar_arg = float(args)
                bar_length = (4.0 / clip.signature_denominator) * clip.signature_numerator
                split_size = bar_length * bar_arg
                num_splits = int(clip.length / split_size)
                if split_size * num_splits < clip.end_marker:
                    num_splits += 1
                if num_splits >= 2:
                    slot_index = list(track.clip_slots).index(clip.canonical_parent)
                    current_start = clip.start_marker
                    actual_end = clip.end_marker
                    for index in range(num_splits):
                        track.duplicate_clip_slot(slot_index + index) 
                        dupe_start = (split_size * index) + current_start
                        dupe_end = dupe_start + split_size
                        if dupe_end > actual_end:
                            dupe_end = actual_end
                        dupe = track.clip_slots[slot_index + index + 1].clip
                        dupe.loop_end = dupe_end
                        dupe.start_marker = dupe_start
                        dupe.loop_start = dupe_start
                        dupe.name = clip.name + '-' + str(index + 1)    
            except: pass
            

    def do_clip_loop_action(self, clip, track, xclip, ident, args):
        """ Handle clip loop actions  """
        args = args.strip()
        if args == '' or args in KEYWORDS:
            self.set_loop_on_off(clip, args)
        else:
            if args.startswith('START'):
                self.adjust_loop_start(clip, track, xclip, ident, args.replace('START', '', 1).strip())
            elif args.startswith('END'):
                self.adjust_loop_end(clip, track, xclip, ident, args.replace('END', '', 1).strip())             
            elif args == 'SHOW' and IS_LIVE_9:
                clip.view.show_loop()           
            if clip.looping:
                clip_stats = self.get_clip_stats(clip)
                new_start = clip.loop_start  
                new_end = clip.loop_end  
                if args.startswith(('<', '>')):
                    self.move_clip_loop_by_factor(clip, args, clip_stats)
                    return()
                elif args == 'RESET':
                    new_start = 0.0
                    new_end = clip_stats['real_end']
                elif args.startswith('*'):
                    try:
                        new_end = (clip.loop_end - clip_stats['loop_length']) + (clip_stats['loop_length'] * float(args[1:]))
                    except: pass
                else:
                    self.do_loop_set(clip, args, clip_stats)
                    return()
                self.set_new_loop_position(clip, new_start, new_end, clip_stats)
                    
                    
    def set_loop_on_off(self, clip, value = None):
        """ Toggles or turns clip loop on/off """
        if value in KEYWORDS:
            clip.looping = KEYWORDS[value]
        else:
            clip.looping = not(clip.looping)
            
            
    def move_clip_loop_by_factor(self, clip, args, clip_stats):
        """ Move clip loop by its length or by a specified factor """
        factor = clip_stats['loop_length']
        if args == '<':
            factor = -(factor)
        if len(args) > 1:
            factor = self._parent.get_adjustment_factor(args, True)
        new_end = clip.loop_end + factor
        new_start = clip.loop_start + factor
        if new_start < 0.0:
            new_end = new_end - new_start
            new_start = 0.0
        self.set_new_loop_position(clip, new_start, new_end, clip_stats)
        
        
    def do_loop_set(self, clip, args, clip_stats):
        """ Set loop length and (if clip is playing) position, quantizes to 1/4 by default or bar if specified """
        try:
            qntz = False
            if 'B' in args:
                qntz = True
            bars_to_loop = float(args.strip('B'))    
            bar = (4.0 / clip.signature_denominator) * clip.signature_numerator
            start = clip.loop_start
            if clip.is_playing:
                start = round(clip.playing_position)
                if qntz:
                    distance = start % bar
                    if distance <= bar / 2:
                        start = start - distance
                    else:
                        start = start + (bar - distance)                
            end = start + (bar * bars_to_loop)
            self.set_new_loop_position(clip, start, end, clip_stats)
        except: pass
        
        
    def set_new_loop_position(self, clip, new_start, new_end, clip_stats):
        """ For use with other clip loop actions, ensures that loop settings are within range and applies in correct order """
        if new_end <= clip_stats['real_end'] and new_start >= 0:
            if new_end > clip.loop_start:
                clip.loop_end = new_end
                clip.loop_start = new_start
            else:
                clip.loop_start = new_start
                clip.loop_end = new_end
        
                
    def do_clip_note_action(self, clip, track, xclip, ident, args):
        """ Handle clip note actions """
        if clip.is_audio_clip:
            return()
        note_data = self.get_notes_to_operate_on(clip, args.strip())
        if note_data['notes_to_edit']:
            if note_data['args'] == '' or note_data['args'] in KEYWORDS:
                self.set_notes_on_off(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'REV':
                self.do_note_reverse(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'INV':
                self.do_note_invert(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'COMP':
                self.do_note_compress(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'EXP':
                self.do_note_expand(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'SCRN':
                self.do_pitch_scramble(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'SCRP':
                self.do_position_scramble(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'CMB':
                self.do_note_combine(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'SPLIT':
                self.do_note_split(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'].startswith(('GATE <', 'GATE >')):
                self.do_note_gate_adjustment(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'].startswith(('NUDGE <', 'NUDGE >')):
                self.do_note_nudge_adjustment(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] == 'DEL':
                self.do_note_delete(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'] in ('VELO <<', 'VELO >>'): 
                self.do_note_crescendo(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'].startswith('VELO'):
                self.do_note_velo_adjustment(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])
            elif note_data['args'].startswith('SEMI'):
                self.do_note_action_pitch_adjustment(clip, note_data['args'], note_data['notes_to_edit'], note_data['other_notes'])



    class InternalMidiNote(object):
        """Compatibility class analog of the Live 11 API's MidiNote class, to support Live 10."""
        # Note tuple n[0]..n[4] from get_selected_notes():
        pitch = 0
        start_time = 0.0
        duration = 0.0
        velocity = 64
        mute = False
        # Live 11 only: (for reference)
        note_id = 0
        probability = 1.0
        release_velocity = 64.0
        velocity_deviation = 0.0

        def to_tuple(self):
            return (self.pitch, self.start_time, self.duration, self.velocity, self.mute)
        
        def from_tuple(self, n):
            self.pitch = n[0]
            self.start_time = n[1]
            self.duration = n[2]
            self.velocity = n[3]
            self.mute = n[4]
            return self
        
        def to_live11_spec(self):
            # Note: in Live 11, the returned note can not be modified.
            if not IS_LIVE_11:
                return None
            return Live.Clip.MidiNoteSpecification(
                pitch=self.pitch, start_time=self.start_time,
                duration=self.duration, velocity=self.velocity,
                mute=self.mute, probability=self.probability,
                velocity_deviation=self.velocity_deviation,
                release_velocity=self.release_velocity)

        def from_note(self, n):
            """Sets values from an existing InternalMidiNote or Live11 MidiNote"""
            self.pitch = n.pitch
            self.start_time = n.start_time
            self.duration = n.duration
            self.velocity = n.velocity
            self.mute = n.mute
            self.probability = n.probability
            self.velocity_deviation = n.velocity_deviation
            self.release_velocity = n.release_velocity
            return self


    def set_notes_on_off(self, clip, args, notes_to_edit, other_notes): 
        """ Toggles or turns note mute on/off """
        edited_notes = []
        for n in notes_to_edit:
            new_mute = False
            if args == '':
                n.mute = not(n.mute)
            elif args == 'ON':
                n.mute = True
            else:
                n.mute = False
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_pitch_adjustment(self, clip, factor): 
        """ Adjust note pitch. This isn't a note action, it's called via Clip Semi """
        edited_notes = []
        note_data = self.get_notes_to_operate_on(clip)
        if not note_data['notes_to_edit']:
            return
        for n in note_data['notes_to_edit']:
            n.pitch += factor
            if n.pitch > 127:
                n.pitch = 127
            if n.pitch < 0:
                n.pitch = 0
            edited_notes.append(n)
        self.write_all_notes(clip, edited_notes, note_data['other_notes'])


    def do_note_action_pitch_adjustment(self, clip, args, notes_to_edit, other_notes): 
        """ Adjust note pitch. Like do_note_pitch_adjustment, but a note action"""
        # Also supports specifying specific notes instead of relative notes.
        edited_notes = []
        args = args.replace('SEMI ', '')
        args = args.strip()
        for n in notes_to_edit:
            if args.startswith(('<', '>')):
                factor = self._parent.get_adjustment_factor(args)
                n.pitch += factor
            else:
                (n.pitch, unused) = self.get_note_range(args)
            if n.pitch > 127:
                n.pitch = 127
            if n.pitch < 0:
                n.pitch = 0
            edited_notes.append(n) 
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_gate_adjustment(self, clip, args, notes_to_edit, other_notes): 
        """ Adjust note gate """
        edited_notes = []
        factor = self._parent.get_adjustment_factor(args.split()[1], True)
        for n in notes_to_edit:
            n.duration += (factor * 0.03125)
            if n.start_time + n.duration > clip.loop_end:
                n.duration = clip.loop_end - n.start_time
            if n.duration < 0.03125:
                n.duration = 0.03125
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_nudge_adjustment(self, clip, args, notes_to_edit, other_notes): 
        """ Adjust note position """
        edited_notes = []
        factor = self._parent.get_adjustment_factor(args.split()[1], True)
        for n in notes_to_edit:
            n.start_time += (factor * 0.03125)
            if n.start_time + n.duration > clip.loop_end:
                n.start_time = clip.loop_end - n.duration
            if n.start_time < 0.0:
                n.start_time = 0.0
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_velo_adjustment(self, clip, args, notes_to_edit, other_notes): 
        """ Adjust/set/randomize note velocity """
        edited_notes = []
        args = args.replace('VELO ', '')
        args = args.strip()
        for n in notes_to_edit:
            if args == 'RND':
                n.velocity = Live.Application.get_random_int(0, 128)
            elif args.startswith(('<', '>')):
                factor = self._parent.get_adjustment_factor(args)
                n.velocity += factor
            else:
                try:
                    n.velocity = int(args)
                except: pass
            if n.velocity > 127:
                n.velocity = 127
            elif n.velocity < 0:
                n.velocity = 0
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)              


    def do_pitch_scramble(self, clip, args, notes_to_edit, other_notes):
        """ Scrambles the pitches in the clip, but maintains rhythm. """
        if IS_LIVE_9:
            edited_notes = []
            pitches = [n.pitch for n in notes_to_edit]
            random.shuffle(pitches)
            i = 0
            for n in notes_to_edit:
                n.pitch = pitches[i]
                edited_notes.append(n)
                i += 1
            if edited_notes:
                self.write_all_notes(clip, edited_notes, other_notes)       


    def do_position_scramble(self, clip, args, notes_to_edit, other_notes):
        """ Scrambles the position of notes in the clip, but maintains pitches. """
        if IS_LIVE_9:
            edited_notes = []
            positions = [n.start_time for n in notes_to_edit]
            random.shuffle(positions)
            i = 0
            for n in notes_to_edit:
                n.start_time = positions[i]
                edited_notes.append(n)
                i += 1
            if edited_notes:
                self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_reverse(self, clip, args, notes_to_edit, other_notes): 
        """ Reverse the position of notes """
        edited_notes = []
        for n in notes_to_edit:
            n.start_time = abs(clip.loop_end - (n.start_time + n.duration) + clip.loop_start)
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_invert(self, clip, args, notes_to_edit, other_notes): 
        """ Inverts the pitch of notes. """
        edited_notes = []
        for n in notes_to_edit:
            n.pitch = 127 - n.pitch
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_compress(self, clip, args, notes_to_edit, other_notes): 
        """ Compresses the position and duration of notes by half. """
        edited_notes = []
        for n in notes_to_edit:
            n.start_time /= 2
            n.duration /= 2
            n.duration = max(n.duration, 0.03215)
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_expand(self, clip, args, notes_to_edit, other_notes): 
        """ Expands the position and duration of notes by 2. """
        edited_notes = []
        for n in notes_to_edit:
            n.start_time *= 2
            n.duration *= 2
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)


    def do_note_combine(self, clip, args, notes_to_edit, other_notes):
        """ Combine each consecutive set of 2 notes. (inverse of split) """
        edited_notes = []
        removed_notes = [] 
        current = None
        for next in sorted(notes_to_edit, key=lambda note: (note.pitch, note.start_time)):
            if not current:
                current = next
            elif (current.pitch == next.pitch and
                  current.start_time + current.duration == next.start_time):
                current.duration += next.duration
                edited_notes.append(current)
                removed_notes.append(next)
                current = None
            else:
                edited_notes.append(current)
                current = next
        if current:
            edited_notes.append(current)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes,
                                 removed_notes=removed_notes)


    def do_note_split(self, clip, args, notes_to_edit, other_notes):
        """ Split notes into 2 equal parts """
        edited_notes = []
        new_notes = []
        for n in notes_to_edit:
            if n.duration / 2 < 0.03125:
                return
            else:
                n.duration /= 2
                edited_notes.append(n)
                new_note = self.InternalMidiNote().from_note(n)
                new_note.start_time += n.duration
                new_notes.append(new_note)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes, new_notes=new_notes)
            
    
    def do_note_crescendo(self, clip, args, notes_to_edit, other_notes):
        """ Applies crescendo/decrescendo to notes """
        edited_notes = []; last_pos = -1; pos_index = 0; new_pos = -1; new_index = 0
        sorted_notes = sorted(notes_to_edit, key=lambda note: note.start_time, reverse=False)
        if args == 'VELO <<':
            sorted_notes = sorted(notes_to_edit, key=lambda note: note.start_time, reverse=True)
        for n in sorted_notes:
            if n.start_time != last_pos:
                last_pos = n.start_time
                pos_index += 1
        for n in sorted_notes:
            if n.start_time != new_pos:
                new_pos = n.start_time
                new_index += 1
            n.velocity =  ((128 / pos_index) * new_index) - 1
            edited_notes.append(n)
        if edited_notes:
            self.write_all_notes(clip, edited_notes, other_notes)
            
            
    def do_note_delete(self, clip, args, notes_to_edit, other_notes): 
        """ Delete notes """
        self.write_all_notes(clip, [], other_notes, new_notes=[],
                             removed_notes=notes_to_edit)

        
    def get_clip_stats(self, clip):
        """ Get real length and end of looping clip """
        clip.looping = 0
        length = clip.length
        end = clip.loop_end
        clip.looping = 1
        loop_length = clip.loop_end - clip.loop_start
        return {'clip_length' : length, 'real_end' : end, 'loop_length' : loop_length}  


    def get_notes_to_operate_on(self, clip, args = None):
        """ Get notes within loop braces to operate on """
        notes_to_edit = [] 
        new_args = None
        note_range = (0, 128)
        pos_range = (clip.loop_start, clip.loop_end)
        if args:
            new_args = [a.strip() for a in args.split()]
            note_range = self.get_note_range(new_args[0])
            new_args.remove(new_args[0])
            if new_args and '@' in new_args[0]:
                pos_range = self.get_pos_range(clip, new_args[0])
                new_args.remove(new_args[0])
            new_args = " ".join(new_args)

        clip.select_all_notes()
        if IS_LIVE_11:
            original_notes = clip.get_selected_notes_extended()
        else:
            original_notes = []
            for n in clip.get_selected_notes():
                original_notes.append(self.InternalMidiNote().from_tuple(n))
        clip.deselect_all_notes()

        other_notes = []
        for n in original_notes:
            if (n.pitch in range(note_range[0], note_range[1]) and
                n.start_time < pos_range[1] and n.start_time >= pos_range[0]):
                notes_to_edit.append(n)
            else:
                other_notes.append(n)
        return {'notes_to_edit' : notes_to_edit,
                'other_notes' : other_notes, 'args' : new_args}
    
    
    def get_pos_range(self, clip, string):
        """ Get note position or range to operate on """
        pos_range = (clip.loop_start, clip.loop_end)
        user_range = string.split('-')
        try: start = float(user_range[0].replace('@', ''))
        except: start = None
        if start != None and start >= 0.0:
            pos_range = (start, start)
            if len(user_range) > 1:
                try: end = float(user_range[1])
                except: end = None
                if end != None:
                    pos_range = (start, end)
        return pos_range
                
        
    def get_note_range(self, string):
        """ Get note lane or range to operate on """
        note_range = (0,128)
        string = string.replace('NOTES', '')
        if len(string) > 1:
            int_range = self.get_note_range_from_string(string)
            if int_range:
                note_range = int_range
            else:
                start_note_name = self.get_note_name_from_string(string)
                start_note_num = self.string_to_note(start_note_name)
                note_range = (start_note_num, start_note_num + 1)
                string = string.replace(start_note_name, '').strip()
                if len(string) > 1 and string.startswith('-'):
                    string = string[1:]
                    end_note_name = self.get_note_name_from_string(string)
                    end_note_num = self.string_to_note(end_note_name)
                    if end_note_num > start_note_num:
                        note_range = (start_note_num, end_note_num + 1)
        return note_range
    
    
    def get_note_range_from_string(self, string):
        """ Attempt to get note range (specified in ints) from string and return it or None if not specified or invalid. """
        result = None
        int_split = string.split('-')
        try: 
            start = int(int_split[0])
            end = start + 1
            if(len(int_split) > 1):
                end = int(int_split[1]) + 1
            if start < end and start in range(128) and end in range(129):
                result = (start, end)
            else:
                result = None
        except: result = None
        return result
    
    
    def get_note_name_from_string(self, string):
        """ Get the first note name specified in the given string. """
        result = None
        if len(string) >= 2:
            result = string[0:2].strip() 
            if (result.endswith('#') or result.endswith('-')) and len(string) >= 3:
                result = string[0:3].strip()
                if result.endswith('-') and len(string) >= 4:
                    result = string[0:4].strip()
        return result
                

    def string_to_note(self, string):
        """ Get note value from string """
        converted_note = None
        base_note = None
        octave = None
        for s in string:
            if s in NOTE_NAMES:
                base_note = NOTE_NAMES.index(s)
            if base_note != None and s == '#':
                base_note += 1
        if base_note != None:
            for o in OCTAVE_NAMES:
                if o in string:
                    base_note = base_note + (OCTAVE_NAMES.index(o) * 12)
                    break
        if base_note in range (128):
            converted_note = base_note
        return converted_note


    # In live 11 we need to specify which notes to add, remove, or modify.
    # In live 10 we only specify a set of notes to replace the existing ones.
    # In this case, other_notes represents the clip notes that were not
    # selected in a NOTES range selector.
    def write_all_notes(self, clip, edited_notes, other_notes,
                        new_notes=None, removed_notes=None):
        """ Writes notes to clip """
        self._parent.log_message(
            "Writing {0} edited notes, {1} unmodified notes, {2} new notes, {3} removed notes.".format(
                len(edited_notes), len(other_notes),
                len(new_notes if new_notes else []),
                len(removed_notes if removed_notes else [])))

        if IS_LIVE_11:
            # Remove, update, then add must be done in that order, or we risk
            # having modifications rejected due to temporarily overlapping notes.
            # However, after a note has been removed, it must not be sent into a future
            # update operation or ableton will crash the script.
            if removed_notes:
                clip.remove_notes_by_id([n.note_id for n in removed_notes])
            if edited_notes:
                clip.deselect_all_notes()
                edited_notes_vector = clip.get_selected_notes_extended()
                edited_notes_vector.extend(edited_notes)
                clip.apply_note_modifications(edited_notes_vector)
            if new_notes:
                clip.add_new_notes(tuple([note.to_live11_spec() for note in new_notes]))
            # In Live 11 we can just ignore other_notes since they are unmodified.
            clip.deselect_all_notes()
        else:
            if other_notes:
                edited_notes.extend(other_notes)
            if new_notes:
                edited_notes.extend(new_notes)
            edited_tuples = []
            for note in edited_notes:
                edited_tuples.append(note.to_tuple())
            # In Live 10 we can just ignore removed_notes since they're missing
            # from edited_notes, other_notes, and new_notes.
            clip.select_all_notes()
            clip.replace_selected_notes(tuple(edited_tuples))
            clip.deselect_all_notes()


# local variables:
# tab-width: 4
