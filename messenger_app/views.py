from django.shortcuts import render
from .forms import NickNameSearch, WriteMsg
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Message
from .models import Chat
from django.db.models import Q


# Create your views here.

#
# def home(requset):
#     return render(requset, 'messenger_app/home.html')


def home(request):
    form = NickNameSearch()
    msgs = Chat.objects.filter \
        (Q(user2__username__icontains=request.user.username) | Q(user1__username__icontains=request.user.username))
    return render(request, 'messenger_app/home.html', {'form': form, 'chats': msgs})


def view_chat(request, pk=None):
    form_write_msg = WriteMsg()
    if not pk is None:
        chat = Chat.objects.get(pk=pk)
        msgs = chat.message_set.all()
        if chat.user1.username == request.user.username:
            request.session['recipient'] = chat.user2.username
        else:
            request.session['recipient'] = chat.user1.username
        request.session['chat.pk'] = chat.pk
        return render(request, 'messenger_app/view_chat.html', {'msgs': msgs, 'pk': pk, 'form': form_write_msg, 'chat': chat})
    else:
        if request.method == 'POST':
            form = NickNameSearch(request.POST)
            if form.is_valid():
                try:
                    recipient = User.objects.get(username=form.cleaned_data['nickname'])
                except:
                    recipient = None
                if recipient is not None:
                    msgs = Chat.objects.filter((Q(user1__username__icontains=recipient.username) & Q(user2__username__icontains=request.user.username)) |(Q(user2__username__icontains=recipient.username) & Q(user1__username__icontains=request.user.username)))
                    if not msgs.exists():
                        msgs_temp = Chat.objects.create(user1=request.user, user2=User.objects.get(username=recipient.username))
                        msgs_temp.save()
                        msgs = [msgs_temp, ]
                    request.session['recipient'] = recipient.username
                    request.session['chat.pk'] = msgs[0].pk
                    return render(request, 'messenger_app/view_chat.html', {'msgs': msgs[0].message_set.all(), 'form': form_write_msg, 'chat': msgs[0]})
                else:
                    messages.error(request, 'Ошибка, такого пользователя не существует')
                    return home(request)
        else:
            return home(request)


def write_msg(request):
    if request.method == 'POST':
        form = WriteMsg(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.sender = request.user
            instance.recipient = User.objects.get(username=request.session['recipient'])
            instance.chat = Chat.objects.get(pk=request.session['chat.pk'])
            instance.save()
            return view_chat(request, pk=request.session['chat.pk'])
    else:
        return view_chat(request, pk=request.session['chat.pk'])