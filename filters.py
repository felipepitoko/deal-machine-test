
from typing import List, Dict, Tuple

# Predefined keywords and their intentions, based on populate.py mock messages
PREDEFINED_KEYWORDS = {
    "bom": "cumprimentar",
    "trabalho": "trabalhar",
    "mensagem": "comunicar",
    "teste": "testar sistema",
    "sistema": "testar sistema",
    "tempo": "verificar clima",
    "reunião": "lembrar compromisso",
    "parabéns": "elogiar",
    "ajuda": "pedir suporte",
    "código": "programar",
    "almoço": "informar refeição",
    "motivacional": "motivar equipe",
    "finalizando": "encerrar atividades",
    "tarefas": "gerenciar tarefas",
    "progresso": "elogiar",
    "equipe": "referenciar grupo"
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
        "intention": []
    }
    if len(words) == 2:
        found_keywords = []
        found_intentions = []
        for word in words:
            word_lower = word.lower()
            if word_lower in PREDEFINED_KEYWORDS:
                found_keywords.append(word_lower)
                found_intentions.append(PREDEFINED_KEYWORDS[word_lower])
        result["keywords"] = found_keywords
        result["intention"] = found_intentions
    
    return result
