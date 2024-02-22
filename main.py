from llava_query import LLAVAQuerier
from get_cam import get_image
from quadController import QuadController, goodPorts
from PIL import Image
import cv2


def main():
    controller = QuadController()
    # message = "<image> Do you see a number 6? reply with a simple yes or no."
    message = "If you do not see the number 6, reply with the command 'kup' and if you see the number 6 in this image, reply with the command 'ksit'."
    querier = LLAVAQuerier(model_name="llava-v1.5-7b", controller_address="http://localhost:10000", message = message, worker_address="") 
    while True:
        # image = get_image()
        # cv2.imwrite("tmp.png", image)        
        # # convert numpy array to image
        # image = Image.fromarray(image)

        image = Image.open("no_6.png")

        output = querier.query(image)
        # if output == "yes" or output == "Yes" or output == "YES" or output == "y" or output == "Y" or output == "true":
        #     command = "ksit"
        # else:
        #     command = "kup"
        command =  output
        print(command)
        # controller.sendTask(command, goodPorts, time_taken=0)




if __name__ == "__main__":
    main()    