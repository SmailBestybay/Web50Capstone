from django.test import TestCase
from network.models import User, Post, UserFollowing, Like

# Create your tests here.
# https://www.youtube.com/watch?v=hA_VxnxCHbo&ab_channel=TheDumbfounds
# https://docs.djangoproject.com/en/4.0/topics/testing/tools/


class ModelsTest(TestCase):
    
    def setUp(self) -> None:
        
        # Create Users
        User.objects.create_user('john', 'john@eagles.com', 'johnpassword').save()
        User.objects.create_user('paul', 'paul@eagles.com', 'paulpassword').save()
        
        # Get Users
        self.u1 = User.objects.get(username='john')
        self.u2 = User.objects.get(username='paul')

        # Create Post
        self.p1 = Post.objects.create(user=self.u1, content="Test contents").save()


        # Create valid and invalid UserFollowing
        UserFollowing.objects.create(user=self.u1, following_user=self.u2)
        UserFollowing.objects.create(user=self.u1, following_user=self.u1)


    def test_valid_user_following(self):
        f1 = UserFollowing.objects.get(user=self.u1, following_user=self.u2)
        self.assertTrue(f1.is_valid_follow())

    def test_invalid_user_following(self):
        f1 = UserFollowing.objects.get(user=self.u1, following_user=self.u1)
        self.assertFalse(f1.is_valid_follow())

    def test_valid_post_like_count(self):
        p1 = Post.objects.get(user=self.u1)
        Like(user=self.u1, post=p1).save()
        self.assertEqual(1, p1.likes.count())


    

