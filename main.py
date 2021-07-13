
import board
import busio
import time
import math

from api_sphero_message import Message
from drive import raw_motors, drive_to_position_si
uart = busio.UART(board.TX, board.RX, baudrate=115200)

def send_command(did, cid, seq, target, timeout=None, inputs=[], outputs=[]):
        """Creates a Message object using the provided parameters and sends it to the serial port.
        Args:
            did (uint8): Device ID
            cid (uint8): Command ID
            seq (uint8): Sequence Number
            target (uint8): 1 - Nordic; 2 - ST
            timeout (uint8): Time in seconds to wait for a response, if one is requested. Otherwise, ignored.
            inputs (list(Parameter)): Inputs for command that is being sent
            outputs (list(Parameter)): Expected outputs for command that is being sent
        """

        # TODO: implement timeout logic, which should remove any registered callbacks if timeout occurs.
        message = Message()
        message.did = did
        message.cid = cid
        message.seq = seq
        message.target = target
        message.is_activity = True
        #message.requests_response = len(outputs) > 0 or self.request_error_responses_only

        # Messages that already request a response due to expected outputs don't need this
        # extra flag. They will automatically respond with errors if any are generated.
        # This flag is meant only for commands with no expected output.
        message.requests_error_response = True #self.request_error_responses_only if len(outputs) == 0 else False

        for param in inputs:
            message.pack(param.data_type, param.value)

        return message

time.sleep(1.0)
SPEED = 0.4
TILE_WIDTH = 0.8
coordinates = [[0,0],[0,3],[2,3],[2,5],[0,5],[0,0]]
positions = []
for pair in coordinates:
    positions.append([0.0,pair[0]*TILE_WIDTH,pair[1]*TILE_WIDTH])
#positions = [[0.0,0.0,0.0],[90.0, 1.6,0.0],[0.0,1.6,0.8],[270.0,0,0.8],[0.0,0.0,0.0]]
commands = [drive_to_position_si(0.0, 1.6, 0.0, 0.25, 0, None, None),drive_to_position_si(0.0, 1.6, 0.8, 0.25, 0, None, None),drive_to_position_si(0.0, 0, 0.8, 0.25, 0, None, None),drive_to_position_si(0.0, 0.0, 0.0, 0.25, 0, None, None)]

for i in range(len(positions)):
    current_position = positions[i]
    next_position = positions[i+1]
    command = drive_to_position_si(next_position[0],next_position[1],next_position[2],SPEED,0,None,None)
    output = command
    output_command = send_command(output['did'], output['cid'], output['seq'], output['target'], None, output['inputs'])

    uart.write(output_command.serialise())
    response = bytearray(10)
    uart.readinto(response)
    dx = next_position[1] - current_position[1]
    dy = next_position[2] - current_position[2]
    travel_time = math.sqrt(dx*dx + dy*dy)/SPEED + 1.5
    print("Driving to {0},{1}, travel time {2}".format(next_position[1],next_position[2],travel_time))
    time.sleep(travel_time)


#output = raw_motors(1,127,1,65,None,None)

    #print(output_command.serialise())



    #print(response)
