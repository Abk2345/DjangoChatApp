from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
import json

class GetSuggestedFriendsViewTest(TestCase):
    def test_get_suggested_friends(self):
        # test user_id 
        user_id = 5

        # Loading JSON file with user data
        with open('friends/users.json', 'r') as json_file:
            data = json.load(json_file)

        # get request with user_id
        response = self.client.get(reverse('suggest-friends', args=[user_id]))

        # ok response?
        self.assertEqual(response.status_code, 200)

        # contains json?
        self.assertIsInstance(response, JsonResponse)

        # response contains the user_data, user_id, and suggested_friends keys ?
        content = json.loads(response.content)
        self.assertIn('user_data', content)
        self.assertIn('user_id', content)
        self.assertIn('suggested_friends', content)

        # maximum 5 friends?
        suggested_friends = content['suggested_friends']
        self.assertTrue(len(suggested_friends) <= 5)
