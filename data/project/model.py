from __future__ import annotations

from dataclasses import field, dataclass
import random
from typing import Type, cast

import faker_music, faker
from faker_music import MusicProvider
from faker import Faker
from data.project.base import Dataset, Entity


# TODO replace this module with your own types

@dataclass
class RentalDataset(Dataset):
    people: list[Person]
    labels: list[Label]
    songs: list[Song]

    @staticmethod
    def entity_types() -> list[Type[Entity]]:
        return [Person, Label, Song]

    @staticmethod
    def from_sequence(entities: list[list[Entity]]) -> Dataset:
        return RentalDataset(
            cast(list[Person], entities[0]),
            cast(list[Label], entities[1]),
            cast(list[Song], entities[2])
        )

    def entities(self) -> dict[Type[Entity], list[Entity]]:
        res = dict()
        res[Person] = self.people
        res[Label] = self.labels
        res[Song] = self.songs

        return res

    @staticmethod
    def generate(
            count_of_customers: int,
            count_of_labels: int,
            count_of_songs: int
            ):

        def generate_people(n: int, male_ratio: float = 0.5, locale: str = "en_US",
                            unique: bool = False, min_age: int = 0, max_age: int = 100) -> list[Person]:
            assert n > 0
            assert 0 <= male_ratio <= 1
            assert 0 <= min_age <= max_age

            fake = Faker(locale)
            people = []
            for i in range(n):
                male = random.random() < male_ratio
                generator = fake if not unique else fake.unique
                people.append(Person(
                    "P-" + (str(i).zfill(6)),
                    generator.name_male() if male else generator.name_female(),
                    random.randint(min_age, max_age),
                    male))

            return people

        def generate_labels(n: int) -> list[Label]:
            assert n > 0


            fake = Faker()
            fake.add_provider(faker.providers.company)
            fake.add_provider(faker.providers.phone_number)

            labels = []
            for i in range(n ):
                fake = Faker()
                label = Label(
                    fake.company(),
                    str(fake.address()),
                    fake.phone_number()
                )

                labels.append(label)

            return labels

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



        people = generate_people(count_of_customers)
        labels = generate_labels(count_of_labels)
        songs = generate_songs(count_of_songs)
        for i in range(len(songs)):
            song = songs[i]
            label=labels[random.randint(0,len(labels)-1)].name
            song.label = label
        return RentalDataset(people, labels, songs)



@dataclass
class Song(Entity):
    title: str = field(hash=True)
    genre: str = field(repr=True, compare=False)
    release_date: str = field(repr=True, compare=False)
    label: str = field(default="",repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Song:
        return Song(seq[0], seq[1], seq[2], seq[3])

    def to_sequence(self) -> list[str]:
        return [self.title, self.genre, self.release_date, self.label]

    @staticmethod
    def field_names() -> list[str]:
        return ["title", "genre", "release_date", "label"]

    @staticmethod
    def collection_name() -> str:
        return "songs"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Song.collection_name()} (
            title CHAR(4) NOT NULL PRIMARY KEY,
            genre VARCHAR(100),
            release_date VARCHAR(50),
            label VARCHAR(150)
        );
        """


@dataclass
class Label(Entity):
    name: str = field(hash=True)
    address: str = field(repr=True, compare=False)
    telephone: str = field(repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Label:
        return Label(seq[0], seq[1], seq[2])

    def to_sequence(self) -> list[str]:
        return [self.name, self.address, self.telephone]

    @staticmethod
    def field_names() -> list[str]:
        return ["name", "address", "telephone"]

    @staticmethod
    def collection_name() -> str:
        return "Labels"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Label.collection_name()} (
            name VARCHAR(150) NOT NULL PRIMARY KEY,
            address VARCHAR(150),
            telephone  VARCHAR(20)
        );
        """


@dataclass
class Person(Entity):
    id: str = field(hash=True)
    name: str = field(repr=True, compare=False)
    age: int = field(repr=True, compare=False)
    male: bool = field(default=True, repr=True, compare=False)

    @staticmethod
    def from_sequence(seq: list[str]) -> Person:
        return Person(seq[0], seq[1], int(seq[2]), bool(seq[3]))

    def to_sequence(self) -> list[str]:
        return [self.id, self.name, str(self.age), str(int(self.male))]

    @staticmethod
    def field_names() -> list[str]:
        return ["id", "name", "age", "male"]

    @staticmethod
    def collection_name() -> str:
        return "people"

    @staticmethod
    def create_table() -> str:
        return f"""
        CREATE TABLE {Person.collection_name()} (
            id VARCHAR(8) NOT NULL PRIMARY KEY,
            name VARCHAR(50),
            age TINYINT,
            male BOOLEAN
        );
        """
