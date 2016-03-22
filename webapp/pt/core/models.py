# THIRD PARTY
from djangae.db import transaction
from djangae.fields import CharField, SetField, RelatedSetField
from django.db import models

# PARLIAMENT TREE
from pt.core.constants import CONSTITUENCIES, PARTIES


class BaseModel(models.Model):
    """ Base model for all other models. """

    class Meta(object):
        abstract = True

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class MP(BaseModel):
    """ A member of parliament. """

    name = CharField()
    constituency = CharField(
        # Note that this field is unique, but is nullable so that when the MP of a constituency
        # changes we don't have to delete the old one (or their speeches), we just wipe this field
        choices=CONSTITUENCIES.choices,
        unique=True,
        null=True,
    )
    party = CharField(choices=PARTIES.choices)


class Speech(BaseModel):
    """ The words spoken by an MP in a single "speech".
        A "speech" will probably be the words spoken in a single instance of an MP standing up, but
        it might depend on how Hansard publishes the data.
    """

    mp = models.ForeignKey(MP)
    timestamp = models.DateTimeField(
        help_text="The time when the MP spoke these words (not when this was saved to the DB)"
    )
    hansard_url = models.URLField(
        help_text="The URL of where this speech is located on the Hansard website"
    )
    text = models.TextField()
    keywords = SetField(
        CharField(),
        # Not sure if this should be the non-filler words, or the words which users are actually
        # following at the time when it's saved.  TBD.
        help_text="Words from the speech which are relevant for querying by"
    )
    # These fields store the number of users that have like/disliked/flagged this speech.
    # For each of these counts there is a separate "through" table between the users and the
    # speeches, but because we're on a non-relational DB and can't actually JOIN those tables, we
    # store these plain counts directly on the Speech model.
    # These may need sharded counters if we get a lot of users liking/disliking things at the same
    # time, but keeping it simple for now.
    like_count = models.PositiveIntegerField(default=0)
    dislike_count = models.PositiveIntegerField(default=0)
    is_filibustering_count = models.PositiveIntegerField(default=0)
    fact_check_request_count = models.PositiveIntegerField(default=0)


class User(BaseModel): # TODO: subclass Django/Djangae user base model, or something
    """ A public user who is registered on the site. """

    constituency = CharField(choices=CONSTITUENCIES.choices)
    mp = models.ForeignKey(MP) # this can be calculated from constituency, but shortcut for speed.
    follows_mps = RelatedSetField(
        MP,
        help_text="MPs which this user wants to get/see info/updates/notifications about",
        blank=True,
    )
    follows_keywords = SetField(
        CharField(),
        help_text="Keywords which this user wants to know about when an MP says them",
        blank=True,
    )

    def save(self, *args, **kwargs):
        # Make the user follow their own MP.  # TODO: maybe don't be so forceful!
        self.follows_mps_ids.add(self.mp_id)
        return super(User, self).save(*args, **kwargs)


class FlagBaseModel(BaseModel):
    """ Base model for all of the things where a User flags a Speech as <something>.
        All of the subclasses of this model are like "through" tables for a M2M, but we can't JOIN
        them, hence they each have a spearate <something>_count field on the Speech model.
    """
    speech_model_count_field = NotImplemented

    class Meta(object):
        abstract = True

    user = models.ForeignKey(User)
    speech = models.ForeignKey(Speech)

    def save(self, *args, **kwargs):
        """ Ensure that the count field on the Speech is incremented when this is created. """
        if self._state.adding:
            with transaction.atomic(xg=True):
                speech = Speech.objects.get(pk=self.speech_id) # reload inside transaction
                value = getattr(speech, self.speech_model_count_field)
                setattr(speech, self.speech_model_count_field, value + 1)
                speech.save()
                return super(FlagBaseModel, self).save(*args, **kwargs)
        else:
            return super(FlagBaseModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """ Ensure that the count field on the Speech is decremented when this is deleted. """
        with transaction.atomic(xg=True):
            speech = Speech.objects.get(pk=self.speech_id) # reload inside transaction
            value = getattr(speech, self.speech_model_count_field)
            setattr(speech, self.speech_model_count_field, value - 1)
            speech.save()
            return super(FlagBaseModel, self).delete(*args, **kwargs)


class Like(FlagBaseModel):
    """ Records the fact that a particular User likes a particular Speech. """
    speech_model_count_field = "like_count"


class Dislike(FlagBaseModel):
    """ Records the fact that a particular User dislikes a particular Speech. """
    speech_model_count_field = "dislike_count"


class Filibust(FlagBaseModel):
    """ Records the fact that a particular User thinks that a particular Speech is filibustering.
        Busted!
    """
    speech_model_count_field = "is_filibustering_count"


class FactCheckRequest(FlagBaseModel):
    """ Recordss the fact that a particular User wants a particular Speech to be fact checked. """
    speech_model_count_field = "fact_check_request_count"





