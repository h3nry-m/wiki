from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


class SearchForm(forms.Form):
    search = forms.CharField(label="Search")


class InfoForm(forms.Form):
    # title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def results(request):
    if request.method == "GET":
        info = request.GET['search']
        if info in util.list_entries():
            return HttpResponseRedirect(reverse('entry', args=(info,)))
            # get_entry(request, info) <= can try doing it this way?
        else:
            return render(request, "encyclopedia/results.html", {
                "form": SearchForm(),
                "searched": info
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


def get_entry(request, title):
    return render(request, "encyclopedia/get_entry.html", {
        "entry": util.get_entry(title),
        "title": title.capitalize(),
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
