from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from . import util
from django import forms
import secrets

import markdown


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
def entry(request,entry):  
    entrypage=util.get_entry(entry)
    if entrypage is None:
        return render(request,"encyclopedia/nonexistingentry.html",{
            "entryTitle":entry
        })
    else:
         return render(request,"encyclopedia/entry.html",{
         "entry":markdown.markdown(entrypage),
         "entryTitle":entry
        })
def search(request):
    value= request.GET["q"]
    if util.get_entry(value) is not None:
        return HttpResponseRedirect(reverse("entry",kwargs={'entry': value}))
    # else:
    #     substr=[]
    #     for entry in util.list_entries():
    #         if value.upper() in entry.upper():
    #             substr.append(entry)
    # return render(request,"encyclopedia/index.html",{
    #     "entries":substr,
    #     "search":True,
    #     "value":value
    # })
class newentry(forms.Form):
    title=forms.CharField(label="Entry Title",widget=forms.TextInput(attrs={'placeholder': 'enter the title','style':'margin-left:25px'}))
    newentry=forms.CharField(label="Entry Content",widget=forms.Textarea(attrs={'palceholder':'enter some content','style':'height:400px','style':'width:40px','style':'vertical-align:top'}))
    edit=forms.BooleanField(initial=False,widget=forms.HiddenInput(),required=False)

def newpage(request):
    if request.method=="POST":
        form=newentry(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            content=form.cleaned_data["newentry"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse("entry",kwargs={'entry':title}))
            else:
                return render(request,"encyclopedia/newentry.html",{
                    "form":form,
                    "existing": True,
                    "entrytitle":title
                })
        else:
            return render(request,"encyclopedia/newentry.html",{
                "form":form,
                "existing":False
            })
    else:
        return render(request,"encyclopedia/newentry.html",{
            "form":newentry(),
            "existing":False
        })
def edit(request,entry):
    entrypage=util.get_entry(entry)
    if entrypage is None:
        return render(request,"encyclopedia/nonexistingentry.html",{
            "entrytitle":entry
        })
    else:
        form = newentry()
        form.fields["title"].initial=entry
        form.fields["title"].widget=forms.HiddenInput()
        form.fields["newentry"].initial=entrypage
        form.fields["edit"].initial=True
        return render(request,"encyclopedia/newentry.html",{
            "form":form,
            "edit":form.fields["edit"],
            "entrytitle":form.fields["title"].initial
        })

def random( request):
    entries=util.list_entries()
    randomentry=secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry",kwargs={'entry':randomentry}))



