from flask import Blueprint, render_template, request
import requests
import api_data.sources, api_data.languages, api_data.categories

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    sources = api_data.sources.sources
    languages = api_data.languages.languages
    categories = api_data.categories.categories
    return render_template('base.html', sources = sources, languages = languages.keys(), categories = categories)

@main_bp.route('/api', methods=['POST'])
def api():
    # API URL and key
    api_url = 'https://api.worldnewsapi.com/search-news'
    api_key = '81ffe890f50d4d81a8981fd178df573a' # Later requires to be hidden and changed

    selected_categories = ""
    categories = api_data.categories.categories

    selected_sources = request.form.getlist('sources')
    
    # Check which categories are selected
    for category in categories:
        if request.form.get(category): # If the category is selected
            if selected_categories == "":
                selected_categories += category
            else:
                selected_categories += ',' + category
    # If no categories are selected
    if categories == "":
        return "No categories selected"
    
    include_sources = True
    # If no sources are selected select all sources
    if not selected_sources:
        include_sources = False
    
    selected_sources = ['https://www.' + item for item in selected_sources]
    # Making a string separated by commas from a list
    # according to API docs
    selected_sources = ','.join(selected_sources)

    language = request.form.get('language')

    # Parameters for the API request (depending on whether sources are selected)
    if include_sources:
        params = {
            'categories': selected_categories,
            'language': api_data.languages.languages[language],
            'number': 10,
            'news-sources': selected_sources
        }
    else:
        params = {
            'categories': selected_categories,
            'language': api_data.languages.languages[language],
            'number': 10
        }

    headers = {
        'x-api-key': api_key
    }

    # Make the request to the API
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()

    return response.status_code
