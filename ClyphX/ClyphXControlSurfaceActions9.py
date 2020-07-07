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

from __future__ import with_statement
from ClyphXControlSurfaceActions import ClyphXControlSurfaceActions, VisualMetro
    
class ClyphXControlSurfaceActions9(ClyphXControlSurfaceActions):
    __module__ = __name__
    __doc__ = ' Actions related to control surfaces. This is a specialized version for Live 9.'
    
    def __init__(self, parent):
        ClyphXControlSurfaceActions.__init__(self, parent)
	    
    def handle_visual_metro(self, script, args):
	""" Handle visual metro for APCs and Launchpad. 
	This is a specialized version for L9 that uses component guard to avoid dependency issues. """
	if 'ON' in args and not script['metro']['component']:
	    with self._parent.component_guard(): 
		m = VisualMetro(self._parent, script['metro']['controls'], script['metro']['override']) 
		script['metro']['component'] = m
	elif 'OFF' in args and script['metro']['component']:
	    script['metro']['component'].disconnect()
	    script['metro']['component'] = None
    
# local variables:
# tab-width: 4