from llava_query import LLAVAQuerier
from get_cam import get_image
from quadController import QuadController, goodPorts
from PIL import Image
import cv2


def main():
    controller = QuadController()
    # message = "<image> Do you see a number 6? reply with a simple yes or no."
    # message = "If you do not see the number 6, reply 'kup' and if you see the number 6 in this image, reply with 'ksit'."
    # message = "The task is to search for a number in the image and control a robot. "\
    # +"If you see the number 6, 0 or 1, command the robot to sit. "\
    # +"If you do not see these numbers, command the robot to stand up. " \
    # +"Below are the list of instructions available, with its corresponding behavior. "\
    # +"\n sit: robot sits. "\
    # +"\n up: stand up. "\
    # +"\nYour reply must have the format: {instruction, reason for instruction}. "\
    # +"Your reply must look like the following example: "\
    # +"\n'sit, I see the number 6 at the center of the image.' "\
    # +"\n'up, I do not see the numers in the image.' "\
    # +""
    # read the message from the file
    with open("message.txt", "r") as file:
        message = file.read()  
    querier = LLAVAQuerier(model_name="llava-v1.5-13b", controller_address="http://localhost:10000", message = message, worker_address="") 
    while True:
        image = get_image()
        cv2.imwrite("tmp.png", image)        
        # convert numpy array to image
        image = Image.fromarray(image)

        # image = Image.open("no_6.png")

        output, explaination = querier.query(image)
        # if output == "yes" or output == "Yes" or output == "YES" or output == "y" or output == "Y" or output == "true":
        #     command = "ksit"
        # else:
        #     command = "kup"
        command =  output
        print(command, explaination)
        controller.sendTask(command, goodPorts, time_taken=0)




if __name__ == "__main__":
    main()    