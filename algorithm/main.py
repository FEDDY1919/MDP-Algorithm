import sys
import time
from typing import List

import settings
from app import AlgoSimulator, AlgoMinimal
from entities.assets.direction import Direction
from entities.connection.rpi_client import RPiClient
from entities.connection.rpi_server import RPiServer
from entities.grid.obstacle import Obstacle



def run_simulator():
    # Fill in obstacle positions with respect to lower bottom left corner.
    # (x-coordinate, y-coordinate, Direction)
    obstacles = []
    #
    #[[105, 75, 180, 0], [135, 25, 0, 1], [195, 95, 180, 2], [175, 185, -90, 3], [75, 125, 90, 4], [15, 185, -90, 5]]
    app = AlgoSimulator(obstacles)
    app.init()
 


def run_minimal(also_run_simulator):
    # Create a client to connect to the RPi.
    print(f"Attempting to connect to {settings.RPI_HOST}:{settings.RPI_PORT}")
    client = RPiClient(settings.RPI_HOST, settings.RPI_PORT)
    # Wait to connect to RPi.
    while True:
        try:
            client.connect()
            break
        except OSError:
            pass
        except KeyboardInterrupt:
            client.close()
            sys.exit(1)
    print("Connected to RPi!\n")
    print(client.socket.recv(1024).decode())
    print("Waiting to receive obstacle data from RPi...")
    # Create a server to receive information from the RPi.
    server = RPiServer(settings.PC_HOST, settings.PC_PORT)
    # Wait for the RPi to connect to the PC.
    # try:
    #     #server.start()
    # except OSError or KeyboardInterrupt as e:
    #     print(e)
    #     server.close()
    #     client.close()
    #     sys.exit(1)

    # At this point, both the RPi and the PC are connected to each other.
    # Create a synchronous call to wait for RPi data.
    # obstacle_data: list = server.receive_data()
    # server.close()
    # print("Got data from RPi:")
    # print(obstacle_data)
    #
    # obstacles = parse_obstacle_data(obstacle_data)
    # if also_run_simulator:
    #     app = AlgoSimulator(obstacles)
    #     app.init()
    #     app.execute()
    # app = AlgoMinimal(obstacles)
    # app.init()
    # app.execute()
    #
    # # Send the list of commands over.
    # print("Sending list of commands to RPi...")
    # commands = app.robot.convert_all_commands()
    client.send_message()
    client.close()


def run_rpi():
    while True:
        run_minimal(False)
        time.sleep(5)


if __name__ == '__main__':
    run_simulator()
