import time
from xarm.wrapper import XArmAPI

ip = '192.168.1.113'
arm_speed = 30
gripper_speed = 3000

control_lines = [
    'arm 300 0 150',
    'arm 300 0 150 180 0 0',
    'gripper 200',
    'arm 500 0 150 180 0 0',
    'gripper 100'
]

def process_line(line):
    parts = line.strip().split()
    cmd = parts[0]
    values = list(map(float, parts[1:]))
    return cmd, values

def execute_command(arm, cmd, values):
    if cmd == 'arm':
        if len(values) == 3:
            x, y, z = values
            roll, pitch, yaw = -180, 0, 0
        elif len(values) == 6:
            x, y, z, roll, pitch, yaw = values
        else:
            raise ValueError('Invalid arm command format')
        arm.set_position(x=x, y=y, z=z, roll=roll, pitch=pitch, yaw=yaw,
                         speed=arm_speed, is_radian=False, wait=True)
    elif cmd == 'gripper':
        pos = values[0]
        arm.set_gripper_position(pos, speed=gripper_speed, wait=True)
    print(arm.get_position(), arm.get_position(is_radian=False))

arm = XArmAPI(ip, is_radian=False)
arm.motion_enable(True)
arm.set_mode(0)
arm.set_state(0)
arm.set_gripper_enable(True)
arm.set_gripper_speed(gripper_speed)
arm.move_gohome(wait=True)

for line in control_lines:
    cmd, values = process_line(line)
    execute_command(arm, cmd, values)

arm.move_gohome(wait=True)
arm.disconnect()
