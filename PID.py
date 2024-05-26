import time

D_desired = 10.0  # Desired distance from the wall in cm
Kp = 1.0 # The responsiveness of the system
Ki = 0.2 # The accumulation of past errors
Kd = 0.4 # Controls damping effect, aka Presistance. Can make the system sluggish if too high
integral = 0.0
previous_error = 0.0
dt = 0.1

def read_distance_sensor():
    pass

def steer_robot(correction):
    pass

while True:
    D_actual = read_distance_sensor()

    error = D_desired - D_actual

    P = Kp * error

    integral += error * dt
    I = Ki * integral

    derivative = (error - previous_error) / dt
    D = Kd * derivative

    correction = P + I + D

    # Positive correction -> turn left
    # Negative correction -> turn right
    steer_robot(correction)

    previous_error = error

    time.sleep(dt)
