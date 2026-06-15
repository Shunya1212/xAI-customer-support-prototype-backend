from django.db import models

class Sex(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'


class Origin(models.TextChoices):
    WILD = 'wild', 'Wild'
    CAPITIVE = 'captive', 'Captive'


class Status(models.TextChoices):
    KEEP = 'keep', 'Keep'
    BREED = 'breed', 'Breed'
    SELL = 'sell', 'Sell'
    SOLD = 'sold', 'Sold'
    DEAD = 'dead', 'Dead'


class FeedingType(models.TextChoices):
    FREE_FEED = 'free_feed', 'Free Feed'
    HAND_FEED = 'hand_feed', 'Hand Feed'
    FORCE_FEED = 'force_feed', 'Force Feed'


class Result(models.TextChoices):
    SUCCESS = 'success', 'Success'
    REFUSED = 'refuse', 'Refuse'
    PARTIAL = 'partial', 'Partial'
    REGURGITATION = 'regurgitation', 'regurgitation'


class Cause(models.TextChoices):
    DISEASE = 'disease', 'Disease'
    ACCIDENT = 'accident', 'Accident'
    OLD_AGE = 'old_age', 'Old age'
    REPRODUCTIVE = 'reproductive', 'Reproductive issue'
    UNKNOWN = 'unknown', 'Unknown'


class Criteria(models.TextChoices):
    WEIGHT = 'weight', 'Weight'
    AGE = 'age', 'Age'


class Type(models.TextChoices):
    LIVING_ANIMAL = 'living_animal', 'Living Animal'
    FROZEN_ANIMAL = 'frozen animal', 'Frozen Animal'
    VEGITABLE = 'vegitable', 'Vegitable'
    INSECT = 'insect', 'Insect'
    FISH = 'fish', 'Fish'
    OTHER = 'other', 'Other'


class Unit(models.TextChoices):
    ITEM = 'item', 'Item'
    KILOGRAM = 'kilogram', 'kg'
    GRAM = 'gram', 'g'


class BreedingResult(models.TextChoices):
    SUCCESS = 'success', 'Success'
    IN_PROGRESS = 'in_progress', 'In Progress'
    FAIL = 'fail', 'Fail'


class InbreedingLevel(models.IntegerChoices):
    OUTCROSS_ONLY = 0, "Outcross only (no relation)"
    DISTANT = 1, "Distant relation allowed"
    COUSIN = 2, "Cousin level allowed"
    LINEBREEDING = 3, "Linebreeding allowed"
    CLOSE = 4, "Close inbreeding allowed"