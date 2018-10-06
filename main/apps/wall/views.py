from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, UserManager, Message, Comment

def index(request):
    return render(request, 'wall/index.html')

def register(request):
    request.session['first_name'] = request.POST['first_name']

    errors = User.objects.validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = hashed)
        request.session['user_id'] = user.id
        return redirect('/wall')

def login(request):
    if User.objects.filter(email = request.POST['email']):
        user = User.objects.get(email=request.POST['email'])
        if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            messages.error(request, "Successfully logged in!")
            return redirect('/wall')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('/')
    else:
        messages.error(request, "Invalid email or password.")
        return redirect('/')


def wall(request):
    context = {
        'first_name': request.session['first_name'],
        'Users': User.objects.all(),
        'Messages': Message.objects.all(),
        'Comments': Comment.objects.all()
    }
    return render(request, 'wall/wall.html', context)

def message(request):
    user_id = request.session['user_id']
    user = User.objects.get(id=user_id)
    Message.objects.create(message = request.POST['message'], user=user)

    return redirect('/wall')

def comment(request):
    user_id = request.session['user_id']
    message_id = request.POST['message_id']
    comment = request.POST['comment']
    
    Comment.objects.create(comment = comment, user_id = user_id, message_id = message_id)

    return redirect('/wall')

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out!")
    print
    return redirect('/')