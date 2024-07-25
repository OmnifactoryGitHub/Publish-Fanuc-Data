import paho.mqtt.client as mqtt
from datetime import datetime
import time
import json
from Read_Robot_Data import FanucReaderCSV, FanucReaderRPI
import Calc_Robot_Indices as ri

class RobotOperation:
    UPDATE_TIME = 1

    def __init__(self, rpi=True):
        # Get the fanuc reader
        self.fanuc_reader = FanucReaderRPI(
            robot_model="Fanuc",
            host="127.0.0.1",
            port=18736,
            ee_DO_type="RDO",
            ee_DO_num=7,
        )
        self.previous_cost = 0
        self.previous_time = -1
        self.previous_velocity = None
        self.previous_reading = None

        # MQTT setup
        self.broker_address = "localhost"  # or the IP address of your broker
        self.broker_port = 1883  # The standard MQTT port
        self.topic = "mir/data"

        # Create a new instance of the client
        self.mqtt_client = mqtt.Client("python_publisher")  # client_id

        # Connect to the broker
        self.mqtt_client.connect(self.broker_address, self.broker_port, 60)

    def perform_calculations(self):
        while True:
            # Compute fields
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            current_time = time.time()
            current_reading = self.fanuc_reader.get_next_reading()

            # Print current readings
            print(f"Time: {current_datetime}")
            current_X = current_reading.get('X', None)
            current_Y = current_reading.get('Y', None)
            current_Z = current_reading.get('Z', None)
            current_rdo = current_reading.get('rdo', None)
            current_rdi101 = current_reading.get('rdi101', None)
            current_rdi102 = current_reading.get('rdi102', None)
            current_rdi103 = current_reading.get('rdi103', None)
            current_rdi104 = current_reading.get('rdi104', None)
            current_rdi105 = current_reading.get('rdi105', None)
            current_rdi106 = current_reading.get('rdi106', None)
            current_rdi107 = current_reading.get('rdi107', None)
            current_rdi108 = current_reading.get('rdi108', None)
            current_do101 = current_reading.get('do101', None)
            current_do102 = current_reading.get('do102', None)
            print(f"current_X = {current_X}")
            print(f"current_Y = {current_Y}")
            print(f"current_Z = {current_Z}")

            if self.previous_time != -1:
                dt = current_time - self.previous_time

                current_velocity = ri.compute_velocity(self.previous_reading, current_reading, dt)
                current_acceleration = ri.compute_acceleration(self.previous_velocity, current_velocity, dt)
                cost = ri.compute_energy_cost(current_reading, self.previous_cost, dt)

                # Print computed values
                print(f"Velocity: {current_velocity}")
                print(f"Acceleration: {current_acceleration}")
                print(f"Energy Cost: {cost}")

                # Prepare payload
                payload = {
                    "timestamp": current_datetime,
                    "velocity": current_velocity,
                    "acceleration": current_acceleration,
                    "energy_cost": cost,
                    "rdo": current_rdo,
                    "rdi101": current_rdi101,
                    "rdi102": current_rdi102,
                    "rdi103": current_rdi103,
                    "rdi104": current_rdi104,
                    "rdi105": current_rdi105,
                    "rdi106": current_rdi106,
                    "rdi107": current_rdi107,
                    "rdi108": current_rdi108,
                    "do101": current_do101,
                    "do102": current_do102
                }

                # Publish to MQTT
                self.mqtt_client.publish(self.topic, json.dumps(payload))
                print(f"Published: {json.dumps(payload)}")  # Optional: Print the payload for verification

                # Update the previous values
                self.previous_velocity = current_velocity
                self.previous_cost += cost['cost']

            print("-" * 40)

            # Sleep to maintain the update interval
            time.sleep(self.UPDATE_TIME)
            self.previous_time = current_time
            self.previous_reading = current_reading

if __name__ == '__main__':
    robot_operation = RobotOperation(rpi=True)
    robot_operation.perform_calculations()
