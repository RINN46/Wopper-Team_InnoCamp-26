import fastapi
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

users = []
sessions = {

}

class User:
    def __init__(self):
        self.steck = ""
        self.login = ""
        self.password = ""
        self.name = ""
        self.id = 0

class Organization:
    def __init__(self):
        self.users = []
        self.organization = ""
        self.messages = []

organizations = []

def find_organization(user_id):
    for org in organizations:
        if user_id in org.users:
            return org
    return None

class Message:
    def __init__(self):
        self.sender = ""
        self.text = ""

@app.post("/send")
async def send(request: Request, text: str):

    user = users[sessions[request.cookies.get("session_id")]]

    org = find_organization(user.id)

    if org is None:
        return {
            "OK": False,
            "error": "Пользователь не состоит в организации"
        }

    m = Message()
    m.sender = user.name
    m.text = text

    org.messages.append(m)

    return {"OK": True}

@app.get("/chat")
async def chat(request: Request):

    user = users[sessions[request.cookies.get("session_id")]]

    org = find_organization(user.id)

    if org is None:
        return {
            "OK": False,
            "error": "Организация не найдена"
        }

    chat = []

    for message in org.messages:
        chat.append({
            "sender": message.sender,
            "text": message.text
        })

    return {
        "OK": True,
        "organization": org.organization,
        "messages": chat
    }

@app.post("/create_organization")
async def create_organization(request: Request, name: str):

    user = users[sessions[request.cookies.get("session_id")]]

    if find_organization(user.id) is not None:
        return {"OK": False}

    org = Organization()
    org.organization = name
    org.users.append(user.id)

    organizations.append(org)

    return {"OK": True}


@app.post("/join_organization")
async def join_organization(request: Request, name: str):

    user = users[sessions[request.cookies.get("session_id")]]

    if find_organization(user.id) is not None:
        return {"OK": False}

    for org in organizations:
        if org.organization == name:
            org.users.append(user.id)
            return {"OK": True}

    return {"OK": False}

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "Regestr_Web.html", {})

@app.get("/main_page", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(request, "Regestr_Web.html", {})

def check_login(login):
    if 5 <= len(login) <= 75:
        for i in login:
            if not (i.isalpha() or i.isdigit() or i in ["-", "_"]):
                return False
        for i in users:
            if i.login == login:
                return False
        return True
    return False


def first_id():
    a = 0
    while a in sorted(users, key=lambda x: x["ID"]):
        a += 1
    return a


def check_password(password):
    symbols = "!@#$%^*(),[]{}"

    if len(password) < 10 or len(password) > 50:
        return False

    has_lower = False
    has_upper = False
    has_digit = False
    has_symbol = False

    for char in password:
        if 'a' <= char <= 'z':
            has_lower = True
        elif 'A' <= char <= 'Z':
            has_upper = True
        elif '0' <= char <= '9':
            has_digit = True
        elif char in symbols:
            has_symbol = True
        else:
            return False

    return has_lower and has_upper and has_digit and has_symbol


@app.post("/reg")
async def reg(request, login: str, password: str, name: str, stack: str):
    u = User()
    if not check_login(login):
        return {"OK": False, "id": 0, "error": 1}
    u.login = login
    if not check_password(password):
        return {"OK": False, "id": 0, "error": 2}
    u.password = password
    if not check_name(name):
        return {"OK": False, "id": 0, "error": 3}
    u.name = name
    if not check_stack(stack):
        return {"OK": False, "id": 0, "error": 4}

    ID = first_id()
    u.id = ID
    users.append(u)
    sessions[request.cookies.get("session_id")] = len(users)-1
    return {"OK": True, "id": ID}


def check_name(name):
    if len(name) < 6 or len(name) > 200:
        return False

    words = name.split()

    if len(words) == 0:
        return False

    for word in words:
        if not ('А' <= word[0] <= 'Я'):
            return False

        for char in word[1:]:
            if not ('а' <= char <= 'я'):
                return False

    return True

@app.post("/login")
async def login(request, login: str, password: str):
    for u in users:
        if u.login == login:
            if u.password == password:
                sessions[request.cookies.get("session_id")] = users.index(u)
                return {
                    "OK": True,
                    "id": u.id
                }

            else:
                return {
                    "OK": False,
                    "id": 0,
                    "error": 1
                }

    return {
        "OK": False,
        "id": 0,
        "error": 2
    }

def check_stack(stack):
    if 3 <= len(stack) <= 75:
        return True
    return False

class Message:
    def __init__(self):
        self.sender = ""
        self.text = ""

messages = []

@app.post("/send")
async def send(request, organization: int, text: str):

    m = Message()
    m.sender = users[sessions[request.cookies.get("session_id")]].name
    m.text = text


    return {"OK": True}

@app.get("/chat")
async def chat(request):
    u = users[sessions[request.cookies.get("session_id")]]
    org = find_organization(u)
    chat = 0

    for message in  :
        if (
            (message.sender == user1 and message.receiver == user2)
            or
            (message.sender == user2 and message.receiver == user1)
        ):
            chat.append({
                "sender": message.sender,
                "receiver": message.receiver,
                "text": message.text
            })

    return {"OK": True, "messages": chat}

