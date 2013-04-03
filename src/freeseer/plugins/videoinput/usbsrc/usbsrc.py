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
    device = None

    input_type = "video/x-raw-rgb"
    framerate = 10
    resolution = "NOSCALE"
    
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
            videosrc.set_property("device-name", self.device)
        bin.add(videosrc)

        videorate = gst.element_factory_make("videorate", "videorate")
        bin.add(videorate)
        videorate_cap = gst.element_factory_make("capsfilter",
                          "video_rate_cap")
        videorate_cap.set_property("caps",
                        gst.caps_from_string("%s, framerate=%d/1" % (self.input_type, self.framerate)))
        bin.add(videorate_cap)
        # --- End Video Rate

        # Video Scaler (Resolution)
        videoscale = gst.element_factory_make("videoscale", "videoscale")
        bin.add(videoscale)
        videoscale_cap = gst.element_factory_make("capsfilter",
                                                    "videoscale_cap")
        if self.resolution != "NOSCALE":
            videoscale_cap.set_property('caps',
                                        gst.caps_from_string('%s, width=640, height=480' % (self.input_type)))
        bin.add(videoscale_cap)
        # --- End Video Scaler

        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        bin.add(colorspace)

        # Link Elements
        videosrc.link(videorate)
        videorate.link(videorate_cap)
        videorate_cap.link(videoscale)
        videoscale.link(videoscale_cap)
        videoscale_cap.link(colorspace)

        srcpad = colorspace.get_pad("src")
        src_ghostpad = gst.GhostPad("src", srcpad)
        bin.add_pad(src_ghostpad)

        return bin
    
    def load_config(self, plugman):
        self.plugman = plugman
        
        try:
            self.device = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device")
            self.input_type = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type")
            self.framerate = int(self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate"))
            self.resolution = self.plugman.get_plugin_option(self.CATEGORY, self.get_config_name(), "Resolution")
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", self.device)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type", self.input_type)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate", self.framerate)
            self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Resolution", self.resolution)
        
    def get_widget(self):
        if self.widget is None:
            self.widget = QtGui.QWidget()
            
            layout = QtGui.QFormLayout()
            self.widget.setLayout(layout)
            
            self.label = QtGui.QLabel("Video Device")
            self.combobox = QtGui.QComboBox()
            self.combobox.setMinimumWidth(150)
            layout.addRow(self.label, self.combobox)

            self.label = QtGui.QLabel("Video Input")
            self.combobox = QtGui.QComboBox()
            layout.addRow(self.label, self.combobox)

            self.videocolourLabel = QtGui.QLabel(self.widget.tr("Colour Format"))
            self.videocolourComboBox = QtGui.QComboBox()
            self.videocolourComboBox.addItem("video/x-raw-rgb")
            self.videocolourComboBox.addItem("video/x-raw-yuv")
            self.videocolourComboBox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
            layout.addRow(self.videocolourLabel, self.videocolourComboBox)

            self.framerateLabel = QtGui.QLabel("Framerate")
            self.framerateLayout = QtGui.QHBoxLayout()
            self.framerateSlider = QtGui.QSlider()
            self.framerateSlider.setOrientation(QtCore.Qt.Horizontal)
            self.framerateSlider.setMinimum(0)
            self.framerateSlider.setMaximum(60)
            self.framerateSpinBox = QtGui.QSpinBox()
            self.framerateSpinBox.setMinimum(0)
            self.framerateSpinBox.setMaximum(60)
            self.framerateLayout.addWidget(self.framerateSlider)
            self.framerateLayout.addWidget(self.framerateSpinBox)
            layout.addRow(self.framerateLabel, self.framerateLayout)

            self.videoscaleLabel = QtGui.QLabel("Video Scale")
            self.videoscaleComboBox = QtGui.QComboBox()
            self.videoscaleComboBox.addItem("NOSCALE")
            self.videoscaleComboBox.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
            layout.addRow(self.videoscaleLabel, self.videoscaleComboBox)
            
            # Connections
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(int)'), self.set_device)
            self.widget.connect(self.combobox, QtCore.SIGNAL('currentIndexChanged(const QString&)'), self.set_input)
            self.widget.connect(self.framerateSlider, QtCore.SIGNAL("valueChanged(int)"), self.framerateSpinBox.setValue)
            self.widget.connect(self.framerateSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.framerateSlider.setValue)
            self.widget.connect(self.videocolourComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.set_videocolour)
            self.widget.connect(self.framerateSlider, QtCore.SIGNAL("valueChanged(int)"), self.set_framerate)
            self.widget.connect(self.framerateSpinBox, QtCore.SIGNAL("valueChanged(int)"), self.set_framerate)
            
        return self.widget

    def widget_load_config(self, plugman):
        self.load_config(plugman)
                
        # Load the combobox with inputs
        self.combobox.clear()
        n = 0
        for device, devurl in self.get_devices().items():
            self.combobox.addItem(device, devurl)
            if device == self.device:
                self.combobox.setCurrentIndex(n)
            n = n + 1
    
        vcolour_index = self.videocolourComboBox.findText(self.input_type)
        self.videocolourComboBox.setCurrentIndex(vcolour_index)
            
    def get_devices(self):
        """
        Returns a list of possible devices detected as a dictionary
        
        On Linux the dictionary is a key, value pair of:
            Device Name : Device Path
            
        On Windows the dictionary is a key, value pair of:
            Device Name : Device Name
        
        NOTE: GstPropertyProbe has been removed in later versions of Gstreamer
              When a new method is available this function will need to be
              redesigned:
                  https://bugzilla.gnome.org/show_bug.cgi?id=678402
        """
        
        devicemap = {}
        
        if sys.platform.startswith("linux"):
            videosrc = gst.element_factory_make("v4l2src", "videosrc")
            videosrc.probe_property_name('device')
            devices = videosrc.probe_get_values_name('device')            
            
            for device in devices:
                videosrc.set_property('device', device)
                devicemap[videosrc.get_property('device-name')] = device
            
        elif sys.platform in ["win32", "cygwin"]:
            videosrc = gst.element_factory_make("dshowvideosrc", "videosrc")
            videosrc.probe_property_name('device-name')
            devices = videosrc.probe_get_values_name('device-name')  
            
            for device in devices:
                devicemap[device] = device
                
        return devicemap
    
    def set_input(self, input):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Input", input)
        
    def set_videocolour(self, input_type):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Input Type", input_type)
        
    def set_framerate(self, framerate):
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Framerate", str(framerate))
    
    def set_device(self, device):
        devname = self.combobox.itemData(device).toString()
        self.plugman.set_plugin_option(self.CATEGORY, self.get_config_name(), "Video Device", devname)
