import wx
 
from python_logo import get_python_logo
 
 
class ImageFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SetIcon(get_python_logo.GetIcon())
        self.main_logo_image = wx.Image(get_python_logo.getImage())
        self.panel = wx.Panel(self)
        self.create_main_logo_static_bitmap()
        self.create_spin_button()
        self.add_sizers()
        self.SetInitialSize((300, 250))
 
    def create_main_logo_static_bitmap(self):
        self.static_bitmap = wx.StaticBitmap(
            self.panel, bitmap=self.main_logo_image.ConvertToBitmap())
 
    def create_spin_button(self):
        scaled_image = self.main_logo_image.Scale(
            32, 32, wx.IMAGE_QUALITY_HIGH)
        button_bitmap = scaled_image.ConvertToBitmap()
        self.spin_button = wx.Button(self.panel, label='Spin Logo')
        self.spin_button.SetBitmap(button_bitmap)
        self.spin_button.SetBitmapMargins(2, 2)
        self.spin_button.SetInitialSize()
        self.spin_button.Bind(wx.EVT_BUTTON, self.on_spin_button)
 
    def add_sizers(self):
        frame_sizer = wx.BoxSizer(wx.VERTICAL)
        frame_sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(frame_sizer)
 
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(main_sizer)
        main_sizer.AddSpacer(20)
 
        image_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_sizer.AddStretchSpacer(1)
        image_sizer.Add(self.static_bitmap)
        image_sizer.AddStretchSpacer(1)
        main_sizer.Add(image_sizer, flag=wx.EXPAND)
        main_sizer.AddSpacer(20)
 
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.AddStretchSpacer(1)
        button_sizer.Add(self.spin_button)
        button_sizer.AddStretchSpacer(1)
        main_sizer.Add(button_sizer, flag=wx.EXPAND)
 
        main_sizer.AddSpacer(20)
 
    def on_spin_button(self, event):
        self.main_logo_image = self.main_logo_image.Rotate90()
        self.static_bitmap.SetBitmap(self.main_logo_image.ConvertToBitmap())
 
 
if __name__ == '__main__':
    wx_app = wx.App(False)
    frame = ImageFrame(None, title='Image Frame')
    frame.Show()
    wx_app.MainLoop()