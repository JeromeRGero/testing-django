# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Quote
import bcrypt, datetime

# Create your views here.


def index(request):
    return render(request, 'quotes/index.html')


def reg(request):
    if request.POST:
        errors = User.objects.validate_reg(request.POST)
        if len(errors) > 0:
            user_errors = ""
            for error in errors:
                user_errors += error + " \n"
            request.session['reg_errors'] = user_errors
            # for tag, error in errors.itteritems():
            #     print (tag, error)
            #     messages.error(request, error, extra_tags=tag)
            return redirect('/')
        if 'reg_errors' in request.session.keys():
            del request.session['reg_errors']
        name = request.POST['full_name']
        alias = request.POST['alias']
        email = request.POST['email']
        email = email.lower()
        NOTHASHED = request.POST['password']
        hashedPassword = bcrypt.hashpw(NOTHASHED.encode(), bcrypt.gensalt())
        bdate = request.POST['birthdate']
        bdate = datetime.datetime.strptime(bdate, "%Y-%m-%d")
        User.objects.create(name=name, alias=alias, email=email, hashedPassword=hashedPassword, birthdate=bdate)
        userid = User.objects.get(email=email).id
        print(userid)
        request.session['userid'] = int(userid)
    return redirect('/quotes')


def login(request):
    if request.POST:
        error = User.objects.validate_log(request.POST)
        if len(error) > 0:
            print("There was an error during login,")
            print(error)
            request.session['log_error'] = error
            # for tag, error in errors.itteritems():
            #     print (tag, error)
            #     messages.error(request, error, extra_tags=tag)
            return redirect('/')
        if 'log_error' in request.session.keys():
            del request.session['log_error']
        email = request.POST['email']
        email = email.lower()
        userObj = User.objects.get(email=email)
        userid = userObj.id
        print(userid)
        request.session['userid'] = userid
        return redirect('/quotes')
    print("No request.POST found... huh?")
    return redirect('/')


def logout(request):
    del request.session['userid']
    return redirect('/')


def quotes(request):
    if 'userid' in request.session.keys():
        userid = request.session['userid']
        user = User.objects.get(id=userid)
        print(userid)
        users_favs = User.objects.get(id=userid).favorite_quotes.order_by("-id")
        other_quotes = Quote.objects.exclude(favorited_by=user).order_by("-id")
        username = user.name
        context = {
            'users_favs': users_favs,
            'other_quotes': other_quotes,
            'name': username,
            'userid': userid,
        }
        return render(request, 'quotes/quotes.html', context)
    else:
        a = 'Not logged in yet! Visit the main page to login.'
        return HttpResponse(a)


def userpage(request, num):
    user = User.objects.get(id=num)
    users_posts = User.objects.get(id=num).posted.all()
    total = users_posts.count
    context = {
        'user': user,
        'user_posts': users_posts,
        'total': total,
    }
    return render(request, 'quotes/user.html', context)


def adding(request):
    if request.POST:
        by_person = request.POST['by_person']
        desc = request.POST['desc']
        check = Quote.objects.validate_quote(request.POST)
        if check or len(by_person) < 4:
            request.session['newq_error'] = "Either the person who said that had a first and last name that was less than 4 characters in total... or a user has already submitted that quote! Thanks though."
            return redirect("/quotes")
        userid = request.session['userid']
        print('There should be a new author\'s name next line!')
        made_it = User.objects.get(id=userid)
        Quote.objects.create(by_person=by_person, desc=desc, posted_by=made_it)
    return redirect('/quotes')

def addfav(request, num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id=request.session['userid'])
    user.favorite_quotes.add(quote)
    user.save()
    return redirect('/quotes')

def unfavorite(request, num):
    quote = Quote.objects.get(id=num)
    user = User.objects.get(id=request.session['userid'])
    user.favorite_quotes.remove(quote)
    user.save()
    return redirect('/quotes')