#Boa:Frame:Frame1

import wx

def create(parent):
    return Frame1(parent)

[wxID_FRAME1, wxID_FRAME1PANEL1, 
] = [wx.NewId() for _init_ctrls in range(2)]

class Frame1(wx.Frame):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Frame.__init__(self, id=wxID_FRAME1, name='', parent=prnt,
              pos=wx.Point(441, 306), size=wx.Size(492, 430),
              style=wx.DEFAULT_FRAME_STYLE, title='Frame1')
        self.SetClientSize(wx.Size(484, 396))

        self.panel1 = wx.Panel(id=wxID_FRAME1PANEL1, name='panel1', parent=self,
              pos=wx.Point(32, 24), size=wx.Size(200, 100),
              style=wx.TAB_TRAVERSAL)

    def __init__(self, parent):
        self._init_ctrls(parent)
