import json
import requests
from bs4 import BeautifulSoup
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import auth
from django.http import HttpResponse
import re
import string
import pytz
import datetime, time, timedelta
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

from django.contrib.auth.decorators import login_required

import os
from .forms import RegistrationForm, UserForm, ProfileForm
from .models import News, Profile, RunPosts


def get_words(filename):
    with open(filename, encoding="utf8") as file:
        text = file.read()
    text = text.replace("\n"," ")
    text = text.lower()
    words = text.split()
    words.sort()
    return words


def get_words_dict(words):
    words_dict = dict()

    for word in words:
        if word in words_dict:
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1
    return words_dict

def index(request):
    context = {}
    return render(request, 'main/index.html')

def price(request):
    return render(request, 'main/price.html')

def game(request):
    return render(request, 'main/game.html')

def payment(request):
    return render(request, 'main/payment.html')


def registration(request):
    data = {}
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            data['form'] = form
            data['res'] = "Все прошло успешно"
            print(data['res'])
            return redirect('auth')
    else:
        form = RegistrationForm()
        data['form'] = form
        return render(request, 'main/registration.html', data)

    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("IP ADDRESS OF USER : ", ip)
    r = open("ipaddr.txt", 'a+')
    r.write(ip + ' ')
    r.close()
    filename = "ipaddr.txt"
    if not os.path.exists(filename):
        print("Указанный файл не существует")
    else:
        words = get_words(filename)
        words_dict = get_words_dict(words)
        print("Кол-во слов: %d" % len(words))
        print("Кол-во уникальных слов: %d" % len(words_dict))
        print("Все использованные слова:")
        for word in words_dict:
            if words_dict[word] > 5:
                return redirect('price')
            print(word.ljust(20), words_dict[word])
    return render(request, 'main/registration.html', data)

def time_login():
    tt1 = datetime.datetime.now().time()
    login_time = tt1
    return login_time

def time_logout():
    tt2 = datetime.datetime.now().time()
    logout_time = tt2
    return logout_time

def auth(request):
    global diff_time
    global numbers
    numbers = []
    for line in open("time_of_session.txt").readlines():
        numbers.extend([str(n) for n in line.split()])
    data = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile/{}'.format(request.user.username))
    for index in range(len(numbers)):
        try:
            numbers[index] = int(numbers[index])
        except ValueError:
            aa = 1
    print(numbers)
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print("IP ADDRESS OF USER : ", ip)
    r = open("ipaddr.txt", 'a+')
    r.write(ip + ' ')
    r.close()
    filename = "ipaddr.txt"
    if not os.path.exists(filename):
        print("Указанный файл не существует")
    else:
        words = get_words(filename)
        words_dict = get_words_dict(words)
        print("Кол-во слов: %d" % len(words))
        print("Кол-во уникальных слов: %d" % len(words_dict))
        print("Все использованные слова:")
        for word in words_dict:
            if words_dict[word] > 5:
                return redirect('price')
            print(word.ljust(20), words_dict[word])
        for i in range(len(numbers) - 1):
            if numbers[i] == ip and numbers[i + 1] > 100:
                return redirect('price')
    global t1
    tr1 = time_login()
    date_format = "%H:%M:%S.%f"
    t1 = datetime.datetime.strptime(str(tr1), date_format)
    return render(request, 'main/auth.html', data)



@login_required
def profile(request, username):
    active_person = request.user.username
    if str(active_person) == username:
        posts = RunPosts.objects.all().filter(user=request.user)
        list_posts = posts.order_by("-id")
        all_student = User.objects.all()
        for student in all_student:
            if str(student) == username:
                logStudent = student
        title = str(logStudent.first_name) + ' ' + str(logStudent.last_name)
        return render(request, 'main/profile.html', {'title': title, 'logStudent': logStudent, 'username': username})
    else:
        all_student = User.objects.all()
        for student in all_student:
            if str(student) == username:
                logStudent = student
        posts = RunPosts.objects.all().filter(user=logStudent)
        list_posts = posts.order_by("-id")
        title = str(logStudent.first_name) + ' ' + str(logStudent.last_name)
        return render(request, 'main/profile.html', {'title': title, 'logStudent': logStudent, 'list_posts': list_posts})

def last_login(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        last_login_user = user.last_login.strftime('%y-%m-%d %a %H:%M:%S')
        return last_login_user


@login_required
def leave_profile(request):
    x_forw_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forw_for is not None:
        ip = x_forw_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    for line in open("time_of_session.txt").readlines():
        numbers.extend([str(n) for n in line.split()])
    print(numbers)

    logout(request)
    tr2 = time_logout()
    date_format = "%H:%M:%S.%f"
    #user = User.objects.get(username=request.user)
    #user_last_login = user.last_login.strftime(date_format)
    #t1 = user_last_login
    print("Время входа", t1)
    t2 = datetime.datetime.strptime(str(tr2), date_format)
    print("Время выхода", t2)
    d_time = t2-t1
    dif_time = d_time.seconds
    diff_time = dif_time*1
    print("Разница по времени", d_time)
    for index in range(len(numbers)):
        try:
            numbers[index] = int(numbers[index])
        except ValueError:
            aa = 1
    for i in range(len(numbers)-1):
        if numbers[i] == ip:
            numbers[i+1] += diff_time
    MyFile = open('time_of_session.txt', 'w')
    for element in numbers:
        MyFile.write(str(element) + ' ')
    MyFile.close()
    r = open("time_of_session.txt", 'a+')
    r.write(ip + ' ')
    r.close()
    r = open("time_of_session.txt", 'a+')
    r.write(str(diff_time) + ' ')
    r.close()
    return redirect('/')
    # date_format = "%m/%d/%Y" t1 = datetime.datetime.strptime(str(time_login()), date_format) t2 = datetime.datetime.strptime(str(time_logout()), date_format)
    #resp = HttpResponse('view count=' + str(num_visits))
    #return resp

@login_required
@transaction.atomic
def edit_profile(request):
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('profile', request.user.username)
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'main/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def new_post(request, username):
    if request.method == 'POST':
        url = request.POST.get('train_link')

    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        item = soup.select_one("[data-react-class='ActivityPublic']")
        name_train = json.loads(item.get("data-react-props"))['activity']['name']
        time_quotes = json.loads(item.get("data-react-props"))['activity']['date']
        name_student = json.loads(item.get("data-react-props"))['activity']['athlete']['name']
        run_distance = json.loads(item.get("data-react-props"))['activity']['distance']
        run_time = json.loads(item.get("data-react-props"))['activity']['time']
        active_name = request.user.first_name + ' ' + request.user.last_name
        if item is None:
            messages.error(request, "Too many requests!")
            return redirect('profile', username)

        if active_name == name_student:
            RunPosts.objects.create(name=name_train, link_post=url, distance=run_distance, run_time=run_time,
                                    date_running=time_quotes, user=request.user)
        else:
            messages.error(request, "Это не ваша тренировка!")
        return redirect('profile', username)

    except:
        messages.error(request, "Неверная ссылка! Ссылка должна содержать информацию о тренировке! Пример ссылки: "
                                "https://www.strava.com/activities/<id_activities>")
        return redirect('profile', username)


def all_profiles(request):
    all_users = User.objects.all()
    list_users = all_users.order_by("username")
    return render(request, 'main/all_users.html', {'title': 'Все пользователи', 'list_users': list_users})


