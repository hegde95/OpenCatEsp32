import requests
import cv2
import numpy as np
import time

# The URL of the video stream from the img tag
stream_url = 'http://192.168.4.1:8888/stream'

def get_image(wait_time=0):
    time.sleep(wait_time)  # Consider setting this to a very small value or removing it.
    
    with requests.get(stream_url, stream=True) as response:
        if response.status_code == 200:
            bytes_buffer = bytes()
            for chunk in response.iter_content(chunk_size=256):
                bytes_buffer += chunk
                # Find the last JPEG start and end
                a = bytes_buffer.rfind(b'\xff\xd8', 0, -2)
                b = bytes_buffer.rfind(b'\xff\xd9', 2)
                
                # If we have a start and end of the last frame, process the image
                if a != -1 and b != -1 and b > a:
                    jpg = bytes_buffer[a:b+2]
                    bytes_buffer = bytes_buffer[b+2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    return image  # Return the most recent image

    return None 
    #             cv2.imshow('Video feed', image)
    #             if cv2.waitKey(1) == 27:
    #                 break
    #     cv2.destroyAllWindows()
    # else:
    #     print(f'Failed to get the video feed. Status code: {response.status_code}')

if __name__ == '__main__':
    while True:
        time.sleep(0.01)
        image = get_image()
        # cv2.imshow('Video feed', image)
        # save image to jpeg
        cv2.imwrite("tmp.png", image)