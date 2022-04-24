from django.shortcuts import render
from . import util
from django import forms
from encyclopedia.templatetags import markdown_to_html
import random

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'style': 'width: 800px'}))
    content = forms.CharField(widget=forms.Textarea )

def index(request):
    request.session["entries"] = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": request.session["entries"]
    })

def display_html_entry(request, title, entry, editbutton):
    htmlfile = markdown_to_html.markdowntohtml(util.get_entry(title))
    return render(request, "encyclopedia/entry_template.html", {
        "content": htmlfile,
        "title": entry,
        "editbutton": editbutton
    })

def entry_doesnt_exist(request, title):
    return render(request, "encyclopedia/entry_template.html", {
        "content": f'<h3>ERROR: Page \'{title}\' does not exist </h3>',
        "editbutton": False
    })

def view_entry(request,title):
    for entry in request.session["entries"]:
        if title.upper() == entry.upper():
            return display_html_entry(request, title, entry, True)
    return entry_doesnt_exist(request, title)
            
def search_entry(request):
    search_title =  request.GET["q"]
    entries = request.session["entries"]
    search_list = [x for x in entries if x.upper().startswith(search_title.upper())]

    for entry in entries:
        if search_title.upper() == entry.upper():
            return display_html_entry(request, search_title, entry, True)
        if (entry.upper().startswith(search_title.upper())):
            return render(request, "encyclopedia/index.html", {
                "entries": search_list
            })
    return entry_doesnt_exist(request, search_title)

def random_entry(request):
    random_entry = (random.choice(request.session["entries"]))
    return view_entry(request, random_entry)

def new_entry(request):
    if request.method == "POST": 
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            for entry in request.session["entries"]:
                if title.upper() == entry.upper():
                    if request.POST["edit"]:
                        util.save_entry(title,content)
                        request.session["entries"] += [title]
                        return display_html_entry(request, title, entry, True)
                    
                    return render(request, "encyclopedia/entry_template.html", {
                        "content": f'<h3>ERROR: Page \'{title}\' already exists</h3>',
                        "title":title,
                        "editbutton": False
                    })
            else:
                util.save_entry(title,content)
                request.session["entries"] += [title]
    return render(request, "encyclopedia/new_entry.html",{
        "form": NewEntryForm(),
        "page_exists": False
    })

def edit_entry(request, title):
    form = NewEntryForm({
            "content":util.get_entry(title),
            "title": title
    })
    form.fields['title'].widget.attrs['readonly'] = True
    form.fields['title'].widget.attrs['class'] = 'grayOut'
    return render(request, "encyclopedia/new_entry.html",{ 
        "form": form,
        "page_exists": True
    })
