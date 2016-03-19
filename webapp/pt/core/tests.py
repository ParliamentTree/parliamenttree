# THIRD PARTY
from djangae.test import TestCase
from django.test import TestCase
from django.utils import timezone

# PARLIAMENT TREE
from pt.core.constants import CONSTITUENCIES, PARTIES
from pt.core.models import MP, Speech, User, Like


class FlagsTest(TestCase):

    def test_like_objects_change_like_count(self):
        """ Creating and deleting Like objects should increment & decrement the like_count on the
            speech accordingly.
        """
        mp = MP.objects.create(
            name="Julius Caesar",
            constituency=CONSTITUENCIES.constants[0],
            party=PARTIES.constants[0]
        )
        speech = Speech.objects.create(
            mp=mp,
            timestamp=timezone.now(),
            text="Make dancing Tuesdays mandatory",
        )
        user = User.objects.create(mp=mp, constituency=mp.constituency)
        self.assertEqual(speech.like_count, 0)
        like = Like.objects.create(user=user, speech=speech)
        speech = Speech.objects.get(pk=speech.pk) # reload
        self.assertEqual(speech.like_count, 1)
        # Now re-save the Like and make sure it doesn't increment again
        like.save()
        speech = Speech.objects.get(pk=speech.pk) # reload
        self.assertEqual(speech.like_count, 1)
        # Now delete the Like.  The count should reset to 0.
        like.delete()
        speech = Speech.objects.get(pk=speech.pk) # reload
        self.assertEqual(speech.like_count, 0)

