# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate(self, data):
        no_spaces= re.compile(r'^\S+$')
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
        username=data['username']
        first_name= data['first_name']
        last_name= data['last_name']
        email=data['email']
        pw=data['password']
        confirm_pw=data['confirm_pw']
        valid=True
        message=[]
        if len(username)<1 or len(first_name)<1 or len(last_name)<1 or len(email)<1 or len(pw)<1 or len(confirm_pw)<1:
            message.append("All fields are required!")
            valid=False
        if not no_spaces.match(username):
            message.append("No spaces allowed in username!")
            valid=False
        if not no_spaces.match(first_name):
            message.append("No spaces allowed in first name!")
            valid=False
        if not no_spaces.match(last_name):
            message.append("No spaces allowed in last name!")
            valid=False
        if not email_regex.match(email):
            message.append("Must be a valid Email Address!")
            valid=False
        if pw!=confirm_pw:
            message.append("Password Confirmation must match Password!")
            valid=False
        if len(pw)<8:
            message.append("Password must be longer than 8 characters!")
            valid=False
        if User.objects.filter(username=username):
            message=[]
            message.append("Username already exists! Try loggin in!")
        return message

    def hashPW(self, data):
        pw = data['password'].encode()
        hashed = bcrypt.hashpw(pw, bcrypt.gensalt())
        return hashed

    def login(self, data):
        username = data['username']
        input_pw = data['password'].encode()
        user = User.objects.filter(username=username)
        message=[]
        if user:
            db_pw = user[0].password.encode()
            if bcrypt.hashpw(input_pw, db_pw)==db_pw:
                return message
            else:
                message.append('The Username or Password is incorrect')
                return message
        else:
            message.append('Username does not exist')
            return message

class User(models.Model):
    username = models.CharField(max_length=16)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField()
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    objects=UserManager()

class BookManager(models.Manager):
    def validate(self, data):
        book_message = []
        if len(data['title'])<1:
            book_message.append('Title is a required field!')
        if len(data['author'])<1 and len(data['new_author'])<1:
            book_message.append('If the author is not on the list, please fill out a new author!')
        if len(data['author'])>1 and len(data['new_author'])>1:
            book_message.append('Please leave dropdown blank if you are writing a new author!')
        if data['new_author']:
            if Book.objects.filter(author=data['new_author']):
                book_message.append('This author already exists, please choose them from the dropdown!')
        return book_message

class Book(models.Model):
    name = models.CharField(max_length=55)
    author = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookManager()

    def __str__(self):
        return self.name + " by " + self.author

class ReviewManager(models.Manager):
    def validate(self, data):
        review_message=[]
        if len(data['review'])<1 or len(data['rating'])<1:
            review_message.append('Review and Rating are required fields!')
        return review_message

class Review(models.Model):
    content = models.TextField()
    rating = models.PositiveSmallIntegerField()
    user = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    objects = ReviewManager()

    def __str__(self):
        return "review " + self.book + " " + self.user
