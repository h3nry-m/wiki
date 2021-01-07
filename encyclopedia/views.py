from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util
from collections import Counter
from random import randint


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


class SearchForm(forms.Form):
    search = forms.CharField(label="Search")


def get_entry(request, title):
    return render(request, "encyclopedia/get_entry.html", {
        "entry": util.get_entry(title),
        "title": title.capitalize(),
    })


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def random(request):
    max_number = len(util.list_entries())-1
    chosen_number = randint(0, max_number)
    chosen_entry = util.list_entries()[chosen_number]
    return HttpResponseRedirect(reverse('entry', args=(chosen_entry,)))


def results(request):
    if request.method == "GET":
        info = request.GET['search']
        if info in util.list_entries():
            return HttpResponseRedirect(reverse('entry', args=(info,)))
            # get_entry(request, info) <= can try doing it this way?
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
                "form": SearchForm(),
                "searched": info,
                "similar_words": similar_words,
                "exist": exist
            })
    return render(request, "encyclopedia/results.html")


def edit(request, title):
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
