from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Room, Message, PersonalMessage
from django.contrib.sessions.models import Session
from django.utils import timezone

class RoomsViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test rooms
        self.room1 = Room.objects.create(name='Room 1', slug='room-1')
        self.room2 = Room.objects.create(name='Room 2', slug='room-2')

    def test_authenticated_user_can_access_rooms(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the rooms view
        response = self.client.get(reverse('rooms'))

        # Check the HTTP response status code (200 OK)
        self.assertEqual(response.status_code, 200)

        # Check if the rooms are present in the response context
        self.assertIn(self.room1, response.context['rooms'])
        self.assertIn(self.room2, response.context['rooms'])

    def test_unauthenticated_user_redirected_to_login(self):
        # Make a GET request to the rooms view without logging in
        response = self.client.get(reverse('rooms'))

        # Check the HTTP response status code (302 Redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('rooms'))


class ActiveUsersTestCase(TestCase):
    
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        #create active session for the user
        # Create an active session for the user
        session = Session.objects.create(
            session_key='testsessionkey',
            expire_date=timezone.now() + timezone.timedelta(days=1)
        )
        session_data = session.get_decoded()
        session_data['_auth_user_id'] = self.user.pk
        session.save()

    def test_authenticated_user_can_access_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the view
        response = self.client.get(reverse('online_users'))

        # Check the HTTP response status code (200 OK)
        self.assertEqual(response.status_code, 200)

        self.assertIn(self.user, response.context['active_users'])

    def test_unauthenticated_user_redirected_to_login(self):
        # Make a GET request to the view without logging in
        response = self.client.get(reverse('online_users'))

        # Check the HTTP response status code (302 Redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('online_users'))


class RoomViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user_can_access_view(self):
        # Create a test room and some messages
        room = Room.objects.create(name='Test Room', slug='test-room')
        msg1 = Message.objects.create(room=room, user=self.user, content='Test message 1')
        msg2 = Message.objects.create(room=room, user=self.user, content='Test message 2')

        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the room view
        response = self.client.get(reverse('room', kwargs={'slug': 'test-room'}))

        # Check the HTTP response status code (200 OK)
        self.assertEqual(response.status_code, 200)

        # checking rendering of template
        self.assertTemplateUsed(response, 'rooms/room.html')

        # Check if the room  and messages are present in the response context
        self.assertEqual(room, response.context['room'])
        self.assertIn(msg1, response.context['messages'])
        self.assertIn(msg2, response.context['messages'])

    def test_unauthenticated_user_redirected_to_login(self):
        # Make a GET request to the room view without logging in
        response = self.client.get(reverse('room', kwargs={'slug': 'test-room'}))

        # Check the HTTP response status code (302 Redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('room', kwargs={'slug': 'test-room'}))


class PersonalChatUserTestCase(TestCase):
    def setUp(self):
        # Create two test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

        # Create a test message from user1 to user2
        self.message = PersonalMessage.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Test message from user1 to user2'
        )

        # Create a test client
        self.client = Client()

    def test_authenticated_user_can_access_view(self):
        # Log in user1
        self.client.login(username='user1', password='password1')

        # Make a GET request to the personal chat view
        url = reverse('personal-chat', args=['user2'])  # Assuming the username 'user2' exists
        response = self.client.get(url)

        # Check the HTTP response status code (200 OK)
        self.assertEqual(response.status_code, 200)

        # Check if the 'friend' and 'messages' context variables are passed to the template
        self.assertIn('friend', response.context)
        self.assertIn('messages', response.context)

    def test_unauthenticated_user_redirected_to_login(self):
        # Make a GET request to the personal chat view without logging in
        url = reverse('personal-chat', args=['user2'])  # Assuming the username 'user2' exists
        response = self.client.get(url)

        # Check the HTTP response status code (302 Redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_messages_displayed_for_authenticated_user(self):
        # Log in user1
        self.client.login(username='user1', password='password1')

        # Make a GET request to the personal chat view
        url = reverse('personal-chat', args=['user2'])  # Assuming the username 'user2' exists
        response = self.client.get(url)

        # Check if the message sent by user1 to user2 is displayed in the response
        self.assertContains(response, 'Test message from user1 to user2')

    def test_messages_not_displayed_for_unrelated_authenticated_user(self):
        # Log in user1
        self.client.login(username='user1', password='password1')

        # Make a GET request to the personal chat view for an unrelated user (user3)
        url = reverse('personal-chat', args=['user3'])  # Assuming the username 'user3' does not exist
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        # print(response.content)

        # assert context messages is empty queryset
        empty_query_set = PersonalMessage.objects.none()
        self.assertQuerysetEqual(empty_query_set, response.context['messages'])
