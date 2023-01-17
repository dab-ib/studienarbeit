from dbconnector import DBConnector
import mysql.connector
from models.camera import Camera
from models.settings import Settings
from typing import List


class MariaDBConnector:

    def __init__(self, host: str, user: str, password: str, database: str) -> None:
        super().__init__()
        self.__connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.__cursor = self.__connection.cursor()

    def get_cameras(self) -> List[Camera]:
        query = "SELECT * FROM cameras"
        self.__cursor.execute(query)
        result = self.__cursor.fetchall()
        cameras = []
        for row in result:
            cam = Camera(row[1], row[2])
            cam.id = row[0]
            cameras.append(cam)
        return cameras


    def get_camera(self, id: int) -> Camera:
        query = "SELECT * FROM cameras WHERE id = %s"
        self.__cursor.execute(query, (id,))
        result = self.__cursor.fetchone()
        if result:
            cam = Camera(result[1], result[2])
            cam.id = result[0]
            return cam
        else:
            return None

    def insert_camera(self, cam: Camera) -> int:
        query = "INSERT INTO cameras (name, url) VALUES (%s, %s)"
        self.__cursor.execute(query, (cam.name, cam.url))
        self.__connection.commit()
        return self.__cursor.lastrowid

    def update_camera(self, id: int, cam: Camera):
        query = "UPDATE cameras SET name = %s, url = %s WHERE id = %s"
        self.__cursor.execute(query, (cam.name, cam.url, id))
        self.__connection.commit()

    def delete_camera(self, id: int):
        query = "DELETE FROM cameras WHERE id = %s"
        self.__cursor.execute(query, (id,))
        self.__connection.commit()

    # Settings
    def get_settings(self) -> Settings:
        query = "SELECT * FROM settings LIMIT 1"
        self.__cursor.execute(query)
        result = self.__cursor.fetchone()
        if result:
            return Settings(result[0], result[1])
        else:
            return None

    def update_settings(self, settings: Settings):
        query = "UPDATE settings SET frame_buffer_size = %s, video_path = %s WHERE id = 0"
        self.__cursor.execute(query, (settings.frame_buffer_size, settings.video_path))
        self.__connection.commit()


