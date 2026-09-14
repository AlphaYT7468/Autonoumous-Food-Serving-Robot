import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    pkg = get_package_share_directory('articubot_one')

    # 1. Robot drivers: robot_state_publisher, controller_manager, diff_cont, twist_mux
    robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'launch_robot.launch.py'))
    )

    # 2. Lidar driver -> /scan
    lidar = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'rplidar.launch.py'))
    )

    # 3. slam_toolbox in localization mode -> loads saved map, publishes map->odom
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg, 'launch', 'online_async_launch.py')),
        launch_arguments={
            'use_sim_time': 'false',
            'params_file': os.path.join(pkg, 'config',
                                        'mapper_params_online_async.yaml'),
        }.items()
    )

    # 4. Nav2 navigation stack (use nav2_bringup's launch file, not the
    #    outdated copy bundled in articubot_one which references the
    #    renamed 'nav2_recoveries' package).
    nav2_bringup = get_package_share_directory('nav2_bringup')
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_bringup, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'use_sim_time': 'false',
            'params_file': os.path.join(pkg, 'config', 'nav2_params.yaml'),
        }.items()
    )

    # 5. RViz - the touchscreen UI for clicking 2D Goal Pose
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(pkg, 'config', 'main.rviz')],
        output='screen'
    )

    # Staggered startup so each layer has what it depends on.
    return LaunchDescription([
        robot,
        lidar,
        TimerAction(period=10.0, actions=[slam]),
        TimerAction(period=20.0, actions=[nav2]),
        TimerAction(period=20.0, actions=[rviz]),
    ])
