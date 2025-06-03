from openai import OpenAI
import base64

import re
import requests
from pathlib import Path
import uuid
import markdown
import os

from django.utils.html import escape
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import Group

from MainlyChat.settings import (OPENAI_API_KEY, MODEL_ANALYSIS, MODEL_FUTURE, MEDIA_ROOT)
from justchat.models import Chat, ChatImage
from justchat.forms import OtherModelsForm

chat_row_pattern = 'c_r_p'
client = OpenAI(api_key=OPENAI_API_KEY)

# Create your views here.
def get_completion_chat_o3(turbomode_messages):
    completion = client.chat.completions.create(
        model=MODEL_FUTURE,
        messages=turbomode_messages,
    )
    get_completion_chat_reply = completion.choices[0].message.content
    return get_completion_chat_reply


def get_responses(turbomode_messages):
    response = client.responses.create(
        model=MODEL_ANALYSIS,
        input=turbomode_messages,
        tools=[{"type": "web_search_preview"}],
    )
    return response.output_text


def title_ai(dialoque):
    turbomode_messages = [{"role": "system",
                           "content": "You are a conversation title generator. Respond only with a simple title."}, {
        "role": "user",
        "content": f"Please create a title for this conversation:{dialoque}."
    }]
    result = get_responses(turbomode_messages)
    return result


def turbomode_ai(dialoque, question):
    turbomode_messages = [{
        "role": "user",
        "content": f"Read this TEXT: {dialoque}. "
                   f"Then use finnish language in your answer to this question TEXT: {question}. "
                   f"Formulate your answer nicely with line breaks <br> and paragraphs <p>."
    }]
    result = get_responses(turbomode_messages)
    return result


def thislocalimage(question, image_path):
    # Function to encode the image
    def encode_image(image_path):
      with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    base64_image = encode_image(image_path)
    messages = [
        {
            "role": "user",
            "content": [{"type": "input_text", "text": f"{question}"},
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        },
                        ],
        }
    ]
    reply = get_responses(messages)
    return reply


def image_ai(image_question, image_url):
    response = client.chat.completions.create(
        model=MODEL_ANALYSIS,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant who always answers well structured and little entertaining"},
            {"role": "user", "content": [
                {"type": "text", "text": f"{image_question}"},
                {"type": "image_url", "image_url": {
                    "url": f"{image_url}"}
                 }
            ]}
        ],
        temperature=0.0,
        max_tokens=4096,
    )
    reply = response.choices[0].message.content
    return reply


def startchat(request):
    user = request.user
    stories = Chat.get_all_chats(user)
    context = {
            'user': user,
            'stories': stories,
        }
    return render(request, 'chatindex.html', {'context': context})


def newchatbutton(request):
    return render(request, 'partials/chat_modal_new.html')


def createnewchat(request):
    if request.method == 'POST':
        whoisasking = request.user.username
        empty_dialoque = ''
        dialoque = request.POST.get('myquestion')
        image_file = request.FILES.get('imagefile')
        chatname = title_ai(dialoque)
        response = turbomode_ai(empty_dialoque, dialoque)
        new_answer = chat_row_pattern + response
        dialoque = f"<{whoisasking}> " + dialoque + new_answer
        savenewchat = Chat(name=chatname, dialoque=dialoque, owner=request.user)
        savenewchat.save()
        chat_id = savenewchat.id
        request.session['this_chat'] = chat_id
        return getchat(request, id=chat_id)
    return render(request, 'chatindex.html')


def process_chat_rows(raw_rows):
    processed = []
    for i, row in enumerate(raw_rows, start=1):  # 1-based count matching Django loop
        if i % 2 == 0:  # AI message, even rows
            html_content = markdown.markdown(row)
            processed.append({'content': html_content, 'is_ai': True})
        else:
            # Escape to avoid raw HTML injection in user messages
            safe_content = escape(row)
            processed.append({'content': safe_content, 'is_ai': False})
    return processed


def getchat(request, id):
    """ Chatin sisältö"""
    chat_instance = get_object_or_404(Chat, id=id)
    chat_rows = re.split(chat_row_pattern, chat_instance.dialoque)

    processed_rows = process_chat_rows(chat_rows)

    chat_images = chat_instance.chatimage_set.all()
    chat_imag_rows = {image.chatrow: image.image.url for image in chat_images}
    request.session['this_chat'] = id
    form = OtherModelsForm(request.POST or None, user=request.user, instance=chat_instance)
    if request.method == 'POST' and form.is_valid():
            form.save()
    context = {
        'form': form,
        'chat_id': id,
        'chat_name': chat_instance.name,
        'chat_time': chat_instance.timestamp,
        'chat_rows': processed_rows,
        'chat_images': chat_imag_rows,
    }
    return render(request, 'partials/chat_modal.html', {'context': context})


def savechat(request):
    if request.method == 'POST':
        question = request.POST['myquestion']
        media_file = request.POST.get('media_file', '')  # URL input
        image_file = request.FILES.get('imagefile')  # File input
        # logger.info(f'media_file: {media_file}')
        # logger.info(f'image_file: {image_file}')
        whoisasking = request.user.username

        current_chat = Chat.get_chat_by_name(request.session['this_chat'])
        chat_name = current_chat.name
        new_question = chat_row_pattern + f"<{whoisasking}> " + question

        dialoque = ''
        image_new_name = None
        media_url = None
        image_new_answer = ''
        web_new_answer = ''
        new_answer = ''
        response = ''

        # Helper function for consistent logic to save files
        def save_image_file(file_data, file_name_prefix):
            file_extension = Path(file_data).suffix if isinstance(file_data, str) else Path(file_data.name).suffix
            image_name = f"{file_name_prefix}_{uuid.uuid4()}{file_extension}"
            image_path = os.path.join(MEDIA_ROOT, "images", image_name)

            # Save file differently based on input type
            if isinstance(file_data, str):  # Web URL
                response = requests.get(file_data)
                with open(image_path, "wb") as f:
                    f.write(response.content)
            else:  # Uploaded file
                with open(image_path, "wb") as f:
                    for chunk in file_data.chunks():
                        f.write(chunk)
            return image_path, os.path.basename(image_path)

        # Handle uploaded image file
        if image_file:
            local_image_path, image_new_name = save_image_file(image_file, chat_name)
            # logger.info(f"Saved local image: {local_image_path}")
            local_image_file_response = thislocalimage(question, local_image_path)
            new_answer = local_image_file_response

        # Handle web URL media file
        elif media_file:
            web_image_path, web_image_name = save_image_file(media_file, chat_name)
            web_media_response = image_ai(question, media_file)
            new_answer = web_media_response

            # Ensure naming follows the same standards
            if not image_new_name:
                image_new_name = web_image_name

        # Handle User question
        else:
            response = turbomode_ai(current_chat.dialoque, question)
            new_answer = response

        # Construct the dialogue
        dialoque = current_chat.dialoque + new_question + chat_row_pattern + new_answer
        save_chat = Chat(id=current_chat.id, name=chat_name, dialoque=dialoque)
        save_chat.save()

        # Save the chat image if there was one
        chat_rows = re.split(chat_row_pattern, dialoque)
        second_last_index = len(chat_rows) - 1
        if image_new_name:
            save_chat_image = ChatImage(
                name=image_new_name,
                chatrow=second_last_index,
                chat=current_chat,
                image=f"images/{image_new_name}"
            )
            save_chat_image.save()

        return getchat(request, id=current_chat.id)
    return render(request, "chatindex.html")


def deletechat(request, id):
    current_chat = Chat.get_chat_by_name(id)
    current_chat.delete()
    user = request.user
    stories = Chat.get_all_chats(user)
    context = {
            'user': user,
            'stories': stories,
        }
    return render(request, 'partials/chat_nav.html', {'context': context})


def upusergroup(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        user_groups_ids = request.POST.getlist('user_groups')
        chat = get_object_or_404(Chat, id=chat_id)

        # Clear existing group associations
        chat.usergroup.clear()

        # Add selected groups to the chat
        for group_id in user_groups_ids:
            group = get_object_or_404(Group, id=group_id)
            chat.usergroup.add(group)

        chat.save()

        form = OtherModelsForm(user=request.user, instance=chat)

        context = {
            'form': form,
            'chat': chat,
        }
        return render(request, 'partials/upusergroup.html', {'context': context})
    return render(request, "chatindex.html")


def toggle_tools(request):
    if request.method == 'GET':
        togglestate = request.GET.get('togglestate', '') == 'on'
        return render(request, "partials/tools_nav.html",{'tools_visible': togglestate})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def user_guide(request):
    """View function for the user guide page"""
    return render(request, 'user_guide.html')


def tools_demo(request):
    if request.method == 'GET':
        image_name = request.GET.get('teknoma')
        if image_name:  # Ensure 'teknoma' is provided
            image = f'images/{image_name}.png'
            logo = f'images/logo_{image_name}.png'
        else:
            image = 'images/ouraring.png'  # Fallback image if no parameter
        context = {
            'logo': logo,  # Pass the constructed image path to the context
            'image_name': image_name,  # Pass the constructed image path to the context
            'image': image  # Pass the constructed image path to the context
        }
        return render(request, 'partials/tool_functions.html', {'context': context})
