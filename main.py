from flask import Flask,request,redirect,render_template_string,session,url_for,jsonify
from flask_cors import CORS
import json,random
import os,time


app = Flask(__name__)
CORS(app)
TOKEN = "QUEFYEcewfiuWIENINOidednoqenfd979uhn979N9U79BU9U7Q"
api_img = "https://pkgsppomj3395kendseimkxg.pythonanywhere.com"
app.secret_key = TOKEN
exp_time = 900000000001
link_me = "https://t.me/qqqqqq2"

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




def GENID():
    return ''.join(random.choices("1234567890",k=22))

def GetDataFromManger(tp,dt):
    id = GENID()
    data = {"id":id,"type":tp,"data":dt}
    JsonManager("listRequests.json").add(id,data)
    for i in range(200):
        js_data = JsonManager("listRequests.json")
        js_res = JsonManager("listRespones.json")
        if js_data.get(id) == None and type(js_res.get(id)) in [dict,list]:
            ret = js_res.get(id)
            js_res.remove(id)
            return ret
        time.sleep(0.5)

def LoadHtml(path):
    path = "html-code/"+path
    return open(path,encoding="utf-8").read()

@app.route("/")
def index():
    if int(exp_time) > int(time.time()):
        listLogins =  GetDataFromManger("getLogins",{})
        return render_template_string(LoadHtml("home/home.html"),data=listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/login-number",methods=["POST","GET"])
def login_number():
    if int(exp_time) > int(time.time()):
        if request.method == "POST":
            number = str(request.form["number"])
            if number:
                number = "+" + number
                log = GetDataFromManger("login",{"number":number})
                if log["ok"]:
                    session["number"] = number
                    return redirect(url_for("login_code"))
                else:return render_template_string(LoadHtml("login/number.html"),text=log["text"],iserror=True)
            else:return render_template_string(LoadHtml("login/number.html"),text="يرجى كتابة الرقم بشكل صحيح",iserror=True)
        return render_template_string(LoadHtml("login/number.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/login-code",methods=["POST","GET"])
def login_code():
    if int(exp_time) > int(time.time()):
        if not "number" in session:return redirect(url_for("index"))
        if request.method == "POST":
            code = str(request.form["code"])
            if code:
                log = GetDataFromManger("sendCodeLogin",{"number":session["number"],"code":str(code)})
                if log["ok"] == True and log["password"] == False:
                    session.pop("number")
                    return redirect(url_for("index"))
                elif log["ok"] == True and log["password"] == True:
                    session["password"] = True
                    return redirect(url_for("login_password"))
                else:
                    session.pop("number")
                    return render_template_string(LoadHtml("login/number.html"),text=log["text"],iserror=True);session.pop("number")
            else:
                session.pop("number")
                return render_template_string(LoadHtml("login/number.html"),text="يرجى كتابة الكود",iserror=True);session.pop("number")
        return render_template_string(LoadHtml("login/code.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/login-password",methods=["POST","GET"])
def login_password():
    if int(exp_time) > int(time.time()):
        if "number" in session and "password" in session:
            pass
        else:
            return redirect(url_for("index"))
        if request.method == "POST":
            password = str(request.form["password"])
            if password:
                log = GetDataFromManger("sendPasswordLogin",{"number":session["number"],"password":str(password)})
                if log["ok"]:
                    return redirect(url_for("index"))
                else:
                    session.pop("number")
                    return render_template_string(LoadHtml("login/number.html"),text=log["text"],iserror=True)
            else:
                session.pop("number")
                return render_template_string(LoadHtml("login/number.html"),text="يرجى كتابة الرمز",iserror=True)
        return render_template_string(LoadHtml("login/password.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/seting/<number>",methods=["POST","GET"])
def seting_number(number):
    if int(exp_time) > int(time.time()):
        if request.method == "POST":
            GetDataFromManger("setRun",{"number":number,"value":request.form["value"]})
        listLogins = GetDataFromManger("getLogins",{})[number]
        return render_template_string(LoadHtml("home/seting.html"),data=listLogins,len=len,api_img=api_img)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/getChats/api/<number>")
def getChats(number):
    if int(exp_time) > int(time.time()):
        listLogins = GetDataFromManger("getChats",{"number":number})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)
@app.route("/get/image/<id>/<num>")
def getimg(id,num):
    if int(exp_time) > int(time.time()):
        listLogins = GetDataFromManger("getImageChat",{"id":id,"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/serachChatLink/<num>",methods=["POST","GET"])
def serachChatLink(num):
    if int(exp_time) > int(time.time()):
        link = request.json["link"]
        listLogins = GetDataFromManger("serachChatLink",{"link":link,"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/addTextsList/<num>",methods=["POST","GET"])
def addTextsList(num):
    if int(exp_time) > int(time.time()):
        d = request.json
        print(d)
        listLogins = GetDataFromManger("addTextsList",{"name":d["name"],"text":d["text"],"sleep":d["sleep"],"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/deletChat/<num>/<id>",methods=["POST","GET"])
def deletChat(num,id):
    if int(exp_time) > int(time.time()):
        listLogins = GetDataFromManger("deletChat",{"id":str(id),"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/deletText/<num>/<id>",methods=["POST","GET"])
def deletText(num,id):
    if int(exp_time) > int(time.time()):
        listLogins = GetDataFromManger("deletText",{"index":str(id),"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)


@app.route("/api/addRespons/<id>/<token>",methods=["POST"])
def addRespons(id,token):
    if token == TOKEN:
        js_data = JsonManager("listRequests.json")
        js_res = JsonManager("listRespones.json")
        js_res.add(id,request.get_json())
        js_data.remove(id)
        return "ok"
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)

@app.route("/api/getRequests/<token>",methods=["POST"])
def addRequests(token):
    if token == TOKEN:
        js_data = JsonManager("listRequests.json")
        return js_data.get_all()
    else:
        return render_template_string(LoadHtml("home/time.html"),link=link_me)



@app.route("/isimage/<idd>", methods=["POST"])
def upload_imaggdge(idd):
    file_path = 'static/image/' + idd +'.jpg'
    if os.path.exists(file_path):
        return "ok"
    else:
        return "0"

@app.route("/upload/<idd>", methods=["POST"])
def upload_image(idd):
    if "file" not in request.files:
        return jsonify({"error": "لم يتم إرسال ملف"}), 400
    file = request.files["file"]
    file_path = 'static/image/' + idd +'.jpg'
    if not os.path.exists(file_path):
        file.save(file_path)
    return jsonify({"message": "تم رفع الصورة بنجاح", "file_path": file_path}), 200


app.run(host="0.0.0.0", port=8080)

