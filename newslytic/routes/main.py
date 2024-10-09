from flask import Blueprint, render_template, request, make_response, current_app
import requests
import api_data.sources, api_data.languages, api_data.categories
import json
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Get the data from other source files
    categories = api_data.categories.categories
    sources = api_data.sources.sources
    languages = api_data.languages.languages

    selected_categories = (',').join(categories)
    # Parameters for the API request
    params = {
        'language': 'en',
        'number': 12,
        'categories': selected_categories
    }
    # Headers for the API request
    headers = {
        'x-api-key': current_app.config.get('API_KEY')
    }
    # Make the request to the API
    api_response = requests.get('https://api.worldnewsapi.com/search-news', params=params, headers=headers)

    if api_response.status_code != 200:
        return render_template('error.html', error = "You reached requests limit. Please try again later.", sources = sources,
                                languages = languages.keys(), categories = categories)
    
    news = process_response(api_response)

    response = make_response(render_template('news.html', news = news, sources = sources,
                                languages = languages.keys(), categories = categories))
    news_json = json.dumps(news)
    # Save the news in the cookie (for sorting)
    response.set_cookie("news", news_json)

    return response

@main_bp.route('/news', methods=['POST', 'GET'])
def news():
    # Get the data from other source files
    sources = api_data.sources.sources
    languages = api_data.languages.languages
    categories = api_data.categories.categories

    # If the request is POST, make the API request
    if request.method == 'POST':
        news = api()
        if not isinstance(news, list):
            return render_template('error.html', error = "You reached requests limit. Please try again later.", sources = sources,
                                   languages = languages.keys(), categories = categories)
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
    sources = api_data.sources.sources
    languages = api_data.languages.languages
    categories = api_data.categories.categories
    
    # API URL and key
    api_url = 'https://api.worldnewsapi.com/search-news'
    api_key = current_app.config.get('API_KEY')

    selected_categories = ""

    selected_sources = request.form.getlist('sources')
    
    # Check which categories are selected
    selected_categories = request.form.getlist('categories')
    # If no categories are selected
    if selected_categories == []:
        return render_template('error.html', error = "No categories selected. Please try again.", sources = sources,
                                languages = languages.keys(), categories = categories)
    
    include_sources = True

    # If no sources are selected select all sources
    if not selected_sources:
        include_sources = False
    
    selected_sources = ['https://www.' + item for item in selected_sources]

    # Making a string separated by commas from a list
    # according to API docs
    selected_sources = ','.join(selected_sources)
    selected_categories = (',').join(selected_categories)
    language = "en"
    language = request.form.get('language')

    # Parameters for the API request (depending on whether sources are selected)
    if include_sources: # If sources are selected
        params = {
            'categories': selected_categories,
            'language': api_data.languages.languages[language],
            'number': 12,
            'news-sources': selected_sources
        }
    else: # If sources are not selected (select all sources)
        params = {
            'categories': selected_categories,
            'language': api_data.languages.languages[language],
            'number': 12
        }

    headers = {
        'x-api-key': api_key
    }

    # Make the request to the API
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        return process_response(response)

    return None

# Process the response from the API
# Returns a list of dictionaries with necessary information for the news
def process_response(response):
    response = response.json()
    unprocessed_news = response['news']
    news = []
    category = "catgory"
    for item in unprocessed_news:
        domain = item['url'].split('https://')[1].split('/')[0]
        if 'www.' in domain:
            domain = domain.split('www.')[1]

        if "catgory" not in item.keys():
            category = "category"
        else: 
            category = "catgory"
        news_item = {
            'title': item['title'],
            'category': item[category], # Typo in the API response
            'image': item['image'],
            'url': item['url'],
            'publish_date': item['publish_date'], 
            'domain': domain
        }
        news.append(news_item)
    return news

# Sort the news based on the selected sorting option
def sort_news(news, sort_by):
    if sort_by == "source":
        news.sort(key = lambda x: x['domain'])
    elif sort_by == "category":
        news.sort(key = lambda x: x['category'])
    elif sort_by == "date":
        news.sort(key = lambda x: datetime.strptime(x['publish_date'], '%Y-%m-%d %H:%M:%S'), reverse = True)
    return news

