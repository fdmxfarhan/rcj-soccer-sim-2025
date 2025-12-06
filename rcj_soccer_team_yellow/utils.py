from math import *

# فاصله بین دو نقطه
def dist(x1, y1, x2, y2):
    return(sqrt((x1-x2)**2 + (y1-y2)**2))

def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

# آپدیت کردن دیتای سنسور ها و ارسال و دریافت دیتا به رباتهای دیگر
def readData(self):
    gps = self.get_gps_coordinates() # خواندن سنسور GPS
    self.heading = degrees(self.get_compass_heading()) # خواندن سنسور قطب نما
    if self.heading > 180: self.heading -= 360
    if self.heading <-180: self.heading += 360
    self.xr = gps[0] # x robot
    self.yr = gps[1] # y robot
    # اگر تیم آبی بودیم باید محور های مختصات قرینه بشه
    if self.robot.getName()[0] == 'B':
        self.xr *= -1
        self.yr *= -1
    if self.is_new_ball_data(): # اگر توپ دیده شد
        self.is_ball = True # متغیری که دیدن یا عدم دیدن توپ رو مشخص میکنه
        ball_data = self.get_new_ball_data()
        ball_angle = degrees(atan2(ball_data['direction'][1], ball_data['direction'][0]))
        ball_distance = abs(0.01666666/(abs(ball_data['direction'][2])/sqrt(1 - ball_data['direction'][2]**2)))
        self.xb = -sin(radians(ball_angle + self.heading)) * ball_distance + self.xr # x toop
        self.yb =  cos(radians(ball_angle + self.heading)) * ball_distance + self.yr # y toop
    else:
        self.is_ball = False
    # ارسال اطلاعات به روبات های دیگر
    self.send_data_to_team({
        "is_ball": self.is_ball,
        "xb": self.xb,
        "yb": self.yb,
        "xr": self.xr,
        "yr": self.yr,
        "id": int(self.robot.getName()[1])
    })
    # دریافت اطلاعات از ربات های دیگر
    while self.is_new_team_data(): # تازمانی که دیتای جدیدی از رباتهای دیگر وجود دارد
        team_data = self.get_new_team_data()['robot_id']
        if not self.is_ball and team_data['is_ball']:
            self.xb = team_data['xb']
            self.yb = team_data['yb']
            self.is_ball = True
    # if self.xb > 0.58: self.xb = 0.58
    # if self.xb < -0.58: self.xb = -0.58 
    # if self.yb > 0.62: self.yb = 0.62
    # if self.yb < -0.62: self.yb = -0.62
def move(self, xt, yt):
    at = degrees(atan2(self.xr - xt, yt - self.yr))
    e = at - self.heading
    if e > 180: e -= 360
    if e <-180: e += 360
    
    # Calculate distance to target
    distance = dist(self.xr, self.yr, xt, yt)
    
    # Base speed based on distance (faster when far, slower when close)
    # Cap the base speed at 10 and ensure it's at least 5
    base_speed = min(10, max(5, min(distance * 20, 10)))
    
    # Adjust turning speed based on angle error
    if abs(e) > 30:  # Sharp turn needed
        turn_speed = 10
    elif abs(e) > 10:  # Moderate turn
        turn_speed = 7
    else:  # Small adjustment
        turn_speed = 4
        
    # Apply movement
    if e > 10:
        motor(self, base_speed, -turn_speed)
    elif e < -10:
        motor(self, -turn_speed, base_speed)
    else:
        # When aligned, move forward with full speed
        motor(self, base_speed, base_speed)

def moveAndLook(self, xt, yt, xl, yl):
    at = degrees(atan2(self.xr - xt, yt - self.yr))
    e = at - self.heading
    if e > 180: e -= 360
    if e <-180: e += 360
    if dist(self.xr, self.yr, xt, yt) < 0.02:
        at = degrees(atan2(self.xr - xl, yl - self.yr))
        e = at - self.heading
        if e > 180: e -= 360
        if e <-180: e += 360
        motor(self, e, -e)
    elif e > 10: motor(self, 10, -10)
    elif e < -10:motor(self, -10, 10)
    else: motor(self, 10,10)
def motor(self, vl, vr):
    # Cap velocities at maximum of 10
    vl = max(-10, min(10, vl))
    vr = max(-10, min(10, vr))
    self.left_motor.setVelocity(vl)
    self.right_motor.setVelocity(vr)
def stop(self):
    motor(self, 0, 0)
def tarif_moteghayer(self):
    self.xb = 0 # x ball
    self.yb = 0 # y ball
    self.heading = 0 # zavieh robot
    self.xr = 0 # x robot
    self.yr = 0 # y robot
# آرایش دفاعی
def formation(self):
    if self.robot.getName()[1] == '3':
        moveAndLook(self, -0.4, -0.2, 0, 0.7)
    if self.robot.getName()[1] == '2':
        moveAndLook(self,  0.4, -0.2, 0, 0.7)
    if self.robot.getName()[1] == '1':
        moveAndLook(self, 0, -0.5, 0, 0.7)


