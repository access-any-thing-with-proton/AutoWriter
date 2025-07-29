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
import re

@staticmethod
def check_ip_address(income_ip_address):
    org_ip_address = get_ip_address()
    return income_ip_address == org_ip_address

def get_ip_address():
    name = socket.gethostname()
    org_ip_address = socket.gethostbyname(name)

    return org_ip_address

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
                if re.search("<html.*>",message,flags=re.M):
                    " remove the comments in the html text "
                    pattern = r"<!--[^-->]+-->"
                    removed_comments = re.sub(pattern=pattern, repl="", string=message, flags=re.M) # removes the comments in html
                    message = "<!--\n" + removed_comments

                if len(CodeDB.objects.all()) == 0:
                    CodeDB(text= "l1\n" + message).save()
                else:
                    obj = CodeDB.objects.get(id=1)
                    obj.text = "l1\n" + message
                    # adding default line for not skipping the first char
                    obj.is_new_data = True
                    obj.save()
                    
                return_message = "Data Added Successfully.."
            except Exception as e:
                return_message = f"Error: {e}"
            return JsonResponse(data={"output": return_message})
        
        except Exception as e:
            return JsonResponse(data={"output": f"Error: {str(e)}"}, status=400)
        
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
    </head>
    <body>
        <h2 style=text-align:center>Server Started...</h2>
        <p>You can send messages now.</p>
        <p>After closing GUI close the console also</p>
        <p>System IP Address: <span style=color:green;font-size:1.5rem>{get_ip_address()}</span> </p>
        <strong>Enter the Above IP Address in the HTML Page.</strong> <br>
        <a href="https://github.com/access-any-thing-with-proton/AutoWriter/tree/main/web-based" target="_blank" 
        style="position:fixed;top:95%; left:50%;transform:translate(-50%,-50%);">GitHub Url</a>
    </body>
    </html>

    """

    return HttpResponse(content=html_content)

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
            time.sleep(3)
            threading.Thread(target=bot_writer, args=(data.get("bracketsOption"),), daemon=True).start()
        
        return JsonResponse(data={"output":"Options changed successfully"})

    return HttpResponse(content="changed additional options")



def bot_writer(brackets_option:str):
    obj = CodeDB.objects.get(id=1)
    obj.is_new_data = False
    obj.save()


    index = 0
    text = CodeDB.objects.get(id=1).text

    lines = re.split(r'\r\n|\r|\n', text)
    lines = [line for line in lines if line.strip()]

    keyboard.press_and_release('enter')

    while True:

        if index == len(lines):
            break

        if lines[1].startswith("<!--"):
            keyboard.write(lines[1], delay=0.3)

            keyboard.press_and_release("enter")
            keyboard.press_and_release("up")

            time.sleep(1)
            lines[1] = "" # makes the empty string of the index 1

        line:str = lines[index]

        letter_index = 0
        
        while True:
            if letter_index == len(line):
                break
            
            if index == 0:
                letter_index +=1
                # skipping the default line from preventing of not typing first char
                continue

            elif CodeDB.objects.get(id=1).is_stop:
                continue
            
            elif CodeDB.objects.get(id=1).is_new_data:
                index = len(lines) - 1
                break

            if line[letter_index] in ["{","[","("] and brackets_option == "1":
                # 1 means remove the closing brackets
                keyboard.write(text=line[letter_index], delay=CodeDB.objects.get(id=1).time_delay)
                keyboard.press_and_release("right")
                keyboard.press_and_release("backspace")
                time.sleep(0.2)
            else:
                keyboard.write(text=line[letter_index], delay=CodeDB.objects.get(id=1).time_delay)

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
    
