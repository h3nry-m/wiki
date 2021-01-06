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
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def results(request):
    if request.method == "GET":
        info = request.GET['search']
        if info in util.list_entries():
            print('1st part')
            return HttpResponseRedirect(reverse('entry', args=(info,)))
            # get_entry(request, info) <= can try doing it this way?
        else:
            print("2nd part")
            return render(request, "encyclopedia/results.html", {
                "form": SearchForm(),
                "searched": info
            })
    print("3rd part")
    return render(request, "encyclopedia/results.html")


def edit(request, title):
    if request.method == "POST":
        form = InfoForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))
        # else:
        #     return render(request, "encyclopedia/edit.html", {
        #         "form": form,
        #         "content": util.get_entry(title),
        #         "title": title.capitalize(),
        #     })
    return render(request, "encyclopedia/edit.html", {
        "form": InfoForm(),
        "content": util.get_entry(title),
        "title": title.capitalize()
        # return render(request, "encyclopedia/edit.html", {
        #     "entry": util.get_entry(title),
        #     "title": title.capitalize(),
    })


def get_entry(request, title):
    return render(request, "encyclopedia/get_entry.html", {
        "entry": util.get_entry(title),
        "title": title.capitalize(),
    })


def new(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        print('First part, ', form)
        if form.is_valid():
            title = form.cleaned_data['title']
            print('Title is ', title)
            if title not in util.list_entries():
                content = form.cleaned_data['content']
                print('Content is ', content)
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
