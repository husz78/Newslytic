from flask import Blueprint, render_template, request, make_response
import requests
import api_data.sources, api_data.languages, api_data.categories
import json
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    sources = api_data.sources.sources
    languages = api_data.languages.languages
    categories = api_data.categories.categories
    return render_template('base.html', sources = sources, languages = languages.keys(), categories = categories)

@main_bp.route('/news', methods=['POST', 'GET'])
def news():
    # Get the data from other source files
    sources = api_data.sources.sources
    languages = api_data.languages.languages
    categories = api_data.categories.categories

    # If the request is POST, make the API request
    if request.method == 'POST':
        news = api()
        response = make_response(render_template('news.html', news = news, sources = sources,
                                languages = languages.keys(), categories = categories))
        news_json = json.dumps(news)
        response.set_cookie("news", news_json)
        
        return response
    
    # If the request is GET, get the news from the cookie and sort it
    elif request.method == 'GET':
        # Get the news from the cookie and parse json
        news = json.loads(request.cookies.get('news'))

        # Get the sorting method from the request
        sorting_method = request.args.get('sort_by')

        # Sort the news based on the selected sorting method
        # If the sorting method is not selected don't sort the news
        if sorting_method == "source":
            sort_news(news, "source")
            sort_by = "source"
        elif sorting_method == "category":
            sort_news(news, "category")
            sort_by = "category"
        elif sorting_method == "publish_date":
            sort_news(news, "date")
            sort_by = "publish_date"
        else:
            sort_by = ""
            
    return render_template('news.html', news = news, sources = sources, sort_by = sort_by,
                            languages = languages.keys(), categories = categories)
    


# Function to make the API request
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
    if selected_categories == "":
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
    if include_sources: # If sources are selected
        params = {
            'categories': selected_categories,
            'language': api_data.languages.languages[language],
            'number': 10,
            'news-sources': selected_sources
        }
    else: # If sources are not selected (select all sources)
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
        return process_response(response)

    return response.status_code

# Process the response from the API
# Returns a list of dictionaries with necessary information for the news
def process_response(response):
    response = response.json()
    unprocessed_news = response['news']
    news = []
    for item in unprocessed_news:
        news_item = {
            'title': item['title'],
            'category': item['catgory'], # Typo in the API response
            'image': item['image'],
            'url': item['url'],
            'publish_date': item['publish_date'], 
        }
        news.append(news_item)
    return news

# Sort the news based on the selected sorting option
def sort_news(news, sort_by):
    if sort_by == "source":
        news.sort(key = sort_by_source)
    elif sort_by == "category":
        news.sort(key = lambda x: x['category'])
    elif sort_by == "date":
        news.sort(key = lambda x: datetime.strptime(x['publish_date'], '%Y-%m-%d %H:%M:%S'), reverse = True)
    return news

# Sort the news by source
def sort_by_source(article):
    domain = article['url'].split('https://')[1].split('/')[0]
    return domain
