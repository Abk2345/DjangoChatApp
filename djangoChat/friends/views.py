import json
from django.http import JsonResponse

def calculate_similarity(user1, user2):
    # age similarity
    age_difference = abs(user1['age'] - user2['age'])
    age_similarity = 1 / (age_difference + 1)  # handling divided by zero

    # interest similarity (common interest)
    shared_interests = set(user1['interests'].keys()) & set(user2['interests'].keys())
    interest_similarity = sum(
        user1['interests'][interest] * user2['interests'][interest]
        for interest in shared_interests
    )

    # calculating score after combining
    overall_similarity = (age_similarity + interest_similarity) / 2

    # print(overall_similarity)

    return overall_similarity


def recommend_friends(user_data, all_users_data):
    # similarity score for each user
    user_scores = []
    for user in all_users_data:
        if user['id'] != user_data['id']:
            similarity_score = calculate_similarity(user_data, user)
            user_scores.append((user, similarity_score))

    # users by similarity score in descending order
    user_scores.sort(key=lambda x: x[1], reverse=True)

    # Return the sorted list of users
    return [user_data for user_data, _ in user_scores]


# returning json file
def get_suggested_friends(request, user_id):
    # print(int(user_id))
    # loading json data
    with open('friends/users.json', 'r') as json_file:
        data = json.load(json_file)

    # Get the user data for the specified user_id

    # print(data['users'][0])

    data = data['users']
    # user_id = 5 # for testing
    user_data = None
    for user in data:
        if user['id'] == user_id:
            user_data = user
            break

    if not user_data:
        return JsonResponse({'error': 'User not found'}, status=404)

    # algorithm
    suggested_friends = recommend_friends(user_data, data)

    # top 5 suggested friends
    top_5_suggested_friends = suggested_friends[:5]

    context = {
        'user_data': user_data,
        'user_id': user_id,
        'suggested_friends': top_5_suggested_friends,
    }

    return JsonResponse(context)
