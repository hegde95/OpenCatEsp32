from llava_query import LLAVAQuerier
from get_cam import get_image
from quadController import QuadController, goodPorts
from PIL import Image
import cv2


def main():
    controller = QuadController()
    message = "<image> Do you see a number 6? reply with a simple yes or no."
    querier = LLAVAQuerier(model_name="llava-v1.5-7b", controller_address="http://localhost:10000", message = message, worker_address="") 
    while True:
        image = get_image()
        # cv2.imwrite("tmp.png", image)        
        # convert numpy array to image
        image = Image.fromarray(image)

        # image = Image.open("tmp.png")

        output = querier.query(image)
        print(output)
        if output == "yes" or output == "Yes" or output == "YES" or output == "y" or output == "Y" or output == "true":
            command = "ksit"
        else:
            command = "kup"
        controller.sendTask(command, goodPorts)




if __name__ == "__main__":
    main()    