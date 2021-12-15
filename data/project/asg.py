import faker
from faker import Faker
from faker_music import MusicProvider

from data.project.model import Song


def generate_songs(n: int,
                   ) -> list[Song]:
    assert n > 0

    fake = Faker()
    fake.add_provider(MusicProvider)
    fake.add_provider(faker.providers.file)
    fake.add_provider(faker.providers.date_time)

    songs = []
    for i in range(n):
        song = Song(
            fake.file_name(category="audio"),
            fake.music_genre(),
            fake.date()
        )

        songs.append(song)

    return songs


fake = Faker()
fake.add_provider(MusicProvider)
fake.add_provider(faker.providers.file)
fake.add_provider(faker.providers.date_time)

asd= generate_songs(10)