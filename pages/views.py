from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Account, Note


@login_required
@csrf_exempt
def homePageView(request):
	#Flaw 4: SQL Injection
	injection = request.GET.get("find", "")
	query = f"SELECT id, title FROM pages_note WHERE user_id = {request.user.id} AND title LIKE '%{injection}%'"
	notes = Note.objects.raw(query)

	return render(request, 'pages/index.html', {'notes': notes})

	#This would fix the injection problem:
	#
	# notes = Note.objects.filter(
	# 	user=request.user,
	# )


@login_required
@csrf_exempt
def noteAddView(request):
	if request.method == "POST":
		note = Note(
			user=request.user,
			title=request.POST.get("title"),
			content=request.POST.get("content"),
		)
		note.save()
	return redirect(request.META.get("HTTP_REFERER"), "/")


@login_required
def noteView(request, note_id):
    note = Note.objects.get(pk=note_id)
    return render(request, "pages/note.html", {"note": note})


@login_required
#Flaw 1: Broken Access Control
def noteDeleteView(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect("/")

	# if note.user != request.user: 
    # 	return HttpResponseForbidden() 