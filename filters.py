
from typing import List, Dict, Tuple

# Predefined keywords, intentions, and feelings, based on populate.py mock messages
PREDEFINED_KEYWORDS = {
    "bom": {"intention": "cumprimentar", "feeling": "positivo"},
    "trabalho": {"intention": "trabalhar", "feeling": "neutro"},
    "mensagem": {"intention": "comunicar", "feeling": "neutro"},
    "teste": {"intention": "testar sistema", "feeling": "neutro"},
    "sistema": {"intention": "testar sistema", "feeling": "neutro"},
    "tempo": {"intention": "verificar clima", "feeling": "neutro"},
    "reunião": {"intention": "lembrar compromisso", "feeling": "neutro"},
    "parabéns": {"intention": "elogiar", "feeling": "positivo"},
    "ajuda": {"intention": "pedir suporte", "feeling": "negativo"},
    "código": {"intention": "programar", "feeling": "neutro"},
    "almoço": {"intention": "informar refeição", "feeling": "positivo"},
    "motivacional": {"intention": "motivar equipe", "feeling": "positivo"},
    "finalizando": {"intention": "encerrar atividades", "feeling": "neutro"},
    "tarefas": {"intention": "gerenciar tarefas", "feeling": "neutro"},
    "progresso": {"intention": "elogiar", "feeling": "positivo"},
    "equipe": {"intention": "referenciar grupo", "feeling": "positivo"}
}

def analyze_message(message_text: str) -> Dict[str, object]:
    """
    Receives a message text, checks if it has only two words, searches for predefined keywords,
    and returns a dict with the message, found keywords, and their intentions.
    """
    words = message_text.strip().split()
    result = {
        "message": message_text,
        "keywords": [],
        "intention": [],
        "feeling": []
    }

    if len(words) == 3:
        found_keywords = []
        found_intentions = []
        found_feelings = []
        for word in words:
            word_lower = word.lower()
            if word_lower in PREDEFINED_KEYWORDS:
                found_keywords.append(word_lower)
                found_intentions.append(PREDEFINED_KEYWORDS[word_lower]["intention"])
                found_feelings.append(PREDEFINED_KEYWORDS[word_lower]["feeling"])
        result["keywords"] = found_keywords
        result["intention"] = found_intentions
        result["feeling"] = found_feelings
    else:
        # Use analyze_agent.py function for other cases
        try:
            from analyze_agent import analyze_ai_agent
            agent_result = analyze_ai_agent(message_text)
            if agent_result and isinstance(agent_result, list):
                all_keywords = []
                all_intentions = []
                all_feelings = []
                for item in agent_result:
                    all_keywords.extend(item.get("keywords", []))
                    all_intentions.extend(item.get("intention", []))
                    all_feelings.extend(item.get("feeling", []))
                result["keywords"] = all_keywords
                result["intention"] = all_intentions
                result["feeling"] = all_feelings
            elif agent_result and isinstance(agent_result, dict):
                result["keywords"] = agent_result.get("keywords", [])
                result["intention"] = agent_result.get("intention", [])
                result["feeling"] = agent_result.get("feeling", [])
        except ImportError:
            pass
    return result
