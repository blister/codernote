from models import Note
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import render_to_response
from forms import NoteForm
import re
from django.core import serializers

""" Utilities """

def slugify(string):
    string = re.sub('\s+', '_', string)
    string = re.sub('[^\w.-]', '', string)
    return string.strip('_.- ').lower()


def find_slug_for(string):
    i = 0
    new_str = string
    while (Note.objects.filter(slug=new_str).count() > 0):
        new_str = u"%s%s" % (string, i)
        i = i + 1
    return new_str

def make_tags_uniform(string):
    return string.replace(", "," ").replace("  "," ").replace(" ",", ")


""" Note """

def note_list(request):
    'Non-Ajax view.'
    extra = {'serialized':serializers.serialize("json", Note.objects.all()) }
    return render_to_response('codernote/note_list.html', extra)

def note_detail(request, slug):
    'Non-Ajax view.'
    note = Note.objects.get(slug=slug)
    extra = {'object':note}
    return render_to_response('codernote/note_detail.html', extra)


def note_create(request):
    'Non-Ajax view.'
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.slug = find_slug_for(slugify(new_note.title))
            new_note.tags = make_tags_uniform(new_note.tags)
            new_note.save()
            return HttpResponseRedirect(new_note.get_absolute_url())
    else:
        form = NoteForm()
    extra = {'create_form':form}
    return render_to_response('codernote/note_create.html', extra)

def note_info_all(request):
    pass

def note_info(request, slug=None):
    pass


def note_delete(request, slug=None):
    pass

def note_update(request, slug=None):
    if slug is None:
        if request.POST.has_key('slug'):
            slug = request.POST['slug']
        else:
            return HttpResponseServerError('Failed to supply a slug.')
    try:
        note = Note.objects.get(slug=slug)
    except:
        return HttpResponse("Failed to retrieve note.")
    updated = []
    if request.POST.has_key('title'):
        note.title = request.POST['title']
        updated.append('title')
    if request.POST.has_key('tags'):
        note.tags = request.POST['tags']
        updated.append('tags')
    note.save()

    msg = "Updated %s." % ", ".join(updated)
    return HttpResponse(msg)
    


""" Non-Authenticated Views """

def front(request):
    pass

def about(request):
    pass

def help(request):
    pass


""" Config """

def config(request):
    pass


""" Rendering """

def render_markdown(request):
    pass

def render_textile(request):
    pass

def render_syntax(request):
    pass
