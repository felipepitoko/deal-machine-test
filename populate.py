mock_data = [
  {
    "message": "Primeira mensagem de bom dia",
    "username": "Master"
  },
  {
    "message": "Mensagem de teste para o sistema",
    "username": "Alice"
  },
  {
    "message": "Como está o tempo hoje?",
    "username": "Bob"
  },
  {
    "message": "Lembrete: reunião às 15h",
    "username": "Master"
  },
  {
    "message": "Parabéns pelo seu progresso!",
    "username": "Alice"
  },
  {
    "message": "Preciso de ajuda com o código",
    "username": "Bob"
  },
  {
    "message": "Bom trabalho, equipe!",
    "username": "Master"
  },
  {
    "message": "Almoço em 10 minutos",
    "username": "Alice"
  },
  {
    "message": "Finalizando as tarefas do dia",
    "username": "Bob"
  },
  {
    "message": "Mensagem motivacional para todos",
    "username": "Master"
  }
]

import requests

#make a post request for each dict to http://localhost:8000/add_message/
for data in mock_data:
  response = requests.post('http://localhost:8000/add_message/', json=data)
  print(response.status_code)