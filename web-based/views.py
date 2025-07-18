import PIL.ImageGrab
from django.shortcuts import render,HttpResponse
from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

from .models import CodeDB

import keyboard
import time
import threading
import clipboard
import PIL
import base64
from pathlib import Path
import socket

@staticmethod
def check_ip_address(income_ip_address):
    name = socket.gethostname()
    org_ip_address = socket.gethostbyname(name)

    return income_ip_address == org_ip_address

@csrf_exempt
def incoming_message(request:WSGIRequest):

    if request.method == "POST":
        if not check_ip_address(json.loads(request.body).get("ipAddress")):
            return JsonResponse(data={"output":"Error Invalid ip address"})
        
        try:
            data:dict = json.loads(request.body)
            message = data.get("message", "")
            return_message = ""
            try:
                if len(CodeDB.objects.all()) == 0:
                    CodeDB(text=message).save()
                else:
                    obj = CodeDB.objects.get(id=1)
                    obj.text = message
                    obj.is_new_data = True
                    obj.save()
                return_message = "Data Added Successfully.."
            except:
                return_message = f"Error: {e}"
            return JsonResponse(data={"output": return_message})
        
        except Exception as e:
            return JsonResponse(data={"output": f"Error: {str(e)}"}, status=400)

    return HttpResponse(content="Server Started...<br>You can send messages Now.")

@csrf_exempt
def additional_options(request:WSGIRequest):
    if request.method == "POST":

        if not check_ip_address(json.loads(request.body).get("ipAddress")):
            return JsonResponse(data={"output":"Error Invalid ip address"})
        
        data:dict = json.loads(request.body)

        obj = CodeDB.objects.get(id=1)
        if data.get("stop"):
            obj.is_stop = True
        else:
            obj.is_stop = False
        
        time_delay = float(data.get("delay"))
        obj.time_delay = time_delay
        obj.save()
        
        if CodeDB.objects.get(id=1).is_new_data:
            threading.Thread(target=bot_writer, daemon=True).start()
        
        return JsonResponse(data={"output":"Options changed successfully"})

    return HttpResponse(content="changed additional options")


@staticmethod
def bot_writer():
    obj = CodeDB.objects.get(id=1)
    obj.is_new_data = False
    obj.save()

    time.sleep(2)

    index = 0
    text = CodeDB.objects.get(id=1).text
    words = text.split("\n")
    words = list(filter(lambda x: x if x != "" else False, words))

    keyboard.press_and_release('enter')

    while True:

        if index == len(words):
            break
        
        word = words[index]
        letter_index = 0
        
        while True:
            if letter_index == len(word):
                break

            elif CodeDB.objects.get(id=1).is_stop:
                continue
            
            elif CodeDB.objects.get(id=1).is_new_data:
                index = len(words) - 1
                break

            keyboard.write(text=word[letter_index], delay=CodeDB.objects.get(id=1).time_delay)
            letter_index +=1
        
        index +=1

        keyboard.press_and_release('end')
        time.sleep(0.05)
        keyboard.press_and_release('enter')
        time.sleep(0.05)
        keyboard.press_and_release('home')
        time.sleep(0.05)


@csrf_exempt
def get_last_copied_text(request:WSGIRequest):
    if not check_ip_address(json.loads(request.body).get("ipAddress")):
        return JsonResponse(data={"output":"Error Invalid ip address"})
    
    try:
        text = clipboard.paste()
        return JsonResponse(data={"copied_text":text})
    except Exception as e:
        return JsonResponse(data={"copied_text":f"Error: {e}"})


@csrf_exempt
def take_screen_shot(request:WSGIRequest):

    if not check_ip_address(json.loads(request.body).get("ipAddress")):
        return JsonResponse(data={"output":"Error Invalid ip address"})
    
    media_dir = Path(__file__).parent.parent / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    try:
        image_path = Path(media_dir / "image.png").as_posix()
        PIL.ImageGrab.grab().save(image_path)
        base64_string = file_to_base64(image_path)
        return JsonResponse(data={"output":"success","image_data":f"data:image/png;base64,{base64_string}"})
    except Exception as e:
        return JsonResponse(data={"output":f"Error: {e}"})

    
def file_to_base64(image_path):

    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    return encoded
    