import board
import adafruit_dht
from time import sleep, time
import socketio

from celsiusclient.settings import HOST

dht_device = adafruit_dht.DHT22(board.D12)
# DHT22 sensor connected to GPIO12.
sio = socketio.Client()
sio.connect(HOST)
print("[press ctrl+c to end the script]")
last_update = 0
try: # Main program loop
    while True:
        try:
            temperature = dht_device.temperature
            humidity = dht_device.humidity
        except RuntimeError:
            print("Error")
            continue
        sleep(2.5)
        if humidity is not None and temperature is not None and 0 <= temperature <= 50:
            print("Temp={0:0.1f}*C  Humidity={1:0.1f}%"
                              .format(temperature, humidity))
            now = time()
            if now - last_update > 60:
                sio.emit('data', {'temperature': temperature, 'humidity': humidity})
                last_update = now
        else:
            print("Failed to get reading. Try again!")
# Scavenging work after the end of the program
except KeyboardInterrupt:
    print("Script end!")
