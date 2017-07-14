# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import bcrypt, re

# Create your models here.
class UserManager(models.Manager):
    def validate(self, postData):
        errors = [] # make a list of errors
        #first name validation
        if len(postData['first_name']) == 0:
            errors.append('Please Enter Name.')
        elif len(postData['first_name']) < 2:
            errors.append('Name must be between 3-45 characters')
        elif not re.search(r'^[A-Za-z]+$', postData['first_name']):
            errors.append('Name must only contain letters')
        #last name validation
        if len(postData['last_name']) == 0:
            errors.append('Please Enter Name.')
        elif len(postData['last_name']) < 2:
            errors.append('Name must be between 3-45 characters')
        elif not re.search(r'^[A-Za-z]+$', postData['last_name']):
            errors.append('Name must only contain letters')
        #username validation
        if len(postData['username']) == 0:
            errors.append('Please Enter a Username.')
        elif len(postData['username']) < 2:
            errors.append('Username must be between 3-45 characters')
        elif not re.search(r'^[a-zA-Z0-9]+$', postData['username']):
            errors.append('Username cannot contain speacial characters ')
        #email validation
        if len(postData['email']) == 0:
            errors.append('Email cannot be left blank')
        elif not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',postData['email']):
            errors.append('You have entered an invalid Email')
        elif len(User.objects.filter(email=postData['email']))>0:
            errors.append('This email is already registered')
        #password validation
        if len(postData['password']) < 7:
            errors.append('Password must be at least 8 characters')
        if postData['confirm'] != postData['password']:
            errors.append('Password and confirm password does not match')
        #Date of birth Validation
        # try:
        #     hire = datetime.strptime(postData['hire'], '%m/%d/%Y')
        #     if datetime.now() < hire:
        #         errors.append('Hire Date cannot be in the future')
        # except ValueError:
        #     errors.append('Invalid date entry, must be mm/dd/yyyy')

        # still need the validation of hire format mm/dd/yyyy
        if len(errors)== 0:
            user = User.objects.create(first_name=postData['first_name'],last_name=postData['last_name'], email=postData['email'], username= postData['username'], admin=postData['admin'], pw_hash=bcrypt.hashpw(postData['password'].encode(),bcrypt.gensalt()))
            return (True, user)


        return(False, errors)
    #login Authentication
    def authenticate(self, postData):
        if 'email' in postData and 'password' in postData:
            try:
                user = User.objects.get(email=postData['email'])

            except User.DoesNotExist:
                return(False, 'Invalid Username, or password does not match email')

            u = user.pw_hash.encode()
            pw_match = bcrypt.hashpw(postData['password'].encode(),u)
            if pw_match == u:
                return (True, user)
            else:
                return (False, 'Email and password combination do not match')
        else:
            return (false, 'Please enter Login information')

class RecipeManager(models.Manager):
    def recipe_validate(self, postData, id):
        error = []
        #dish name validation
        if len(["dish_name"]) == 0 :
            error.append('Please Enter Recipe Name.')
        elif len(postData['dish_name']) < 3:
            error.append('The dish name must be at least 3 characters')
        #cook time validation
        if int(postData["cook_time"]) <= 1:
            error.append('Cook time must be longer then 1 minute!')
        #instructions
        if len(postData["instruction"]) == 0 :
            error.append('Come on getting food delivered has more steps')
        elif len(postData['instruction']) < 10 :
            error.append('Its got to be more then 1 step! Ramen doesnt count')
        #ingredients
        if len(postData["ingredient"]) == 0 :
            error.append('Add more ingredients, Even air is an ingredient')
        #checking for errors
        if len(error) == 0:
            recipe = Recipe.objects.create(dish_name=postData['dish_name'], instruction=postData['instruction'], ingredient=postData['ingredient'], video=postData['video'], cook_time=postData['cook_time'],  add_by=User.objects.get(id=id))

            return (True, recipe)
        else:
            return (False, error)


class CommentManager(models.Manager):
    def comment_validate(self, postData):
        if len(["content"]) < 6 :
            errors.append('Your Question or Comment is too short')
            return (False, errors)

class User(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    admin = models.BooleanField(default=False)
    pw_hash = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Recipe(models.Model):
    dish_name = models.CharField(max_length=100)
    cook_time = models.IntegerField(default=1)
    video = models.CharField(max_length=1500)
    instruction = models.TextField()
    ingredient = models.TextField()
    add_by = models.ForeignKey(User, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects= RecipeManager()

class Comment(models.Model):
    content = models.TextField(max_length=1000)
    person = models.ForeignKey(User, related_name='people')
    food = models.ForeignKey(Recipe, related_name='foods')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()
