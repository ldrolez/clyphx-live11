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

#---This module contains CS and DR Pad Mix Rack.

from _Generic.Devices import *
from consts import *
from functools import partial
from MacrobatParameterRackTemplate9 import MacrobatParameterRackTemplate
from _Framework.SubjectSlot import Subject, SlotManager, subject_slot

		
class MacrobatDRPadMixRack(MacrobatParameterRackTemplate):
    
    __module__ = __name__
    __doc__ = ' Macros to mixer params of selected DR pad '
    
    def __init__(self, parent, rack, track):
	self._drum_rack = {}
	self._rack = None
	self._selected_chain = None
        MacrobatParameterRackTemplate.__init__(self, parent, rack, track)
	
	
    def disconnect(self):
	self._drum_rack = None
	self._rack = None
	self._selected_chain = None
	MacrobatParameterRackTemplate.disconnect(self)
	
	
    def setup_device(self, rack):
	""" Set up macros and drum rack params """   
	MacrobatParameterRackTemplate.setup_device(self, rack)
	self._rack = rack
	self._drum_rack = self.get_drum_rack()
	self._selected_chain = None
	self._on_sends_changed.subject = None
	self._on_selected_pad_changed.subject = None
	if self._drum_rack:
	    self._on_selected_pad_changed.subject = self._drum_rack['rack'].view
	    self._set_selected_chain()
	    if self._selected_chain:
		num_sends = len(self._selected_chain.mixer_device.sends)
		for index in range(1,9):
		    if rack.parameters[index].is_enabled:
			param = None
			if index == 1:
			    param = self._selected_chain.mixer_device.volume
			elif index == 2:
			    param = self._selected_chain.mixer_device.panning
			else:
			    s_index = index - 3
			    if s_index < num_sends:
				param = self._selected_chain.mixer_device.sends[s_index]
			if param and param.is_enabled:
			    macro = rack.parameters[index]
			    m_listener = lambda index = index:self.macro_changed(index)
			    macro.add_value_listener(m_listener)
			    p_listener = lambda index = index:self.param_changed(index)
			    param.add_value_listener(p_listener)
			    self._param_macros[index] = (macro, param)
		self._tasks.add(self.get_initial_value)

		
    @subject_slot('selected_drum_pad')
    def _on_selected_pad_changed(self):
	self.setup_device(self._rack)
    
    
    @subject_slot('sends')
    def _on_sends_changed(self):
	self.setup_device(self._rack)


    def _set_selected_chain(self):
	self._selected_chain = None
	self._on_sends_changed.subject = None
	if self._drum_rack:
	    sel_pad = self._drum_rack['rack'].view.selected_drum_pad
	    if sel_pad and sel_pad.chains:
		self._selected_chain = sel_pad.chains[0]
		self._on_sends_changed.subject = self._selected_chain.mixer_device
    
	    
class CSWrapper(Subject, SlotManager):
    """ Wrapper for a chain selector that limits the max value to the number
    of chains in the rack. """
	
    __subject_events__ = ('value',)

    def __init__(self, cs):
	super(CSWrapper, self).__init__()
	self._cs = cs
	self._max = 0
	self._on_cs_value_changed.subject = self._cs

    @property
    def is_enabled(self):
	return self._cs.is_enabled

    def _get_value(self):
	return min(self._cs.value, self._max)

    def _set_value(self, value):
	if value <= self._max:
	    self._cs.value = value
    
    value = property(_get_value, _set_value)

    @property
    def min(self):
	return self._cs.min
    
    def _get_max(self):
	return self._max
    
    def _set_max(self, value):
	self._max = value
    
    max = property(_get_max, _set_max)

    @subject_slot('value')
    def _on_cs_value_changed(self):
	if self._cs.value <= self._max:
	    self.notify_value()
	    

class MacrobatChainSelectorRack(MacrobatParameterRackTemplate):
    __module__ = __name__
    __doc__ = ' Macro 1 to chain selector'
    
    def __init__(self, parent, rack, track):
	self._rack = rack
	self._wrapper = None
        MacrobatParameterRackTemplate.__init__(self, parent, rack, track)
	
	
    def disconnect(self):
	self._rack = None
	self._wrapper = None
	MacrobatParameterRackTemplate.disconnect(self)

	
    def scale_macro_value_to_param(self, macro, param):
	return (((param.max - param.min) / 126.0) * macro.value) + param.min


    def setup_device(self, rack):
	""" Set up macro 1 and chain selector """   
	MacrobatParameterRackTemplate.setup_device(self, rack)
	self._rack = rack
	if self._rack:
	    macro = self._rack.parameters[1]
	    cs = self._rack.parameters[9]
	    if macro.is_enabled and cs.is_enabled:
		self._wrapper = CSWrapper(cs)
		self._wrapper.max = len(self._rack.chains)
		if self._wrapper.max > 1:
		    self._on_chains_changed.subject = self._rack
		    index = 1
		    m_listener = lambda index = index:self.macro_changed(index)
		    macro.add_value_listener(m_listener)
		    p_listener = lambda index = index:self.param_changed(index)
		    self._wrapper.add_value_listener(p_listener)
		    self._param_macros[index] = (macro, self._wrapper)
		if IS_LIVE_9:
		    self._tasks.add(self.get_initial_value)
		else:
		    self._get_initial_value = True
		    

    @subject_slot('chains')
    def _on_chains_changed(self):
	if self._wrapper and self._rack:
	    self._wrapper.max = len(self._rack.chains)
	    self.param_changed(0)
	
# local variables:
# tab-width: 4