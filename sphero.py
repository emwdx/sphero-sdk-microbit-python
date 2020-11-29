import busio
import struct

class LEDs:
    RIGHT_HEADLIGHT = [0x00, 0x00, 0x00, 0x07]
    LEFT_HEADLIGHT = [0x00, 0x00, 0x00, 0x38]
    LEFT_STATUS = [0x00, 0x00, 0x01, 0xC0]
    RIGHT_STATUS = [0x00, 0x00, 0x0E, 0x00]
    BATTERY_DOOR_FRONT = [0x00, 0x03, 0x80, 0x00]
    BATTERY_DOOR_REAR = [0x00, 0x00, 0x70, 0x00]
    POWER_BUTTON_FRONT = [0x00, 0x1C, 0x00, 0x00]
    POWER_BUTTON_REAR = [0x00, 0xE0, 0x00, 0x00]
    LEFT_BRAKELIGHT = [0x07, 0x00, 0x00, 0x00]
    RIGHT_BRAKELIGHT = [0x38, 0x00, 0x00, 0x00]


class RawMotorModes:
    OFF = 0
    FORWARD = 1
    BACKWARD = 2


class RVR:

    def __init__(self, tx, rx):
        self._uart = busio.UART(tx, rx, baudrate=115200)



    def drive(self, speed, heading):

        flags = 0x00

        if speed < 0:
            speed *= -1
            heading += 180
            heading %= 360
            flags = 0x01

        drive_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x07, 0x00,
            speed, heading >> 8, heading & 0xFF, flags
        ]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(drive_data))

        return


    def stop(self,heading):
        self.drive(0, heading)

        return


    def set_raw_motors(self, left_mode, left_speed, right_mode, right_speed):
        if left_mode < 0 or left_mode > 2:
            left_mode = 0

        if right_mode < 0 or right_mode > 2:
            right_mode = 0

        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x01, 0x00,
            left_mode, left_speed, right_mode, right_speed
        ]

        raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(raw_motor_data))

        return

    def float_to_hex(self,f):
        #return hex(struct.unpack('<I', struct.pack('<f', f))[0])
        result = bytearray(struct.pack('<f', f))

        return result

    def drive_to_position_si(self, heading,x, y, speed):
        raw_motor_data = [
            0x8D, 0x3E, 0x12, 0x01, 0x16, 0x38, 0x00]

        bytesHeading = self.float_to_hex(heading)
        bytesX = self.float_to_hex(x)
        bytesY = self.float_to_hex(x)
        bytesSpeed = self.float_to_hex(speed)
        header = bytearray(raw_motor_data)
        header.extend(bytesHeading)
        header.extend(bytesX)
        header.extend(bytesY)
        header.extend(bytesSpeed)
        ending = bytearray([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        header.extend(ending)
        #raw_motor_data.extend([~((sum(raw_motor_data) - 0x8D) % 256) & 0x00FF, 0xD8])
        print(header)
        self._uart.write(header)

    def reset_yaw(self):
        drive_data = [0x8D, 0x3E, 0x12, 0x01, 0x16, 0x06, 0x00]

        drive_data.extend([~((sum(drive_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(drive_data))

        return

    def set_all_leds(self, red, green, blue):
        led_data = [
            0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00,
            0x3F, 0xFF, 0xFF, 0xFF
        ]

        for _ in range (10):
            led_data.extend([red, green, blue])

        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(led_data))

        return


    def set_rgb_led_by_index(self, index, red, green, blue):
        led_data = [0x8D, 0x3E, 0x11, 0x01, 0x1A, 0x1A, 0x00]

        led_data.extend(index)
        led_data.extend([red, green, blue])
        led_data.extend([~((sum(led_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(led_data))

        return

    def wake(self):
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x0D, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(power_data))

        return


    def sleep(self):
        power_data = [0x8D, 0x3E, 0x11, 0x01, 0x13, 0x01, 0x00]
        power_data.extend([~((sum(power_data) - 0x8D) % 256) & 0x00FF, 0xD8])

        self._uart.write(bytearray(power_data))

        return
