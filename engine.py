import random
import math
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

class SensorEngine(QObject):
    # This signal acts as a messenger to send a dictionary of data to the UI
    data_received = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self._generate_data)
        self.counter = 0

    def start(self):
        self.timer.start(1000)  # Updates every 1000ms (1 second)

    def stop(self):
        self.timer.stop()

    def _generate_data(self):
        self.counter += 1
        
        # We simulate 3 sensors as required by the exam:
        # Temperature: Baseline 25°C + sine wave drift + minor random noise
        # Humidity: Baseline 50% + random drift
        # Pressure: Stable around 1013 hPa
        data = {
            "temperature": round(25 + 5 * math.sin(self.counter / 10) + random.uniform(-0.5, 0.5), 2),
            "humidity": round(50 + 10 * math.sin(self.counter / 15) + random.uniform(-1, 1), 2),
            "pressure": round(1013 + random.uniform(-2, 2), 2)
        }
        
        # Emit the signal to any UI elements listening
        self.data_received.emit(data)