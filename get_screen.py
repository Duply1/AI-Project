import cv2
import numpy as np
import win32gui
import win32api
import win32ui
from win32.lib import win32con


def get_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        wid = x2 - left + 1
        high = y2 - top + 1
    else:
        wid = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        high = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)


    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, wid, high)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (wid, high), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmaps(True)
    img = np.fromstring(signedIntsArray, dtype='unit8')
    img.shape = (high, wid, 4)

    srcdc.DeleteDc()
    memdc.DeleteDc()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

