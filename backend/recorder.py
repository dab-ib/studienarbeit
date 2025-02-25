from dbconnector import DBConnector
from enum import Enum
from tinydbconnector import TinyDBConnector
from rx.core.typing import Disposable
from models.camera import Camera
from frameserver import FrameServer
from videowriter import VideoWriter
import asyncio
from datetime import datetime
from typing import Tuple, Dict

class RecordingTrigger(Enum):
    MOTION = 0
    MANUAL = 1

class Recorder:

    def __init__(self, fs: FrameServer, db: DBConnector) -> None:
        self.__frameserver = fs
        self.__recording: Dict[str, ActiveRecording] = dict()
        self.__db = db

    async def capture(self, cam: Camera, trigger: RecordingTrigger, duration: int = 10):
        if cam.id in self.__recording:
            return

        self.start_capture(cam, trigger)
        await asyncio.sleep(duration)
        self.stop_capture(cam)

    def start_capture(self, cam: Camera, trigger: RecordingTrigger, with_buffer: bool = False) -> Tuple[VideoWriter, Disposable]:
        print("starting capture of " + cam.name)
        if cam.id in self.__recording:
            return

        buffer = self.__frameserver.get_buffer(cam.id)
        writer = VideoWriter(self.__generate_name(cam, trigger))
        writer.open()
        if with_buffer:
            writer.write_packets(buffer.get_packets())
        subscription = buffer.get_observable().subscribe(on_next=lambda p: writer.write_packet(p))
        self.__recording[cam.id] = ActiveRecording(writer, subscription, datetime.now())

    def stop_capture(self, cam: Camera):
        print("stopping capture of " + cam.name)
        if cam.id not in self.__recording:
            return
        self.__recording[cam.id].subscription.dispose()
        self.__recording[cam.id].writer.close()
        del self.__recording[cam.id]

    async def capture_while_motion(self, cam: Camera, trigger: RecordingTrigger, threshold: int):
        if cam.id in self.__recording:
            self.__recording[cam.id].last_motion = datetime.now()
            return

        self.start_capture(cam, trigger, True)

        # return
        # while True:
        await asyncio.sleep(10)
        #     now = datetime.now()
        #     last_motion = self.__recording[cam.id].last_motion
        #     if last_motion is not None and (now - last_motion).seconds > threshold:
        #         break
        self.stop_capture(cam)

    def __generate_name(self, cam: Camera, trigger: RecordingTrigger) -> str:
        dateTimeObj = datetime.now()
        timestampStr = dateTimeObj.strftime("%d-%m-%Y_%H-%M-%S")
        return self.__db.get_settings().video_path + str(cam.id) + "_" + timestampStr + "_"+ ".mp4"

class ActiveRecording:
    def __init__(self, writer: VideoWriter, subscription: Disposable, last_motion: datetime) -> None:
        self.writer = writer
        self.subscription = subscription
        self.last_motion = last_motion