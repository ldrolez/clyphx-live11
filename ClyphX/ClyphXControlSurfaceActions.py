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
from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent 
from _Framework.MixerComponent import MixerComponent
from _Framework.DeviceComponent import DeviceComponent
from consts import *
from ClyphXPushActions import ClyphXPushActions
from ClyphXPXTActions import ClyphXPXTActions
from ClyphXMXTActions import ClyphXMXTActions
from ClyphXArsenalActions import ClyphXArsenalActions
from ableton.v2.control_surface import ControlSurface as CS

    
class ClyphXControlSurfaceActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Actions related to control surfaces '
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
        self._parent = parent
	self._push_actions = ClyphXPushActions(parent)
	self._pxt_actions = ClyphXPXTActions(parent)
	self._mxt_actions = ClyphXMXTActions(parent)
	self._arsenal_actions = ClyphXArsenalActions(parent)
	self._scripts = {}
	
	
    def disconnect(self):
	self._scripts = {}
	self._parent = None
	self._arsenal_actions = None
	self._push_actions = None
	self._pxt_actions = None
	self._mxt_actions = None
	ControlSurfaceComponent.disconnect(self)		
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass    
    
    
    def connect_script_instances(self, instanciated_scripts):
	""" Build dict of connected scripts and their components, doesn't work with non-Framework scripts, but does work with User Remote Scripts """
	instanciated_scripts = self._parent._control_surfaces()
	self._scripts = {}
	for index in range (len(instanciated_scripts)):
	    script = instanciated_scripts[index]
	    self._scripts[index] = {'script' : script, 'name' : None, 'repeat' : False, 'mixer' : None, 'device' : None, 'last_ring_pos' : None,
	                            'session' : None, 'track_link' : False, 'scene_link' : False, 'centered_link' : False, 'color' : False}
	    script_name = script.__class__.__name__
	    if isinstance (script, (ControlSurface, CS)):
		if script_name == 'GenericScript':
		    script_name = script._suggested_input_port
		if script_name.startswith('Arsenal'):
                    self._arsenal_actions.set_script(script)
		if script_name == 'Push':
		    self._push_actions.set_script(script)
		if script_name.startswith('PXT_Live'):
		    self._pxt_actions.set_script(script)
		if script_name == 'MXT_Live':
		    self._mxt_actions.set_script(script)
		if not script_name.startswith('ClyphX'):
		    if script._components == None:
			return 
		    else:
			self._scripts[index]['name'] = script_name.upper()
			for c in script.components:
			    if isinstance (c, SessionComponent):
				self._scripts[index]['session'] = c
				if script_name.startswith('APC'):
				    self._scripts[index]['color'] = {'GREEN' : (1, 2), 'RED' : (3, 4), 'AMBER' : (5, 6)}
				    self._scripts[index]['metro'] = {'controls' : c._stop_track_clip_buttons, 'component' : None, 'override' : None}
				if script_name == 'Launchpad':
				    self._scripts[index]['color'] = {'GREEN' : (52, 56), 'RED' : (7, 11), 'AMBER' : (55, 59)}
				    self._scripts[index]['metro'] = {'controls' : script._selector._side_buttons, 'component' : None, 'override' : script._selector}
			    if isinstance (c, MixerComponent):
				self._scripts[index]['mixer'] = c
			    if isinstance (c, DeviceComponent):
				self._scripts[index]['device'] = c
			if script_name == 'Push':
			    self._scripts[index]['session'] = script._session_ring
			    self._scripts[index]['mixer'] = script._mixer
			    self._scripts[index]['device'] = script._device_component
                        elif script_name == 'Push2':
                            # hackish way to delay for Push2 init, using monkey patching doesn't work for some reason
                            self.canonical_parent.schedule_message(50, partial(self._handle_push2_init, index))
	    elif script_name == 'Nocturn':
		self._scripts[index]['device'] = script.device_controller
		script.device_controller.canonical_parent = script
	

    def _handle_push2_init(self, index):
        script = self._scripts[index]['script']
        self._push_actions.set_script(script, is_push2=True)
        self._scripts[index]['session'] = script._session_ring
	self._scripts[index]['device'] = script._device_component


    def dispatch_push_action(self, track, xclip, ident, action, args): 
	""" Dispatch Push-related actions to PushActions. """
	if self._push_actions:
	    self._push_actions.dispatch_action(track, xclip, ident, action, args)
	    
	    
    def dispatch_pxt_action(self, track, xclip, ident, action, args): 
	""" Dispatch PXT-related actions to PXTActions. """
	if self._pxt_actions:
	    self._pxt_actions.dispatch_action(track, xclip, ident, action, args)
	    
	    
    def dispatch_mxt_action(self, track, xclip, ident, action, args): 
	""" Dispatch MXT-related actions to MXTActions. """
	if self._mxt_actions:
	    self._mxt_actions.dispatch_action(track, xclip, ident, action, args)


    def dispatch_arsenal_action(self, track, xclip, ident, action, args):
        """ Dispatch Arsenal-related actions to ArsenalActions. """
	if self._arsenal_actions:
	    self._arsenal_actions.dispatch_action(track, xclip, ident, action, args)
    
	
    def dispatch_cs_action(self, track, xclip, ident, action, args):  
	""" Dispatch appropriate control surface actions """
	script = self._get_script_to_operate_on(action)
	if script != None:
	    if 'METRO ' in args and self._scripts[script].has_key('metro'):
		self.handle_visual_metro(self._scripts[script], args)
	    elif 'RINGLINK ' in args and self._scripts[script]['session']:
		self.handle_ring_link(self._scripts[script]['session'], script, args[9:])
	    elif 'RING ' in args and self._scripts[script]['session']:
		self.handle_session_offset(script, self._scripts[script]['session'], args[5:]) 
	    elif 'COLORS ' in args and self._scripts[script]['session'] and self._scripts[script]['color']:
		self.handle_session_colors(self._scripts[script]['session'], self._scripts[script]['color'], args[7:])
	    elif 'DEV LOCK' in args and self._scripts[script]['device']:
		self._scripts[script]['device'].canonical_parent.toggle_lock()
	    elif 'BANK ' in args and self._scripts[script]['mixer']:
		self.handle_track_bank(script, xclip, ident, self._scripts[script]['mixer'], self._scripts[script]['session'], args[5:])
	    elif 'RPT' in args:
		self.handle_note_repeat(self._scripts[script]['script'], script, args)
	    else:
		if self._scripts[script]['mixer'] and '/' in args[:4]:
		    self.handle_track_action(script, self._scripts[script]['mixer'], xclip, ident, args)
		
		    
    def _get_script_to_operate_on(self, script_info):
	""" Returns the script index to operate on, which can be specified in terms of its index
	or its name. Also, can use SURFACE (legacy) or CS (new) to indicate a surface action. """
	script = None
	try: 
	    script_spec = None
	    if 'SURFACE' in script_info:
		script_spec = script_info.strip('SURFACE')
	    elif 'CS' in script_info:
		script_spec = script_info.strip('CS')
	    if len(script_spec) == 1:
		script = int(script_spec) - 1
		if not self._scripts.has_key(script):
		    script = None
	    else:
		script_spec = script_spec.strip('"').strip()
		for k, v in self._scripts.items():
		    if v['name'] == script_spec:
			script = k
	except: script = None
	return script
    
		
    def handle_note_repeat(self, script, script_index, args):
	""" Set note repeat for the given surface """
	args = args.replace('RPT', '').strip()
	if args in REPEAT_STATES:
	    if args == 'OFF':
		script._c_instance.note_repeat.enabled = False
		self._scripts[script_index]['repeat'] = False
	    else:
		script._c_instance.note_repeat.repeat_rate = REPEAT_STATES[args]
		script._c_instance.note_repeat.enabled = True
		self._scripts[script_index]['repeat'] = True
	else:
	    self._scripts[script_index]['repeat'] = not self._scripts[script_index]['repeat']
	    script._c_instance.note_repeat.enabled = self._scripts[script_index]['repeat']
			        
	
    def handle_track_action(self, script_key, mixer, xclip, ident, args):  
	""" Get control surface track(s) to operate on and call main action dispatch """
	track_start = None
	track_end = None
	track_range = args.split('/')[0]
	actions = str(args[args.index('/')+1:].strip()).split()
	new_action = actions[0]
	new_args = ''
	if len(actions) > 1:
	    new_args = ' '.join(actions[1:])
	if 'ALL' in track_range:
	    track_start = 0
	    track_end = len(mixer._channel_strips)
	elif '-' in track_range:
	    track_range = track_range.split('-')
	    try:
		track_start = int(track_range[0]) - 1
		track_end = int(track_range[1])
	    except: 
		track_start = None
		track_end = None
	else:
	    try: 
		track_start = int(track_range) - 1
		track_end = track_start + 1
	    except:
		track_start = None
		track_end = None
	if track_start != None and track_end != None:
	    if track_start in range (len(mixer._channel_strips) + 1) and track_end in range (len(mixer._channel_strips) + 1) and track_start < track_end:
		track_list = []
		if self._scripts[script_key]['name'] == 'PUSH':
                    offset, _ = self._push_actions.get_session_offsets(self._scripts[script_key]['session'])
                    tracks_to_use = self._scripts[script_key]['session'].tracks_to_use()
                else:
                    offset = mixer._track_offset
                    tracks_to_use = mixer.tracks_to_use()
		for index in range (track_start, track_end):
		    if index + offset in range (len(tracks_to_use)):
			track_list.append(tracks_to_use[index + offset])
		if track_list:
		    self._parent.action_dispatch(track_list, xclip, new_action, new_args, ident)  
   	
    
    def handle_track_bank(self, script_key, xclip, ident, mixer, session, args):
	""" Move track bank (or session bank) and select first track in bank...this works even with controllers without banks like User Remote Scripts """
	if self._scripts[script_key]['name'] == 'PUSH':
	    t_offset, s_offset = self._push_actions.get_session_offsets(session)
	    tracks = session.tracks_to_use()
	else:
	    t_offset, s_offset = mixer._track_offset, session._scene_offset if session else None
	    tracks = mixer.tracks_to_use()
	new_offset = None
	if args == 'FIRST':
	    new_offset = 0
	elif args == 'LAST':
	    new_offset = len(tracks) - len(mixer._channel_strips)
	else:
	    try: 
		offset = int(args)
		if offset + t_offset in range (len(tracks)):
		    new_offset = offset + t_offset
	    except: new_offset = None 
	if new_offset >= 0:
	    if session:
		session.set_offsets(new_offset, s_offset)
	    else:
		mixer.set_track_offset(new_offset)
		self.handle_track_action(script_key, mixer, xclip, ident, '1/SEL') 
		
    
    def handle_session_offset(self, script_key, session, args):
	""" Handle moving session offset absolutely or relatively as well as storing/recalling its last position. """
	if self._scripts[script_key]['name'] in ('PUSH', 'PUSH2'):
	    last_pos = self._push_actions.handle_session_offset(session, self._scripts[script_key]['last_ring_pos'], args, self._parse_ring_spec)
	    self._scripts[script_key]['last_ring_pos'] = last_pos or None
	    return
	try:
	    new_track = session._track_offset
	    new_scene = session._scene_offset 
	    if args.strip() == 'LAST':
		last_pos = self._scripts[script_key]['last_ring_pos']
		if last_pos:
		    session.set_offsets(last_pos[0], last_pos[1])
		return
	    else:
		self._scripts[script_key]['last_ring_pos'] = (new_track, new_scene)		
	    new_track, args = self._parse_ring_spec('T', args, new_track, self.song().tracks)
	    new_scene, args = self._parse_ring_spec('S', args, new_scene, self.song().scenes) 
	    if new_track == -1 or new_scene == -1:
		return
	    session.set_offsets(new_track, new_scene)
	except: pass
	
	
    def _parse_ring_spec(self, spec_id, arg_string, default_index, list_to_search):
	""" Parses a ring action specification and returns the specified track/scene index
	as well as the arg_string without the specification that was parsed. """
	index = default_index
	arg_array = arg_string.split()
	for a in arg_array:
	    if a.startswith(spec_id):
		if a[1].isdigit():
		    index = int(a.strip(spec_id)) - 1
		    arg_string = arg_string.replace(a, '', 1).strip()
		    break
		elif a[1] in ('<', '>'):
		    index += self._parent.get_adjustment_factor(a.strip(spec_id))
		    arg_string = arg_string.replace(a, '', 1).strip()
		    break
		elif a[1] == '"':
		    name_start_pos = arg_string.index(spec_id + '"')
		    name = arg_string[name_start_pos + 2:]
		    name_end_pos = name.index('"')
		    name = name[:name_end_pos]
		    for i, item in enumerate(list_to_search):
			if name == item.name.upper():
			    index = i
			    break
		    arg_string = arg_string.replace(spec_id + '"' + name + '"', '', 1).strip()
		    break	    
	return (index, arg_string)
	
	
    def handle_ring_link(self, session, script_index, args):
	""" Handles linking/unliking session offsets to the selected track or scene with centering if specified. """
	self._scripts[script_index]['track_link'] = args == 'T' or 'T ' in args or ' T' in args
	self._scripts[script_index]['scene_link'] = 'S' in args
	self._scripts[script_index]['centered_link'] = 'CENTER' in args
    
    
    def handle_session_colors(self, session, colors, args):
	""" Handle changing clip launch LED colors """
	args = args.split()
	if len(args) == 3:
	    for a in args:
		if not a in colors:
		    return
	    for scene_index in range(session.height()):
		scene = session.scene(scene_index)
		for track_index in range(session.width()):
		    clip_slot = scene.clip_slot(track_index)
		    clip_slot.set_started_value(colors[args[0]][0])
		    clip_slot.set_triggered_to_play_value(colors[args[0]][1])
		    clip_slot.set_recording_value(colors[args[1]][0])
		    clip_slot.set_triggered_to_record_value(colors[args[1]][1])
		    clip_slot.set_stopped_value(colors[args[2]][0])
		    clip_slot.update()
	    
	    
    def handle_visual_metro(self, script, args):
	""" Handle visual metro for APCs and Launchpad. """
	if 'ON' in args and not script['metro']['component']:
	    m = VisualMetro(self._parent, script['metro']['controls'], script['metro']['override']) 
	    script['metro']['component'] = m
	elif 'OFF' in args and script['metro']['component']:
	    script['metro']['component'].disconnect()
	    script['metro']['component'] = None
    
	    
    def on_selected_track_changed(self):
	""" Moves the track offset of all track linked surfaces to the selected track with centering if specified. """
	trk = self.song().view.selected_track
	if trk in self.song().tracks:
	    trk_id = list(self.song().visible_tracks).index(trk)
	    for k, v in self._scripts.items():
		if v['track_link']:
		    new_trk_id = trk_id
		    try:
			session = self._scripts[k]['session']
			if v['name'] in ('PUSH', 'PUSH2'):
			    width = self._push_actions.get_session_dimensions(session)[0]
			    t_offset, s_offset = self._push_actions.get_session_offsets(session)
			else:
			    width = session.width()
			    t_offset, s_offset = session._track_offset, session._scene_offset
			if self._scripts[k]['centered_link']:
			    mid_point = (width / 2)
			    if new_trk_id < mid_point:
				if t_offset <= new_trk_id:
				    return
				else:
				    new_trk_id = 0
			    else:
				centered_id = new_trk_id - mid_point
				if centered_id in range(len(self.song().visible_tracks)):
				    new_trk_id = centered_id
			session.set_offsets(new_trk_id, s_offset)
		    except: pass
		    
    
    def on_selected_scene_changed(self):
	""" Moves the scene offset of all scene linked surfaces to the selected scene with centering if specified. """
	scn_id = list(self.song().scenes).index(self.song().view.selected_scene)
	for k, v in self._scripts.items():
	    if v['scene_link']:
		new_scn_id = scn_id
		try:
		    session = self._scripts[k]['session']		    
		    if v['name'] in ('PUSH', 'PUSH2'):
			height = self._push_actions.get_session_dimensions(session)[1]
			t_offset, s_offset = self._push_actions.get_session_offsets(session)
		    else:
			height = session.height()
			t_offset, s_offset = session._track_offset, session._scene_offset
		    
		    if self._scripts[k]['centered_link']:
			mid_point = (height / 2)
			if new_scn_id < mid_point:
			    if s_offset <= new_scn_id:
				return
			    else:
				new_scn_id = 0
			else:
			    centered_id = new_scn_id - mid_point
			    if centered_id in range(len(self.song().scenes)):
				new_scn_id = centered_id
		    session.set_offsets(t_offset, new_scn_id)
		except: pass
    
    
class VisualMetro(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' Visual metro for APCs and Launchpad '
    
    def __init__(self, parent, controls, override):
        ControlSurfaceComponent.__init__(self)
	self._parent = parent
        self._controls = controls
	self._override = override
	self._last_beat = -1
	self.song().add_current_song_time_listener(self.on_time_changed)
	self.song().add_is_playing_listener(self.on_time_changed)
	
	
    def disconnect(self):
	if self._controls:
	    self.clear()
	self._controls = None
	self.song().remove_current_song_time_listener(self.on_time_changed)	
	self.song().remove_is_playing_listener(self.on_time_changed)
	self._override = None
	self._parent = None
	ControlSurfaceComponent.disconnect(self)
	    
    
    def on_enabled_changed(self):
	pass
        

    def update(self):    
        pass    
	
	
    def on_time_changed(self):
	""" Show visual metronome via control LEDs upon beat changes (will not be shown if in Launchpad User 1) """
	if self.song().is_playing and (not self._override or (self._override and self._override._mode_index != 1)):
	    time = str(self.song().get_current_beats_song_time()).split('.')
	    if self._last_beat != int(time[1])-1:
		self._last_beat = int(time[1])-1
		self.clear()
		if self._last_beat < len(self._controls):
		    self._controls[self._last_beat].turn_on()
		else:
		    self._controls[len(self._controls)-1].turn_on()
	else:
	    self.clear()
		
		
    def clear(self):
	""" Clear all control LEDs """
	for c in self._controls:
	    c.turn_off()

    
# local variables:
# tab-width: 4
