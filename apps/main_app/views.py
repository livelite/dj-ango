from django.shortcuts import render, redirect
from .models import *
import bcrypt

def index(request):
	context = {
		'users': User.objects.all()
	}
	return render(request, "main_app/index.html", context)

def register(request):
	if request.method == 'POST':
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		email = request.POST.get('email')
		password = request.POST.get('pass')
		passwordc = request.POST.get('passc')

		if User.objects.is_user_valid(request, fname, lname, email, password, passwordc):
			# generate password hash
			pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

			# form data is Valid, save user to database, and log them in
			user = User.objects.create(email=email, first_name=fname, last_name=lname, password=pw_hash)
			request.session['user_id'] = user.id
			request.session['user_email'] = user.email
			request.session['user_first_name'] = user.first_name
			request.session['user_last_name'] = user.last_name

	return redirect('/')

def login(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		password = request.POST.get('pass')

		login = User.objects.login_user(request, email, password)
		if login[0]:
			# log user in
			request.session['user_id'] = login[1].id
			request.session['user_email'] = login[1].email
			request.session['user_first_name'] = login[1].first_name
			request.session['user_last_name'] = login[1].last_name

	return redirect('/')

def logout(request):
	request.session.clear()
	return redirect('/')

def delete_user(request, id):
	User.objects.get(id=id).delete()
	return redirect('/')
