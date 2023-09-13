from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Room, Message, PersonalMessage
from django.contrib.sessions.models import Session
from django.utils import timezone

# Rooms Api (list of all chat rooms): 2 tests, one for authenticated, 1 for unauthenticated [since login is required to view chat rooms]
class RoomsViewTestCase(TestCase):
    def setUp(self):
        # test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # test rooms
        self.room1 = Room.objects.create(name='Room 1', slug='room-1')
        self.room2 = Room.objects.create(name='Room 2', slug='room-2')

    def test_authenticated_user_can_access_rooms(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # get rooms
        response = self.client.get(reverse('rooms'))

        # ok?
        self.assertEqual(response.status_code, 200)

        # both rooms are present in response?
        self.assertIn(self.room1, response.context['rooms'])
        self.assertIn(self.room2, response.context['rooms'])

    def test_unauthenticated_user_redirected_to_login(self):
        # request without logging in
        response = self.client.get(reverse('rooms'))

        # redirect?
        self.assertEqual(response.status_code, 302)

        # redirect to login?
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('rooms'))


# Active users api (list of active users except who is currently logged in) : 2 tests, 1 authenticated, 1 unauthenticated [since login is required to view chat rooms]

class ActiveUsersTestCase(TestCase):
    
    def setUp(self):
        # test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        #active session
        session = Session.objects.create(
            session_key='testsessionkey',
            expire_date=timezone.now() + timezone.timedelta(days=1)
        )
        session_data = session.get_decoded()
        session_data['_auth_user_id'] = self.user.pk
        session.save()

    def test_authenticated_user_can_access_view(self):
        # user logged in
        self.client.login(username='testuser', password='testpassword')

        # request to api using client
        response = self.client.get(reverse('online_users'))

        # ok?
        self.assertEqual(response.status_code, 200)

        # online users won't contain testuser as this person is logged in, so it will show other online users to logged in person
        self.assertNotIn(self.user, response.context['active_users'])

    def test_unauthenticated_user_redirected_to_login(self):
        # without logging in
        response = self.client.get(reverse('online_users'))

        # redirect ?
        self.assertEqual(response.status_code, 302)

        # redirect to log in?
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('online_users'))


# Detail view of chatroom api : 2 tests, authenticated and unauthenticated
class RoomViewTestCase(TestCase):
    def setUp(self):
        #test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_authenticated_user_can_access_view(self):
        # test room and some messages
        room = Room.objects.create(name='Test Room', slug='test-room')
        msg1 = Message.objects.create(room=room, user=self.user, content='Test message 1')
        msg2 = Message.objects.create(room=room, user=self.user, content='Test message 2')

        # user logged in using client
        self.client.login(username='testuser', password='testpassword')

        # get request to api with slug data
        response = self.client.get(reverse('room', kwargs={'slug': 'test-room'}))

        # ok?
        self.assertEqual(response.status_code, 200)

        # right template rendered?
        self.assertTemplateUsed(response, 'rooms/room.html')

        # room  and messages are present in the response context ?
        self.assertEqual(room, response.context['room'])
        self.assertIn(msg1, response.context['messages'])
        self.assertIn(msg2, response.context['messages'])

    def test_unauthenticated_user_redirected_to_login(self):
        # get request without logging in
        response = self.client.get(reverse('room', kwargs={'slug': 'test-room'}))

        # redirect ?
        self.assertEqual(response.status_code, 302)

        # redirect to log in?
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('room', kwargs={'slug': 'test-room'}))


# Personal chat between two users api: 4 tests: authenticated accessing view, unauthenticated redirected to login, right message sent and recieved between valid users, invalid users not receiving this message test
class PersonalChatUserTestCase(TestCase):
    def setUp(self):
        # two test users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.user3 = User.objects.create_user(username='user3', password='password3')

        # test message from user1 to user2
        self.message = PersonalMessage.objects.create(
            sender=self.user1,
            recipient=self.user2,
            content='Test message from user1 to user2'
        )

        # test client
        self.client = Client()

    def test_authenticated_user_can_access_view(self):
        # user1 logged in
        self.client.login(username='user1', password='password1')

        # get request to chat with user2
        url = reverse('personal-chat', args=['user2'])
        response = self.client.get(url)

        # ok?
        self.assertEqual(response.status_code, 200)

        # right messed passed in context
        self.assertIn('friend', response.context)
        self.assertIn('messages', response.context)

    def test_unauthenticated_user_redirected_to_login(self):
        # without logging in, accessing chat
        url = reverse('personal-chat', args=['user2'])
        response = self.client.get(url)

        # redirect ?
        self.assertEqual(response.status_code, 302)

        # redirected to login ?
        self.assertRedirects(response, reverse('login') + '?next=' + url)

    def test_messages_displayed_for_authenticated_user(self):
        # user1 logged in
        self.client.login(username='user1', password='password1')

        # get request to the personal chat view with user 2
        url = reverse('personal-chat', args=['user2'])  
        response = self.client.get(url)

        # right message in response ?
        self.assertContains(response, 'Test message from user1 to user2')

    def test_messages_not_displayed_for_unrelated_authenticated_user(self):
        # user1 logged in
        self.client.login(username='user1', password='password1')

        # get request to chat with unrelated user: user3
        url = reverse('personal-chat', args=['user3'])  
        response = self.client.get(url)

        # ok?
        self.assertEqual(response.status_code, 200)

        # print(response.content)

        # assert context messages is empty queryset, since no data have been sent from user1-> user3 or user3 -> user1
        empty_query_set = PersonalMessage.objects.none()
        self.assertQuerysetEqual(empty_query_set, response.context['messages'])
