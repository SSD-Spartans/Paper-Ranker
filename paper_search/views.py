from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_http_methods
from .fetch_api import get_conference_ranks, get_paper_details
from paper_search.models import Category, PaperDetail, ConferenceRank


@require_http_methods(["POST", "GET"])
def search(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query')
        if Category.objects.filter(title=search_query).exists():
            category = Category.objects.get(title=search_query)
            papers = PaperDetail.objects.filter(category=category)
            return render(request, 'search.html', {'valid': True, 'papers': papers})
        else:
            return render(request, 'search.html', {'valid': False})

    elif request.method == "GET":
        return render(request, 'search.html', None)


@user_passes_test(lambda u: u.is_superuser)
def update_db(request):
    conferences = get_conference_ranks()
    for item in conferences:
        if len(item) == 3:
            if not ConferenceRank.objects.filter(title=item[0]).exists():
                conference = ConferenceRank.objects.create(title=item[0], name=item[1], rank=item[2])
                conference.save()
    paper_details = get_paper_details()
    if not Category.objects.filter(title="machine learning").exists():
        category = Category.objects.create(title="machine learning")
        category.save()
    else:
        category = Category.objects.get(title="machine learning")
    for item in paper_details:
        for element in item["data"]:
            if not PaperDetail.objects.filter(title=element["title"]).exists():
                if ConferenceRank.objects.filter(title=element["venue"]).exists():
                    paper_conference = ConferenceRank.objects.get(title=element["venue"])
                    paper_detail = PaperDetail.objects.create(title=element["title"], published_year=element["year"],
                                                              url=element["url"], category=category,
                                                              conference=paper_conference)
                    paper_detail.save()
    return
