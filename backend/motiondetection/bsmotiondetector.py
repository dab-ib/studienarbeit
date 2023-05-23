import av
import imutils

from motiondetection.motiondetector import MotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from models.camera import Camera
from framebuffer import FrameBuffer
import cv2
import asyncio
import datetime

class BSMotionDetector(MotionDetector):
    count = 0

    def __init__(self, *args) -> None:
        self.framestore = dict()
        super().__init__(*args)
        self.backSub = cv2.createBackgroundSubtractorMOG2()
        self.initial_frame = None

    async def _analyze(self, camera: Camera, buffer: FrameBuffer) -> MotionDetectionResult:
        packet = buffer.get_latest_keyframe()
        if packet is None:
            return MotionDetectionResult(False, 0, camera)
        frames = packet.decode()
        vfs = [x for x in frames if isinstance(x, av.VideoFrame)]
        if len(vfs) == 0:
            return MotionDetectionResult(False, 0, camera)
        frame = vfs[0]

        img = cv2.cvtColor(frame.to_rgb().to_ndarray(), cv2.COLOR_BGR2RGB)
        img = imutils.resize(img, width=600)

        if self.initial_frame is None:
            self.initial_frame = img
            return MotionDetectionResult(False, 0, camera)

        dilated_frame = self.backSub.apply(img)

        contours = cv2.findContours(dilated_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        
        for contour in contours:
            if cv2.contourArea(contour) < 9000:
                continue
            
            Console.out("Motion detected")
            
            return MotionDetectionResult(True, 5000, camera)

        return MotionDetectionResult(False, 0, camera)
