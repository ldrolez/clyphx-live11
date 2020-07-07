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
from consts import IS_LIVE_9

class ClyphXClipEnvCapture(ControlSurfaceComponent):
    """ Captures mixer/device parameters as clip envelopes. """  

    def disconnect(self):
	self._parent = None
	if IS_LIVE_9:
	    ControlSurfaceComponent.disconnect(self)	
    
    def update(self):
	pass

    def capture(self, clip, track, args):
	clip.clear_all_envelopes()
	if args == '' or 'MIX' in args:
	    self._capture_mix_settings(clip, track, args)
	if (args == '' or 'DEV' in args) and track.devices:
	    self._capture_device_settings(clip, track, args)
	    
    def _capture_mix_settings(self, clip, track, args):
	if not 'MIXS' in args:
	    self._insert_envelope(clip, track.mixer_device.volume)
	    self._insert_envelope(clip, track.mixer_device.panning)
	if not 'MIX-' in args:
	    for s in track.mixer_device.sends:
		self._insert_envelope(clip, s)
		
    def _capture_device_settings(self, clip, track, args):
	dev_range = self._get_device_range(args, track)
	if dev_range:
	    for dev_index in range (dev_range[0], dev_range[1]):
		if dev_index < (len(track.devices)):
		    current_device = track.devices[dev_index]
		    for p in current_device.parameters:
			self._insert_envelope(clip, p)
		    if current_device.can_have_chains:
			self._capture_nested_devices(clip, current_device)		
		
    def _capture_nested_devices(self, clip, rack):
	if rack.chains:
	    for chain in rack.chains:
		for device in chain.devices:
		    for p in device.parameters:
			self._insert_envelope(clip, p)
		    if not rack.class_name.startswith('Midi'):
			self._insert_envelope(clip, chain.mixer_device.volume)
			self._insert_envelope(clip, chain.mixer_device.panning)
			self._insert_envelope(clip, chain.mixer_device.chain_activator)
			sends = chain.mixer_device.sends
			if sends:
			    for s in sends:
				self._insert_envelope(clip, s)
		    if device.can_have_chains and device.chains:
			self._capture_nested_devices(clip, device)

    def _insert_envelope(self, clip, param):
	env = clip.automation_envelope(param)
	if env:
	    env.insert_step(clip.loop_start, 0.0, param.value)
		    		
    def _get_device_range(self, args, track):
	""" Returns range of devices to capture """
	dev_args = args.replace('MIX', '')
	dev_args = dev_args.replace('DEV', '')
	start = 0
	end = start + 1
	if dev_args:
	    if 'ALL' in dev_args:
		start = 0
		end = len(track.devices)
	    elif '-' in dev_args:
		try:
		    name_split = dev_args.split('-')
		    start = int(name_split[0].strip()) - 1
		    end = int(name_split[1].strip())
		except: pass
	    else:
		try: 
		    start = int(dev_args) - 1
		    end = start + 1
		except: pass
	if start > len(track.devices) or start < 0 or end > len(track.devices) or end < start:
	    return()
	return (start, end)
    
# local variables:
# tab-width: 4