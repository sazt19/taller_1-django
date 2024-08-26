from django.shortcuts import render
from django.http import HttpResponse

from .models import Movie
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

# Create your views here.

def home(request):
    #return HttpResponse('<h1>Welcome to home page </h1>')
    #return render(request, 'home.html', {'name':'Sara Zuluaga'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm':searchTerm, 'movies':movies})

def about(request):
    return render(request,'about.html')

def statistics_view(request):
    matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year')
    genres = Movie.objects.values_list('genre', flat=True).distinct().order_by('genre')
    movie_counts_by_year = {}
    movie_counts_by_genre = {}
    for year in years:
        if year:
            movie_in_year = Movie.objects.filter(year=year)
        else:
            movie_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movie_in_year.count()
        movie_counts_by_year[year] = count

    for genre in genres:
        if genres:
            movie_in_genre = Movie.objects.filter(genre=genre)
        else:
            movie_in_genre = Movie.objects.filter(genre__isnull=True)
            genre = "None"
        count_g = movie_in_genre.count()
        movie_counts_by_genre[genre] = count_g

    bar_width = 0.5
    bar_spacing = 0.5
    bar_positions = range(len(movie_counts_by_year))
    bar_positions_genre = range(len(movie_counts_by_genre))

    #movies per year chart
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    #movies per genre chart
    plt.bar(bar_positions_genre, movie_counts_by_genre.values(), width=0.7, align='center')
    plt.title('Movies per genre')
    plt.xlabel('Genre')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions_genre, movie_counts_by_genre.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.4)
    plt.tight_layout()
    buffer_1 = io.BytesIO()
    plt.savefig(buffer_1, format='png')
    buffer_1.seek(0)
    plt.close()

    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    genre_png = buffer_1.getvalue()
    buffer_1.close()
    graphic_2 = base64.b64encode(genre_png)
    graphic_2 = graphic_2.decode('utf-8')

    return render(request, 'statistics.html', {'graphic':graphic,'graphic_2':graphic_2})