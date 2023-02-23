from flask import Flask, request
from time import sleep
import json
import serial
import sys

MODULES_SEQ = [5, 4, 2, 3, 1, 0, 6, 7, 9, 8, 10, 11]
RST_INPUT = "000000000000"

WAVE_PROPAGATION_INPUT = [
    '720000000000',
    '272000000000',
    '027200000000',
    '002720000000',
    '000272000000',
    '000027200000',
    '000002720000',
    '000000272000',
    '000000027200',
    '000000002720',
    '000000000272',
    '000000000027',
]

# TODO: adicionar descrição das funções

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
    if mode == 'r':
        return json.dumps({'success': True, "message": f"Input recebido {input}, com periodo {period}"})
    for sequence in input:
        serialPort.write(bytes(sequence, 'utf-8'))
        sleep(period)
    return json.dumps({'success': True, "message": f"Input recebido {input}, com periodo {period}"})


if __name__ == '__main__':
    app.run()
