from flask import Flask,request,redirect,render_template_string,session,url_for,jsonify
from flask_cors import CORS
import random,asyncio,os,time,json
import traceback
import urllib
import urllib.parse
from urllib.parse import unquote
import json
import hmac,time
import hashlib

app = Flask(__name__)
CORS(app)

TOKEN = "QUEFYEcewfiuWIENINOidednoqenfd979uhn979N9U79BU9U7Q"

api_img = "https://pubgmobilehack.pythonanywhere.com"
app.secret_key = TOKEN

exp_time = 9000145645663463
link_me = "https://t.me/qqqqqq2"

listRequests = {}
listRespones = {}

botToken = "5239149505:AAG_G1OpIuzUy0oEbbIkviNEDuCVJfojwjE"
idTele = "1044160205"


def validate_hash(hash_str, init_data, token, c_str="WebAppData"):
    init_data = sorted([chunk.split("=")
                        for chunk in unquote(init_data).split("&")
                        if not chunk.startswith("hash=")],
                       key=lambda x: x[0])
    init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])
    secret_key = hmac.new(c_str.encode(), token.encode(),
                         hashlib.sha256).digest()
    data_check = hmac.new(secret_key, init_data.encode(),
                          hashlib.sha256)
    return data_check.hexdigest() == hash_str


def GENID():
    return ''.join(random.choices("1234567890",k=22))

async def GetDataFromManger(tp,dt):
    id = GENID()
    data = {"id":id,"type":tp,"data":dt}
    listRequests.update({id:data})
    while True:
        if id in listRespones and not id in listRequests:
            ret = listRespones[id]
            listRespones.pop(id)
            return ret
        

     
        
def LoadHtml(path):
    return open(path,encoding="utf-8").read()

@app.route("/")
async def index():
    tg_data = request.args.get("tgWebAppData")
    if not tg_data:
        return """
        <script>
    if (window.location.hash) {
        let params = new URLSearchParams(window.location.hash.substring(1));
        let tgData = params.get("tgWebAppData");

        if (tgData) {
            let newUrl = window.location.origin + "/?" + params.toString();
            window.location.replace(newUrl);
        }
    }
</script>


        """


    decoded_data = urllib.parse.unquote(tg_data)
    params = dict(urllib.parse.parse_qsl(decoded_data))
    session["hash"] = params["hash"]
    session["tg_data"] = str(tg_data)
    session["idTele"] = str(json.loads(params["user"])["id"])

    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("getLogins",{})
        return render_template_string(LoadHtml("home.html"),data=listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/login-number",methods=["POST","GET"])
async def login_number():
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("getLogins",{})
        if len(listLogins) > 4:
            return redirect(url_for("index"))
        if request.method == "POST":
            number = str(request.form["number"])
            if number:
                number = "+" + number
                log = await GetDataFromManger("login",{"number":number})
                if log["ok"]:
                    session["number"] = number
                    return redirect(url_for("login_code"))
                else:return render_template_string(LoadHtml("number.html"),text=log["text"],iserror=True)
            else:return render_template_string(LoadHtml("number.html"),text="يرجى كتابة الرقم بشكل صحيح",iserror=True)
        return render_template_string(LoadHtml("number.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    
@app.route("/login-code",methods=["POST","GET"])
async def login_code():
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        if not "number" in session:return redirect(url_for("index"))
        if request.method == "POST":
            code = str(request.form["code"])
            if code:
                log = await GetDataFromManger("sendCodeLogin",{"number":session["number"],"code":str(code)})
                if log["ok"] == True and log["password"] == False:
                    session.pop("number")
                    return redirect(url_for("index"))
                elif log["ok"] == True and log["password"] == True:
                    session["password"] = True
                    return redirect(url_for("login_password"))
                else:
                    session.pop("number")
                    return render_template_string(LoadHtml("number.html"),text=log["text"],iserror=True);session.pop("number")
            else:
                session.pop("number")
                return render_template_string(LoadHtml("number.html"),text="يرجى كتابة الكود",iserror=True);session.pop("number")
        return render_template_string(LoadHtml("code.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    
@app.route("/login-password",methods=["POST","GET"])
async def login_password():
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        if "number" in session and "password" in session:
            pass
        else:
            return redirect(url_for("index"))
        if request.method == "POST":
            password = str(request.form["password"])
            if password:
                log = await GetDataFromManger("sendPasswordLogin",{"number":session["number"],"password":str(password)})
                if log["ok"]:
                    return redirect(url_for("index"))
                else:
                    session.pop("number")
                    return render_template_string(LoadHtml("number.html"),text=log["text"],iserror=True)
            else:
                session.pop("number")
                return render_template_string(LoadHtml("number.html"),text="يرجى كتابة الرمز",iserror=True)
        return render_template_string(LoadHtml("password.html"),text="",iserror=False)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    
@app.route("/seting/<number>",methods=["POST","GET"])
async def seting_number(number):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        if request.method == "POST":
            await GetDataFromManger("setRun",{"number":number,"value":request.form["value"]})
            return redirect(url_for("index"))
        Send = await GetDataFromManger("getLogins",{})
        listLogins = Send[number]
        return render_template_string(LoadHtml("seting.html"),data=listLogins,len=len,api_img=api_img)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/getChats/api/<number>")
async def getChats(number):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("getChats",{"number":number})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/get/image/<id>/<num>")
async def getimg(id,num):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("getImageChat",{"id":id,"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/serachChatLink/<num>",methods=["POST","GET"])
async def serachChatLink(num):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        link = request.json["link"]
        listLogins = await GetDataFromManger("serachChatLink",{"link":link,"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/addTextsList/<num>",methods=["POST","GET"])
async def addTextsList(num):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        d = request.json
        print(d)
        listLogins = await GetDataFromManger("addTextsList",{"name":d["name"],"text":d["text"],"sleep":d["sleep"],"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    
@app.route("/deletChat/<num>/<id>",methods=["POST","GET"])
async def deletChat(num,id):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("deletChat",{"id":str(id),"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/deletText/<num>/<id>",methods=["POST","GET"])
async def deletText(num,id):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("deletText",{"index":str(id),"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)


@app.route("/api/addRespons/<id>/<token>",methods=["POST"])
def addRespons(id,token):
    if token == TOKEN:
        listRespones.update({id:request.get_json()})
        listRequests.pop(id)
        return "ok"
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)

@app.route("/exitLogin/<num>",methods=["POST","GET"])
async def exitLoginSes(num):
    if int(exp_time) > int(time.time()) and validate_hash(session["hash"],session["tg_data"],botToken) and str(session["idTele"]) == str(idTele):
        listLogins = await GetDataFromManger("exitLogin",{"number":num})
        return jsonify(listLogins)
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    

@app.route("/api/getRequests/<token>",methods=["POST","GET"])
def addRequests(token):
    if token == TOKEN:
        return listRequests
    else:
        return render_template_string(LoadHtml("time.html"),link=link_me)
    


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


app.run(host="0.0.0.0",threaded=True)