from flask import Blueprint, render_template, request
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('base.html')

@main_bp.route('/api', methods=['POST'])
def api():
    # API URL and key
    api_url = 'https://api.worldnewsapi.com/search-news'
    api_key = '81ffe890f50d4d81a8981fd178df573a'

    # These are the categories that the API supports
    categories = ["politics", "sports", "business", "technology", "entertainment", "health", "science",
                  "lifestyle", "travel", "culture", "education", "environment", "other"]
    selected_categories = ""

    # Check which categories are selected
    for category in categories:
        if request.form.get(category): # If the category is selected
            if selected_categories == "":
                selected_categories += category
            else:
                selected_categories += ',' + category

    params = {
        'categories': selected_categories,
        'language': 'en',
        'source-countries': 'us',
        'number': 10,
    }

    headers = {
        'x-api-key': api_key
    }

    # Make the request to the API
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()

    return response.status_code
