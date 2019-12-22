class Settings:
    """
    This is where application-wide settings are stored. Currently they are hard coded, but in the future
    they will be read from a file at launch to maintain settings over multiple application launches.
    """
    def __init__(self):
        # FILE SETTINGS
        self.zip_types = [".cbz", ".zip"]
        self.image_types = [".jpg", ".jpeg", ".png"]
        self.directories = [r"D:\Porn\Hentai\test"]

        # IMAGE SETTINGS
        self.anti_alias = True

        # WINDOW SETTINGS

        # COMIC EXPLORER SETTINGS
        self.zoom = self.Zoom()

        # DEBUG SETTINGS
        self.debug = self.Debug()

    class Zoom:
        def __init__(self):
            super().__init__()
            self._zoom = 1
            self.observers = []

        @property
        def zoom(self):
            return self._zoom

        @zoom.setter
        def zoom(self, value):
            print(f"setting _zoom to {value}")
            self._zoom = value
            for callback in self.observers:
                print(f"announcing change to {callback}")
                callback(self._zoom)

        def bind_to(self, callback):
            print(f"{callback} bound to zoom")
            self.observers.append(callback)

        def set(self, value):
            self.zoom = value

        def __rmul__(self, other):
            return other
        __mul__ = __rmul__

        def __int__(self):
            return self.zoom

    class Debug:
        def __init__(self):
            self._debug = True
            self.observers = []

        @property
        def debug(self):
            return self._debug

        @debug.setter
        def debug(self, value):
            print(f"setting _debug to {value}")
            self._debug = value
            self.announce_change()

        def announce_change(self):
            for callback in self.observers:
                print(f"announcing change to {callback}")
                callback(self._debug)

        def set(self, value):
            self.debug = value

        def bind_to(self, callback):
            print(f"{callback} bound to debug")
            self.observers.append(callback)


settings = Settings()


if __name__ == "__main__":
    print(settings.debug)
