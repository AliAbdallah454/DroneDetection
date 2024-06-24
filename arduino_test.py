import pyfirmata2
import time

com_port = "COM10"

board = pyfirmata2.Arduino(com_port)

servo_y = board.get_pin('d:8:s')
servo_x = board.get_pin("d:10:s")

servo_x.write(90)
servo_y.write(90)
# while True:
#     angle = input(">> ")
#     x, y = angle.split(' ')
#     x = int(x)
#     y = int(y)
#     servo_x.write(x)
#     servo_y.write(y)

# time.sleep(1)

board.exit()