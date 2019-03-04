from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Movie, Review, Genre, Actor, Watch, User, GenreChoice
from .forms import UserModelForm, MovieModelForm, ReviewModelForm
from datetime import datetime
from operator import itemgetter
from django.db.models import Avg, Func, Count


# Create your views here.


def index(request):
    context = {}

    # sending context if user is logged in or not
    context['user_logged'] = False
    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    m = Movie.objects.annotate(Avg('review__rating'))
    context['featured'] = m.filter(special=Movie.FEATURED)[:7]
    context['trending'] = m.filter(special=Movie.TRENDING)[:7]
    context['new_release'] = m.all().order_by('-release_date')[:7]
    context['highest_rated'] = m.order_by('-review__rating__avg')[:7]

    return render(request, 'index.html', context)


def catalog(request, page=1):
    context = {}

    # sending context if user is logged in or not
    context['user_logged'] = False
    try:
        context['username'] = request.session['user']
        context['user_pic'] = User.objects.get(username=context['username']).display_pic
        context['user_logged'] = True
    except:
        pass

    context['genres'] = GenreChoice

    offset = page - 1
    m = Movie.objects.annotate(Count('review'), Avg('review__rating'))
    if request.method == 'POST':
        sorter = request.POST.get('sort', '')
        order = request.POST.get('order', '-')
        search = request.POST.get('search', '')
        min_rating = float(request.POST.get('min', 0))
        max_rating = float(request.POST.get('max', 5))
        show = int(request.POST.get('show', 0))
        offset *= show

        genres = []
        # For rendering the list of genres please use the genres context
        # example usage: for genre in GenreChoice:
        #                    <input type="text" name="{{genre.name}}" value="{{genre.value}}"/>
        for genre in GenreChoice:
            try:
                genres += request.POST[genre.name]
            except KeyError:
                pass

        if sorter == 'az':
            sorter = 'title'
        elif sorter == 'release':
            sorter = 'release_date'
        elif sorter == 'score':
            sorter = 'review__rating__avg'
        elif sorter == 'reviews':
            sorter = 'review__count'
        else:
            sorter = 'time_posted'

        filters = dict(title__contains=search, review__rating__range=(min_rating, max_rating), genres__in=genres)
        context['movies'] = m.filter(**filters).order_by(order + sorter)[0 + offset:show + offset]
    else:
        context['movies'] = m.all().order_by('-time_posted')[0 + offset:16 + offset]
    return render(request, 'catalog.html', context)


def details(request, movie_id):
    context = {}
    context['movie'] = Movie.objects.get(id=movie_id)
    reviews = context['movie'].review_set.all()
    reviews_reloaded = reviews.annotate(Avg('rating'))
    context['overall'] = reviews_reloaded.get('rating__avg', 0)
    context['count'] = reviews.count()
    context['breakdown'] = [reviews.get(rating=rating) for rating in range(6)]
    context['reviews'] = reviews
    context['trending'] = Movie.objects.filter(special=Movie.TRENDING)
    return render(request, 'details.html', context)


def user(request, username):
    context = {}
    context['user'] = User.objects.get(username=username)
    reviews = Review.objects.get(reviewer=context['user'])
    min_rating = request.GET.get('min', 0)
    max_rating = request.GET.get('max', 5)
    status = request.GET.get('status_r', 'active') == 'active'
    context['reviews'] = reviews.objects.filter(rating__range=(min_rating, max_rating)).filter(movie__isactive=status)

    movies = Movie.objects.get(posted_by=context['user'])
    status = request.GET.get('status_m', 'active') == 'active'

    # Hello, code below should be replaced with the ajax function of catalog

    context['genres'] = GenreChoice
    m = movies.objects.annotate(Count('review'), Avg('review__rating'))
    if request.method == 'POST':
        sorter = request.POST.get('sort', '')
        order = request.POST.get('order', '-')
        search = request.POST.get('search', '')
        min_rating = float(request.POST.get('min', 0))
        max_rating = float(request.POST.get('max', 5))
        show = int(request.POST.get('show', 0))

        genres = []
        # For rendering the list of genres please use the genres context
        # example usage: for genre in GenreChoice:
        #                    <input type="text" name="{{genre.name}}" value="{{genre.value}}"/>
        for genre in GenreChoice:
            try:
                genres += request.POST[genre.name]
            except KeyError:
                pass

        if sorter == 'az':
            sorter = 'title'
        elif sorter == 'release':
            sorter = 'release_date'
        elif sorter == 'score':
            sorter = 'review__rating__avg'
        elif sorter == 'reviews':
            sorter = 'review__count'
        else:
            sorter = 'time_posted'

        filters = dict(title__contains=search, review__rating__range=(min_rating, max_rating), genres__in=genres, isactive=status)
        context['movies'] = m.filter(**filters).order_by(order + sorter)[0:show]
    if username == request.session['user']:
        context['editable'] = True
    else:
        context['editable'] = False
    return render(request, 'user.html', context)


def login(request):
    context = {}
    if request.method == 'POST':
        try:
            m = User.objects.get(username=request.POST['username'])
            if m.password == request.POST['password']:
                request.session['id'] = m.id
                request.session['user'] = m.username
                request.session['type'] = m.usertype
                context['fail'] = False
                return JsonResponse(context)
            else:
                context['fail'] = True
                # return render(request, 'index.html', context)
                return JsonResponse(context)
        except:
            context['fail'] = True
            return JsonResponse(context)
    else:
        context['fail'] = False
        return JsonResponse(context)


def logout(request):
    try:
        del request.session['id']
        del request.session['user']
        del request.session['type']
    except KeyError:
        pass
    return redirect('/')


def signup(request):
    context = {}
    return render(request, 'signup.html', context)


def review(request, movie_id):
    # This is placeholder code for ajax review code
    context = {}
    # For checking if logged in, manual user creation huhu
    try:
        user_loggedin = User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/' + str(movie_id))
    movie = Movie.objects.get(id=movie_id)
    if request.method == 'POST':
        form = ReviewModelForm(request.POST)
        if form.is_valid():
            review = form.save()
            # Assign foreign keys below
            review.movie = movie
            review.reviewer = user_loggedin
            return redirect('/movie/' + str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review.html', context)
    else:
        context['form'] = ReviewModelForm()
        return render(request, 'review.html', context)


def edit_review(request, movie_id, review_id):
    # This is placeholder code for ajax review code
    context = {}
    review = Review.objects.get(id=review_id)
    # For checking if logged in, manual user creation huhu
    try:
        User.objects.get(request.session['id'])
    except KeyError:
        return redirect('/movie/' + str(movie_id))
    if request.method == 'POST':
        form = ReviewModelForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save()
            return redirect('/movie/' + str(movie_id))
        else:
            context['form'] = form
            return render(request, 'review_edit.html', context)
    else:
        context['form'] = ReviewModelForm(instance=review)
        return render(request, 'review_edit.html', context)


def post(request):
    context = {}
    if request.method == 'POST':
        form = MovieModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'addmovie.html', context)
    else:
        context['form'] = MovieModelForm()
        return render(request, 'addmovie.html', context)


def edit_post(request, movie_id):
    context = {}
    movie = Movie.objects.get(id=movie_id)
    context['movie'] = movie
    if request.method == 'POST':
        form = MovieModelForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('/movie/' + str(movie_id))
        else:
            context['form'] = form
            return render(request, 'editmovie.html', context)
    else:
        context['form'] = MovieModelForm(instance=movie)
        return render(request, 'editmovie.html', context)


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            context['form'] = form
            return render(request, 'signup.html', context)
    else:
        context['form'] = UserModelForm()
        return render(request, 'signup.html', context)
