import wx
 
 
class MainFrame(wx.Frame):
 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panel_sizer)
        self.label = wx.StaticText(self.panel, label='Player 1 turn')
        self.panel_sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)
        self.button = wx.Button(self.panel, label='Player 1 Move')
        self.button.Bind(wx.EVT_BUTTON, self.on_button)
        self.panel_sizer.Add(self.button, 0, wx.ALL | wx.CENTER, 5)
        self.Layout()
        self.Show()
 
    def on_button(self, event):
        print('Button clicked')
        self.label.SetLabel('player 2 thinking')
        self.button.Disable()
        wx.CallLater(3000, self.delayed_player_2)
 
    def delayed_player_2(self):
        self.label.SetLabel('player 2 moving')
        wx.CallLater(1000, self.player_2_finsihed)
 
    def player_2_finsihed(self):
        self.label.SetLabel('player 1 turn')
        self.button.Enable()
 
 
if __name__ == '__main__':
    app = wx.App(False)
    main_frame = MainFrame(None)
    app.MainLoop()