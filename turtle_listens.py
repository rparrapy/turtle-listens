# -*- coding: utf-8 -*-
#Copyright (c) 2014, Rodrigo Parra
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import os
import glob

from gettext import gettext as _

from plugins.plugin import Plugin
from TurtleArt.tapalette import (make_palette, define_logo_function)
from TurtleArt.talogo import (primitive_dictionary, logoerror)

from TurtleArt.tautils import (debug_output, get_path, data_to_string,
                               hat_on_top, listify, data_from_file)
from TurtleArt.taprimitive import (ArgSlot, ConstantArg, Primitive)
from TurtleArt.tatype import (TYPE_BOOL, TYPE_BOX, TYPE_CHAR, TYPE_INT,
                              TYPE_FLOAT, TYPE_OBJECT, TYPE_STRING,
                              TYPE_NUMBER)
from TurtleArt.taturtle import Turtle
from sugarlistens import helper
import logging



class Turtle_listens(Plugin):
    """ A class for defining an extra palette for speech recognition in Turtle Blocks
    """

    def __init__(self, turtle_window):
        Plugin.__init__(self)
        self.tw = turtle_window
        self.command = None

    def setup(self):
        palette = make_palette('listens',
                               colors=["#FFC000", "#A08000"],
                               help_string=_('Palette for speech recognition'))

        palette.add_block('turtle-listens',
                          style='basic-style-extended-vertical',
                          label=_('start listening'),
                          prim_name='listens',
                          help_string=_('Start listening'))

        self.tw.lc.def_prim('listens', 0,
                            Primitive(self.listen),
                            True)

        palette.add_block('turtle-listen-to',
                          style='boolean-1arg-block-style',
                          label=_('listen to'),
                          prim_name='listen_to',
                          value_block=True,
                          help_string=_('Listen to'))
        self.tw.lc.def_prim('listen_to', 1,
                            Primitive(self.listen_to,
                                      return_type=TYPE_BOOL,
                                      arg_descs=[ArgSlot(TYPE_STRING)]))


    def listen(self):
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__recognizer = helper.RecognitionHelper(self.__path)
        self.__recognizer.listen(self.final_result)
        self.__recognizer.start_listening()


    def final_result(self, text):
        self.command = text

    def listen_to(self, text):
        flag = False
        if self.command and self.command == text:
            self.command = None
            flag = True
        return flag

