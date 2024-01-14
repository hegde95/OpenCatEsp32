import requests
import cv2
import numpy as np

# The URL of the video stream from the img tag
stream_url = 'http://192.168.4.1:8888/stream'

# Open a connection to the stream
response = requests.get(stream_url, stream=True)

# Check if the connection was successful
if response.status_code == 200:
    # Use a bytes buffer to store bytes from the stream
    bytes_buffer = bytes()
    for chunk in response.iter_content(chunk_size=1024):
        bytes_buffer += chunk
        # Check for the start and end of a JPEG frame
        a = bytes_buffer.find(b'\xff\xd8')
        b = bytes_buffer.find(b'\xff\xd9')
        # If we have a start and end of a frame, process the image
        if a != -1 and b != -1:
            jpg = bytes_buffer[a:b+2]
            bytes_buffer = bytes_buffer[b+2:]
            # Decode the JPEG data and do something with the image, for example, display it
            image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            cv2.imshow('Video feed', image)
            if cv2.waitKey(1) == 27:
                break
    cv2.destroyAllWindows()
else:
    print(f'Failed to get the video feed. Status code: {response.status_code}')
