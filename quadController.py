from serialMaster.ardSerial import *
import numpy as np

class QuadController:
    def __init__(self,):
        connectPort(goodPorts)
        t = threading.Thread(target=keepCheckingPort, args=(goodPorts,))
        t.start()
        if len(sys.argv) >= 2:
            if len(sys.argv) == 2:
                cmd = sys.argv[1]
                token = cmd[0][0]
            else:
                token = sys.argv[1][0]
            #                sendTaskParallel([sys.argv[1][0], sys.argv[1:], 1])
            send(goodPorts, [sys.argv[1][0], sys.argv[1:], 1])
        printH('Model list',config.modelList)
        print("You can type 'quit' or 'q' to exit.")
    
    # def sendTask(self, x, ports, time_taken=1, following_behavior=None):
    #     if x != "":
    #         if x == "q" or x == "quit":
    #             return False
    #         else:
    #             token = x[0]
    #             task = x[1:].split()  # white space
    #             # if len(task) <= 1:
    #             send(ports, [x, 1])
    #             if time_taken > 0:
    #                 time.sleep(time_taken)
    #             if following_behavior == "up":
    #                 send(ports, ["kup", 1])
    #             # else:
    #             #     send(ports, [token, list(map(int, task)), 1])
    
    def sendTask(self, x, ports, time_taken=2, following_behavior=None):
        if x == "sit":
            send(ports, ["ksit", 1])
            time.sleep(time_taken)
            return 1
        elif x == "up":
            send(ports, ["kup", 1])
            time.sleep(time_taken)
            return 0
        elif x == "reset":
            send(ports, ["kup", 1])
            send(ports, ['m', [0, 0], 0])
            time.sleep(time_taken)
            return 0
        elif "turn" in x:
            angle  = np.random.randint(-90,90)
            send(ports, ['m', [0, angle], 0])
            time.sleep(time_taken)
            return 0

if __name__ == "__main__":
    quadController = QuadController()
    while True:
        x = input("Enter command: ")
        if not quadController.sendTask(x, goodPorts):
            break
    print("Exiting...")