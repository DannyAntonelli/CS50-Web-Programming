from markdown2 import Markdown
import random
from django.shortcuts import render, redirect
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    content = util.get_entry(entry)
    if content is None:
        return render(request, "encyclopedia/entry_not_found.html", {
            "title": entry
        })
    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "content": Markdown().convert(content)
    })
    

def newEntry(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if not title or not content:
            return render(request, "encyclopedia/new_entry.html", 
            {
                "text": "Title and content can't be empty.",
                "title": title,
                "content": content
            })
        if title in util.list_entries():
            return render(request, "encyclopedia/new_entry.html", 
            {
                "text": "A page with this title already exits.",
                "title": title,
                "content": content
            })
        util.save_entry(title, content)
        return redirect("entry", entry=title)
    return render(request, "encyclopedia/new_entry.html")


def edit(request, entry):
    content = util.get_entry(entry)
    if request.method == "POST":
        content = request.POST.get("content")
        if not content:
            return render(request, "encyclopedia/edit.html", 
            {
                "text": "Content can't be empty.",
                "title": entry,
                "content": content
            })
        util.save_entry(entry, content)
        return redirect("entry", entry=entry)
    return render(request, "encyclopedia/edit.html", 
    {
        "title": entry,
        "content": content
    })


def randomEntry(request):
    entries = util.list_entries()
    entry = random.choices(entries, k=1)[0]
    return redirect('entry', entry=entry)


def search(request):
    query = request.GET.get("q").lower()
    entries = [entry.lower() for entry in util.list_entries()]
    if query in entries:
        return redirect("entry", entry=query)
    search = []
    for entry in entries:
        if query in entry:
            search.append(entry)
    return render(request, "encyclopedia/search.html", 
    {
        "entries": search,
        "query": query
    })