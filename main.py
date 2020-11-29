import board
import busio
import digitalio
import time
import sphero

#uart = busio.UART(board.D1, board.D0, baudrate=115200)
rvrLED = sphero.RVRLed(board.D1, board.D0)
rvrDrive = sphero.RVRLed(board.D1, board.D0)


rvr.set_all_leds(255,0,0)
rvrDrive.drive(50,0)
time.sleep(1.0)
rvr.set_all_leds(0,255,0)
rvrDrive.drive(50,90)
time.sleep(1.0)
