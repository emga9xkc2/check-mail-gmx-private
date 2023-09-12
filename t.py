from windows_toasts import WindowsToaster, ToastText1
wintoaster = WindowsToaster('Python')
newToast = ToastText1()
newToast.SetBody('Hello, world!')
newToast.on_activated = lambda _: print('Toast clicked!')
wintoaster.show_toast(newToast)
import time
time.sleep(10)
