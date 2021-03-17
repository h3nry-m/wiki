from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
from collections import Counter
from random import randint
from markdown2 import Markdown


class NewEntryForm(forms.Form):
    """A class to facilitate creating new search forms"""
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


class SearchForm(forms.Form):
    """A class to faciliate creating new search forms"""
    search = forms.CharField(label="Search")


def get_entry(request, title):
    """Retrieves the entry and converts the entry information into Markdown formatting"""
    item_of_interest = util.get_entry(title)
    markdowner = Markdown()
    new = markdowner.convert(item_of_interest)
    return render(request, "encyclopedia/get_entry.html", {
        "entry": new,
        "title": title.capitalize(),
    })


def index(request):
    """Main page with a list of all entries"""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def random(request):
    """Returns a random page based off the existing entries"""
    max_number = len(util.list_entries())-1
    chosen_number = randint(0, max_number)
    chosen_entry = util.list_entries()[chosen_number]
    return HttpResponseRedirect(reverse('entry', args=(chosen_entry,)))


def results(request):
    """Returns the appropriate page if search results are found. If not then redirects to a different page that has results close to the search parameter."""
    if request.method == "GET":
        info = request.GET['search']
        if info in util.list_entries():
            return HttpResponseRedirect(reverse('entry', args=(info,)))
            # get_entry(request, info) <= can also try doing it this way
        else:
            exist = False
            reference = Counter(info.lower())
            temp = []
            for word in util.list_entries():
                temp.append([Counter(word.lower()), word])
            similar_words = []
            for key, word in temp:
                if reference & key == reference:
                    similar_words.append(word)
            if len(similar_words) > 0:
                exist = True
            return render(request, "encyclopedia/results.html", {
                "searched": info,
                "similar_words": similar_words,
                "exist": exist
            })
    return render(request, "encyclopedia/results.html")


def edit(request, title):
    """Allows edit of the post and redirects to the same page"""
    if request.method == "POST":
        form = request.POST
        title = form['title']
        content = form['content']
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=(title,)))
    return render(request, "encyclopedia/edit.html", {
        "content": util.get_entry(title),
        "title": title.capitalize()
    })


def new(request):
    """Allows creation of a new post and redirects to the new page"""
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title not in util.list_entries():
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", args=(title,)))
            else:
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": True,
                })
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })
