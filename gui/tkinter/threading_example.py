import tkinter as tk
from concurrent import futures
import time
import functools

thread_pool_executor = futures.ThreadPoolExecutor(max_workers=1)


def tk_after(target):

    @functools.wraps(target)
    def wrapper(self, *args, **kwargs):
        args = (self,) + args
        self.after(0, target, *args, **kwargs)

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


class MainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = tk.Label(self, text='not running')
        self.label.pack()
        self.listbox = tk.Listbox(self)
        self.listbox.pack()
        self.button = tk.Button(
            self, text='blocking task', command=self.on_button)
        self.button.pack(pady=15)
        self.pack()

    def on_button(self):
        print('Button clicked')
        self.blocking_code()

    @tk_after
    def set_label_text(self, text=''):
        self.label['text'] = text

    @tk_after
    def listbox_insert(self, item):
        self.listbox.insert(tk.END, item)
        print(item)

    @submit_to_pool_executor(thread_pool_executor)
    def blocking_code(self):
        self.set_label_text('running')

        for number in range(5):
            self.listbox_insert(number)
            time.sleep(1)

        self.set_label_text('not running')


if __name__ == '__main__':
    app = tk.Tk()
    main_frame = MainFrame()
    app.mainloop()
