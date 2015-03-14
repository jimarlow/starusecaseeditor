#Boa:Dialog:AlternativeFlowDialog

import wx

def create(parent):
    return AlternativeFlowDialog(parent)


class AlternativeFlowDialog(wx.Dialog):
    def _init_ctrls(self, prnt):
        # generated method, don't edit
        wx.Dialog.__init__(self, id=-1,
              name='AlternativeFlowDialog', parent=prnt, pos=wx.Point(858, 481),
              size=wx.Size(420, 149), style=wx.DEFAULT_DIALOG_STYLE,
              title='New alternative flow')
        self.SetClientSize(wx.Size(412, 115))
        self.SetAutoLayout(True)
        self.Center(wx.BOTH)
        self.SetHelpText('Create a new alternative flow')
        self.SetToolTipString('New alternative flow')

        self.baseUseCaseComboBox = wx.ComboBox(choices=self.items,
              id=-1,
              name='baseUseCaseComboBox', parent=self, pos=wx.Point(16, 40),
              size=wx.Size(176, 21), style=0, value='')
        self.baseUseCaseComboBox.SetLabel('')

        self.staticText1 = wx.StaticText(id=-1,
              label='_', name='staticText1', parent=self, pos=wx.Point(200, 40),
              size=wx.Size(10, 23), style=0)
        self.staticText1.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))

        self.alternativeFlowNameTextCtrl = wx.TextCtrl(id=-1,
              name='alternativeFlowNameTextCtrl', parent=self, pos=wx.Point(224,
              40), size=wx.Size(176, 21), style=0, value='')

        self.staticText2 = wx.StaticText(id=-1,
              label='BaseUseCaseName_AlternativeFlowName', name='staticText2',
              parent=self, pos=wx.Point(40, 8), size=wx.Size(342, 23), style=0)
        self.staticText2.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.NORMAL,
              False, 'Tahoma'))

        self.okButton = wx.Button(id=wx.ID_OK,
              label='OK', name='button1', parent=self, pos=wx.Point(64, 80),
              size=wx.Size(75, 23), style=0)
        self.okButton.SetDefault()

        self.cancelButton = wx.Button(id=wx.ID_CANCEL,
              label='Cancel', name='button2', parent=self, pos=wx.Point(272,
              80), size=wx.Size(75, 23), style=0)
              
    def __init__(self, parent, items):
        self.items = items
        self._init_ctrls(parent)
        
    def getAlternativeFlowName( self ):
        baseUseCaseName = self.baseUseCaseComboBox.GetValue()
        alternativeFlowName = self.alternativeFlowNameTextCtrl.GetValue()
        if baseUseCaseName == "" or alternativeFlowName == "":
            return None
        else:
            return baseUseCaseName + "_" + alternativeFlowName
