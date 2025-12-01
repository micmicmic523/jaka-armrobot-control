import socket
import time
import multiprocessing
import math
import os
import jkrc

def get_ip_address():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "127.0.0.1"

def deg_to_rad(pos_list):
    return [math.radians(x) for x in pos_list]

def start_server(data_queue, result_queue):
    ip_address = get_ip_address()
    port = 12345
    
    print(f"Server IP: {ip_address}")
    print(f"Port: {port}")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((ip_address, port))
    except:
        return

    server_socket.listen(1)

    while True:
        try:
            connection, client_address = server_socket.accept()
            connection.setblocking(False)
            
            while True:
                if not result_queue.empty():
                    feedback_code = result_queue.get()
                    msg_back = f"{feedback_code}\n"
                    connection.sendall(msg_back.encode())

                try:
                    data = connection.recv(1024)
                    if data:
                        data_str = data.decode().strip()
                        try:
                            data_int = int(data_str)
                            data_queue.put(data_int)
                        except ValueError:
                            pass
                    else:
                        break
                except BlockingIOError:
                    pass
                except Exception:
                    break
                
                time.sleep(0.1)

        except:
            pass
        finally:
            try:
                connection.close()
            except:
                pass

def main():
    pos_bangun_1 = [-2.704, 96.921, -9.621, 87.815, -88.683, -88.683]
    pos_bangun_2 = [-2.847, 71.087, -9.626, 87.809, -88.683, 102.707]
    pos_bangun_3 = [-2.833, 44.293, -9.628, 87.749, -88.681, 102.707]
    pos_bangun_4 = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    pos_target_list = [
        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.242, -12.313, 92.270, 0.000, 100.043, 0.242],
        [0.242, -12.178, 112.951, 0.000, 79.227, 0.242],
        [-15.597, -10.844, 111.887, 0.000, 79.957, -15.597],
        [-3.930, -12.194, 112.964, 0.000, 79.230, -3.930],
        [-3.930, -13.172, 100.576, 0.000, 92.595, -3.930],
        [-36.074, -2.961, 95.298, 0.000, 87.662, -37.226],
        [-36.074, -2.537, 99.878, 0.000, 82.659, -37.226],
        [-31.172, -5.449, 102.587, 0.000, 82.862, -32.324],
        [-31.172, -4.097, 79.748, 0.000, 104.349, -32.324]
    ]

    pos_draw_list = [
        [-99.278, 5.795, 79.284, 0.000, 98.611, 174.961],
        [-95.421, 1.328, 98.231, 0.559, 80.265, 180.415],
        [-94.734, 9.663, 89.090, 0.555, 81.064, 181.110],
        [-94.227, 17.596, 79.279, 0.551, 82.938, 181.635],
        [-101.062, 18.614, 77.942, 0.569, 83.322, 174.802],
        [-102.454, 10.270, 88.378, 0.574, 81.245, 173.389],
        [-104.507, 0.978, 98.587, 0.580, 80.348, 171.326],
        [-95.421, 1.328, 98.231, 0.559, 80.265, 180.415],
        [-99.278, 5.795, 79.284, 0.000, 98.611, 174.961]
    ]

    pos_taruh_list = [
        [-82.926, -2.779, 78.640, 0.000, 104.139, -82.962],
        [-31.172, -3.913, 78.844, 0.000, 105.069, -32.324],
        [-31.172, -5.449, 102.587, 0.000, 82.862, -32.324],
        [-36.226, -2.537, 99.878, 0.000, 82.659, -37.226],
        [-36.074, -2.748, 87.299, 0.000, 95.450, -37.226],
        [0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
        [-0.775, 43.342, -10.787, 32.753, -32.328, 37.611],
        [-1.188, 66.159, -16.466, 49.995, -49.347, 57.411],
        [-1.188, 66.159, -16.466, 65.922, -65.067, 75.700],
        [-1.853, 103.581, -25.779, 78.275, -77.259, 89.885],
        [-2.117, 118.354, -29.456, 89.438, -88.278, 102.704]
    ]

    data_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    
    process1 = multiprocessing.Process(target=start_server, args=(data_queue, result_queue))
    process1.start()
    
    ABS = 0
    IP_ROBOT = "192.168.1.20"
    
    try:
        robot = jkrc.RC(IP_ROBOT)
        robot.login()
        robot.power_on()
        robot.enable_robot()
        print("Robot Connected")
    except:
        print("Robot Connection Failed")

    while True:
        if not data_queue.empty():
            data = data_queue.get()
            print(f"Executing: {data}")
            
            if data == 1:
                robot.joint_move(deg_to_rad(pos_bangun_1), ABS, True, 0.5)
                robot.joint_move(deg_to_rad(pos_bangun_2), ABS, True, 0.5)
                robot.joint_move(deg_to_rad(pos_bangun_3), ABS, True, 0.5)
                robot.joint_move(deg_to_rad(pos_bangun_4), ABS, True, 0.5)
                result_queue.put(1) 

            elif data == 2:
                for pos in pos_target_list:
                    robot.joint_move(deg_to_rad(pos), ABS, True, 0.5)
                result_queue.put(10)

            elif data == 3:
                for pos in pos_draw_list:
                    robot.joint_move(deg_to_rad(pos), ABS, True, 0.5)
                result_queue.put(20)

            elif data == 4:
                for pos in pos_taruh_list:
                    robot.joint_move(deg_to_rad(pos), ABS, True, 0.5)
                result_queue.put(30)

            elif data == 5:
                robot.logout()
                os._exit(0)

            time.sleep(1)
            result_queue.put(0)
            
            while not data_queue.empty():
                data_queue.get()

        else:
            time.sleep(0.1)

if __name__ == "__main__":
    main()
