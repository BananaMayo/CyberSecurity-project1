from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Account, Note


@login_required
def homePageView(request):
	accounts = Account.objects.exclude(user_id=request.user.id)

	notes = Note.objects.filter(
		user=request.user,
	)
	return render(request, 'pages/index.html', {'notes': notes})


@login_required
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
def noteDelete(request, note_id):
    note = Note.objects.get(pk=note_id)
    note.delete()
    return redirect("/")