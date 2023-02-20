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


def generate_wave(m):
    return [f"{RST_INPUT[:n] + m + RST_INPUT[n+1:]}" for n in MODULES_SEQ]


def generate_wave_module(n, m):
    # TESTAR
    return [f"{RST_INPUT[:n] + v + RST_INPUT[n+1:]}" for v in range(1, m)]


serialPort = ''
if mode == 'a':
    serialPort = serial.Serial(
        port="/dev/ttyUSB0",
        baudrate=115200,
        bytesize=8,
        timeout=2,
        stopbits=serial.STOPBITS_ONE)


app = Flask(__name__)


@app.route('/test')
def test():
    serialPort.write(bytes("111111111111", 'utf-8'))
    return json.dumps({"message": "Sistema em estado 1"})


@app.route('/rst')
def rst():
    serialPort.write(bytes(RST_INPUT, 'utf-8'))
    return json.dumps({"message": "Sistema ressetado"})


@app.route('/max')
def max():
    serialPort.write(bytes("777777777777", 'utf-8'))
    return json.dumps({"message": "Sistema em estado 7"})


@app.route('/moduletst', methods=['POST'])
def module_test():
    period = request.json['period']
    module = request.json['module']
    magnitude = request.json['magnitude']
    wave_module_input = generate_wave_module(module, magnitude)
    for input in wave_module_input:
        serialPort.write(bytes(input, 'utf-8'))
        sleep(period)
    serialPort.write(bytes(RST_INPUT, 'utf-8'))
    return json.dumps({"message": f"Modulo {module} variou até o estado {magnitude}"})


@app.route('/waveinput', methods=['POST'])
def wave_input():
    period = request.json['period']
    magnitude = request.json['magnitude']
    wave_input = generate_wave(magnitude)
    if mode == 'r':
        return json.dumps({"message": f"Sistema executou onda de periodo {period} com magnitude {magnitude}"})
    for input in wave_input:
        serialPort.write(bytes(input, 'utf-8'))
        sleep(period)
    serialPort.write(bytes(RST_INPUT, 'utf-8'))
    return json.dumps({"message": f"Sistema executou onda de periodo {period} com magnitude {magnitude}"})

@app.route('/wavepropagation', methods=['POST'])
def wave_propagation():
    period = request.json['period']
    for input in WAVE_PROPAGATION_INPUT:
        serialPort.write(bytes(input, 'utf-8'))
        sleep(period)
    serialPort.write(bytes(RST_INPUT, 'utf-8'))
    return json.dumps({"message": f"Sistema executou onda de periodo {period}"})

@app.route('/custominput', methods=['POST'])
def custom_input():
    input = request.json['input']
    period = request.json['period']
    if mode == 'r':
        return json.dumps({'success': True, "message": f"Input recebido {input}, com periodo {period}"})
    for sequence in input:
        serialPort.write(bytes(sequence, 'utf-8'))
        sleep(period)
    return json.dumps({'success': True, "message": f"Input recebido {input}"})


if __name__ == '__main__':
    app.run()
