import wx
import wx.gizmos
import wx.richtext
import os
from useCaseModel import *
from AlternativeFlowDialog import *

ID_SAVE = 510

def create( parent ):
    return UseCaseEditorFrame( parent )

class STARRichTextCtrl( wx.richtext.RichTextCtrl ):
        
    def HilightAll( self, searchString, style ):
        start = 0
        text = self.GetRange( start, self.GetLastPosition() )
        while text.find( searchString, start ) > -1:
            beginning = text.find( searchString, start )
            end = beginning + len( searchString )
            self.SetStyle( wx.richtext.RichTextRange( beginning, end ), style )
            start = end
        

class UseCaseEditorFrame(wx.Frame):
    
    def __init__(self, parent):
        self._init_ctrls(parent)
        self._init_styles()
        self.currentItem = None

    def _init_styles( self ):
        # Create the normal style
        self.normalStyle = wx.richtext.RichTextAttr()
        self.normalStyle.SetTextColour( wx.BLACK )
        self.normalStyle.SetBackgroundColour( wx.WHITE )	

        self.headerStyle = wx.richtext.RichTextAttr()
        self.headerStyle.SetTextColour( wx.BLACK )
        self.headerStyle.SetBackgroundColour( wx.WHITE )       
        self.headerStyle.SetFontWeight( wx.BOLD ) # possible values wx.NORMAL, wx.LIGHT, wx.BOLD, wx.MAX
        
        self.actorStyle = wx.richtext.RichTextAttr()
        self.actorStyle.SetTextColour( wx.BLUE )
        self.actorStyle.SetBackgroundColour( wx.WHITE )       
        
        self.useCaseStyle = wx.richtext.RichTextAttr()
        self.useCaseStyle.SetTextColour( wx.GREEN )
        self.useCaseStyle.SetBackgroundColour( wx.WHITE )       

    def _init_sizers(self):
        self.topPanelBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.topPanelBoxSizer.AddWindow(self.splitterWindow2, 1, border=2,flag=wx.EXPAND | wx.ALIGN_RIGHT | wx.ALIGN_LEFT)

        self.leftPanelBoxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
        self.leftPanelBoxSizer.AddWindow(self.modelNotebook, 1, border=1, flag=wx.ALIGN_TOP | wx.ALIGN_BOTTOM | wx.EXPAND)

        self.rightPanelBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.rightPanelBoxSizer.AddWindow(self.specificationNotebook, 1, border=1, flag=wx.ALIGN_TOP | wx.ALIGN_BOTTOM | wx.EXPAND)

        self.bottomPanelBoxSizer = wx.BoxSizer(orient=wx.VERTICAL)
        self.bottomPanelBoxSizer.AddWindow(self.qualityNotebook, 1, border=0, flag=wx.EXPAND | wx.ALIGN_TOP | wx.ALIGN_BOTTOM)

        self.topPanel.SetSizer(self.topPanelBoxSizer)
        self.bottomPanel.SetSizer(self.bottomPanelBoxSizer)
        self.leftPanel.SetSizer(self.leftPanelBoxSizer)
        self.rightPanel.SetSizer(self.rightPanelBoxSizer)

    def _init_ctrls(self, prnt):
        wx.Frame.__init__(self, id=-1, name='', parent=prnt, style=wx.DEFAULT_FRAME_STYLE, title='STAR Use Case Editor')
        self.SetClientSize(wx.Size(800, 600))

        # Set up the horizontal split into top and bottom panels       
        self.splitterWindow1 = wx.SplitterWindow(id=-1, name='splitterWindow1', parent=self, style=wx.SP_3D)
        self.topPanel = wx.Panel(id=-1, name='topPanel', parent=self.splitterWindow1, style=wx.TAB_TRAVERSAL)
        self.bottomPanel = wx.Panel(id=-1, name='bottomPanel', parent=self.splitterWindow1, style=wx.TAB_TRAVERSAL)
        self.splitterWindow1.SplitHorizontally(self.topPanel, self.bottomPanel, 500)

        # Set up the vertical split into left and right panels       
        self.splitterWindow2 = wx.SplitterWindow(id=-1, name='splitterWindow2', parent=self.topPanel, style=wx.SP_3D)
        self.leftPanel = wx.Panel(id=-1, name='leftPanel', parent=self.splitterWindow2, style=wx.TAB_TRAVERSAL)
        self.rightPanel = wx.Panel(id=-1, name='rightPanel', parent=self.splitterWindow2, style=wx.TAB_TRAVERSAL)
        self.splitterWindow2.SplitVertically(self.leftPanel, self.rightPanel, 200)

        # Set up the quality notebook
        self.qualityNotebook = wx.Notebook(id=-1, name='notebook1', parent=self.bottomPanel, style=0)
        self.qualityNotebook.SetFitToCurrentPage(True)
        self.qualityNotebook.SetAutoLayout(True)
        # Add the quality page        
        self.qrtc = wx.richtext.RichTextCtrl(id=-1, parent=self.qualityNotebook, style=wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS, value='')
        self.qualityNotebook.AddPage(imageId=-1, page=self.qrtc, select=True, text='Quality hints')

        # Set up the model notebook. This has a tree list containing the use case model
        self.modelNotebook = wx.Notebook(id=-1, name='notebook2', parent=self.leftPanel, style=0)
        self.modelNotebook.SetAutoLayout(True)
        self.modelTree = wx.TreeCtrl( id=-1, name='modelTree', parent=self.modelNotebook )
        self.modelNotebook.AddPage(imageId=-1, page=self.modelTree, select=True,text='Use case model')
        
        # Set up the specification notebook        
        self.specificationNotebook = wx.Notebook(id=-1, name='notebook3', parent=self.rightPanel, style=0)
        self.specificationNotebook.SetFitToCurrentPage(True)
        self.specificationNotebook.SetAutoLayout(True)
        # Add the specification page                
        self.rtc = STARRichTextCtrl(id=-1, parent=self.specificationNotebook, style=wx.VSCROLL|wx.HSCROLL|wx.WANTS_CHARS, value='')
        self.specificationNotebook.AddPage(imageId=-1, page=self.rtc, select=True, text='Specification')

        self._init_sizers()
        self._init_menuBar()
        self._init_treeEvents()

    def _init_menuBar( self ):
                
        # Setting up the file menu.
        self.fileMenu = wx.Menu()
        self.Bind( wx.EVT_MENU, self.OnFileOpenUseCaseModel, self.fileMenu.Append(-1, "&Open use case model\tCtrl+O", "Open an existing use case model") )
        self.Bind( wx.EVT_MENU, self.OnFileNewUseCaseModel, self.fileMenu.Append(-1, "&New use case model\tCtrl+N", "Create a new use case model") )
        self.Bind( wx.EVT_MENU, self.OnFileSave, self.fileMenu.Append(ID_SAVE, "&Save\tCtrl+S", "Save the current item") )
        self.fileMenu.AppendSeparator()
        self.Bind( wx.EVT_MENU, self.OnFileExit, self.fileMenu.Append(-1, "E&xit\tCtrl+Q", "Quit this program") )
  
        # Setting up the edit menu.        
        self.editMenu = wx.Menu()
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z") )
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_REDO, "&Redo\tCtrl+Y") )
        self.editMenu.AppendSeparator()
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_CUT, "Cu&t\tCtrl+X") )
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_COPY, "&Copy\tCtrl+C") )
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_PASTE, "&Paste\tCtrl+V") )
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_CLEAR, "&Delete\tDel") )
        self.editMenu.AppendSeparator()
        self.Bind( wx.EVT_MENU, self.ForwardEvent, self.editMenu.Append(wx.ID_SELECTALL, "Select A&ll\tCtrl+A") )

        # Setting up the new menu.        
        self.newMenu = wx.Menu()
        self.Bind( wx.EVT_MENU, self.NewActor, self.newMenu.Append(-1, "New &actor\tCtrl+A") )
        self.newMenu.AppendSeparator()
        self.Bind( wx.EVT_MENU, self.NewUseCase, self.newMenu.Append(-1, "New &use case\tCtrl+U") )
        self.Bind( wx.EVT_MENU, self.NewAlternativeFlow, self.newMenu.Append(-1, "New al&ternative flow\tCtrl+T") )
        self.Bind( wx.EVT_MENU, self.NewExtensionUseCase, self.newMenu.Append(-1, "New &extension use case\tCtrl+E") )
        self.newMenu.AppendSeparator()
        self.Bind( wx.EVT_MENU, self.DeleteModelElement, self.newMenu.Append(-1, "&Delete model element\tCtrl+D") )
      
        # Creating the menubar.
        mb = wx.MenuBar()
        mb.Append(self.fileMenu, "&File")
        mb.Append(self.editMenu, "&Edit")
        mb.Append(self.newMenu, "&Model element")

        # Adding the MenuBar to the Frame.
        self.SetMenuBar( mb )    
        
        # Disable the fileMenu:Save, editMenu and newMenu.
        self.enableMenuItems( self.editMenu, False ) 
        self.enableMenuItems( self.newMenu, False )  
        self.fileMenu.Enable( ID_SAVE, False )         
     
        
    def _init_treeEvents( self ):
        self.Bind( wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelectionChanged, self.modelTree ) 
        
    def enableMenuItems( self, menu, state ):
        for item in menu.GetMenuItems():
            item.Enable( state )
        
    def nameAvailable( self, name ):
        if self.useCaseModel.containsName( name ):
            dlg = wx.MessageDialog( None, "This name is already in use.", "Name in use", wx.OK | wx.ICON_ERROR )
            dlg.ShowModal()
            dlg.Destroy()
            return False
        else:
            return True
        
    def DeleteModelElement( self, evt ):
        if not self.currentItem:
            dlg = wx.MessageDialog( None, "Please select an item in the tree to delete ", "No item selected", style=wx.OK | wx.ICON_ERROR )
            dlg.Destroy()
            return
        dlg = wx.MessageDialog( None, "Are you sure you want to delete " + self.currentItem.getName(), "Are you sure you want to delete this item?", style=wx.OK | wx.CANCEL | wx.ICON_QUESTION )
        if dlg.ShowModal() == wx.ID_OK:
            # If item has children            
            if self.useCaseModel.itemHasChildren( self.currentItem ):         
                d = wx.MessageDialog( None, "This item has children. Please delete the children first.", "Can't delete item", style=wx.OK | wx.ICON_ERROR )
                d.ShowModal()
                d.Destroy()
                return
            # If item is included
            if self.useCaseModel.itemIsIncluded( self.currentItem ):  
                includingUseCaseNames = self.useCaseModel.getIncludingUseCaseNamesForItem( self.currentItem ) 
                d = wx.MessageDialog( None, "This item is included by the following use cases: " + ", ".join( includingUseCaseNames ), "Can't delete item", style=wx.OK | wx.ICON_ERROR )
                d.ShowModal()
                d.Destroy()
                return            
            # If item has alternative flows
            if self.useCaseModel.itemHasAlternativeFlows( self.currentItem ):         
                d = wx.MessageDialog( None, "This item has alternative flows. Please delete the alternative flows first.", "Can't delete item", style=wx.OK | wx.ICON_ERROR )
                d.ShowModal()
                d.Destroy()
                return
            # If item is an actor and it is being used by one or more use cases
            if self.useCaseModel.actorIsInUse( self.currentItem ):  
                usingUseCaseNames = self.useCaseModel.getUsingUseCaseNamesForActor( self.currentItem )
                d = wx.MessageDialog( None, "This actor is in use by the following use cases: " + ", ".join( usingUseCaseNames ) , "Can't delete item", style=wx.OK | wx.ICON_ERROR )
                d.ShowModal()
                d.Destroy()
                return
            
        dlg.Destroy()
        
        # If we haven't returned yet, then it's OK to delete the item            
        self.useCaseModel.removeItem( self.currentItem )
        self.modelTree.Delete( self.currentItem.getTreeItem() )
        self.currentItem = None
        self.rtc.Clear()  # Clear the buffer
        self.qrtc.Clear() # Clear the quality buffer
             
        
    def NewActor( self, evt ):
        dialog = wx.TextEntryDialog( None, "Enter the new actor name", "New actor", style=wx.OK | wx.CANCEL )
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetValue()
            dialog.Destroy()
            if self.nameAvailable( name ):
                item = self.useCaseModel.newActor( name )
                treeItem = self.modelTree.AppendItem( self.actorsBranch, item.getName() )
                item.setTreeItem( treeItem )
                self.modelTree.SelectItem( treeItem )
    
    def NewUseCase( self, evet ):
        dialog = wx.TextEntryDialog( None, "Enter the new use case name", "New use case", style=wx.OK | wx.CANCEL )
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetValue()
            dialog.Destroy()
            if self.nameAvailable( name ):
                item = self.useCaseModel.newUseCase( name )
                treeItem = self.modelTree.AppendItem( self.useCasesBranch, item.getName() )
                item.setTreeItem( treeItem )
                self.modelTree.SelectItem( treeItem )

    def NewAlternativeFlow( self, evet ):
        dialog = AlternativeFlowDialog( None, self.useCaseModel.getUseAllCaseNames() )
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.getAlternativeFlowName()
            dialog.Destroy()
            if self.nameAvailable( name ):
                item = self.useCaseModel.newAlternativeFlow( name )
                baseUseCase = self.useCaseModel.getUseCase( item.getBaseUseCaseName() )
                treeItem = self.modelTree.AppendItem( baseUseCase.getTreeItem(), item.getName() )
                item.setTreeItem( treeItem )
                self.modelTree.SelectItem( treeItem )
    
    def NewExtensionUseCase( self, evet ):
        dialog = wx.TextEntryDialog( None, "Enter the new extension use case name", "New extension use case", style=wx.OK | wx.CANCEL )
        if dialog.ShowModal() == wx.ID_OK:
            name = dialog.GetValue()
            dialog.Destroy()            
            if self.nameAvailable( name ):
                item = self.useCaseModel.newExtensionUseCase( name )
                treeItem = self.modelTree.AppendItem( self.extensionUseCasesBranch, item.getName() )
                item.setTreeItem( treeItem )
                self.modelTree.SelectItem( treeItem )
        
    def OnTreeSelectionChanged( self, evt ):
        # If this is the first time in, there is no currentItem
        if not self.currentItem:
            self.currentItem = self.useCaseModel.getItem( self.modelTree.GetItemText( evt.GetItem() ) )
        # If the existing buffer has been modified, we need to deal with it
        if self.rtc.IsModified():
            # Ask if the changes should be saved
            dialog = wx.MessageDialog( None, "Save changes", "Save changes", style=wx.YES_NO | wx.ICON_QUESTION )
            if dialog.ShowModal() == wx.ID_YES:
                self.OnFileSave( None ) # Save the changes
                self.rtc.DiscardEdits()
            dialog.Destroy()
        # Load the new item            
        self.currentItem = self.useCaseModel.getItem( self.modelTree.GetItemText( evt.GetItem() ) )
        if self.currentItem:                   
            self.rtc.Clear() # Clear the buffer  
            self.rtc.AppendText( self.currentItem.toString() )
            self.Hilight()
            # The newly loaded buffer hasn't been edited yet           
            self.rtc.DiscardEdits() 
            self.QualityReport()
            
    def QualityReport( self ):
        # Quality report   
        self.qrtc.Clear()        
        self.qrtc.AppendText( self.currentItem.getQualityReport() )

    def OnFileOpenUseCaseModel( self, evt ):
        dialog = wx.DirDialog( None, "Choose a directory containing a use case model:", style = wx.DD_DIR_MUST_EXIST)
        if dialog.ShowModal() == wx.ID_OK:
            self.LoadUseCaseModel( dialog.GetPath() )
            self.enableMenuItems( self.editMenu, True ) 
            self.enableMenuItems( self.newMenu, True ) 
            self.fileMenu.Enable( ID_SAVE, True )           
        dialog.Destroy()
        
    def OnFileNewUseCaseModel( self, evt ):
        dialog = wx.DirDialog( None, "Choose or create a directory for a use case model:" )
        if dialog.ShowModal() == wx.ID_OK:
            self.LoadUseCaseModel( dialog.GetPath() ) 
            self.enableMenuItems( self.editMenu, True ) 
            self.enableMenuItems( self.newMenu, True )  
            self.fileMenu.Enable( ID_SAVE, True )         
        dialog.Destroy()     

    def LoadUseCaseModel( self, directory ):
        # Load the model
        self.useCaseModel = UseCaseModel( directory )
        self.RefreshTree()
        
    def RefreshTree( self ):
        # Clean up        
        self.modelTree.DeleteAllItems()
        self.rtc.Clear()
        self.qrtc.Clear()
        self.selectedItem = None
        # Set up the tree branches                
        self.root = self.modelTree.AddRoot( self.useCaseModel.getModelName() )
        self.actorsBranch = self.modelTree.AppendItem( self.root, "Actors" )
        self.useCasesBranch = self.modelTree.AppendItem( self.root, "Use cases" ) 
        self.extensionUseCasesBranch = self.modelTree.AppendItem( self.root, "Extension use cases" ) 
        # Add the actors        
        for ac in self.useCaseModel.getActors():
            acItem = self.modelTree.AppendItem( self.actorsBranch, ac.getName() )
            ac.setTreeItem( acItem )
        # Add the use cases
        for uc in self.useCaseModel.getUseCases():
            ucItem = self.modelTree.AppendItem( self.useCasesBranch, uc.getName() )
            uc.setTreeItem( ucItem )
            # Add the alternative flows as children of the use cases
            for af in self.useCaseModel.getAlternativeFlowsForUseCase( uc.getName() ):
                afItem = self.modelTree.AppendItem( ucItem, af.getName() )
                af.setTreeItem( afItem )
        # Add the extension use cases
        for uc in self.useCaseModel.getExtensionUseCases():
            ucItem = self.modelTree.AppendItem( self.extensionUseCasesBranch, uc.getName() )
            uc.setTreeItem( ucItem )
            # Add the alternative flows as children of the use cases
            for af in self.useCaseModel.getAlternativeFlowsForUseCase( uc.getName() ):
                afItem = self.modelTree.AppendItem( ucItem, af.getName() )
                af.setTreeItem( afItem )
                
    def AppendItemToTree( self, branch, item ):
        self.modelTree.AppendItem( branch, item )
                        
    def OnFileSave( self, evt ):
        if self.currentItem:
            oldName = self.currentItem.getName() 
            self.currentItem.updateFromString( self.rtc.GetRange(0, self.rtc.GetLastPosition() ) )
            # If the current item is an alternative flow, the only way we can consistently change the base use case part of it's name is by
            # editing the base use case itself. Therefore if the base use case name has been edited, we must set it back to 
            # it's original value before we save.
            if self.currentItem.__class__ == AlternativeFlow:
                oldBaseName, oldFlowName = parseAlternativeFlowName( oldName )
                newBaseName, newFlowName = parseAlternativeFlowName( self.currentItem.getName() )
                if newBaseName != oldBaseName:
                    self.currentItem.changeName( oldBaseName + "_" + newFlowName )
                    dlg = wx.MessageDialog( None, "Sorry - you can't change the base use case for an alternative flow. The file has been saved, but the base use case has not been changed.", 
                                            "Can't change base use case", wx.OK | wx.ICON_ERROR )
                    dlg.ShowModal()
                    dlg.Destroy()
                    # We need to reload so the rtc is up to date
                    self.rtc.Clear() # Clear the buffer  
                    self.rtc.AppendText( self.currentItem.toString() )
            if oldName != self.currentItem.getName():
                # If we've changed the name of the model element we have to update the tree,
                # and everywhere the name is referenced in the use case model
                self.updateTreeWithItem( self.currentItem )
                # Update the base use cases of the alternative flows
                self.UpdateAlternativeFlowsBaseUseCaseName( oldName, self.currentItem.getName() )
                # Update all other references
                self.useCaseModel.replaceTerm( oldName, self.currentItem.getName() )
            # No changes
            self.rtc.DiscardEdits()
            self.QualityReport()
                    
    def UpdateAlternativeFlowsBaseUseCaseName( self, oldName, newName ):
        for af in self.useCaseModel.getAlternativeFlowsForUseCase( oldName ):
            af.changeBaseUseCaseName( newName )
            self.updateTreeWithItem( af )
            
    def updateTreeWithItem( self, item ):
        self.modelTree.SetItemText( item.getTreeItem(), item.getName() )

    def OnFileExit( self, evt ):
        self.Close( 1 )

    def ForwardEvent( self, evt ):
        self.rtc.ProcessEvent( evt )
            
    def Hilight( self ):
        self.rtc.SetStyle( wx.richtext.RichTextRange( 0, self.rtc.GetLastPosition() ), self.normalStyle )        
        for x in self.currentItem.getSectionHeaders(): self.rtc.HilightAll( x, self.headerStyle )   # Headers       
        for x in self.useCaseModel.getActorNames(): self.rtc.HilightAll( x, self.actorStyle )     # Use cases        
        for x in self.useCaseModel.getAllUseCaseNames(): self.rtc.HilightAll( x, self.useCaseStyle )   # Actors         


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = UseCaseEditorFrame( None )
    frame.Show()

    app.MainLoop()
