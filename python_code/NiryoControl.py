from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSlider, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtCore import Qt
import serial
import serial.tools.list_ports
import threading
import sys


# Detect available serial ports
def get_serial_ports():
    return [port.device for port in serial.tools.list_ports.comports()]


# Initialize serial communication
def init_serial(port):
    try:
        ser = serial.Serial(port, 115200, timeout=1)
        return ser
    except serial.SerialException:
        print(f"Could not open serial port: {port}")
        return None


class StepperControllerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stepper Motor Controller")
        self.setGeometry(100, 100, 400, 400)  # Fixed window size
        self.serial_port = None
        self.sliders = {}
        self.value_labels = {}

        layout = QVBoxLayout()

        # Dropdown for Serial Port Selection
        self.port_dropdown = QComboBox()
        self.port_dropdown.addItems(get_serial_ports())
        self.port_dropdown.currentIndexChanged.connect(self.connect_serial)
        layout.addWidget(QLabel("Select Serial Port:"))
        layout.addWidget(self.port_dropdown)

        # Motor Sliders
        self.create_slider(layout, "Motor 1", 1)
        self.create_slider(layout, "Motor 2", 2)
        self.create_slider(layout, "Motor 3", 3)

        # Send Button
        self.send_button = QPushButton("Send Commands")
        self.send_button.clicked.connect(self.send_all_commands)
        layout.addWidget(self.send_button)

        # Reset Button
        self.reset_button = QPushButton("Reset Sliders")
        self.reset_button.clicked.connect(self.reset_sliders)
        layout.addWidget(self.reset_button)

        # Status Label
        self.status_label = QLabel("Select a Serial Port")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def create_slider(self, layout, label, motor):
        slider_layout = QHBoxLayout()

        label_widget = QLabel(label)
        slider_layout.addWidget(label_widget)

        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(-2000)
        slider.setMaximum(2000)
        slider.setValue(0)
        slider.valueChanged.connect(lambda value, m=motor: self.update_value_label(m, value))
        slider_layout.addWidget(slider)

        value_label = QLabel("0")
        slider_layout.addWidget(value_label)

        layout.addLayout(slider_layout)

        self.sliders[motor] = slider
        self.value_labels[motor] = value_label

    def update_value_label(self, motor, value):
        self.value_labels[motor].setText(str(value))

    def connect_serial(self):
        port = self.port_dropdown.currentText()
        if self.serial_port:
            self.serial_port.close()
        self.serial_port = init_serial(port)
        if self.serial_port:
            self.status_label.setText(f"Connected to {port}")
        else:
            self.status_label.setText("Connection Failed")

    def send_all_commands(self):
        if self.serial_port and self.serial_port.is_open:
            for motor, slider in self.sliders.items():
                steps = slider.value()
                threading.Thread(target=self.send_command, args=(motor, steps), daemon=True).start()

    def send_command(self, motor, steps):
        direction = "CW" if int(steps) > 0 else "CCW"
        steps = abs(int(steps))
        command = f"M{motor} {direction} {steps}\n"
        try:
            self.serial_port.write(command.encode())
            print(f"Sent: {command}")
        except serial.SerialException as e:
            print(f"Serial Error: {e}")
            self.status_label.setText("Serial Error")

    def reset_sliders(self):
        for motor, slider in self.sliders.items():
            slider.setValue(0)
        self.status_label.setText("Sliders Reset")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StepperControllerApp()
    window.show()
    sys.exit(app.exec_())
