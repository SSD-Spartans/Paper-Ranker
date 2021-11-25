from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from .fetch_api import get_conference_ranks, to_lower, paper_details
from paper_search.models import Category, PaperDetail, ConferenceRank
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@require_http_methods(["POST", "GET"])
def search(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query')
        search_query = to_lower(search_query)
        if Category.objects.filter(title=search_query).exists():
            category = Category.objects.get(title=search_query)
            papers = PaperDetail.objects.filter(category=category)
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
            papers = PaperDetail.objects.filter(category=new_search_query)
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
            new_conference = ConferenceRank.objects.create(title=conf_title, name=conf_name, rank=conf_rank)
            new_conference.save()
        else:
            new_conference = ConferenceRank.objects.get(title=conf_title)
        if not PaperDetail.objects.filter(title=paper_title).exists():
            new_paper = PaperDetail.objects.create(title=paper_title, published_year=paper_year, url=paper_url,
                                                   category=new_category, conference=new_conference)
            new_paper.save()
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
            ret_message = "User Logged in Successfully"
            return render(request, 'search.html', {'msg': ret_message})
        else:
            ret_message = "No such user exists"
            return render(request, 'login.html', {'msg': ret_message})
    else:
        return render(request, 'login.html', None)


@login_required
@require_http_methods(["POST", "GET"])
def log_out(request):
    logout(request)
    return render(request, 'search.html', None)


@require_http_methods(["POST", "GET"])
def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'msg': "User already exists"})
        else:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            user.save()
            return render(request, 'login.html', {'msg': "User created successfully"})
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
                conference = ConferenceRank.objects.create(title=item[0], name=item[1], rank=item[2])
                conference.save()
    return "Done"

