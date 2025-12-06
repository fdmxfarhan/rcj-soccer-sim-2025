from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from math import *
from utils import *

class MyRobot1(RCJSoccerRobot):
    def __init__(self, robot):
        super().__init__(robot)
        self.manual_control = False
        
    def GoalKeeperAI(self):
        # If ball is in dangerous position (past penalty area)
        if self.yb < -0.4 and (self.xb > 0.3 or self.yb < -0.3):
            if self.xb > 0:
                move(self, 0.4, self.yb-0.2)
            else:
                move(self, -0.4, self.yb-0.2)
        # If goalkeeper is not on the penalty line
        elif self.yr > -0.5 or self.yr < -0.55:
            move(self, clamp(self.xb, -0.4, 0.4), -0.55)
        # If on penalty line, maintain position and face forward
        else:
            # Adjust heading to face forward (90 degrees)
            if self.heading > 95: 
                motor(self, -10, 10)
            elif self.heading < 85:
                motor(self, 10, -10)
            else:
                # If no ball data, assume ball is at center
                if not self.is_ball: 
                    self.xb = 0
                
                # Move horizontally to intercept ball
                if clamp(self.xb, -0.4, 0.4) > self.xr:
                    motor(self, -10, -10)
                else:
                    motor(self, 10, 10)
                    
    def run(self):
        tarif_moteghayer(self)
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                readData(self)
                if self.is_ball:
                    self.GoalKeeperAI()
                else:
                    formation(self)
