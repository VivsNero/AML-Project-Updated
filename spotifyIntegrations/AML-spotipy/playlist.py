#as found in https://www.youtube.com/watch?v=3vvvjdmBoyc&ab_channel=ValerioVelardo-TheSoundofAI
class Playlist:
    def __init__(self, name, id):
        """
        :param name(str): playlists name¨
        :param id (int) spotify playlist id
        """
        self.name = name
        self.id = id

    def __str__(self):
        return f"Playlist: {self.name}"