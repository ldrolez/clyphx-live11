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
from ActionList import ActionList
from consts import IS_LIVE_9

""" This script allows you to create your own ClyphX actions that can be used like any other ClyphX action.

PLEASE NOTE: nativeKONTROL cannot provide support on writing Python code or on accessing Live's API through Python. 
These are extremely vast subjects that would be difficult to support, particularly in the context of ClyphX, which
is sometimes difficult to support on its own.  However, this script is full of comments to help you.  Also, the rest 
of the scripts in the ClyphX folder include plenty of examples of how to do things.  Lastly, we would make the 
following recommendations:

- You can edit this file with any text editor, but an IDE makes this easier: http://wingware.com/

- To learn about Python: http://www.diveintopython.net/toc/index.html and http://www.google.com

- To learn the basics of MIDI Remote Scripts/Live API access: http://remotescripts.blogspot.com/

- Reference of Live functions and such that you can access: http://cycling74.com/docs/max5/refpages/m4l-ref/m4l_live_object_model.html

- After making changes to this file, you will need to recompile.  The quickest way to do that is by loading a set.  Note, however, that if you
  make a change that results in errors, this can sometimes break all control surface scripts (cause them to throw strange errors for no reason)
  until you reload Live. 
  
  
TO CREATE ACTIONS:
 - You'll first add the action to the action_dict (dictionary below). 
 
 - Then you'll add and implement a function that will be called when the action is triggered.  
 
 - The function has to receive the following parameters: (self, track, args)
 
 - See the example functions below (example_action_one and example_action_two) for some examples of how to set up functions.

PARAMETER EXPLANATION:
- track = the track to apply the action to.  If the action isn't applied to any particular track, this will either be the selected track 
  (in the case of X-Controls and X-Cues) or the track the X-Clip resides on.  All of the actions CAN be (but don't HAVE to be) applied 
  to ranges of tracks (like 1-8/MY_ACTION, which will apply to tracks 1-8).  If applied to a range of tracks, the function associated with
  the action will be called once for each track in the range.  

- args = these are arguments that follow the name of the action.  For example, with the action VOL 10.  The 10 is an argument.  These arguments will always be in all caps.  

RESTRICTIONS:
- Action names (which you define in the dictionary below) should NOT be the same as any current ClyphX action and should be composed of 
  just letters and numbers. 

- Arguments should NOT use any of the special characters used in ClyphX: semi-colon(;), comma(,), percent sign(%), equals sign(=) 
"""
    
class ClyphXUserActions(ControlSurfaceComponent):
    __module__ = __name__
    __doc__ = ' User actions '    
    
    def __init__(self, parent):
        ControlSurfaceComponent.__init__(self)
	
	""" Below is the dictionary of actions that this script provides. 
	
	For each entry:
	- The key = the one-word (not case-sensitive) name of the action.  This is the name that is used when accessing the action from an X-Trigger.
	
	- The value = the name of the function in this script to call to perform the action. 
	
	Except for the last entry, every entry should be followed by a comma.  You can remove the 2 example entries from the dictionary if you wish. """
	self._action_dict = {#<--DO NOTE REMOVE THIS
	    'EX_ACTION_1' : 'example_action_one',
	    'EX_ACTION_2' : 'example_action_two'
	    }#<--DO NOTE REMOVE THIS
	
	""" The parent ClyphX script.  Through this you can access things such as the log_message function (writes to Live's Log.txt file), 
	which you'll likely use quite a bit.  The Troubleshooting section of the ClyphX manual covers how to access Log.txt. """
        self._parent = parent
	
	
    def disconnect(self):
	""" Called by the control surface on disconnect (app closed, script closed).  DO NOT REMOVE THIS. """
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)
	    
    
    def on_enabled_changed(self):
	""" Called when this script is enabled/disabled (by calling set_enabled on it).  DO NOT REMOVE THIS. """
	pass
        

    def update(self):    
	""" Called by the control surface on instantiation and in other cases such as when exiting MIDI map mode.  DO NOT REMOVE THIS. """
        pass
	

    def example_action_one(self, track, args):
	""" Example action that writes to Live's log file and then triggers standard ClyphX METRO action. 
	This can receive the same args as the METRO action (like EX_ACTION_1 ON), so it just passes args it receives to the METRO function. 
	
	NOTE: The arguments passed to handle_action_list_trigger are:
	 - The track associated with the trigger.  Since our function here is not associated with any particular track, we pass the selected track.
	 
	 - The ActionList object, which is just a simple object that contains a name field.  You just instantiate one of these with the action list 
	   as a string(proceeded by an identifier). """
	self._parent.log_message('example_action_one triggered with args=' + str(args))
	self._parent.handle_action_list_trigger(self.song().view.selected_track, ActionList('[] METRO ' + str(args)))	
	
	
    def example_action_two(self, track, args):
	""" Example action that sets mixer settings of the given track to be the same as the master track. 
	If no args or args contains VOL, sets volume.
	If no args or args contains PAN, sets panning.
	Obviously, does nothing if the given track is the master track. """	
	if track != self.song().master_track:
	    if not args or 'VOL' in args:
		track.mixer_device.volume.value = self.song().master_track.mixer_device.volume.value
	    if not args or 'PAN' in args:
		track.mixer_device.panning.value = self.song().master_track.mixer_device.panning.value
    

    def on_track_list_changed(self):
        """ Called by the control surface if tracks are added/removed, to be overridden """
        pass


    def on_scene_list_changed(self):
        """ Called by the control surface if scenes are added/removed, to be overridden """
        pass


    def on_selected_track_changed(self):
        """ Called by the control surface when a track is selected, to be overridden """
        pass


    def on_selected_scene_changed(self):
        """ Called by the control surface when a scene is selected, to be overridden """
        pass
    
    
# local variables:
# tab-width: 4