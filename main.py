import sys
import pyqtgraph as pg
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, 
                             QPushButton, QWidget, QSlider, QHBoxLayout)
from PyQt6.QtCore import Qt
from engine import SensorEngine

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Device Monitor Dashboard")
        self.resize(500, 600)
        
        # Requirement #3: Data history for charting (last 20-30 points)
        self.temp_history = []
        self.threshold = 30.0 # Default warning threshold
        
        # Requirement #6: Separate logic/UI (Initialize engine)
        self.engine = SensorEngine()
        self.engine.data_received.connect(self.update_ui)
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        
        # Requirement #5: Status Indicator & Visual Warning
        self.status_label = QLabel("Status: Stopped")
        self.status_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        # Requirement #2: 3 Simulated Sensors
        self.temp_label = QLabel("Temperature: -- °C")
        self.humidity_label = QLabel("Humidity: -- %")
        self.pressure_label = QLabel("Pressure: -- hPa")
        for lbl in [self.temp_label, self.humidity_label, self.pressure_label]:
            layout.addWidget(lbl)

        # Requirement #3: Working Chart
        self.graph = pg.PlotWidget()
        self.graph.setBackground('w')
        self.graph.setTitle("Temperature Trends", color="b", size="12pt")
        self.curve = self.graph.plot(pen=pg.mkPen(color='b', width=2))
        layout.addWidget(self.graph)

        # Requirement #4: Secondary Control (Threshold Slider)
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(20, 40)
        self.slider.setValue(30)
        self.slider.valueChanged.connect(self.update_threshold)
        self.slider_label = QLabel(f"Warning Threshold: {self.threshold}°C")
        slider_layout.addWidget(self.slider_label)
        slider_layout.addWidget(self.slider)
        layout.addLayout(slider_layout)
        
        # Requirement #4: Start/Stop Button
        self.btn = QPushButton("Start Monitoring")
        self.btn.clicked.connect(self.toggle_engine)
        layout.addWidget(self.btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_threshold(self, value):
        self.threshold = float(value)
        self.slider_label.setText(f"Warning Threshold: {self.threshold}°C")

    def toggle_engine(self):
        if self.engine.timer.isActive():
            self.engine.stop()
            self.btn.setText("Start Monitoring")
            self.status_label.setText("Status: Stopped")
            self.status_label.setStyleSheet("color: gray;")
        else:
            self.engine.start()
            self.btn.setText("Stop Monitoring")
            self.status_label.setText("Status: Running")
            self.status_label.setStyleSheet("color: green;")

    def update_ui(self, data):
        temp = data['temperature']
        self.temp_label.setText(f"Temperature: {temp} °C")
        self.humidity_label.setText(f"Humidity: {data['humidity']} %")
        self.pressure_label.setText(f"Pressure: {data['pressure']} hPa")

        # Requirement #5: Visual Warning Logic
        if temp > self.threshold:
            self.temp_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.temp_label.setStyleSheet("color: black; font-weight: normal;")

        # Update Chart Data
        self.temp_history.append(temp)
        if len(self.temp_history) > 30:
            self.temp_history.pop(0)
        self.curve.setData(self.temp_history)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())