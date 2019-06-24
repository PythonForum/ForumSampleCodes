import functools
import time
import tkinter as tk
from concurrent import futures

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


def func1():
    time.sleep(2)


def func2():
    time.sleep(3)


class MainFrame(tk.Frame):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.run_thread = False
        self.label = tk.Label(self, text='not running')
        self.label.pack()
        self.button = tk.Button(
            self, text='start task', command=self.on_button)
        self.button.pack(pady=15)
        self.pack()

    def on_button(self):
        if not self.run_thread:
            self.run_thread = True
            self.blocking_code()
            self.set_button_text('Stop task')
        else:
            self.run_thread = False
            self.set_button_state(False)
            self.set_button_text('Stopping')
            self.blocking_code_stopped()

    @tk_after
    def set_label_text(self, text=''):
        self.label['text'] = text

    @tk_after
    def set_button_text(self, text=''):
        self.button['text'] = text

    @tk_after
    def set_button_state(self, enable=True):
        state = 'normal' if enable else 'disable'
        self.button['state'] = state

    @submit_to_pool_executor(thread_pool_executor)
    def blocking_code(self):
        self.set_label_text('running')
        while self.run_thread:
            func1()
            self.set_label_text('func1 complete')
            func2()
            self.set_label_text('func2 complete')

    @submit_to_pool_executor(thread_pool_executor)
    def blocking_code_stopped(self):
        self.set_button_state(True)
        self.set_label_text('not running')
        self.set_button_text('Start task')


if __name__ == '__main__':
    app = tk.Tk()
    main_frame = MainFrame()
    app.mainloop()