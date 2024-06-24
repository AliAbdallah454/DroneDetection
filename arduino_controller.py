import pyfirmata2 as firmata

class arduino_controller:

    def __init__(self, com: str, x_servo_pin: int, y_servo_pin: int, laser_pin: int) -> None:
        try:
            self.board = firmata.Arduino(com)
            self.servo_x = self.board.get_pin(f"d:{x_servo_pin}:s")
            self.servo_y = self.board.get_pin(f"d:{y_servo_pin}:s") 
            self.laser = self.board.get_pin(f"d:{laser_pin}:o")
            self.laser.write(1)
        except:
            print("Something wrong")

    def move_x_servo(self, angle: int) -> None:
        self.servo_x.write(angle)
    
    def move_y_servo(self, angle: int) -> None:
        self.servo_y.write(angle)

    def move_servos(self, x_angle: int, y_angle: int) -> None:
        self.servo_x.write(x_angle)
        self.servo_y.write(y_angle)