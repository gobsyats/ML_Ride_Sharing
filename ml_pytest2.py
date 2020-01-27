import constants
from sklearn.feature_extraction import DictVectorizer
from sklearn.metrics.pairwise import cosine_similarity



def vectorDistance(data, len):

    vec = DictVectorizer()
    matrix = vec.fit_transform(data)
    print(matrix.toarray())
    similarity_scores = cosine_similarity(matrix)
    print(similarity_scores)
    rider_index = []
    matching_score = similarity_scores[0, 1]
    print("Printing the  similarity")
    for i in range(1, len(similarity_scores)):
        print(similarity_scores[0, i])
        if similarity_scores[0, i] > 0.80:
            rider_index.append(i)
            print(i)

    return matching_score

scoreDict1 = {"chatty": 4, "safety": 6, "punctuality": 3, "friendlinees": 1, "comfortibility": 2}
scoreDict2 = {"chatty": 3, "safety": 2, "punctuality": 2, "friendlinees": 3, "comfortibility": 4}
scoreDict3 = {"chatty": 1, "safety": 3, "punctuality": 1, "friendlinees": 4, "comfortibility": 5}
scoreDict4 = {"chatty": 3, "safety": 2, "punctuality": 3, "friendlinees": 5, "comfortibility": 2}
scoreDict5 = {"chatty": 2, "safety": 1, "punctuality": 4, "friendlinees": 3, "comfortibility": 3}
scoreDict6 = {"chatty": 1, "safety": 5, "punctuality": 2, "friendlinees": 4, "comfortibility": 5}
scoreDict7 = {"chatty": 5, "safety": 2, "punctuality": 1, "friendlinees": 1, "comfortibility": 1}
scoreDict8 = {"chatty": 3, "safety": 2, "punctuality": 4, "friendlinees": 2, "comfortibility": 2}
scoreDict9 = {"chatty": 2, "safety": 1, "punctuality": 1, "friendlinees": 4, "comfortibility": 1}
scoreDict10 = {"chatty": 1, "safety": 4, "punctuality": 5, "friendlinees": 3, "comfortibility": 1}
data = [scoreDict1, scoreDict2, scoreDict3, scoreDict4, scoreDict5, scoreDict6, scoreDict7, scoreDict8, scoreDict9, scoreDict10]
print(len(data))
matching_score = vectorDistance(data, len)
print(matching_score)