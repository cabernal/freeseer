'''
freeseer - vga/presentation capture software

Copyright (C) 2011-2013  Free and Open Source Software Learning Centre
http://fosslc.org

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

For support, questions, suggestions or any other inquiries, visit:
http://wiki.github.com/Freeseer/freeseer/

@author: Thanh Ha
'''

import ConfigParser
import os
import sys

import pygst
pygst.require("0.10")
import gst

from PyQt4 import QtGui, QtCore

from freeseer.framework.plugin import IVideoInput

class USBSrc(IVideoInput):
    name = "USB Source"
    os = ["linux", "linux2", "win32", "cygwin"]
    device = "/dev/video0"
    device_list = []
    
    def __init__(self):
        IVideoInput.__init__(self)
        
        #
        # Detect available devices
        #
        i = 0
        path = "/dev/video"
        devpath = path + str(i)
        
        while os.path.exists(devpath):
            self.device_list.append(devpath)
            i=i+1
            devpath=path + str(i)
    
    def get_videoinput_bin(self):
        """
        Return the video input object in gstreamer bin format.
        """
        bin = gst.Bin() # Do not pass a name so that we can load this input more than once.
        
        videosrc = None
        if sys.platform.startswith("linux"):
            videosrc = gst.element_factory_make("v4l2src", "videosrc")
            videosrc.set_property("device", self.device)
        elif sys.platform in ["win32", "cygwin"]:
            videosrc = gst.element_factory_make("dshowvideosrc", "videosrc")
        bin.add(videosrc)
        
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)
        videosrc.link(colorspace)
        
        # Setup ghost pad
        pad = colorspace.get_pad("src")
        ghostpad = gst.GhostPad("videosrc", pad)
        bin.add_pad(ghostpad)
        
        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.device = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", self.device)
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Device")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)
            
            # Connections
            self.widget.connect(self.combobox, 
                                QtCore.SIGNAL('currentIndexChanged(const QString&)'), 
                                self.set_device)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for i in self.device_list:
            self.combobox.addItem(i)
            if i == self.device:
                self.combobox.setCurrentIndex(n)
            n = n +1
            
    def set_device(self, device):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", device)
