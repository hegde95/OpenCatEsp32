import argparse
import json

import requests
import base64
from io import BytesIO
from PIL import Image
import time

from conversation import default_conversation, conv_templates
import hashlib


def load_image_from_base64(image):
    return Image.open(BytesIO(base64.b64decode(image)))

def convert_image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")




def main():
    if args.worker_address:
        worker_addr = args.worker_address
    else:
        controller_addr = args.controller_address
        ret = requests.post(controller_addr + "/refresh_all_workers")
        ret = requests.post(controller_addr + "/list_models")
        models = ret.json()["models"]
        models.sort()
        print(f"Models: {models}")

        ret = requests.post(controller_addr + "/get_worker_address",
            json={"model": args.model_name})
        worker_addr = ret.json()["address"]
        print(f"worker_addr: {worker_addr}")

    if worker_addr == "":
        return
    image_path = "tmp.png"
    # image = convert_image_to_base64(Image.open(image_path))
    image = Image.open(image_path)

    # conv = default_conversation.copy()
    conv = conv_templates["llava_v1"].copy()
    conv.append_message(conv.roles[0], (args.message, image, "Default"))
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()

    all_image_hash = conv.get_images()

    headers = {"User-Agent": "LLaVA Client"}

    pload = {
        'model': 'llava-v1.5-7b', 
        'prompt': prompt, 
        'temperature': 0.2, 
        'top_p': 0.7, 
        'max_new_tokens': 512, 
        'stop': '</s>', 
        'images': f"List of 1 images: {all_image_hash}"
    }
    pload['images'] = conv.get_images()

 

    print("Response:")
    # # Stream output
    # disable_btn = {"type": "button", "label": "Disable", "disabled": True}
    # enable_btn = {"type": "button", "label": "Enable", "disabled": False}

    response = requests.post(worker_addr + "/worker_generate_stream",
        headers=headers, json=pload, stream=True, timeout=10)
    for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
        if chunk:
            data = json.loads(chunk.decode())
            if data["error_code"] == 0:
                output = data["text"][len(prompt):].strip()
    #             conv.messages[-1][-1] = output + "▌"
    #             yield (conv, conv.to_gradio_chatbot()) + (disable_btn,) * 5
            else:
                output = data["text"] + f" (error_code: {data['error_code']})"
    #             conv.messages[-1][-1] = output
    #             yield (conv, conv.to_gradio_chatbot()) + (disable_btn, disable_btn, disable_btn, enable_btn, enable_btn)
    #             return
    #         time.sleep(0.03)
    print(output)

    # response = requests.post(worker_addr + "/worker_generate_stream", headers=headers,
    #         json=pload, stream=True)
    # for line in response.iter_lines():
    #     if line:
    #         # convert from bytes to string
    #         line_str = line.decode('utf-8')
    #         print(line_str)
    #         print("-----------------------------------")

    print("")


class LLAVAQuerier():
    def __init__(self, model_name, worker_address, controller_address, message):
        self.model_name = model_name
        self.worker_address = worker_address
        self.controller_address = controller_address
        self.message = "<image> " + message
        # self.message = message
        # self.self_explain_message = "<image> Here is the most recent image, what do you see here?"

        if self.worker_address:
            self.worker_addr = self.worker_address
        else:
            controller_addr = self.controller_address
            ret = requests.post(controller_addr + "/refresh_all_workers")
            ret = requests.post(controller_addr + "/list_models")
            models = ret.json()["models"]
            models.sort()
            print(f"Models: {models}")

            ret = requests.post(controller_addr + "/get_worker_address",
                json={"model": self.model_name})
            worker_addr = ret.json()["address"]
            print(f"worker_addr: {worker_addr}")    
            self.worker_addr = worker_addr    
        
        if self.worker_addr == "":
            raise Exception("Worker address is empty")

        # self.conv = conv_templates["llava_robot_controller"].copy()
        self.conv = conv_templates["llava_v1"].copy()

    def get_response(self, conv, max_new_tokens=512):
        prompt = conv.get_prompt()

        all_image_hash = conv.get_images()

        headers = {"User-Agent": "LLaVA Client"}

        pload = {
            'model': 'llava-v1.5-7b', 
            'prompt': prompt, 
            'temperature': 0, #0.2, 
            'top_p': 0,#0.7, 
            'max_new_tokens': max_new_tokens, 
            'stop': '</s>', 
            'images': f"List of 1 images: {all_image_hash}"
        }
        pload['images'] = conv.get_images()        

        response = requests.post(self.worker_addr + "/worker_generate_stream",
            headers=headers, json=pload, stream=True, timeout=10)
        for chunk in response.iter_lines(decode_unicode=False, delimiter=b"\0"):
            if chunk:
                data = json.loads(chunk.decode())
                if data["error_code"] == 0:
                    output = data["text"][len(prompt):].strip()
                else:
                    output = data["text"] + f" (error_code: {data['error_code']})"   
        return output     
    def parse_output(self, output):
        # the output is a string of dictionary of {explanations:command}

        # remove the curly braces
        output = output[1:-1]

        # split the string into a list of strings
        output = output.split(":")

        command = output[1].strip().strip("\"").lower()
        explaination = output[0].strip().strip("\"").lower()
        return command, explaination 
    
    def query(self, image):

        conv = self.conv.copy()
        # conv.append_message(conv.roles[0], (self.self_explain_message, image, "Default"))
        # conv.append_message(conv.roles[1], None)
        # explaination = self.get_response(conv, max_new_tokens=512)

        # add the explaination to the conversation
        # conv.replace_message(-1, conv.roles[1], explaination)
        conv.append_message(conv.roles[0], (self.message, image, "Default"))
        conv.append_message(conv.roles[1], None)

        output = self.get_response(conv, max_new_tokens=512)
        
        command, explaination = self.parse_output(output)

        # add the output to the conversation
        # conv.replace_message(-1, conv.roles[1], output)
        return "k"+command, explaination





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--controller-address", type=str, default="http://localhost:10000")
    parser.add_argument("--worker-address", type=str)
    parser.add_argument("--model-name", type=str, default="llava-v1.5-7b")
    parser.add_argument("--max-new-tokens", type=int, default=32)
    parser.add_argument("--message", type=str, default=
        # "<image> You are controlling a robot. The robot has to navigate to 5 cm in front of the tick mark. You available actions are walk straight, a: walk left, b: walk right, c: turn back, d: Do nothing. Choose one."
        # "<image> What is unusual about this image?"    
        "<image> Do you see a tick mark? reply with a simple yes or no."     
        )
    args = parser.parse_args()
    # main()
    image = Image.open("tmp.png")
    querier = LLAVAQuerier(args.model_name, args.worker_address, args.controller_address, args.message)
    print(querier.query(image))