#!/usr/bin/env python

import wx

import UseCaseEditorFrame

modules ={'UseCaseEditorFrame': [1, 'Main frame of Application', u'UseCaseEditorFrame.py']}

class UseCaseEditorApp(wx.App):
    def OnInit(self):
        self.main = UseCaseEditorFrame.create(None)
        self.main.Show()
        self.SetTopWindow(self.main)
        return True

def main():
    application = UseCaseEditorApp(0)
    application.MainLoop()

if __name__ == '__main__':
    main()
