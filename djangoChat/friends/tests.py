from django.test import TestCase
from django.urls import reverse
from django.http import JsonResponse
import json

class GetSuggestedFriendsViewTest(TestCase):
    def test_get_suggested_friends(self):
        # Create a test user_id for the GET request
        user_id = 5

        # Load a sample JSON file with user data
        with open('friends/users.json', 'r') as json_file:
            data = json.load(json_file)

        # Mock the request to the view
        response = self.client.get(reverse('suggest-friends', args=[user_id]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the response contains JSON data
        self.assertIsInstance(response, JsonResponse)

        # Check if the response contains the user_data, user_id, and suggested_friends keys
        content = json.loads(response.content)
        self.assertIn('user_data', content)
        self.assertIn('user_id', content)
        self.assertIn('suggested_friends', content)

        # Check if the suggested_friends list contains at most 5 items
        suggested_friends = content['suggested_friends']
        self.assertTrue(len(suggested_friends) <= 5)
