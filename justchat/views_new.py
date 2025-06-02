from django.shortcuts import render, get_object_or_404
from .models import Chat, ChatImage
from django.http import HttpResponse

chat_row_pattern = 'c_r_p'
def startchat(request):
    user = request.user
    stories = Chat.objects.get_all_chats_for_user(user)
    context = {'user': user, 'stories': stories}
    return render(request, 'chatindex.html', {'context': context})


def createnewchat(request):
    if request.method == 'POST':
        user = request.user
        dialoque = request.POST.get('myquestion')
        chatname = title_ai(dialoque)
        response = turbomode_ai('', dialoque)
        initial_dialoque = f"<{user.username}> {dialoque}{chat_row_pattern}{response}"

        new_chat = Chat.objects.create(name=chatname, dialoque=initial_dialoque, owner=user)
        chat_rows = re.split(chat_row_pattern, initial_dialoque)

        request.session['this_chat'] = new_chat.id
        context = {
            'chat_id': new_chat.id,
            'chat_name': chatname,
            'chat_rows': chat_rows,
        }
        return render(request, 'partials/chat_modal.html', {'context': context})
    return render(request, 'chatindex.html')


def savechat(request):
    if request.method == 'POST':
        question = request.POST['myquestion']
        chat_instance = Chat.get_chat_by_id(request.session.get('this_chat'))
        if chat_instance:
            response = turbomode_ai(chat_instance.dialoque, question)
            new_answer = chat_row_pattern + response
            chat_instance.append_dialogue(question, new_answer)
            return getchat(request, chat_instance.id)
    return render(request, "chatindex.html")
