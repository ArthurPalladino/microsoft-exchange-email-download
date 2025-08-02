# microsoft-exchange-email-download

Um cliente solicitou um robô que acessasse diariamente a conta de e-mail Exchange da Microsoft e fizesse o download automático de planilhas recebidas no dia. Após bastante pesquisa, foi possível implementar a solução utilizando os endpoints corretos da Microsoft Graph API. Embora o código seja simples, encontrar esses endpoints e entender os fluxos de autenticação levou algum tempo, pois a documentação da Graph API nem sempre é direta, especialmente no que diz respeito a manipular anexos de e-mails.

Este repositório contém um exemplo funcional e direto ao ponto, que pode ser útil para outras pessoas com necessidades semelhantes.

## ✨ O que o projeto faz

- Acessa uma conta Microsoft Exchange (Outlook, Hotmail, Office 365)
- Lista os e-mails recebidos no dia atual
- Identifica e baixa anexos do tipo `.xlsx`

## 🔍 Tecnologias e bibliotecas usadas

- Python 3
- Microsoft Graph API
- `requests`


## 🚀 Como usar

1. Clone o repositório.
2. Instale as dependências:
pip install -r requirements.txt

3. Configure suas credenciais e permissões no portal do Azure para obter o client_id, tenant_id e client_secret e coloque em config.cfg.

4. Execute o script:
main.py
