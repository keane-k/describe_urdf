import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

from launch_ros.actions import Node
import xacro


def generate_launch_description():

    # Specify the name of the package and path to xacro file within the package
    pkg_name = 'urdf_example'
    file_subpath = 'description/example_robot.urdf.xacro'


    # Use xacro to process the file
    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    # Defining world
    default_world = os.path.join(
        get_package_share_directory(pkg_name),
        'worlds',
        'my_world.world'
    )

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
    )
    
    # 1. Launch robot_state_publisher_node
    # Configure the node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )


    # 2. Launch Gazebo 
    # Include launch file for GazeboSim, found in ros_gz_sim package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]),
            launch_arguments={'gz_args': ['-r -v4 --render-engine ogre ', world], 'on_exit_shutdown': 'true'}.items()
    )


    # 3. Spawn robot model
    # Spawner node taken from ros_gz_sim package
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic','robot_description',
                                   '-name','my_robot',
                                   '-z','0.1'],
                        output='screen')


    # Create the bridge node for gz_bridge
    bridge_params = os.path.join(get_package_share_directory(pkg_name),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}'
        ]
    )

    # Create the bridge node for gz_image_bridge
    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"]
    )



    # Run the node
    return LaunchDescription([
        world_arg,
        node_robot_state_publisher,
        gazebo,
        spawn_entity,
        ros_gz_bridge,
        ros_gz_image_bridge
    ])