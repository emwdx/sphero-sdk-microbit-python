import board
import busio
import digitalio
import time
import sphero

#uart = busio.UART(board.D1, board.D0, baudrate=115200)
rvr = sphero.RVR(board.D1, board.D0)


'''
rvr.set_all_leds(255,0,0)
rvr.drive(50,0)
time.sleep(1.0)
rvr.set_all_leds(0,255,0)
rvr.drive(50,90)
time.sleep(1.0)
rvr.set_all_leds(255,255,0)
rvr.drive(50,180)
time.sleep(1.0)
rvr.set_all_leds(0,255,255)
rvr.drive(50,270)
time.sleep(1.0)
'''
rvr.drive_to_position_si(0.0,0.5,2.0,50.0)
