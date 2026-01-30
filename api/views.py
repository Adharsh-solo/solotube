import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urllib.parse import quote_plus

API_KEY = "c00978db"
# YouTube API Key - Get one from https://console.cloud.google.com/apis/credentials
# For now, using a fallback method that doesn't require API key
YOUTUBE_API_KEY = None  # Set your YouTube API key here if you have one

@api_view(['GET'])
def get_data(request):
    query = request.GET.get("q", "stranger things")
    url = f"https://www.omdbapi.com/?s={query}&apikey={API_KEY}"

    response = requests.get(url)
    data = response.json()

    return Response(data)

@api_view(['GET'])
def get_trailer(request):
    movie_title = request.GET.get("title", "")
    year = request.GET.get("year", "")
    
    search_query = f"{movie_title} {year} official trailer"
    
    # If YouTube API key is available, use it
    if YOUTUBE_API_KEY:
        youtube_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={quote_plus(search_query)}&type=video&key={YOUTUBE_API_KEY}&maxResults=1"
        
        try:
            response = requests.get(youtube_url)
            data = response.json()
            
            if data.get('items') and len(data['items']) > 0:
                video_id = data['items'][0]['id']['videoId']
                embed_url = f"https://www.youtube.com/embed/{video_id}?autoplay=1"
                return Response({"trailerUrl": embed_url})
        except Exception as e:
            print(f"YouTube API error: {e}")
    
    # Fallback: Use YouTube's search embed (less reliable but works without API key)
    # This uses YouTube's nocookie domain and search functionality
    search_encoded = quote_plus(search_query)
    # Return a search URL that can be used to find the trailer
    # Frontend will handle displaying this appropriately
    return Response({
        "trailerUrl": None, 
        "searchQuery": search_query,
        "message": "Please configure YouTube API key for direct trailer access, or search manually"
    })
