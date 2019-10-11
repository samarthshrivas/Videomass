# -*- coding: UTF-8 -*-

#########################################################
# Name: shownormlist.py
# Porpose: Show audio volume data list
# Compatibility: Python3, wxPython4
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3
# Rev: October.07.2019
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################

import wx

class NormalizationList(wx.Dialog):
    """
    Show a dialog with FFmpeg volumedetect command data and  report 
    offset and gain results need for normalization process.
    
    """
    def __init__(self, title, data, OS):
        """
        detailslist is a list of items list.
        
        """
        wx.Dialog.__init__(self, None, style=wx.DEFAULT_DIALOG_STYLE |
                                             wx.RESIZE_BORDER)
        """
        constructor:
        with 'None' not depend from parent:
        wx.Dialog.__init__(self, None, style=wx.DEFAULT_DIALOG_STYLE)
        
        With parent, -1:
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        if close videomass also close parent window:
        
        """
        normlist = wx.ListCtrl(self, wx.ID_ANY, 
                                style=wx.LC_REPORT | 
                                wx.SUNKEN_BORDER
                                    )
        #----------------------Properties----------------------#
        self.SetTitle(_(title))
        normlist.SetMinSize((850, 200))
        normlist.InsertColumn(0, _('File name'), width=300)
        normlist.InsertColumn(1, _('Max volume dBFS'), width=150)
        normlist.InsertColumn(2, _('Mean volume dBFS'), width=150)
        normlist.InsertColumn(3, _('Offset dBFS'), width=100)
        normlist.InsertColumn(4, _('Result dBFS'), width=120)
        self.button_close = wx.Button(self, wx.ID_CLOSE, "")
        descript = wx.StaticText(self, wx.ID_ANY,  (_('Post-normalization '
                                                      'references:')))
        red = wx.StaticText(self, wx.ID_ANY, "\t")
        red.SetBackgroundColour(wx.Colour(233, 80, 77)) # #e9504d
        txtred = wx.StaticText(self, wx.ID_ANY,  (_("=  Clipped peaks")))
        
        grey = wx.StaticText(self, wx.ID_ANY, "\t")
        grey.SetBackgroundColour(wx.Colour(100, 100, 100))# #646464
        txtgrey = wx.StaticText(self, wx.ID_ANY, (_("=  No changes")))
        
        yell = wx.StaticText(self, wx.ID_ANY, "\t")
        yell.SetBackgroundColour(wx.Colour(198, 180, 38))# #C6B426
        txtyell = wx.StaticText(self, wx.ID_ANY, (_("=  Below max peak")))
        

        sizer = wx.BoxSizer(wx.VERTICAL)
        
        gridbtn = wx.GridSizer(1, 1, 0, 0)
        sizer.Add(normlist, 1, wx.EXPAND|wx.ALL, 5)
        #sizer.Add(descript, 0, wx.ALL, 10)
        
        grid_list = wx.FlexGridSizer(1, 7, 0, 0)
        grid_list.Add(descript, 1, wx.ALL, 5)
        grid_list.Add(red, 1,wx.ALL, 5)
        grid_list.Add(txtred, 1,wx.ALL, 5)
        
        grid_list.Add(grey, 1,wx.ALL, 5)
        grid_list.Add(txtgrey, 1,wx.ALL, 5)
        
        grid_list.Add(yell, 1,wx.ALL, 5)
        grid_list.Add(txtyell, 1,wx.ALL, 5)
        
        sizer.Add(grid_list, 0, wx.ALL, 5)
        
        sizer.Add(gridbtn, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=5)
        gridbtn.Add(self.button_close, 1, wx.ALL, 5)
        self.SetSizerAndFit(sizer)
        
        if OS == 'Darwin':
            normlist.SetFont(wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL))
            txtred.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtgrey.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtyell.SetFont(wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL))
        else:
            normlist.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL))
            txtred.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtgrey.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
            txtyell.SetFont(wx.Font(8, wx.SWISS, wx.ITALIC, wx.NORMAL))
        
        self.Bind(wx.EVT_BUTTON, self.on_close, self.button_close)
        self.Bind(wx.EVT_CLOSE, self.on_close) # controlla la chiusura (x)

        index = 0 
        if title == _('RMS-based volume statistics'):
            for i in data: #### populate dmx listctrl:
                normlist.InsertItem(index, i[0])
                normlist.SetItem(index, 1, i[1])
                normlist.SetItem(index, 2, i[2])
                if float(i[3]) == 0.0:# not changes
                    normlist.SetItemBackgroundColour(index, '#646464')#grey
                    normlist.SetItem(index, 3, i[3])
                else:
                    normlist.SetItem(index, 3, i[3])
                if float(i[4]) > 0.0:# is clipped red
                    normlist.SetItemBackgroundColour(index, '#e9504d')#red
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])
                
                if float(i[4]) < float(i[1]):#target/res inf. to maxvol
                    normlist.SetItemBackgroundColour(index, '#C6B426')# yellow
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])
                    
        elif title == _('PEAK-based volume statistics'):
            for i in data: #### populate dmx listctrl:
                normlist.InsertItem(index, i[0])
                normlist.SetItem(index, 1, i[1])
                normlist.SetItem(index, 2, i[2])
                normlist.SetItem(index, 3, i[3])
                if float(i[4]) == float(i[1]):#not changes
                    normlist.SetItemBackgroundColour(index, '#646464')# grey
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])
                if float(i[4]) < float(i[1]):#target/res inf. to maxvol
                    normlist.SetItemBackgroundColour(index, '#C6B426')# yellow
                    normlist.SetItem(index, 4, i[4])
                else:
                    normlist.SetItem(index, 4, i[4])
            
    #--------------------------------------------------------------# 
    def on_close(self, event):
        '''
        destroy dialog by button and the X
        '''
        self.Destroy()
        #event.Skip()

    #-------------------------------------------------------------------#
