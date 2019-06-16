import wx
from concurrent import futures
import time
import functools

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


def wx_call_after(target):

    @functools.wraps(target)
    def wrapper(self, *args, **kwargs):
        args = (self,) + args
        wx.CallAfter(target, *args, **kwargs)

    return wrapper


def submit_to_pool_executor(executor):
    '''Decorates a method to be sumbited to the passed in executor'''
    def decorator(target):

        @functools.wraps(target)
        def wrapper(*args, **kwargs):
            result = executor.submit(target, *args, **kwargs)
            result.add_done_callback(executor_done_call_back)
            return result

        return wrapper

    return decorator


def executor_done_call_back(future):
    exception = future.exception()
    if exception:
        raise exception


class MainFrame(wx.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.panel = wx.Panel(self)
        self.panel_sizer = wx.BoxSizer(wx.VERTICAL)
        self.panel.SetSizer(self.panel_sizer)
        self.label = wx.StaticText(self.panel, label='not running')
        self.panel_sizer.Add(self.label, 0, wx.ALL | wx.CENTER, 5)
        self.listbox = wx.ListBox(self.panel)
        self.panel_sizer.Add(self.listbox, 1, wx.ALL | wx.CENTER, 5)
        self.button = wx.Button(self.panel, label='blocking task')
        self.button.Bind(wx.EVT_BUTTON, self.on_button)
        self.panel_sizer.Add(self.button, 0, wx.ALL | wx.CENTER, 5)
        self.Layout()
        self.Show()

    def on_button(self, event):
        print('Button clicked')
        self.blocking_code()

    @wx_call_after
    def set_label_text(self, text=''):
        self.label.SetLabel(text)

    @wx_call_after
    def listbox_insert(self, item):
        self.listbox.Append(item)
        print(item)

    @submit_to_pool_executor(thread_pool_executor)
    def blocking_code(self):
        self.set_label_text('running')

        for number in range(5):
            self.listbox_insert(str(number))
            time.sleep(1)

        self.set_label_text('not running')


if __name__ == '__main__':
    app = wx.App(False)
    main_frame = MainFrame(None)
    app.MainLoop()
