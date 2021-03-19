from django.shortcuts import render
import requests

class Data(object):
    def __init__(self, address, rating, review_count, link, name, image, score):
        self.address = address
        self.rating = rating
        self.review_count = review_count
        self.link = link
        self.name = name
        self.image = image
        self.score = score

# Create your views here.
def index(request):
    location = request.GET.get('location') or 'New York'
    results = call_api(location)
    return render(request, 'index.html', {'location_fill' : location, 'parking' : results})

def call_api(location):
    headers = {
        'Authorization': 'Bearer mi5qSSqdhmrNXBjLq5MBMwuqcS0q8aE4u52fwqrG8CkrBjjksgdV8ZblHdh4ThtDqQVFa'+
        'pfOwrCqadcTH4sJIMhQgEcWpc0bK_9ms_rJ1H-xMT1Amp4tmH_PhAg3X3Yx'}
    response = requests.request('GET', 'https://api.yelp.com/v3/businesses/search?categories=parking&location='+location,
                                headers=headers)
    if response.status_code != 200:
        return None

    response = response.json()['businesses']

    results_arr = []
    for biz in response:
        response_json = dict()
        response_json['address'] = biz.get('location').get('display_address')[0] or None
        response_json['rating'] = biz.get('rating') or None
        response_json['review count'] = biz.get('review_count') or None
        response_json['link'] = biz.get('url') or None
        response_json['name'] = biz.get('name') or None
        response_json['image_url'] = biz.get('image_url') or None

        score = (response_json['review count'] * response_json['rating']) / (response_json['review count'] + 1)
        score = round(score, 2)

        results_arr.append(Data(response_json['address'],
                                response_json['rating'],
                                response_json['review count'],
                                response_json['link'],
                                response_json['name'],
                                response_json['image_url'],
                                score))
    return sorted(results_arr, key=lambda x: x.score)


