
from django.urls import reverse
from profiles import models

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token


class TestRegistrationTestCases(APITestCase):

    def test_create_account(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        response = self.client.post(path=url, data=data, format='json')
        user = models.User.objects.get(username="django-user")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()['message'], 'django-user Succesfully registerd !'
        )
        self.assertEqual(user.username, 'django-user')
        self.assertEqual(user.email, 'django@test.com')

    def test_create_account_password_not_matching(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "test"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()[0], "Password didn't match")

    def test_create_account_without_fields(self):
        url = reverse('register')
        data = {
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['username'][0], 'This field is required.'
        )

    def test_user_already_exists(self):
        url = reverse('register')
        data = {
            "username": "django-user",
            "email": "django@test.com",
            "password": "testpassword",
            "password_2": "testpassword"
        }
        models.User.objects.create_user(
            username='django-user',
            password='testpassword',
            email="django@test.com"
        )
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()[0], 'User with the given email already exists'
        )


class TestLogin(APITestCase):

    def setUp(self):
        models.User.objects.create_user(username='django', password='testpass')

    def test_successfull_login(self):
        url = reverse('login')
        data = {
            "username": "django",
            "password": "testpass"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unsuccessfull_login(self):
        url = reverse('login')
        data = {
            "username": "djangoooo",
            "password": "testpass"
        }
        response = self.client.post(path=url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json()['non_field_errors'][0],
            'Unable to log in with provided credentials.'
        )


class TestLogOut(APITestCase):

    def setUp(self):
        models.User.objects.create_user(username='django', password='testpass')

    def test_successfull_logout(self):
        self.token = Token.objects.get(user__username='django')
        url = reverse('logout')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(path=url)
        self.assertEqual(response.status_code, 200)


class TestGetProfiles(APITestCase):

    def setUp(self):
        self.user = models.User.objects.create_user(
            username='django', password='testpass'
        )
        self.token, self.created = Token.objects.get_or_create(
            user_id=self.user.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.path = reverse('list')

    def test_get_profile(self):
        response = self.client.get(path=self.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["username"], 'django')

    def test_get_profile_by_id_profile_doesnot_exist(self):
        response = self.client.get(
            path=reverse("detail", args=(2,)),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_profile_by_id(self):
        response = self.client.get(
            path=reverse("detail", args=(1,)),
        )
        self.assertEqual(response.status_code, 200)


class TestFollowUnfollow(APITestCase):

    def setUp(self):
        self.user = models.User.objects.create_user(
            username='django', password='testpass', email="django@gmail.com"
        )
        self.token, self.created = Token.objects.get_or_create(
            user_id=self.user.id
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_follow_request(self):
        path = "/profiles/2/follow"
        dummy_user = models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'successfully following dummy-user.')
        dummy_user.refresh_from_db()
        self.assertEqual(dummy_user.followers.count(), 1)

    def test_follow_request_target_user_not_found(self):
        path = "/profiles/5/follow"
        models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_request_already_following(self):
        path = "/profiles/2/follow"
        django_user = models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        django_user.followers.add(self.user.id)
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            f"You are already following {django_user.username}."
        )

    def test_unfollow_request(self):
        path = "/profiles/2/unfollow"
        django_user = models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        django_user.followers.add(self.user.id)
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(), f"successfully unfollowed {django_user.username}."
        )

    def test_unfollow_request_not_following(self):
        path = "/profiles/2/unfollow"
        django_user = models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(), f"you are not following {django_user.username}."
        )

    def test_follow_unfollow_request_invlid_action(self):
        path = "/profiles/2/dummy-action"
        models.User.objects.create_user(
            username='dummy-user', password='testpass', email="dummy@gmail.com"
        )
        response = self.client.post(path=path)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), "Invalid action")
