import fastapi
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

users = []


class User:
    def init_user(self):
        self.login = ""
        self.password = ""
        self.name = ""
        self.id = 0


app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
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
async def reg(login: str, password: str, name: str, stack: str):
    u = User()
    if not check_login(login):
        return {"OK": False, "id": 0}
    u.login = login
    if not check_password(password):
        return {"OK": False, "id": 0}
    u.password = password
    if not check_name(name):
        return {"OK": False, "id": 0}
    u.name = name
    if not check_stack(stack):
        return {"OK": False, "id": 0}

    ID = first_id()
    u.id = ID
    users.append(u)
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
async def login(login: str, password: str):
    for u in users:
        if u.login == login:
            if u.password == password:
                return {
                    "OK": True,
                    "id": u.id
                }
            else:
                return {
                    "OK": False,
                    "id": 0
                }

    return {
        "OK": False,
        "id": 0
    }

def check_stack(stack):
    if 3 <= len(stack) <= 75:
        return True
    return False