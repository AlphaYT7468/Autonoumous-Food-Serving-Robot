# articubot_one

ROS 2 Humble package for a differential-drive mobile robot: robot description,
`ros2_control` configuration, SLAM and Nav2 parameters, and launch files for both
real hardware and Gazebo simulation.

**Full documentation — build instructions, hardware parameters, running the
robot, mapping, troubleshooting — is in the workspace README:
[`../../README.md`](../../README.md).**

## Quick reference

```bash
# Full autonomous stack on the real robot
ros2 launch articubot_one bringup.launch.py

# Simulation
ros2 launch articubot_one launch_sim.launch.py
```

| Directory | Contents |
|---|---|
| `description/` | URDF / xacro robot model |
| `config/` | Controller, SLAM, Nav2, twist_mux and RViz configuration |
| `launch/` | Launch files (`bringup.launch.py` is the main entry point) |
| `worlds/` | Gazebo worlds |

Derived from [joshnewans/articubot_one](https://github.com/joshnewans/articubot_one)
at commit `cd1eb0f`, part of the
[Articulated Robotics](https://articulatedrobotics.xyz/) series.
