from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse

from random import choice
from . import util
from markdown2 import Markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "title": "Encyclopedia",
        "page_title" : "All Pages",
        "entries": util.list_entries()
    })

def page(request, title):
    markdown = Markdown()
    list = util.list_entries()
    if title not in list:
        raise Http404("Page Not Found")
    else:
        return render(request, "encyclopedia/page.html", {
            "title_page": title,
            "content": markdown.convert(util.get_entry(title))
            })


def create_page(request):
    list = util.list_entries()
    if request.method == "POST":
        items = request.POST
        title = items.get("title")
        content = items.get("entry")
        if title in list:
            return render(request, "encyclopedia/create.html", {
            "title": title,
            "content": content,
            "error": """<div class='alert alert-danger' role='alert'>
                            Page Already Exists. Change the Title
                        </div>""",
        })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:page", kwargs={"title" : title} ))
    else:
        return render(request, "encyclopedia/create.html")

def random(request):
    list = util.list_entries()
    r_title = choice(list)
    return HttpResponseRedirect(reverse("wiki:page", kwargs={"title" : r_title} ))

def edit_page(request, title):
    list = util.list_entries()
    list.remove(title)
    if request.method == "POST":
        items = request.POST
        new_title = items.get("title")
        content = items.get("entry")
        if new_title in list:
            return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content,
            "error": """<div class='alert alert-danger' role='alert'>
                            Page Already Exists. Change the Title
                        </div>""",
        })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("wiki:page", kwargs={"title" : title} ))
    else:
        return render(request, "encyclopedia/edit.html", {
            "title_page": title+":Edit",
            "title": title,
            "content": util.get_entry(title)
        })

def search(request):
    strs = []
    list = util.list_entries()
    if request.method == 'GET':
        search_title = request.GET.get("title")
        for each in list:
            if search_title.lower() == each.lower():
                return HttpResponseRedirect(reverse("wiki:page", kwargs={"title" : each} ))
            elif search_title.lower() in each.lower():
                strs.append(each)
        return render(request, "encyclopedia/index.html", {
            "title": "Search Results",
            "page_title": "Results for the search",
            "entries": strs,
            "if_none": "<h2>None Found</h2>"
        })
                