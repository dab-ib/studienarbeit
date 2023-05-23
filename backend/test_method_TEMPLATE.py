import asyncio
import time

import av
from av.video.motion import MotionDetector
from av.video.motion.bsdetector import BSDetector

def motion_detection(frame):
    # Logik Bewegungserkennung
    return True

async def run():
    frame.color_range = av.ColorRange.FULL

    #container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    #test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)


    motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))


    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if motion_detection(frame):
                # Aktionen: Was wenn Bewegung?

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
