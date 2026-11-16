# Sistema de Controle de Estoque

MVP web para pequenos comércios, desenvolvido como projeto acadêmico de Projeto de Software (ADS).

## Funcionalidades
- Login de usuário.
- Cadastro de produtos com código, preço, quantidade e estoque mínimo.
- Registro de entradas e saídas com atualização do saldo.
- Bloqueio de saídas que deixariam o estoque negativo.
- Consulta e busca por nome ou código.
- Alerta textual de estoque baixo.

## Tecnologias
Python 3.12, Flask 3, Flask-SQLAlchemy, Flask-Login, SQLite (padrão), PostgreSQL (configurável), Bootstrap 5 e pytest.

## Executar localmente
Requer Python 3.12 ou superior.

```bash
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# Linux/macOS:
source .venv/bin/activate
pip install -r requirements.txt
python run.py
```

Acesse http://127.0.0.1:5000.

**Acesso inicial de demonstração:** usuário `admin`, senha `admin123`. Altere a senha e configure `SECRET_KEY` antes de qualquer uso fora de demonstração. O MVP não deve ser publicado com dados reais enquanto não houver fluxo seguro de criação/alteração de senha e endurecimento de segurança.

## Testes
```bash
pytest -q
```

Os testes verificam proteção de rota, cadastro e alerta de estoque baixo, entrada de mercadoria e bloqueio de saída acima do saldo.

## Banco de dados
Por padrão, usa SQLite e cria o banco automaticamente em `instance/estoque.db`. Para PostgreSQL, configure a variável `DATABASE_URL`, por exemplo:
`postgresql+psycopg://usuario:senha@localhost:5432/estoque`.

## Integração contínua
O workflow `.github/workflows/ci.yml` executa os testes automaticamente em cada push para `main` e em Pull Requests direcionados a `main`.

## Limitações conhecidas e próximos passos
- Conta administrativa inicial fixa para demonstração; implementar alteração segura de senha e gestão de usuários.
- Adicionar proteção CSRF, limitação de tentativas de login e migrações de banco.
- Criar histórico de movimentações na interface e relatórios.
- Executar validação com representantes da comunidade e registrar feedback real.
- Revisar configurações de produção, HTTPS, cookies seguros e segredos antes de publicar.

## Escopo acadêmico
Este repositório contém uma primeira implementação do MVP. A documentação e os testes devem ser atualizados conforme novas funcionalidades e evidências forem produzidas. Não registrar como realizados testes de campo que ainda não aconteceram.
