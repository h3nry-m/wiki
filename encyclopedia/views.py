from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from django.urls import reverse
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(label="Content")
    # content = forms.CharField(label="Content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def get_entry(request, title):
    return render(request, "encyclopedia/get_entry.html", {
        "entry": util.get_entry(title),
        "title": title.capitalize(),
    })


def new(request):
    error = False
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if title not in util.list_entries():
                content = form.cleaned_data['content']
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))
            else:
                error = True
                return render(request, "encyclopedia/new.html", {
                    "form": form,
                    "error": error,
                })
    return render(request, "encyclopedia/new.html", {
        "form": NewEntryForm()
    })
