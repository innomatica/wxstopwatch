#!/usr/bin/env python3
from datetime import datetime
import time
import wx
import wx.lib.analogclock as ac

#--------1---------2---------3---------4---------5---------6---------7---------8
## MainFrame Window
#
class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title)

        self.clkMain = ac.AnalogClock(self, size=(300,300))
        self.lstLap = wx.ListCtrl(self, -1, style=wx.LC_REPORT)
        self.lstLap.InsertColumn(0, 'Time Stamp')
        self.lstLap.InsertColumn(1, 'Lap Time')
        self.lstLap.InsertColumn(2, 'Cumulative')
        self.lstLap.Hide()

        sizer_x = wx.BoxSizer(wx.HORIZONTAL)
        sizer_x.Add(self.clkMain, 1, wx.EXPAND)
        sizer_x.Add(self.lstLap, 0, wx.EXPAND)

        self.SetSizerAndFit(sizer_x)
        self.trs = 0xff
        self.Show()

        self.clkMain.Bind(wx.EVT_LEFT_DOWN, self.OnShowList)
        self.lstLap.Bind(wx.EVT_LEFT_DOWN, self.OnHideList)
        self.clkMain.Bind(wx.EVT_MOUSEWHEEL, self.OnTransparent)


    def OnShowList(self, evt):
        curr_ts = time.strftime('%H:%M:%S', time.localtime())
        idx = self.lstLap.GetItemCount()
        self.lstLap.InsertItem(idx, curr_ts )

        # compute lap time
        if idx == 0:
            self.lstLap.SetItem(0, 1, '0')
            self.lstLap.SetItem(0, 2, '0')
        else:
            init_ts = self.lstLap.GetItemText(0,0)
            prev_ts = self.lstLap.GetItemText(idx - 1, 0)

            init_tm = time.strptime(init_ts, '%H:%M:%S')
            prev_tm = time.strptime(prev_ts, '%H:%M:%S')
            curr_tm = time.strptime(curr_ts, '%H:%M:%S')

            diff = (curr_tm[3] * 3600 + curr_tm[4] * 60 + curr_tm[5]
                    - init_tm[3] * 3600 - init_tm[4] * 60 - init_tm[5])
            self.lstLap.SetItem(idx, 2, str(diff))

            diff = (curr_tm[3] * 3600 + curr_tm[4] * 60 + curr_tm[5]
                    - prev_tm[3] * 3600 - prev_tm[4] * 60 - prev_tm[5])
            self.lstLap.SetItem(idx, 1, str(diff))

        self.lstLap.Show()
        self.Fit()

    def OnHideList(self, evt):
        self.lstLap.Hide()
        self.Fit()
        self.lstLap.DeleteAllItems()

    def OnTransparent(self, evt):
        self.trs = self.trs + (evt.GetWheelRotation()) / 5
        if self.trs > 0xff:
            self.trs = 0xff
        elif self.trs < 0x30:
            self.trs = 0x30
        self.SetTransparent(self.trs)


#--------1---------2---------3---------4---------5---------6---------7---------8
if __name__=="__main__":

    app = wx.App()
    frame = MyFrame(None,
            "Clock(Time Stamp), List(Reset), Wheel(Transparancy)")

    app.MainLoop()
