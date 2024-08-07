from datetime import datetime
import time 
from Read_Robot_Data import FanucReaderRPI
import Calc_Robot_Indices as ri


from src.fanucpy.robot import Robot

update_time = 1
 
robot = Robot(
    robot_model="Fanuc",
    host="127.0.0.1",
    port=18735,
    ee_DO_type="RDO",
    ee_DO_num=7,
)
 
robot.connect()

fanuc_reader = FanucReaderRPI(
    robot_model="Fanuc",
    host="127.0.0.1",
    port=18736,
    ee_DO_type="RDO",
    ee_DO_num=7,
)
 
print(robot.get_curjpos())
 
poses = {
    "white": [
        [16.116, 49.928, -36.11, 1.103, -54.888, 70.511],
        [16.117, 65.295, -48.122, 1.328, -42.989, 70.168],
        [16.116, 49.928, -36.11, 1.103, -54.888, 70.511],
        [-14.908, 46.757, -33.431, 1.533, -56.965, 101.338],
        [-14.908, 64.349, -48.247, 1.915, -42.155, 100.753],
        [-14.908, 46.757, -33.431, 1.533, -56.965, 101.338],
    ],
    "red": [
        [13.627, 60.441, -24.709, -1.048, -66.248, -16.398],
        [13.557, 75.505, -36.109, -1.172, -54.851, -16.075],
        [13.627, 60.441, -24.709, -1.048, -66.248, -16.398],
        [-13.958, 60.342, -24.189, -0.444, -67.101, 10.933],
        [-13.957, 75.752, -35.898, -0.496, -55.392, 11.042],
        [-13.958, 60.342, -24.189, -0.444, -67.101, 10.933],
    ],
    "green": [
        [25.815, 52.821, -26.217, -1.403, -63.691, -115.988],
        [25.82, 71.066, -41.578, -1.683, -48.334, -115.493],
        [25.815, 52.821, -26.217, -1.403, -63.691, -115.988],
        [-18.019, 36.527, -38.043, -1.225, -52.764, -72.027],
        [-18.019, 56.983, -56.329, -1.723, -34.483, -71.348],
        [-18.019, 36.527, -38.043, -1.225, -52.764, -72.027],
    ],
}
 
def pick(p1, p2, p3):
    robot.move(move_type="joint", vals=p1, velocity=50, acceleration=50)
    robot.gripper(True)
    robot.move(move_type="joint", vals=p2, velocity=50, acceleration=50)
    robot.gripper(False)
    robot.move(move_type="joint", vals=p3, velocity=50, acceleration=50)
 
 
def place(p1, p2, p3):
    robot.move(move_type="joint", vals=p1, velocity=50, acceleration=50)
    robot.move(move_type="joint", vals=p2, velocity=50, acceleration=50)
    robot.gripper(True)
    robot.move(move_type="joint", vals=p3, velocity=50, acceleration=50)

previous_cost = 0
previous_time, previous_velocity = -1, None
update_time = time.time()
 
colors = ["white", "red", "green"]
for _ in range(1):
    for color in colors:
        pick(poses[color][0], poses[color][1], poses[color][2])
        current_time = time.time()
        dt = current_time - previous_time
        current_reading = fanuc_reader.get_next_reading()
        print(current_reading)
        current_time = time.time()
        cost = ri.compute_energy_cost(current_reading, previous_cost, dt)
        previous_cost += cost['cost']
        previous_time = current_time
        previous_reading = current_reading
        print(f"cost: {cost}")
        print("Hello")
        place(poses[color][3], poses[color][4], poses[color][5])
 
    for color in colors:
        pick(poses[color][3], poses[color][4], poses[color][5])
        current_reading = fanuc_reader.get_next_reading()
        print(current_reading)
        place(poses[color][0], poses[color][1], poses[color][2])
 


 
# FanucReader = FanucReaderRPI( 
#         robot_model="Fanuc",
#         host="127.0.0.1",
#         port=18735,
#         ee_DO_type="RDO",
#         ee_DO_num=7,
#          )
 
 
# for i in range (1,100):
#     print(FanucReaderRPI.get_next_reading())
