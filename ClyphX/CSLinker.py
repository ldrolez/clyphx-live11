"""
# Copyright (C) 2014-2017 Stray <stray411@hotmail.com>
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

from functools import partial
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ControlSurface import ControlSurface
from _Framework.SessionComponent import SessionComponent

from consts import *

class CSLinker(ControlSurfaceComponent):
    """ CSLinker links the SessionComponents of two control surface scripts in Live 9. """
    
    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._slave_objects = [None, None]
        self._script_names = None
        self._horizontal_link = False
        self._matched_link = False
        self._multi_axis_link = False
        
        
    def disconnect(self):
        """ Extends standard to disconnect and remove slave objects. """
        for obj in self._slave_objects:
            if obj:
                obj.disconnect()
        self._slave_objects = None
        ControlSurfaceComponent.disconnect(self)
        
        
    def parse_settings(self, settings_string):
        """ Parses settings data read from UserPrefs for linker settings. """
        line_data = settings_string.split('=')
        if 'MATCHED' in line_data[0]:
            self._matched_link = line_data[1].strip() == 'TRUE'
        elif 'HORIZ' in line_data[0] and not self._matched_link:
            self._horizontal_link = line_data[1].strip() == 'TRUE'
        elif 'AXIS' in line_data[0] and not self._matched_link:
            self._multi_axis_link = line_data[1].strip() == 'TRUE'
        else:
            if 'NONE' in line_data[1]:
                self._script_names = None
            else:
                if '1' in line_data[0]:
                    self._script_names = [line_data[1].strip()]
                else:
                    if self._script_names:
                        self._script_names.append(line_data[1].strip())
                        if 'PUSH2' in self._script_names:
                            self.canonical_parent.schedule_message(20, partial(self.connect_script_instances,
                                                                               self.canonical_parent._control_surfaces()))
                        else:
                            self.connect_script_instances(self.canonical_parent._control_surfaces())
                            
        
    def connect_script_instances(self, instanciated_scripts):
        """ Attempts to find the two specified scripts, find their SessionComponents and create slave objects for them. """ 
        if self._script_names:
            scripts = [None, None]
            found_scripts = False
            scripts_have_same_name = self._script_names[0] == self._script_names[1]
            for script in instanciated_scripts:
                script_name = script.__class__.__name__.upper()
                if (IS_LIVE_9_5 and script_name in ('PUSH', 'PUSH2')) or (isinstance(script, ControlSurface) and script.components): 
                    if script_name == self._script_names[0]:
                        if scripts_have_same_name:
                            scripts[scripts[0] != None] = script
                        else:
                            scripts[0] = script
                    elif script_name == self._script_names[1]:
                        scripts[1] = script
                    found_scripts = scripts[0] and scripts[1]
                    if found_scripts:
                        break
            if found_scripts:
                self.canonical_parent.log_message('CSLINKER SUCCESS: Specified scripts located!')
                ssn_comps = []
                for script in scripts:
                    if IS_LIVE_9_5 and script.__class__.__name__.upper() in ('PUSH', 'PUSH2'):
                        ssn_comps.append(script._session_ring)
                    for c in script.components:
                        if isinstance (c, SessionComponent):
                            ssn_comps.append(c)
                            break
                if len(ssn_comps) == 2:
                    self.canonical_parent.log_message('CSLINKER SUCCESS: SessionComponents for specified scripts located!')
                    if self._matched_link:
                        for s in ssn_comps:
                            s._link()
                    else:
                        if IS_LIVE_9_5 and self._script_names[0] in ('PUSH', 'PUSH2'):
                            h_offset = ssn_comps[0].num_tracks
                            v_offset = ssn_comps[0].num_scenes
                        else:
                            h_offset = ssn_comps[0].width()
                            v_offset = ssn_comps[0].height()
                        h_offset_1 = 0 if not self._horizontal_link and self._multi_axis_link else -(h_offset)
                        v_offset_1 = 0 if self._horizontal_link and self._multi_axis_link else -(v_offset)
                        h_offset_2 = 0 if not self._horizontal_link and self._multi_axis_link else h_offset
                        v_offset_2 = 0 if self._horizontal_link and self._multi_axis_link else v_offset
                        self._slave_objects[0] = SessionSlave(self._horizontal_link, self._multi_axis_link, ssn_comps[0], ssn_comps[1], h_offset_1, v_offset_1)
                        self._slave_objects[1] = SessionSlaveSecondary(self._horizontal_link, self._multi_axis_link, ssn_comps[1], ssn_comps[0], h_offset_2, v_offset_2)
                        self.canonical_parent.schedule_message(10, self._refresh_slave_objects)
                else:
                    self.canonical_parent.log_message('CSLINKER ERROR: Unable to locate SessionComponents for specified scripts!')       
            else:
                self.canonical_parent.log_message('CSLINKER ERROR: Unable to locate specified scripts!')                 
                
                
    def on_track_list_changed(self):
        """ Refreshes slave objects if horizontally linked. """
        if not self._matched_link and (self._horizontal_link or self._multi_axis_link):
            self._refresh_slave_objects()            
        
        
    def on_scene_list_changed(self):
        """ Refreshes slave objects if vertically linked. """
        if not self._matched_link and (not self._horizontal_link or self._multi_axis_link):
            self._refresh_slave_objects() 
            
        
    def _refresh_slave_objects(self):
        """ Refreshes offsets of slave objects. """
        for obj in self._slave_objects:
            if obj:
                obj._on_offsets_changed()

                
    def update(self):
        pass
                    
                    
class SessionSlave(object):
    """ SessionSlave is the base class for linking two SessionComponents. """
    
    def __init__(self, horz_link, multi_axis, self_comp, observed_comp, h_offset, v_offset):
        self._horizontal_link = horz_link
        self._multi_axis_link = multi_axis
        self._h_offset = h_offset
        self._v_offset = v_offset
        self._self_ssn_comp = self_comp
        self._observed_ssn_comp = observed_comp
        self._last_self_track_offset = -1
        self._last_self_scene_offset = -1
        self._last_observed_track_offset = -1
        self._last_observed_scene_offset = -1
        self._num_tracks = -1
        self._num_scenes = -1
        self._observed_ssn_comp.add_offset_listener(self._on_offsets_changed)

    
    def disconnect(self):
        self._self_ssn_comp = None
        self._observed_ssn_comp.remove_offset_listener(self._on_offsets_changed)
        self._observed_ssn_comp = None
    
    
    def _on_offsets_changed(self, arg_a=None, arg_b=None):
        """ Called on offset changes to the observed SessionComponent to handle moving offsets if possible. """
        if self._horizontal_link or self._multi_axis_link:
            new_num_tracks = len(self._self_ssn_comp.tracks_to_use())
            if new_num_tracks != self._num_tracks: # if track list changed, need to completely refresh offsets
                self._num_tracks = new_num_tracks
                self._last_self_track_offset = -1
                self._last_observed_track_offset = -1
            observed_offset = self._observed_track_offset()
            if observed_offset != self._last_observed_track_offset: # if observed offset unchanged, do nothing
                self._last_observed_track_offset = observed_offset
                if self._track_offset_change_possible():
                    self_offset = max(self._min_track_offset(), min(self._num_tracks, (self._last_observed_track_offset + self._h_offset)))
                    if self_offset != self._last_self_track_offset: # if self offset unchanged, do nothing
                        self._last_self_track_offset = self_offset
                        self._self_ssn_comp.set_offsets(self._last_self_track_offset, self._self_scene_offset())
                else:
                    return
        if not self._horizontal_link or self._multi_axis_link:
            if hasattr(self._self_ssn_comp.song, '__call__'):
                new_num_scenes = len(self._self_ssn_comp.song().scenes)
            else:
                new_num_scenes = len(self._self_ssn_comp.song.scenes)
            if new_num_scenes != self._num_scenes: # if scene list changed, need to completely refresh offsets
                self._num_scenes = new_num_scenes
                self._last_self_scene_offset = -1
                self._last_observed_scene_offset = -1
            observed_offset = self._observed_scene_offset()
            if observed_offset != self._last_observed_scene_offset: # if observed offset unchanged, do nothing
                self._last_observed_scene_offset = observed_offset
                if self._scene_offset_change_possible():
                    self_offset = max(self._min_scene_offset(), min(self._num_scenes, (self._last_observed_scene_offset + self._v_offset)))
                    if self_offset != self._last_self_scene_offset: # if self offset unchanged, do nothing
                        self._last_self_scene_offset = self_offset
                        self._self_ssn_comp.set_offsets(self._self_track_offset(), self._last_self_scene_offset)
                else:
                    return

    def _observed_track_offset(self):
        if hasattr(self._observed_ssn_comp.track_offset, '__call__'):
            return self._observed_ssn_comp.track_offset()
        return self._observed_ssn_comp.track_offset
    
    
    def _self_track_offset(self):
        if hasattr(self._self_ssn_comp.track_offset, '__call__'):
            return self._self_ssn_comp.track_offset()
        return self._self_ssn_comp.track_offset
    
    
    def _observed_scene_offset(self):
        if hasattr(self._observed_ssn_comp.scene_offset, '__call__'):
            return self._observed_ssn_comp.scene_offset()
        return self._observed_ssn_comp.scene_offset
    
    
    def _self_scene_offset(self):
        if hasattr(self._self_ssn_comp.scene_offset, '__call__'):
            return self._self_ssn_comp.scene_offset()
        return self._self_ssn_comp.scene_offset
                
                
    def _track_offset_change_possible(self):
        """ Returns whether or not moving the track offset is possible. """
        if hasattr(self._self_ssn_comp, 'width'):
            w = self._self_ssn_comp.width()
        else:
            w = self._self_ssn_comp.num_tracks
        return self._num_tracks > w
    
    
    def _min_track_offset(self):
        """ Returns the minimum track offset. """
        return 0
    
    
    def _scene_offset_change_possible(self):
        """ Returns whether or not moving the scene offset is possible. """
        if hasattr(self._self_ssn_comp, 'height'):
            h = self._self_ssn_comp.height()
        else:
            h = self._self_ssn_comp.num_scenes
        return self._num_scenes > h
    
    
    def _min_scene_offset(self):
        """ Returns the minimum scene offset. """
        return 0
    

class SessionSlaveSecondary(SessionSlave):
    """ SessionSlaveSecondary is the second of the two linked slave objects. 
    This overrides the functions that return whether offsets can be changed as well as the functions that return minimum offsets. """

    
    def _track_offset_change_possible(self):
        if hasattr(self._self_ssn_comp, 'width'):
            self_width = self._self_ssn_comp.width()
        else:
            self_width = self._self_ssn_comp.num_tracks
        if hasattr(self._observed_ssn_comp, 'width'):
            obs_width = self._observed_ssn_comp.width()
        else:
            obs_width = self._observed_ssn_comp.num_tracks
        return self._num_tracks >= self_width + obs_width
    
    
    def _min_track_offset(self):
        return self._last_observed_track_offset
    
    
    def _scene_offset_change_possible(self):
        if hasattr(self._self_ssn_comp, 'height'):
            self_h = self._self_ssn_comp.height()
        else:
            self_h = self._self_ssn_comp.num_scenes
        if hasattr(self._observed_ssn_comp, 'height'):
            obs_h = self._observed_ssn_comp.height()
        else:
            obs_h = self._observed_ssn_comp.num_scenes
        return self._num_scenes >= self_h + obs_h
    
    
    def _min_scene_offset(self):
        return self._last_observed_scene_offset
    
    