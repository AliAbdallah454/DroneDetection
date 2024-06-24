import threading

def write_angle():
    while True:
        try:
            r = int(input(">> "))
            servo_x.write(r)
        except:
            servo_x.write(0)

motor_thread = threading.Thread(target=write_angle)
motor_thread.start()