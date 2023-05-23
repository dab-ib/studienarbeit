import asyncio
import time

import av
from av.video.motion import MotionDetector
from av.video.motion.bsdetector import BSDetector
import cv2

def body_detection(frame):

    # Lade das vortrainierte Modell für die Körpererkennung
    body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')

    # Konvertiere das Frame in ein OpenCV-Bildobjekt
    img = frame.to_rgb().to_ndarray()

    # Wandle das Bild in Graustufen um
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # Führe die Körpererkennung auf dem Graustufenbild durch
    bodies = body_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Rückgabe der erkannten Körper
    return bodies

async def run():
    frame.color_range = av.ColorRange.FULL

    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if motion_detection(frame):
                # Körpererkennung
                bodies = body_detection(frame)

                # Körpererkennungsergebnis in der Konsole ausgeben
                if len(bodies) > 0:
                    print("Körper erkannt:", len(bodies))

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
