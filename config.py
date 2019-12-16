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
        self.zoom = 1

        # DEBUG SETTINGS
        self.debug = True
