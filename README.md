# Installation

## Vorraussetzungen
- Node 15 => Lieber Node 14 verwenden.
- yarn
- Python3.8

## Backend
- cd backend
- pip install -r requirements.txt
- Überprüfe data/db.json => Vorgefertigtes File für meine Kamera lokal
- mkdir data/videos

## Frontend
- cd frontend
- npm install

# Ausführen
- cd backend && python main.py
- cd frontend && npm run serve

Öffne http://localhost:8080

# Maßnahmen zum Testen der Bewegungserkennungsmethoden
- def motion_detection der Testdatei in motiondetection/bsmotiondetector.py einfügen
ODER (besser => in der Studienarbeit verwendet)
- in main.py einbinden hier ist bereits eine Methode async def motion_result_handler(result: MotionDetectionResult)
