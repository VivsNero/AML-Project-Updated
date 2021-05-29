#as found in https://www.youtube.com/watch?v=3vvvjdmBoyc&ab_channel=ValerioVelardo-TheSoundofAI
class Track:
    def __init__(self, name, id, artist) -> None:
        """
        :param name (str): the name of the track
        :param id (int): spotifys track id
        :param artist (str): artist who created the track
        """
        self.name = name
        self.id = id
        self.artist = artist

    def create_spotify_uri(self):
        return f"spotify:track:{self.id}"

    def __str__(self):
        return f"{self.name} by {self.artist}"
    