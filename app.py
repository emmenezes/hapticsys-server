from flask import Flask, request
from time import sleep
import json
import serial

RST_INPUT = "000000000000"

# mode = 'a'
mode = 'r'

serialPort = ''
if mode == 'a':
    serialPort = serial.Serial(
        port="/dev/ttyUSB0",
        baudrate=115200,
        bytesize=8,
        timeout=2,
        stopbits=serial.STOPBITS_ONE)


app = Flask(__name__)


@app.route('/custominput', methods=['POST'])
def custom_input():
    input = request.json['input']
    period = request.json['period']
    if mode == 'a':
        for sequence in input:
            serialPort.write(bytes(sequence, 'utf-8'))
            sleep(period)
    return json.dumps({'success': True, "message": f"Input recebido {input}, com periodo {period}"})


if __name__ == '__main__':
    app.run()
