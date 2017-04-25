# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from models import User, Book, Review
from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'reviewer/index.html')

def register(request):
    data = {
    "username": request.POST['username'],
    'first_name': request.POST['first_name'],
    'last_name': request.POST['last_name'],
    'email': request.POST['email'],
    'password': request.POST['password'],
    'confirm_pw': request.POST['confirm_pw']
    }
    warnings=User.objects.validate(data)
    if not warnings:
        request.session['current_user_id'] = User.objects.create(username=data['username'],first_name=data['first_name'],last_name=data['last_name'], email=data['email'],password=User.objects.hashPW(data)).id
        return redirect('/books')
    else:
        for i in warnings:
            messages.error(request, i)
        return redirect('/')
    pass

def login(request):
    data = {
    'username': request.POST['username'],
    'password': request.POST['password']
    }
    warnings=User.objects.login(data)
    if not warnings:
        request.session['current_user_id'] = User.objects.get(username=data['username']).id
        return redirect('/books')
    else:
        for i in warnings:
            messages.error(request,i)
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def books(request):
    context = {
    'books': Book.objects.all(),
    'reviews': Review.objects.all(),
    'authors': Book.objects.values('author'),
    'user': User.objects.get(id=request.session['current_user_id'])
    }
    return render(request, 'reviewer/books.html', context)

def addbookpage(request):
    context = {
    'books': Book.objects.all().distinct()
    }
    return render(request, 'reviewer/addbooks.html', context)

def addbook(request):
    data = {
    'title': request.POST['title'],
    'author': request.POST['author'],
    'new_author': request.POST['new_author'],
    'review': request.POST['review'],
    'rating': request.POST['rating']
    }
    if data['review']:
        warnings=Book.objects.validate(data)+Review.objects.validate(data)
    else:
        warnings=Book.objects.validate(data)
    if not warnings:
        if data['author']:
            data['new_author']=data['author']
        new_book = Book.objects.create(name=data['title'],author=data['new_author']).id
        if data['review']:
            Review.objects.create(content=data['review'],rating=data['rating'],user=User.objects.get(id=request.session['current_user_id']),book=Book.objects.get(id=new_book))
        return redirect('/books/'+str(new_book))
    else:
        for i in warnings:
            messages.error(request,i)
        return redirect('/books/add')


def bookpage(request, id):
    context = {
    'book': Book.objects.get(id=id),
    'reviews': Review.objects.filter(user__id=id)
    }
    return render(request, 'reviewer/bookpage.html', context)

def newreview(request, id):
    data = {
    'review': request.POST['review'],
    'rating': request.POST['rating']
    }
    warnings = Review.objects.validate(data)
    if not warnings:
        Review.objects.create(content=data['review'], rating=data['rating'], book=Book.objects.get(id=id), user=User.objects.get(id=request.session['current_user_id']))
        return redirect('/books/'+str(id))
    else:
        for i in warnings:
            messages.error(request, i)
        return redirect('/books/'+str(id))

def userpage(request, id):
    context = {
    'user': User.objects.get(id=id),
    'books': Book.objects.filter(reviews__user__id=id).distinct()
    }
    return render(request, 'reviewer/users.html', context)
