from django import forms
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from revChatGPT.V3 import Chatbot
from chat_website.settings import OPENAI_API_KEY
from chatgpt.forms import NewUserForm


def get_chatbot(request):
    chatbot = Chatbot(api_key=OPENAI_API_KEY)
    if 'chatbot_conversation' in request.session:
        chatbot.conversation = request.session['chatbot_conversation']
    else:
        request.session['chatbot_conversation'] = chatbot.conversation
    return chatbot


def clear_chatbot(request):
    if 'chatbot_conversation' in request.session:
        del request.session['chatbot_conversation']


@login_required
@csrf_exempt
def chat(request):
    if request.method == 'POST':
        chatbot = get_chatbot(request)
        prompt = request.POST.get('prompt')
        try:
            response = chatbot.ask(request.POST.get('prompt'))
        except Exception as e:
            response = "There seems to be an error, you can try again. error message: " + str(e)
        request.session['chatbot_conversation'] = chatbot.conversation
        return JsonResponse({'content': response})
    elif request.method == 'DELETE':
        clear_chatbot(request)
        request.method = 'GET'
        return chat(request)
    else:
        return render(request, 'chatgpt/index.html')


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, f"{form.errors}")
    form = NewUserForm()
    return render(request=request, template_name="registration/registration_form.html", context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form": form})

UserCreationForm
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")
