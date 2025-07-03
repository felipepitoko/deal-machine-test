from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from typing import List
from datetime import date
from create_table import get_session, Message as DBMessage

app = FastAPI()

# Estrutura dos dados
from typing import Optional

class Message(BaseModel):
    word: Optional[str] = None
    username: str  # Obrigatório
    message: str  # Obrigatório
    keywords: Optional[str] = None
    feeling: Optional[str] = None
    intention: Optional[str] = None
    created_at: Optional[str] = None  # ISO timestamp


# Lista simulando um "banco de dados" em memória
messages: List[Message] = [
    Message(word="exemplo", username="user1", message="Mensagem de exemplo"),
    Message(word="teste", username="user2", message="Outra mensagem"),
]

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

    # Use analyze_message to extract keywords and intention if message has two words
    analysis = analyze_message(new_message.message)
    auto_keywords = ",".join(analysis["keywords"]) if analysis["keywords"] else None
    auto_intention = ",".join(analysis["intention"]) if analysis["intention"] else None

    # Prefer user-provided keywords/intention, else use auto
    keywords = getattr(new_message, 'keywords', None) or auto_keywords
    intention = getattr(new_message, 'intention', None) or auto_intention

    session = get_session()
    db_message = DBMessage(
        username=new_message.username,
        message=new_message.message,
        keywords=keywords,
        feeling=getattr(new_message, 'feeling', None),
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
    keywords: Optional[str] = Query(None, description="Comma separated list of keywords to filter (e.g. trabalho,compras)")
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