import csv
from collections import defaultdict

class FriendRecommender:
    def __init__(self, social_graph):
        """
        social_graph: dict[str, set[str]]
        A mapping from user to set of friends.
        """
        self.social_graph = social_graph

    def recommend(self, user, top_n=5):
        friends = self.social_graph.get(user, set())
        recommendations = defaultdict(int)

        for friend in friends:
            friends_of_friend = self.social_graph.get(friend, set())
            for fof in friends_of_friend:
                if fof != user and fof not in friends:
                    recommendations[fof] += 1

        sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)
        return sorted_recs[:top_n]

def load_friendships_from_csv(filepath):
    social_graph = defaultdict(set)
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user = row['user']
            friend = row['friend']
            social_graph[user].add(friend)
    return social_graph

if __name__ == "__main__":
    filepath = 'friendships.csv'
    social_graph = load_friendships_from_csv(filepath)

    recommender = FriendRecommender(social_graph)
    user = 'Alice'
    recommendations = recommender.recommend(user)

    print(f"Friend recommendations for {user}:")
    for friend, mutual_count in recommendations:
        print(f"- {friend} ({mutual_count} mutual friends)")
