import asyncio
import time

import av
import cv2
from av.video.motion import MotionDetector
from av.video.motion.bsdetector import BSDetector

def motion_detection(frame):
    # Konvertiere das Video-Frame in das erforderliche Format für die Bewegungserkennung
    current_frame = frame.to_rgb().to_ndarray()

    # Initialisiere die Ergebnisvariable
    motion_detected = False

    # Führe die Bewegungserkennung mit Optischem Fluss durch
    if motion_detection.previous_frame is not None:
        # Konvertiere die Frames in das erforderliche Format für die optische Flussberechnung
        prev_gray = cv2.cvtColor(motion_detection.previous_frame, cv2.COLOR_BGR2GRAY)
        curr_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)

        # Berechne den optischen Fluss zwischen den beiden Frames
        flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

        # Führe Bewegungserkennungslogik durch
        # Beispielhaft: Prüfe, ob die durchschnittliche optische Flussgeschwindigkeit einen Schwellenwert überschreitet
        threshold = 0.5
        average_flow = abs(flow.mean())
        if average_flow > threshold:
            motion_detected = True

    # Aktualisiere den vorherigen Frame
    motion_detection.previous_frame = current_frame

    # Rückgabe des Ergebnisses der Bewegungserkennung
    return motion_detected

motion_detection.previous_frame = None

def optical_flow(frame1, frame2):
    # Konvertiere die Frames in das erforderliche Format für die optische Flussberechnung
    prev_gray = cv2.cvtColor(frame1.to_rgb().to_ndarray(), cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(frame2.to_rgb().to_ndarray(), cv2.COLOR_BGR2GRAY)

    # Berechne den optischen Fluss zwischen den beiden Frames
    flow = cv2.calcOpticalFlowFarneback(prev_gray, curr_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    # Rückgabe des optischen Flusses
    return flow


async def run():
    frame.color_range = av.ColorRange.FULL

    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    motiondetector.run().subscribe(on_next=lambda res: asyncio.create_task(motion_result_handler(res)))

    prev_frame = None

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Motion Detection
            if motion_detection(frame):

                if prev_frame is not None:
                    # Optischer Fluss
                    optical_flow_result = optical_flow(prev_frame, frame)
                    if optical_flow_result is not None:
                        print("Bewegung und Optischer Fluss erkannt!")

                prev_frame = frame

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
