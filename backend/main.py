import asyncio

import api
from frameserver import FrameServer
from motiondetection.bsmotiondetector import BSMotionDetector
from motiondetection.motiondetectionresult import MotionDetectionResult
from recorder import Recorder, RecordingTrigger
from tinydbconnector import TinyDBConnector
from websocketserver import WebsocketServer

db = TinyDBConnector('data/db.json')
frameserver = FrameServer(db)
websocketserver = WebsocketServer(frameserver)
recorder = Recorder(frameserver, db)


async def run():
    cameras = db.get_cameras()
    if cameras is not None:
        for cam in cameras:
            asyncio.create_task(frameserver.capture(cam))
        motiondetector = BSMotionDetector(db, frameserver)
        motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))
    asyncio.create_task(websocketserver.run())
    asyncio.create_task(api.run(frameserver, db))


async def motion_result_handler(result: MotionDetectionResult):
    msg = "result from " + result.camera.name + ": " + str(result.motion) + " (Magnitude: " + str(
        result.intensity) + ")"
    print(msg,'-----------------------')
    await websocketserver.broadcast_event("MotionResult", result)
    if result.motion:
        print(result.camera)
        await recorder.capture_while_motion(result.camera, RecordingTrigger.MOTION, 10)
        pass


if __name__ == "__main__":
    asyncio.get_event_loop().create_task(run())
    asyncio.get_event_loop().run_forever()
