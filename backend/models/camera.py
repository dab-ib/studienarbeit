from datetime import datetime


class Camera:
    def __init__(self, name, url,minimum,maximum,threshold,sensitivity):
        self.id = 0
        self.name = name
        self.url = url
        self.last_motion: datetime = None
        self.minimum = minimum
        self.maximum = maximum
        self.threshold = threshold
        self.sensitivity = sensitivity
