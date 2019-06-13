import wx
 
 
class Notespad(wx.Frame):
  
    def __init__(self, *args, **kwargs):
        super(Notespad, self).__init__(*args, **kwargs)
        self.frame_settings()
        self.create_menu()
        self.create_gui_items()
        self.create_sizers()
          
    def frame_settings(self):
        self.SetTitle('Untitled - Notespad')
        self.CreateStatusBar()
          
    def create_menu(self):
        menubar = wx.MenuBar()
        self.SetMenuBar(menubar)
        file_menu = wx.Menu()
        menu_open = file_menu.Append(wx.ID_OPEN, '&Open',
                                     'Open an existing file')
         
        menu_new = file_menu.Append(wx.ID_NEW, '&New',
                                    'Creates a new document')  # 1
         
        file_menu.AppendSeparator()
        menu_exit = file_menu.Append(-1, 'E&xit', 'Exit the Application')
        menubar.Append(file_menu, '&File')
          
        self.Bind(wx.EVT_MENU, self.on_menu_exit, menu_exit)
        self.Bind(wx.EVT_MENU, self.on_menu_open, menu_open)
         
        self.Bind(wx.EVT_MENU, self.on_menu_new, menu_new)  # 2
          
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
  
    def on_menu_exit(self, event):
        self.Close()
        event.Skip()
  
    def on_menu_open(self, event):
        wildcard = 'Text Documents (*.txt)|*.txt|Python Documents (*.py)|*.py'
        with wx.FileDialog(self, message='Open', wildcard=wildcard,
                           style=wx.FD_OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.load_file_to_txt_ctrl(directory, filename)
                  
        event.Skip()
         
    def on_menu_new(self, event):  # 3
        self.txt_ctrl.Clear()  # 4
        self.SetTitle('Untitled - Notespad')  # 5
        event.Skip()  # 6
                  
    def load_file_to_txt_ctrl(self, directory, filename):
        self.txt_ctrl.LoadFile('/'.join((directory, filename)))
        self.SetTitle(f'{filename} - Notespad')
  
  
if __name__ == '__main__':
    wx_app = wx.App(False)
    frame = Notespad(None)
    frame.Show()
    wx_app.MainLoop()