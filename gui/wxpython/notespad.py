from pathlib import Path
 
import wx
 
WILDCARD = 'Text Documents (*.txt)|*.txt|Python Documents (*.py)|*.py'
UNTITLED = 'Untitled'
 
 
class Notespad(wx.Frame):
 
    def __init__(self, *args, **kwargs):
        super(Notespad, self).__init__(*args, **kwargs)
        self.path = None
        self.frame_settings()
        self.create_menu()
        self.create_gui_items()
        self.create_sizers()
        self.create_binds()
 
    def frame_settings(self):
        self.update_title()
        self.CreateStatusBar()
        self.SetMinSize((600, 400))
        self.CentreOnScreen()
 
    def create_menu(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        file_menu = wx.Menu()
        self.menu_new = file_menu.Append(wx.ID_NEW, '&New',
                                    'Creates a new document')
        self.menu_open = file_menu.Append(wx.ID_OPEN, '&Open',
                                     'Open an existing file')
        self.menu_save = file_menu.Append(wx.ID_SAVE, '&Save',
                                     'Saves the active document')
        self.menu_saveas = file_menu.Append(wx.ID_SAVEAS, 'Save &As',
                                'Saves the active document with a new name')
        file_menu.AppendSeparator()
        self.menu_exit = file_menu.Append(-1, 'E&xit', 'Exit the Application')
        menubar.Append(file_menu, '&File')
 
    def create_gui_items(self):
        self.frame_panel = wx.Panel(self)
        self.txt_ctrl = wx.TextCtrl(self.frame_panel,
                                    style=wx.TE_MULTILINE | wx.BORDER_NONE)
 
    def create_sizers(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.frame_panel, 1, wx.EXPAND)
        p_sizer = wx.BoxSizer(wx.VERTICAL)
        p_sizer.Add(self.txt_ctrl, 1, wx.EXPAND)
        self.frame_panel.SetSizer(p_sizer)
        self.SetSizer(sizer)
        self.Layout()
 
    def create_binds(self):
        self.Bind(wx.EVT_MENU, self.on_menu_new, self.menu_new)
        self.Bind(wx.EVT_MENU, self.on_menu_open, self.menu_open)
        self.Bind(wx.EVT_MENU, self.on_menu_save, self.menu_save)
        self.Bind(wx.EVT_MENU, self.on_menu_saveas, self.menu_saveas)
        self.Bind(wx.EVT_MENU, self.on_menu_exit, self.menu_exit)
 
        self.Bind(wx.EVT_CLOSE, self.on_close_evt)
 
    def on_menu_new(self, event):
        if self.save_if_modified():
            self.new()
 
    def on_menu_open(self, event):
        if self.save_if_modified():
            self.open()
             
    def on_menu_save(self, event):
        self.save()
         
    def on_menu_saveas(self, event):
        self.save_as()
 
    def on_menu_exit(self, event):
        self.Close()
 
    def on_close_evt(self, event):
        if event.CanVeto():
            if not self.save_if_modified():
                event.Veto()
                return
 
        self.Destroy()
 
    def update_title(self):
        name = UNTITLED
        if self.path:
            name = self.path.name
        self.SetTitle(f'{name} - Notespad')
 
    def save_changes_msg_dialog(self):
        path = self.path or UNTITLED
        dlg = wx.MessageDialog(
            self, (f'Do you want to save changes to {path}?'),
            'Notespad', wx.YES_NO | wx.CANCEL | wx.CENTER)
        dlg.SetYesNoLabels('Save', 'Don\'t Save')
        return dlg.ShowModal()
 
    def save_if_modified(self):
        saved_or_dont_save = True
        if self.txt_ctrl.IsModified():
            dlg_result = self.save_changes_msg_dialog()
            if dlg_result == wx.ID_CANCEL:
                saved_or_dont_save = False
            elif dlg_result == wx.ID_YES:
                self.save()
                if not self.path:
                    saved_or_dont_save = False
 
        return saved_or_dont_save
 
    def new(self):
        self.txt_ctrl.Clear()
        self.path = None
        self.update_title()
 
    def open(self):
        with wx.FileDialog(self, message='Open', wildcard=WILDCARD,
                           style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.path = Path(directory).joinpath(filename)
                self.txt_ctrl.LoadFile(str(self.path))
                self.update_title()
 
    def save(self):
        if not self.path:
            self.save_as()
        else:  #
            self.txt_ctrl.SaveFile(str(self.path))
            self.update_title()
 
    def save_as(self):
        with wx.FileDialog(self, message='Save as', wildcard=WILDCARD,
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.path = Path(directory).joinpath(filename)
                self.save()
 
 
if __name__ == '__main__':
    wx_app = wx.App(False)
    frame = Notespad(None)
    frame.Show()
    wx_app.MainLoop()