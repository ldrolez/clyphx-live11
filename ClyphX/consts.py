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

#--- NOTE: Action names and their corresponding values can't contain a '/' or '-' within the first four chars like this 'EX/ONE', but 'EXMP/ONE' is okay. 

import Live 

app = Live.Application.get_application()
IS_LIVE_10 = app.get_major_version() == 10
IS_LIVE_9 = app.get_major_version() >= 9
IS_LIVE_9_1 = IS_LIVE_10 or (IS_LIVE_9 and app.get_minor_version() >= 1)
IS_LIVE_9_5 = IS_LIVE_10 or (IS_LIVE_9 and app.get_minor_version() >= 5)

GLOBAL_ACTIONS = {
    'ASN' : 'do_variable_assignment',
    'ADDAUDIO' : 'create_audio_track',
    'ADDMIDI' : 'create_midi_track',
    'INSAUDIO' : 'insert_and_configure_audio_track',
    'INSMIDI' : 'insert_and_configure_midi_track',
    'ADDRETURN' : 'create_return_track',
    'ADDSCENE' : 'create_scene',
    'DELSCENE' : 'delete_scene',
    'DUPESCENE' : 'duplicate_scene',
    'LOADDEV' : 'load_device',
    'LOADM4L' : 'load_m4l',
    'SWAP' : 'swap_device_preset',
    'SREC' : 'set_session_record',
    'SRECFIX' : 'trigger_session_record',
    'SATM' : 'set_session_automation_record',
    'B2A' : 'set_back_to_arrange',
    'RPT' : 'set_note_repeat',
    'SWING' : 'adjust_swing',
    'BPM' : 'adjust_tempo',  
    'DEVFIRST' : 'move_to_first_device', 
    'DEVLAST' : 'move_to_last_device', 
    'DEVLEFT' : 'move_to_prev_device', 
    'DEVRIGHT' : 'move_to_next_device', 
    'FOCBRWSR' : 'focus_browser',
    'FOCDETAIL' : 'focus_detail',
    'FOCMAIN' : 'focus_main',
    'GQ' : 'adjust_global_quantize',
    'GRV' : 'adjust_groove',
    'HZOOM' : 'adjust_horizontal_zoom',
    'VZOOM' : 'adjust_vertical_zoom',
    'UP' : 'move_up',
    'DOWN' : 'move_down',
    'LEFT' : 'move_left',
    'RIGHT' : 'move_right',
    'LOOP' : 'do_loop_action',
    'LOC' : 'do_locator_action',
    'LOCLOOP' : 'do_locator_loop_action',
    'METRO' : 'set_metronome', 
    'MIDI': 'send_midi_message',
    'OVER' : 'set_overdub',    
    'PIN' : 'set_punch_in',
    'POUT' : 'set_punch_out',
    'REC' : 'set_record',
    'REDO' : 'set_redo',
    'UNDO' : 'set_undo',
    'RESTART' : 'restart_transport',
    'RQ' : 'adjust_record_quantize',
    'RTRIG': 'retrigger_recording_clips',
    'SIG' : 'adjust_time_signature',
    'SCENE' : 'set_scene',
    'SHOWCLIP' : 'show_clip_view',
    'SHOWDEV' : 'show_track_view',
    'SHOWDETAIL' : 'show_detail_view',
    'TGLBRWSR': 'toggle_browser',
    'TGLDETAIL': 'toggle_detail_view',
    'TGLMAIN': 'toggle_main_view',
    'STOPALL' : 'set_stop_all',
    'SETCONT' : 'set_continue_playback',
    'SETLOC' : 'set_locator',
    'SETSTOP' : 'set_stop_transport',
    'SETFOLD' : 'set_fold_all',
    'SETJUMP' : 'set_jump_all',
    'TAPBPM' : 'set_tap_tempo',
    'UNARM' : 'set_unarm_all',
    'UNMUTE' : 'set_unmute_all',
    'UNSOLO' : 'set_unsolo_all',
    'MAKE_DEV_DOC': 'make_instant_mapping_docs'}

TRACK_ACTIONS = {
    'ARM' : 'set_arm', 
    'MUTE' : 'set_mute', 
    'SOLO' : 'set_solo',
    'MON' : 'set_monitor',
    'XFADE' : 'set_xfade',
    'SEL' : 'set_selection',
    'ADDCLIP' : 'create_clip',
    'DEL' : 'delete_track',
    'DELDEV' : 'delete_device',
    'DUPE' : 'duplicate_track',
    'FOLD' : 'set_fold',
    'PLAY' : 'set_play',
    'PLAYL' : 'set_play_w_legato',
    'PLAYQ' : 'set_play_w_force_qntz',
    'PLAYLQ' : 'set_play_w_force_qntz_and_legato',
    'STOP' : 'set_stop',
    'JUMP' : 'set_jump',
    'VOL' : 'adjust_volume',
    'PAN' : 'adjust_pan',
    'SEND' : 'adjust_sends',
    'CUE' : 'adjust_preview_volume',
    'XFADER' : 'adjust_crossfader',
    'IN' : 'adjust_input_routing',
    'INSUB' : 'adjust_input_sub_routing',
    'OUT' : 'adjust_output_routing',
    'OUTSUB' : 'adjust_output_sub_routing',
    'NAME' : 'set_name',
    'RENAMEALL' : 'rename_all_clips'}  

CLIP_ACTIONS = {
    'CENT' : 'adjust_detune',
    'SEMI' : 'adjust_transpose',
    'GAIN' : 'adjust_gain',
    'CUE' : 'adjust_cue_point', 
    'END' : 'adjust_end',
    'START' : 'adjust_start',
    'GRID' : 'adjust_grid_quantization',
    'TGRID' : 'set_triplet_grid',
    'ENVINS' : 'insert_envelope',
    'ENVCLR' : 'clear_envelope',
    'ENVCAP' : 'capture_to_envelope',
    'ENVSHOW' : 'show_envelope',
    'ENVHIDE' : 'hide_envelopes',
    'QNTZ' : 'quantize',
    'EXTEND' : 'duplicate_clip_content',
    'DEL' : 'delete_clip',
    'DUPE' : 'duplicate_clip',
    'CHOP' : 'chop_clip',
    'SPLIT' : 'split_clip',
    'WARPMODE' : 'adjust_warp_mode',
    'LOOP' : 'do_clip_loop_action',
    'SIG' : 'adjust_time_signature',
    'WARP' : 'set_warp',
    'NAME' : 'set_clip_name'} 

DEVICE_ACTIONS = {
    'CSEL' : 'adjust_selected_chain',
    'CS' : 'adjust_chain_selector', 
    'RESET' : 'reset_params', 
    'RND' : 'randomize_params', 
    'SEL' : 'select_device',
    'SET' : 'set_all_params',
    'P1' : 'adjust_best_of_bank_param', 
    'P2' : 'adjust_best_of_bank_param', 
    'P3' : 'adjust_best_of_bank_param', 
    'P4' : 'adjust_best_of_bank_param',
    'P5' : 'adjust_best_of_bank_param', 
    'P6' : 'adjust_best_of_bank_param', 
    'P7' : 'adjust_best_of_bank_param', 
    'P8' : 'adjust_best_of_bank_param', 
    'B1' : 'adjust_banked_param', 
    'B2' : 'adjust_banked_param', 
    'B3' : 'adjust_banked_param', 
    'B4' : 'adjust_banked_param', 
    'B5' : 'adjust_banked_param', 
    'B6' : 'adjust_banked_param', 
    'B7' : 'adjust_banked_param', 
    'B8' : 'adjust_banked_param'}

if IS_LIVE_9:
    DR_ACTIONS = {
        'SCROLL' : 'scroll_selector',
        'UNMUTE' : 'unmute_all',
        'UNSOLO' : 'unsolo_all'
    }

LOOPER_ACTIONS = {
    'LOOPER' : 'set_looper_on_off', 
    'REV' : 'set_looper_rev', 
    'OVER' : 'set_looper_state',
    'PLAY' : 'set_looper_state', 
    'REC' : 'set_looper_state', 
    'STOP': 'set_looper_state'}   

KEYWORDS = {'ON' : 1, 'OFF' : 0} 

NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVE_NAMES = ['-2', '-1', '0', '1', '2', '3', '4', '5', '6', '7', '8']

GQ_STATES = {'NONE' : 0, '8 BARS' : 1, '4 BARS' : 2, '2 BARS' : 3, '1 BAR' : 4, '1/2' : 5, '1/2T' : 6, '1/4' : 7, '1/4T' : 8, '1/8' : 9, '1/8T' : 10, '1/16' : 11, '1/16T' : 12, '1/32' : 13}
RQ_STATES = {'NONE' : 0, '1/4' : 1, '1/8' : 2, '1/8T' : 3, '1/8 + 1/8T' : 4, '1/16' : 5, '1/16T' : 6, '1/16 + 1/16T' : 7, '1/32' : 8}

XFADE_STATES = {'A': 0, 'OFF' : 1, 'B' : 2}
MON_STATES = {'IN' : 0, 'AUTO' : 1, 'OFF' : 2}

LOOPER_STATES = {'STOP': 0.0, 'REC' : 1.0, 'PLAY' : 2.0, 'OVER' : 3.0}

if IS_LIVE_9:
    R_QNTZ_STATES = {'1/4' : Live.Song.RecordingQuantization.rec_q_quarter, '1/8' : Live.Song.RecordingQuantization.rec_q_eight, 
                   '1/8T' : Live.Song.RecordingQuantization.rec_q_eight_triplet, '1/8 + 1/8T' : Live.Song.RecordingQuantization.rec_q_eight_eight_triplet, '1/16' : Live.Song.RecordingQuantization.rec_q_sixtenth, 
                   '1/16T' : Live.Song.RecordingQuantization.rec_q_sixtenth_triplet, '1/16 + 1/16T' : Live.Song.RecordingQuantization.rec_q_sixtenth_sixtenth_triplet, 
                   '1/32' : Live.Song.RecordingQuantization.rec_q_thirtysecond}
    
    CLIP_GRID_STATES = {'OFF' : Live.Clip.GridQuantization.no_grid, '8 BARS' : Live.Clip.GridQuantization.g_8_bars, 
                        '4 BARS' : Live.Clip.GridQuantization.g_4_bars, '2 BARS' : Live.Clip.GridQuantization.g_2_bars,
                        '1 BAR' : Live.Clip.GridQuantization.g_bar, '1/2' : Live.Clip.GridQuantization.g_half,
                        '1/4' : Live.Clip.GridQuantization.g_quarter, '1/8' : Live.Clip.GridQuantization.g_eighth, 
                        '1/16' : Live.Clip.GridQuantization.g_sixteenth, '1/32' : Live.Clip.GridQuantization.g_thirtysecond}
    
    REPEAT_STATES = {'OFF' : 1.0, '1/4' : 1.0, '1/4T' : 0.666666666667, '1/8' : 0.5, '1/8T' : 0.333333333333, '1/16' : 0.25, '1/16T' : 0.166666666667, '1/32' : 0.125, '1/32T' : 0.0833333333333}
    
    WARP_MODES = {'BEATS': 0, 'TONES': 1, 'TEXTURE': 2, 'RE-PITCH': 3, 'COMPLEX': 4, 'COMPLEX PRO': 6}
    
    AUDIO_DEVS = {u'SIMPLE DELAY': u'Simple Delay', u'OVERDRIVE': u'Overdrive', u'LOOPER': u'Looper', u'AUTO FILTER': u'Auto Filter', u'EXTERNAL AUDIO EFFECT': u'External Audio Effect', u'SATURATOR': u'Saturator', u'PHASER': u'Phaser', u'VINYL DISTORTION': u'Vinyl Distortion', u'DYNAMIC TUBE': u'Dynamic Tube', u'BEAT REPEAT': u'Beat Repeat', u'MULTIBAND DYNAMICS': u'Multiband Dynamics', u'CABINET': u'Cabinet', u'AUDIO EFFECT RACK': u'Audio Effect Rack', u'FLANGER': u'Flanger', u'GATE': u'Gate', u'REVERB': u'Reverb', u'GRAIN DELAY': u'Grain Delay', u'REDUX': u'Redux', u'PING PONG DELAY': u'Ping Pong Delay', u'SPECTRUM': u'Spectrum', u'COMPRESSOR': u'Compressor', u'VOCODER': u'Vocoder', u'AMP': u'Amp', u'GLUE COMPRESSOR': u'Glue Compressor', u'EROSION': u'Erosion', u'EQ THREE': u'EQ Three', u'EQ EIGHT': u'EQ Eight', u'RESONATORS': u'Resonators', u'FREQUENCY SHIFTER': u'Frequency Shifter', u'AUTO PAN': u'Auto Pan', u'CHORUS': u'Chorus', u'LIMITER': u'Limiter', u'CORPUS': u'Corpus', u'FILTER DELAY': u'Filter Delay', u'UTILITY': u'Utility'}
    
    INS_DEVS = {u'TENSION': u'Tension', u'EXTERNAL INSTRUMENT': u'External Instrument', u'ELECTRIC': u'Electric', u'INSTRUMENT RACK': u'Instrument Rack', u'DRUM RACK': u'Drum Rack', u'COLLISION': u'Collision', u'IMPULSE': u'Impulse', u'SAMPLER': u'Sampler', u'OPERATOR': u'Operator', u'ANALOG': u'Analog', u'SIMPLER': u'Simpler'}
    
    MIDI_DEVS = {u'NOTE LENGTH': u'Note Length', u'CHORD': u'Chord', u'RANDOM': u'Random', u'MIDI EFFECT RACK': u'MIDI Effect Rack', u'SCALE': u'Scale', u'PITCH': u'Pitch', u'ARPEGGIATOR': u'Arpeggiator', u'VELOCITY': u'Velocity'}

# local variables:
# tab-width: 4
