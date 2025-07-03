from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List
from datetime import date
from db_manager import get_session, Message as DBMessage

app = FastAPI()


from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Estrutura dos dados
from typing import Optional

class Message(BaseModel):
    username: str  # Obrigatório
    message: str  # Obrigatório
    keywords: Optional[str] = None
    feeling: Optional[str] = None
    intention: Optional[str] = None
    created_at: Optional[str] = None  # ISO timestamp

@app.get("/distinct_usernames/", response_model=List[str])
def distinct_usernames():
    session = get_session()
    usernames = session.query(DBMessage.username).filter(DBMessage.username.isnot(None)).distinct().all()
    session.close()
    flat_usernames = set()
    for (username,) in usernames:
        if username:
            flat_usernames.add(username)
    return sorted(flat_usernames)

@app.get("/distinct_keywords/", response_model=List[str])
def distinct_keywords():
    session = get_session()
    keywords = session.query(DBMessage.keywords).filter(DBMessage.keywords.isnot(None)).all()
    session.close()
    flat_keywords = set()
    for (kwds,) in keywords:
        if kwds:
            for k in kwds.split(","):
                k = k.strip()
                if k:
                    flat_keywords.add(k)
    return sorted(flat_keywords)

@app.get("/distinct_feelings/", response_model=List[str])
def distinct_feelings():
    session = get_session()
    feelings = session.query(DBMessage.feeling).filter(DBMessage.feeling.isnot(None)).all()
    session.close()
    flat_feelings = set()
    for (feeling,) in feelings:
        if feeling:
            for f in feeling.split(","):
                f = f.strip()
                if f:
                    flat_feelings.add(f)
    return sorted(flat_feelings)

@app.get("/distinct_intentions/", response_model=List[str])
def distinct_intentions():
    session = get_session()
    # Get all non-null intentions, split by comma if multiple, flatten, and get unique
    intentions = session.query(DBMessage.intention).filter(DBMessage.intention.isnot(None)).all()
    session.close()
    # Flatten and split comma-separated intentions
    flat_intentions = set()
    for (intent,) in intentions:
        if intent:
            for i in intent.split(","):
                i = i.strip()
                if i:
                    flat_intentions.add(i)
    return sorted(flat_intentions)

# Endpoint 3: Inserir nova mensagem (agora insere no banco de dados)
@app.post("/add_message/", response_model=Message)
def add_message(new_message: Message):
    if not new_message.message or not new_message.username:
        raise HTTPException(status_code=400, detail="Os campos 'username' e 'message' são obrigatórios.")
    from datetime import datetime, timedelta, timezone
    from filters import analyze_message
    # Define UTC-3 timezone
    utc_minus_3 = timezone(timedelta(hours=-3))
    created_at = datetime.now(utc_minus_3).replace(tzinfo=None)

    # Use analyze_message to extract keywords, intention, and feeling if message has two words
    analysis = analyze_message(new_message.message)
    auto_keywords = ",".join(analysis["keywords"]) if analysis.get("keywords") else None
    auto_intention = ",".join(analysis["intention"]) if analysis.get("intention") else None
    auto_feeling = ",".join(analysis["feeling"]) if analysis.get("feeling") else None

    # Prefer user-provided keywords/intention/feeling, else use auto
    keywords = getattr(new_message, 'keywords', None) or auto_keywords
    intention = getattr(new_message, 'intention', None) or auto_intention
    feeling = getattr(new_message, 'feeling', None) or auto_feeling

    session = get_session()
    db_message = DBMessage(
        username=new_message.username,
        message=new_message.message,
        keywords=keywords,
        feeling=feeling,
        intention=intention,
        created_at=created_at
    )
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    session.close()
    return Message(
        username=db_message.username,
        message=db_message.message,
        keywords=getattr(db_message, 'keywords', None),
        feeling=getattr(db_message, 'feeling', None),
        intention=getattr(db_message, 'intention', None),
        created_at=db_message.created_at.isoformat() if db_message.created_at else None
    )

# Endpoint 4: Listar todas as mensagens (agora busca do banco de dados)
from fastapi import Query

@app.get("/list_messages/", response_model=List[Message])
def list_messages(
    username: Optional[str] = None,
    start_date: Optional[str] = Query(None, description="Start date as ISO 8601 string (e.g. 2025-07-03T12:00:00)"),
    end_date: Optional[str] = Query(None, description="End date as ISO 8601 string (e.g. 2025-07-03T13:00:00)"),
    keywords: Optional[str] = Query(None, description="Comma separated list of keywords to filter (e.g. trabalho,compras)"),
    feeling: Optional[str] = Query(None, description="Comma separated list of feelings to filter (e.g. feliz,triste)"),
    intention: Optional[str] = Query(None, description="Comma separated list of intentions to filter (e.g. trabalho,compras)")
):
    from datetime import datetime
    from sqlalchemy import or_
    session = get_session()
    query = session.query(DBMessage)
    if username:
        query = query.filter(DBMessage.username == username)
    if start_date is not None:
        try:
            start_dt = datetime.fromisoformat(start_date)
            query = query.filter(DBMessage.created_at >= start_dt)
        except Exception:
            session.close()
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use ISO 8601 string.")
    if end_date is not None:
        try:
            end_dt = datetime.fromisoformat(end_date)
            query = query.filter(DBMessage.created_at <= end_dt)
        except Exception:
            session.close()
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use ISO 8601 string.")
    if keywords:
        keyword_list = [k.strip() for k in keywords.split(",") if k.strip()]
        if keyword_list:
            # Use ilike for case-insensitive search
            query = query.filter(
                or_(*[DBMessage.keywords.ilike(f"%{kw}%") for kw in keyword_list])
            )
    if feeling:
        feeling_list = [f.strip() for f in feeling.split(",") if f.strip()]
        if feeling_list:
            query = query.filter(
                or_(*[DBMessage.feeling.ilike(f"%{f}%") for f in feeling_list])
            )
    if intention:
        intention_list = [i.strip() for i in intention.split(",") if i.strip()]
        if intention_list:
            query = query.filter(
                or_(*[DBMessage.intention.ilike(f"%{i}%") for i in intention_list])
            )
    db_messages = query.all()
    result = [
        Message(
            username=m.username,
            message=m.message,
            keywords=getattr(m, 'keywords', None),
            feeling=getattr(m, 'feeling', None),
            intention=getattr(m, 'intention', None),
            created_at=m.created_at.isoformat() if m.created_at else None
        ) for m in db_messages
    ]
    session.close()
    return result

from fastapi import Request

@app.post("/from_telegram/")
async def from_telegram(request: Request):
    body = await request.body()
    import json
    try:
        data = json.loads(body)
        username = data["message"]["from"].get("username")
        message_text = data["message"].get("text")
    except Exception as e:
        print(f"Error parsing telegram body: {e}")
        return {"error": "Invalid telegram payload", "details": str(e)}
    print(f"username: {username}, message: {message_text}")

    # Analyze message and save to DB (like add_message)
    from datetime import datetime, timedelta, timezone
    from filters import analyze_message
    utc_minus_3 = timezone(timedelta(hours=-3))
    created_at = datetime.now(utc_minus_3).replace(tzinfo=None)
    analysis = analyze_message(message_text)
    auto_keywords = ",".join(analysis["keywords"]) if analysis.get("keywords") else None
    auto_intention = ",".join(analysis["intention"]) if analysis.get("intention") else None
    auto_feeling = ",".join(analysis["feeling"]) if analysis.get("feeling") else None

    session = get_session()
    db_message = DBMessage(
        username=username,
        message=message_text,
        keywords=auto_keywords,
        feeling=auto_feeling,
        intention=auto_intention,
        created_at=created_at
    )
    print(json.dumps(db_message.__dict__, default=str))
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    session.close()
    return {
        "username": db_message.username,
        "message": db_message.message,
        "keywords": db_message.keywords,
        "feeling": db_message.feeling,
        "intention": db_message.intention,
        "created_at": db_message.created_at.isoformat() if db_message.created_at else None
    }