import requests 
import time
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded, PhoneCodeInvalid, PasswordHashInvalid 
import json,random
import os,time
import traceback


class JsonManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_json()

    def _load_json(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    return {} 
        return {}

    def _save_json(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def add(self, key, value):
        self.data[key] = value
        self._save_json()

    def remove(self, key):
        if key in self.data:
            del self.data[key]
            self._save_json()
        else:
            print(f"⚠ المفتاح '{key}' غير موجود!")

    def update(self, key, new_value):
        if key in self.data:
            self.data[key] = new_value
            self._save_json()
        else:
            print(f"⚠ المفتاح '{key}' غير موجود!")

    def get(self, key):
        return self.data.get(key, None)

    def get_all(self):
        return self.data

    def clear(self):
        self.data = {}
        self._save_json()




TOKEN = "QUEFYEcewfiuWIENINOidednoqenfd979uhn979N9U79BU9U7Q"
api = "https://id124324234324.pythonanywhere.com"
api = "https://webappauto-production.up.railway.app"
api = "http://127.0.0.1:5000"
api_img = "https://pubgmobilehack.pythonanywhere.com"
exp_time = 90001000000
api_id = 15307186
api_hash = "c175436f6e2dfaa182b655441fefab94"
login_client = {}
logins_rum = {}



async def GetUrlImage(client,user_id):
    try:
        if "0" in requests.post(f"{api_img}/isimage/{user_id}").text.strip():
            ss = await client.get_chat_photos(user_id)
            photos = next(ss,None)
            profile_photo = photos.file_id if photos else None
            if profile_photo:
                photo_path = await client.download_media(profile_photo)
                with open(photo_path, "rb") as file:
                    response = requests.post(f"{api_img}/upload/{user_id}", files={"file": file})
                os.remove(photo_path)
            return f"{api_img}/static/image/{user_id}.jpg"
        else:
            return f"{api_img}/static/image/{user_id}.jpg"
    except:
        return ""
    return ""


async def LoadClients():
    js = JsonManager("data.json")
    for i in js.get_all():
        og = js.get_all()[i]
        if i in login_client:
            client = login_client[i]
        else:
            client =  Client(f"logins/{i}", api_id, api_hash)
            await client.connect()
            login_client[i] = client
        me = await client.get_me()
        print("RUN : ",me.first_name)
        og["name"] = f"{me.first_name} {me.last_name if me.last_name else ''}"
        og["username"] = f"{me.username}" if me.username else "لا يوجد اسم مستخدم"
        ig = await GetUrlImage(client,me.id)
        og["img"] = ig
        js.update(i,og)
        



async def newLogin(me,number):
    js_data = JsonManager("data.json")
    data = {
        "id":me.id,
        "name": f"{me.first_name} {me.last_name if me.last_name else ''}",
        "username":f"{me.username}" if me.username else "لا يوجد اسم مستخدم",
        "number":number,
        "list_msg":{},
        "list_text":[],
        "textrd":"",
        "time":"",
        "isPost":False,
        "isRd":False,
        "lenMsgs":0
    }
    js_data.add(number,data)
    await LoadClients()





async def sendLogin(phone_number):
    client = Client(f"logins/{phone_number}", api_id, api_hash)
    await client.connect()
    try:
        sent_code_info = await client.send_code(phone_number)
        logins_rum[phone_number] = {"sent_code_info":sent_code_info,"client":client}
        print(logins_rum)
        return {"ok":True}
    except Exception as e:
        return {"ok":False,"text":f"{e}"}

async def checkLoginCode(phone_number,code):
    client = logins_rum[phone_number]["client"]
    sent_code_info = logins_rum[phone_number]["sent_code_info"]
    try:
        await client.sign_in(phone_number, sent_code_info.phone_code_hash, code)
        logins_rum[phone_number]["client"] = client
        logins_rum[phone_number]["sent_code_info"] = sent_code_info
        me = await client.get_me()
        newLogin(me,phone_number)
        return  {"ok":True,"password":False}
    except SessionPasswordNeeded:
        logins_rum[phone_number]["client"] = client
        logins_rum[phone_number]["sent_code_info"] = sent_code_info
        return  {"ok":True,"password":True}
    except Exception as e:
        return {"ok":False,"text":f"{e}"}

async def checkLoginPassword(phone_number,password):
    client = logins_rum[phone_number]["client"]
    sent_code_info = logins_rum[phone_number]["sent_code_info"]
    try:
        await client.check_password(password)
        logins_rum[phone_number]["client"] = client
        logins_rum[phone_number]["sent_code_info"] = sent_code_info
        login_client[phone_number] = client
        me = await client.get_me()
        newLogin(me,phone_number)
        return  {"ok":True}
    except SessionPasswordNeeded:
        logins_rum[phone_number]["client"] = client
        logins_rum[phone_number]["sent_code_info"] = sent_code_info
        return  {"ok":True,"password":True}
    except Exception as e:
        return {"ok":False,"text":f"{e}"}







def addRespons(id,data):
    print(data)
    url = api + f"/api/addRespons/{id}/{TOKEN}"
    r = requests.post(url,json=data).text
    print(r)
    return True

def GetOrders():
    url = api + f"/api/getRequests/{TOKEN}"
    r = requests.post(url).json()
    return r

idsBlock = []
async def LoadSetings():
    while True:
        if not int(exp_time) > int(time.time()):
            print(f"EXP Time : {exp_time}")
            break
        try:
            js_data = JsonManager("data.json")
            js = js_data.get_all()
            for user in js:
                data = js[user]
                if data["isPost"] == True and len(data["list_msg"]) > 0 and len(data["list_text"]) > 0:
                    for js_text in data["list_text"]:
                        if int(js_text["last_msg_time"]) == 0:
                            for js_chat in data["list_msg"]:
                                js_chat = data["list_msg"][js_chat]
                                print(js_chat)
                                try:
                                    text = str(js_text["text"])
                                    if user in login_client:
                                        client = login_client[user]
                                    else:
                                        client =  Client(f"logins/{user}", api_id, api_hash)
                                        await client.connect()
                                        login_client[user] = client
                                    await client.send_message(int(js_chat["id"]),text)
                                except Exception as e:
                                    e = traceback.format_exc()
                                    print(f"Error SendMessage ")
                            data["lenMsgs"] = int(data["lenMsgs"]) + 1
                            data["list_text"][data["list_text"].index(js_text)]["last_msg_time"] = str(int(time.time()) + int(js_text["sleep"]))
                            js_data.update(user,data)
                        elif int(time.time()) >= int(js_text["last_msg_time"]):
                            for js_chat in data["list_msg"]:
                                js_chat = data["list_msg"][js_chat]
                                try:
                                    text = str(js_text["text"])
                                    if user in login_client:
                                        client = login_client[user]
                                    else:
                                        client =  Client(f"logins/{user}", api_id, api_hash)
                                        await client.connect()
                                        login_client[user] = client
                                    await client.send_message(int(js_chat["id"]),text)
                                except Exception as e:
                                    e = traceback.format_exc()
                                    print(f"Error SendMessage ")
                            data["lenMsgs"] = int(data["lenMsgs"]) + 1
                            data["list_text"][data["list_text"].index(js_text)]["last_msg_time"] = str(int(time.time()) + int(js_text["sleep"]))
                            js_data.update(user,data)
        except Exception as e:
            e = traceback.format_exc()
            print(f"Error Lodging SendMsg : {e}")
                    
        try:
            ordd = GetOrders()
            for i in ordd:
                og = ordd[i]
                print(og)
                idd = str(og["id"])
                if og["type"] == "getLogins":
                    js_data = JsonManager("data.json")
                    addRespons(idd,js_data.get_all())
                if og["type"] == "login" and not idd in idsBlock:
                    idsBlock.append(idd)
                    s = await sendLogin(og["data"]["number"])
                    addRespons(idd,s)
                    idsBlock.remove(idd)
                if og["type"] == "sendCodeLogin" and not idd in idsBlock:
                    idsBlock.append(idd)
                    ss = await checkLoginCode(og["data"]["number"],og["data"]["code"])
                    addRespons(idd,ss)
                    idsBlock.remove(idd)
                if og["type"] == "sendPasswordLogin" and not idd in idsBlock:
                    idsBlock.append(idd)
                    sss = await checkLoginPassword(og["data"]["number"],og["data"]["password"])
                    addRespons(idd,sss)
                    idsBlock.remove(idd)
                if og["type"] == "getChats" and not idd in idsBlock:
                    num = og["data"]["number"]
                    if num in login_client:
                        client = login_client[num]
                    else:
                        client =  Client(f"logins/{num}", api_id, api_hash)
                        await client.connect()
                        login_client[num] = client
                    lists = []
                    js_data = JsonManager("data.json")
                    list_msg =js_data.get_all()[num]["list_msg"]
                    idsBlock.append(idd)
                    try:
                        async for dialog in client.get_dialogs():
                            chat = dialog.chat
                            if chat.permissions and not str(chat.id) in list_msg:
                                chat_id = chat.id 
                                chat_name = chat.title or chat.first_name or "بدون اسم"  # 📌 اسم المحادثة
                                chat_type = str(chat.type)
                                if chat_type == "ChatType.PRIVATE":
                                    chat_type = "حساب خاص"
                                elif chat_type == "ChatType.BOT":
                                    chat_type == "بوت"
                                elif chat_type == "ChatType.GROUP" or chat_type == "ChatType.SUPERGROUP":
                                    chat_type = "مجموعة"
                                elif chat_type == "ChatType.CHANNEL":
                                    chat_type = "قناة"
                                else:
                                    chat_type = "بوت"
                                lists.append([chat_id,chat_name,str(chat_type)])
                    except Exception as e:
                        e = traceback.format_exc()
                        print(e)
                    addRespons(idd,lists)
                    idsBlock.remove(idd)
                if og["type"] == "getImageChat" and not idd in idsBlock:
                    idsBlock.append(idd)
                    num = og["data"]["number"]
                    if num in login_client:
                        client = login_client[num]
                    else:
                        client =  Client(f"logins/{num}", api_id, api_hash)
                        await client.connect()
                        login_client[num] = client
                    chat_id = og["data"]["id"]
                    ig = await GetUrlImage(client,chat_id)
                    addRespons(idd,{"img":ig})
                    idsBlock.remove(idd)
                if og["type"] == "serachChatLink" and not idd in idsBlock:
                    num = og["data"]["number"]
                    if num in login_client:
                        client = login_client[num]
                    else:
                        client =  Client(f"logins/{num}", api_id, api_hash)
                        await client.connect()
                        login_client[num] = client
                    link = og["data"]["link"]
                    idsBlock.append(idd)
                    try:
                        chat = await client.get_chat(link)
                        chat_id = chat.id
                        name = chat.title or chat.first_name or "بدون اسم"
                        chat_type = str(chat.type)
                        chat_type = str(chat.type)
                        if chat_type == "ChatType.PRIVATE":
                            chat_type = "حساب خاص"
                        elif chat_type == "ChatType.BOT":
                            chat_type == "بوت"
                        elif chat_type == "ChatType.GROUP" or chat_type == "ChatType.SUPERGROUP":
                            chat_type = "مجموعة"
                        elif chat_type == "ChatType.CHANNEL":
                            chat_type = "قناة"
                        else:
                            chat_type = "بوت"
                        ig = await GetUrlImage(client,chat_id)
                        chat_img = ig
                        js_data = JsonManager("data.json")
                        user_data = js_data.get_all()[num]
                        list_msg = user_data["list_msg"]
                        list_msg[chat_id] = {
                            "id":str(chat_id),
                            "name":str(name),
                            "type":str(chat_type),
                            "img":str(chat_img)
                        }
                        user_data["list_msg"] = list_msg
                        js_data.update(num,user_data)
                        addRespons(idd,{"ok":True,"chat":[chat_id,name,chat_type,chat_img],"text":"تمت ألاضافة بنجاح"})
                    except Exception as e :
                        e = traceback.format_exc()
                        print(e)
                        addRespons(idd,{"ok":False,"text":"فشلت العملية"})
                    idsBlock.remove(idd)
                if og["type"] == "addTextsList":
                    num = og["data"]["number"]
                    name = og["data"]["name"]
                    text = og["data"]["text"]
                    slp = og["data"]["sleep"]
                    js_data = JsonManager("data.json")
                    user_data = js_data.get_all()[num]
                    texts = user_data["list_text"]
                    gg = {
                        "name":name,
                        "text":text,
                        "sleep":str(slp),
                        "index":str(''.join(random.choices("1234567890",k=22))),
                        "last_msg_time":"0"
                    }
                    texts.append(gg)
                    user_data["list_text"] = texts
                    js_data.update(num,user_data)
                    addRespons(idd,gg)
                if og["type"] == "deletChat":
                    num = og["data"]["number"]
                    id = og["data"]["id"]
                    js_data = JsonManager("data.json")
                    user_data = js_data.get_all()[num]
                    list_msg = user_data["list_msg"]
                    del list_msg[id]
                    user_data["list_msg"] = list_msg
                    js_data.update(num,user_data)
                    addRespons(idd,{"ok":True})
                if og["type"] == "deletText":
                    num = og["data"]["number"]
                    index = og["data"]["index"]
                    js_data = JsonManager("data.json")
                    user_data = js_data.get_all()[num]
                    list_text = user_data["list_text"]
                    for i in list_text:
                        if i["index"] == str(index):
                            list_text.remove(i)
                    user_data["list_text"] = list_text
                    js_data.update(num,user_data)
                    addRespons(idd,{"ok":True})
                if og["type"] == "setRun":
                    num = og["data"]["number"]
                    value = str(og["data"]["value"])
                    js_data = JsonManager("data.json")
                    if value == "off":
                        me = js_data.get_all()[num]
                        me["isPost"] = False
                        js_data.update(num,me)
                    elif value == "on":
                        me = js_data.get_all()[num]
                        me["isPost"] = True
                        js_data.update(num,me)
                    addRespons(idd,{"ok":True})
                if og["type"] == "exitLogin" and not idd in idsBlock:
                    try:
                        idsBlock.append(idd)
                        num = og["data"]["number"]
                        js_data = JsonManager("data.json")
                        js_data.remove(num)
                        if num in login_client:
                            client = login_client[num]
                        else:
                            client =  Client(f"logins/{num}", api_id, api_hash)
                            await client.connect()
                            login_client[num] = client
                        if client.is_connected:
                            await client.log_out()
                        else:
                            await client.start()
                            await client.log_out()
                        if num in login_client:
                            login_client.pop(num)
                        
                    except:
                        pass
                    addRespons(idd,{"ok":True})
                    idsBlock.remove(idd)
        except Exception as e:
            e = traceback.format_exc()
            print(e)



asyncio.run(LoadSetings())