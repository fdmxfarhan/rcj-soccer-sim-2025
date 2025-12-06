import math
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from math import *
from utils import *
Use_Pass = True
class MyRobot2(RCJSoccerRobot):
    def run(self):
        tarif_moteghayer(self)
        while self.robot.step(TIME_STEP) != -1:  # تا زمانی که بازی در حال اجراست
            if self.is_new_data():  # اگر دیتای جدیدی آماده خواندن بود
                readData(self)
                if self.is_ball:
                    if self.xb < 0 and self.yb > -0.15 and Use_Pass:  # اگر توپ در سمت مثبت محور x باشد
                        if dist(self.xb, self.yb, self.xr, self.yr) > 0.2:  # اگر توپ دور از ربات باشد
                            move(self, 0, self.yb - 0.1)
                        else:  # اگر توپ نزدیک ربات باشد
                            move(self, 0, self.yb)
                    else:
                        if self.yr > self.yb:
                            if self.xr > self.xb:
                                move(self, self.xb + 0.15, self.yb)
                            else:
                                move(self, self.xb - 0.15, self.yb)
                        else:
                            if dist(self.xb, self.yb, self.xr, self.yr) > 0.2 and abs(self.xr - self.xb) > 0.1:
                                move(self, self.xb, self.yr)
                            else:
                                move(self, self.xb, self.yb)
                else:
                    formation(self)