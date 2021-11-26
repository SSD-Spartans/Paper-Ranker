from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from .fetch_api import get_conference_ranks, to_lower, paper_details
from paper_search.models import Category, PaperDetail, ConferenceRank
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages


@require_http_methods(["POST", "GET"])
def search(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query')
        search_query = to_lower(search_query)
        if Category.objects.filter(title=search_query).exists():
            category = Category.objects.get(title=search_query)
            papers = PaperDetail.objects.filter(category=category).order_by('conference__priority')
            return render(request, 'search.html', {'valid': True, 'papers': papers})
        else:
            new_search_query = Category.objects.create(title=search_query)
            new_search_query.save()
            papers = paper_details(search_query)
            for element in papers:
                if not PaperDetail.objects.filter(title=element["title"]).exists():
                    if ConferenceRank.objects.filter(title=element["venue"]).exists():
                        paper_conference = ConferenceRank.objects.get(title=element["venue"])
                        paper_detail = PaperDetail.objects.create(title=element["title"],
                                                                  published_year=element["year"],
                                                                  url=element["url"], category=new_search_query,
                                                                  conference=paper_conference)
                        paper_detail.save()
                else:
                    # add category if not there to the current paper
                    pass
            papers = PaperDetail.objects.filter(category=new_search_query).order_by('conference__priority')
            return render(request, 'search.html', {'valid': True, 'papers': papers})
    elif request.method == "GET":
        return render(request, 'search.html', None)


@login_required
@require_http_methods(["POST", "GET"])
def add_paper(request):
    if request.method == "POST":
        category = request.POST['category']
        conf_title = request.POST["conference_title"]
        conf_name = request.POST["conference_name"]
        conf_rank = request.POST["conference_rank"]
        paper_title = request.POST["paper_title"]
        paper_year = request.POST["paper_year"]
        paper_url = request.POST["paper_url"]
        if not Category.objects.filter(title=category).exists():
            new_category = Category.objects.create(title=category)
            new_category.save()
        else:
            new_category = Category.objects.get(title=category)
        if not ConferenceRank.objects.filter(title=conf_title).exists():
            priority = 0
            if conf_rank == "A+":
                priority = 1
            elif conf_rank == "A":
                priority = 2
            elif conf_rank == "B":
                priority = 3
            else:
                priority = 4
            new_conference = ConferenceRank.objects.create(title=conf_title, name=conf_name, rank=conf_rank,
                                                           priority=priority)
            new_conference.save()
        else:
            new_conference = ConferenceRank.objects.get(title=conf_title)
        if not PaperDetail.objects.filter(title=paper_title).exists():
            new_paper = PaperDetail.objects.create(title=paper_title, published_year=paper_year, url=paper_url,
                                                   category=new_category, conference=new_conference)
            new_paper.save()
            messages.success(request, 'Paper added successfully!')
        return render(request, 'add_paper.html', {'msg': "Paper added successfully"})
    else:
        return render(request, 'add_paper.html', None)


@require_http_methods(["POST", "GET"])
def log_in(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'User Logged in Successfully!')
            return render(request, 'search.html', None)
        else:
            messages.success(request, 'Invalid Username or Password!')
            return render(request, 'login.html', None)
    else:
        return render(request, 'login.html', None)


@login_required
@require_http_methods(["POST", "GET"])
def log_out(request):
    logout(request)
    messages.success(request, 'User Logged out Successfully!')
    return render(request, 'search.html', None)


@require_http_methods(["POST", "GET"])
def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'User already exists!')
            return render(request, 'login.html', None)
        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            messages.success(request, 'User created Successfully!')
            return render(request, 'login.html', None)
    else:
        return render(request, 'login.html', None)


@user_passes_test(lambda u: u.is_superuser)
def clear_db(request):
    ConferenceRank.objects.all().delete()
    Category.objects.all().delete()
    PaperDetail.objects.all().delete()
    return "Done"


@user_passes_test(lambda u: u.is_superuser)
def add_conference_details(request):
    conferences = get_conference_ranks()
    for item in conferences:
        if len(item) == 3:
            if not ConferenceRank.objects.filter(title=item[0]).exists():
                priority = 0
                if item[2] == "A+":
                    priority = 1
                elif item[2] == "A":
                    priority = 2
                elif item[2] == "B":
                    priority = 3
                else:
                    priority = 4
                conference = ConferenceRank.objects.create(title=item[0], name=item[1], rank=item[2], priority=priority)
                conference.save()
    return "Done"
