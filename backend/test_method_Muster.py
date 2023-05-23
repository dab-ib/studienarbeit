import asyncio
import av
import cv2

# Mustererkennungsalgorithmen importieren
from pattern_detection import detect_people

async def run():
    container = av.open('input_video.mp4')
    in_stream = container.streams.video[0]

    test_output = av.open('output_video.mp4', 'w')
    out_stream = test_output.add_stream(template=in_stream)

    for packet in container.demux(in_stream):
        for frame in packet.decode():
            # Mustererkennung - Menschen und Autos
            is_person_detected = detect_people(frame)

            # Kodierung und Muxing
            out_packet = out_stream.encode(frame)
            if out_packet:
                test_output.mux(out_packet)

    test_output.close()

def detect_people(frame):
    # Haar Cascade-Modelle von OpenCV
    # Pfade zu den vortrainierten Haar Cascade-Modellen für die Erkennung von Gesichtern und Oberkörpern
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    upperbody_cascade_path = cv2.data.haarcascades + 'haarcascade_upperbody.xml'

    # Lade die Haar Cascade-Modelle
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    upperbody_cascade = cv2.CascadeClassifier(upperbody_cascade_path)

    # Konvertiere das Frame in Graustufen
    gray = cv2.cvtColor(frame.to_rgb().to_ndarray(), cv2.COLOR_BGR2GRAY)

    # Gesichtserkennung
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Oberkörpererkennung
    upperbodies = upperbody_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))

    # Überprüfe, ob Menschen in den Frames erkannt wurden
    if len(faces) > 0 or len(upperbodies) > 0:
        return True

    return False


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
