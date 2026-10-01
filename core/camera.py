import cv2
import numpy as np
import requests
import time
from typing import Generator, Tuple, Optional


class CameraStream:
    def __init__(self, stream_url: str):
        self.stream_url = stream_url
        self.response = None
        self.is_active = False
        self.frames_received = 0
        self.frames_dropped = 0
        self.last_frame_time = 0.0

    def connect(self) -> bool:
        try:
            self.response = requests.get(self.stream_url, stream=True, timeout=5)
            self.is_active = True
            self.frames_received = 0
            self.frames_dropped = 0
            return True
        except requests.RequestException as e:
            print(f"Ошибка подключения к камере: {e}")
            return False

    def disconnect(self):
        self.is_active = False
        if self.response:
            self.response.close()
            self.response = None

    def get_frames(self) -> Generator[Tuple[np.ndarray, bytes], None, None]:
        if not self.response:
            return

        bytes_data = b""
        self.last_frame_time = time.time()

        try:
            for chunk in self.response.iter_content(chunk_size=4096):
                if not self.is_active:
                    break
                if not chunk:
                    continue

                bytes_data += chunk
                start = bytes_data.find(b'\xff\xd8')
                end = bytes_data.find(b'\xff\xd9')

                if start != -1 and end != -1 and end > start:
                    jpg_data = bytes_data[start:end + 2]
                    bytes_data = bytes_data[end + 2:]

                    frame = cv2.imdecode(np.frombuffer(jpg_data, np.uint8), cv2.IMREAD_COLOR)

                    if frame is not None:
                        self.frames_received += 1
                        current_time = time.time()
                        if current_time - self.last_frame_time > 0.5:
                            self.frames_dropped += 1
                        self.last_frame_time = current_time

                        yield frame, jpg_data
                    else:
                        self.frames_dropped += 1
        except Exception as e:
            print(f"Ошибка чтения потока: {e}")
        finally:
            self.disconnect()