class Settings:
    """
    This is where application-wide settings are stored. Currently they are hard coded, but in the future
    they will be read from a file at launch to maintain settings over multiple application launches.
    """
    __instance = None

    def __init__(self):
        if Settings.__instance is None:
            Settings.__instance = self
        else:
            raise Exception("This class is a singleton!")

        # FILE SETTINGS
        self.zip_types = [".cbz", ".zip"]
        self.image_types = [".jpg", ".jpeg", ".png"]
        self.directories = [r"D:\Porn\Hentai\test"]

        # IMAGE SETTINGS
        self.anti_alias = True

        # WINDOW SETTINGS

        # COMIC EXPLORER SETTINGS
        self.explorerZoom = Zoom()

        # DEBUG SETTINGS
        self.debug = Debug()


class Observer:
    def __init__(self, class_name="", value=None):
        self.observers = []
        self.className = str(class_name).lower()

        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        print(f"setting _zoom to {value}")
        self._value = value
        for callback in self.observers:
            print(f"announcing change to {callback.__qualname__}")
            callback(self._value)

    def bind_to(self, callback):
        print(f"{callback.__qualname__} bound to {self.__class__.__name__}")
        self.observers.append(callback)

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value


class Zoom(Observer):
    def __init__(self):
        super().__init__(self.__class__.__name__, 1/8)
        self.zoomScale = 8

        self.set_zoom = self.set_value
        self.get_zoom = self.get_value

    def set_value(self, value):
        self.value = value / self.zoomScale

    def get_value(self):
        return self.value * self.zoomScale


class Debug(Observer):
    def __init__(self):
        super().__init__()
        self._debug = True

        self.set_debug = self.set_value
        self.get_debug = self.get_value


settings = Settings()


if __name__ == "__main__":
    print(settings.explorerZoom)
