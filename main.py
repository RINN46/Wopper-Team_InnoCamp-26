import fastapi
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import BaseModel

users = []
sessions = {

}
app = fastapi.FastAPI()

class RegisterData(BaseModel):
    login: str
    password: str
    name: str
    stack: str

class TimetableData(BaseModel):
    title: str
    time: str
    description: str

class LoginData(BaseModel):
    login: str
    password: str

class OrgCreateData(BaseModel):
    owner: str
    name: str

class TimetableTask:
    def __init__(self):
        self.title = ""
        self.description = ""
        self.time = ""

class Task:
    def __init__(self):
        self.title = ""
        self.deadline = ""

class User:
    def __init__(self):
        self.steck = ""
        self.login = ""
        self.password = ""
        self.name = ""
        self.timetable = []
        self.id = 0
        self.tasks = []

class Organization:
    def __init__(self):
        self.users = []
        self.organization = ""
        self.messages = []


organizations = []

def find_organization(user):
    for org in organizations:
        if user in org.users:
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

@app.get("/chat_page", response_class=HTMLResponse)
async def chat_page(request: Request):
    user = users[sessions[request.cookies.get("session_id")]]

    org = find_organization(user.id)

    if org is None:
        return templates.TemplateResponse(request, "xchat_page.html", {})

    return templates.TemplateResponse(request, "chat_page.html", {})

@app.post("/create_organization")
async def create_organization(request: Request, info: OrgCreateData):

    user = users[sessions[request.cookies.get("session_id")]]

    if find_organization(user) is not None:
        return {"OK": "Организация не найдена"}

    org = Organization()
    org.organization = info.name
    org.users.append(user)

    organizations.append(org)

    return {"OK": True}

@app.post("/join_organization")
async def join_organization(request: Request, name: str):

    user = users[sessions[request.cookies.get("session_id")]]

    if find_organization(user) is not None:
        return {"OK": "Организация не найдена"}

    for org in organizations:
        if org.organization == name:
            org.users.append(user)
            return {"OK": True}

    return {"OK": "Организация не найдена"}

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "RegBlock.html", {})

@app.get("/menagment", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(request, "management.html", {})

@app.get("/login_page", response_class=HTMLResponse)
async def login_p(request: Request):
    return templates.TemplateResponse(request, "Sign_In.html", {})

@app.get("/main_page", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(request, "index.html", {})

@app.get("/tasks", response_class=HTMLResponse)
async def tasks(request: Request):
    return templates.TemplateResponse(request, "tasks.html", {})

@app.get("/staff", response_class=HTMLResponse)
async def staff(request: Request):
    return templates.TemplateResponse(request, "employees.html", {})

def check_login(login):
    if 5 <= len(login) <= 75:
        for i in login:
            if not (i.isalpha() or i.isdigit() or i in ["-", "_"]):
                return "Можно испольщовать только латинские буквы, цифры, и _ -"
        for i in users:
            if i.login == login:
                return "Логин уже существует"
        return True
    return "логин должен быть от 5 до 75 символов"

def first_id():
    a = 0
    while a in sorted(users, key=lambda x: x.id):
        a += 1
    return a

def check_password(password):
    symbols = "!@#$%^*(),[]{}"

    if len(password) < 10 or len(password) > 50:
        return "Пароль должен содержать от 10 до 50 символов"

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

    if has_lower == False:
        return "Нужно использовать строчные буквы"
    if has_upper == False:
        return "Нужно использовать заглавные буквы"
    if has_digit == False:
        return "Нужно использовать цифры"
    if has_symbol == False:
        return "Нужно испрользовать специальные символы"
    return True

@app.post("/reg")
async def reg(request: Request, register_data: RegisterData):
    login = register_data.login
    password = register_data.password
    name = register_data.name
    stack = register_data.stack
    u = User()
    if check_login(login) != True:
        return {"OK": False, "id": 0, "error": 1, "description": check_login(login)}
    u.login = login
    if check_password(password) != True:
        return {"OK": False, "id": 0, "error": 2, "description": check_password(password)}
    u.password = password
    if check_name(name) != True:
        return {"OK": False, "id": 0, "error": 3, "description": check_name(name)}
    u.name = name
    if check_stack(stack) != True:
        return {"OK": False, "id": 0, "error": 4, "description": check_stack(stack)}

    ID = first_id()
    u.id = ID
    users.append(u)
    sessions[request.cookies.get("session_id")] = len(users)-1
    return {"OK": True, "id": ID}

def check_name(name):
    if len(name) < 6 or len(name) > 30:
        return "Имя должно содержать от 6 до 30 символов"

    words = name.split()

    if len(words) == 0:
        return "Введите имя"

    for word in words:
        if not ('А' <= word[0] <= 'Я'):
            return "Используйте Заглавные буквы в начале имени или фамилии"

        for char in word[1:]:
            if not ('а' <= char <= 'я'):
                return "Используйте только строчную киррилицу как непервые символы имени или фамилии"

    return True

@app.post("/login")
async def login(request: Request, login_data: LoginData):

    for u in users:
        print(u.login)
        if u.login == login_data.login:
            if u.password == login_data.password:
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
    return "Стек должен содержать от 3 до 75 символов"

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

@app.get("/personal", response_class=HTMLResponse)
async def personal(request: Request):
    return templates.TemplateResponse(request, "personal.html", {})


@app.get("/user/{id}")
async def get_user(id):

    for user in users:
        if user.id == id:
            return {
                "OK": True,
                "user": {
                    "id": user.id,
                    "login": user.login,
                    "name": user.name,
                    "stack": user.steck
                }
            }

    return {
        "OK": False,
        "error": "Пользователь не найден"
    }

@app.get("/user_timetable")
async def user_timetable(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id not in sessions:
        return {"OK": False}

    user = users[sessions[session_id]]
    table = []
    for i in user.timetable:
        table.append({
            "title": i.title,
            "time": i.time,
            "description": i.description
        })
    return {
        "OK": True,
        "timetable": table
    }

@app.get("/user_tasks")
async def user_tasks(request: Request):

    session_id = request.cookies.get("session_id")

    if session_id not in sessions:
        return {"OK": False}

    user = users[sessions[session_id]]
    table = []
    for i in user.tasks:
        table.append({
            "title": i.title,
            "time": i.deadline,
        })
    return {
        "OK": True,
        "timetable": table
    }


@app.post("/user_timetable/add")
async def add_user_timetable(request: Request, timetableData: TimetableData):
    session_id = request.cookies.get("session_id")

    if session_id not in sessions:
        return {"OK": False}

    user = users[sessions[session_id]]
    table = TimetableTask()
    table.time = timetableData.time
    table.description = timetableData.description
    table.title = timetableData.title
    user.timetable.append()


    return {"OK": True}

