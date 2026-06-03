# Sistema de Pré-Check-in Hoteleiro

> **Otimizando o processo de check-in de hóspedes com tecnologia web moderna**

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0+-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)

## 📋 Visão Geral

Sistema WEB desenvolvido em Python com Flask para otimizar o processo de check-in de hóspedes em hotéis. O sistema permite que hóspedes realizem seu pré-check-in online antes da chegada, reduzindo filas, tempo de espera e melhorando a experiência geral.

### Problema Resolvido

- ✗ Filas extensas nos horários de pico (14h-15h)
- ✗ Sobrecarga de recepcionistas
- ✗ Lentidão no atendimento
- ✗ Experiência negativa na chegada
- ✗ Erros de cadastro manual

### Solução Implementada

- ✓ Pré-check-in 100% online
- ✓ Redução de tempo na recepção
- ✓ Validação automática de dados
- ✓ Assinatura digital integrada
- ✓ QR Code para verificação rápida
- ✓ Painel administrativo completo

## 🚀 Funcionalidades

### Para Hóspedes

- Acesso via link enviado por e-mail
- Preenchimento de dados pessoais
- Upload de documento de identificação
- Assinatura digital na tela
- Confirmação de informações da reserva
- Recebimento de protocolo e QR Code
- Comprovante de pré-check-in

### Para Administrativos

- Dashboard com estatísticas
- Visualização de check-ins realizados
- Pesquisa e filtros avançados
- Visualização de documentos enviados
- Confirmação de chegada do hóspede
- Relatórios de desempenho
- Auditoria de acessos

## 📦 Tecnologias Utilizadas

### Backend
- **Python 3.8+** - Linguagem de programação
- **Flask 3.0** - Framework web
- **Flask-SQLAlchemy** - ORM para banco de dados
- **Flask-WTF** - Validação de formulários
- **SQLite** - Banco de dados

### Frontend
- **HTML5** - Marcação semântica
- **CSS3** - Estilização moderna
- **Bootstrap 5** - Framework CSS
- **JavaScript** - Interatividade
- **Signature Pad** - Captura de assinatura
- **QRCode.js** - Geração de QR Code

### Segurança
- **Werkzeug** - Hash de senhas
- **Flask-WTF** - Proteção CSRF
- **Validação de entrada** - Todas as entradas validadas

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git

### Passo a Passo

1. **Clone o repositório**

```bash
git clone https://github.com/Sabrinakohlhamer/Site-check-in.git
cd Site-check-in
```

2. **Crie um ambiente virtual**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Instale as dependências**

```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**

```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. **Execute a aplicação**

```bash
python app.py
```

6. **Acesse no navegador**

```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
Site-check-in/
├── app.py                  # Aplicação Flask principal
├── models.py              # Modelos de banco de dados
├── forms.py               # Validação de formulários
├── requirements.txt       # Dependências Python
├── .env.example           # Variáveis de ambiente (exemplo)
├── .gitignore             # Arquivos ignorados pelo Git
├── README.md              # Este arquivo
│
├── templates/             # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── login.html        # Login administrativo
│   ├── pre_checkin.html  # Formulário de pré-check-in
│   ├── confirmacao.html  # Tela de confirmação
│   ├── dashboard.html    # Painel administrativo
│   ├── hospedes.html     # Lista de hóspedes
│   ├── detalhes_hospede.html  # Detalhes do hóspede
│   └── erro.html         # Página de erro
│
├── static/                # Arquivos estáticos
│   ├── css/
│   │   └── style.css     # Estilos CSS
│   ├── js/
│   │   └── script.js     # Scripts JavaScript
│   └── uploads/          # Pasta para arquivos enviados
│       ├── documents/    # CPFs/RGs/Passaportes
│       ├── signatures/   # Assinaturas digitais
│       └── qrcodes/      # QR Codes gerados
│
└── database/              # Banco de dados SQLite
    └── hotel.db          # Arquivo do banco (criado automaticamente)
```

## 🎨 Design e UX

### Paleta de Cores

- **Azul Escuro**: `#1E3A5F` - Confiança e profissionalismo
- **Branco**: `#FFFFFF` - Clareza e limpeza
- **Cinza Claro**: `#F5F7FA` - Fundo neutro
- **Verde**: `#22C55E` - Confirmações e sucesso

### Tipografia

- **Poppins** - Headlines e títulos
- **Inter** - Corpo de texto

### Responsividade

- ✓ Desktop (1920px e acima)
- ✓ Laptop (1440px a 1920px)
- ✓ Tablet (768px a 1024px)
- ✓ Mobile (até 767px)

## 🔐 Segurança

### Implementado

- ✓ Hash de senhas com Werkzeug
- ✓ Validação de entrada no servidor
- ✓ Proteção CSRF com Flask-WTF
- ✓ Limite de tamanho de arquivo
- ✓ Extensões de arquivo whitelist
- ✓ Log de auditoria de todas as ações
- ✓ Sessões seguras
- ✓ Sanitização de nomes de arquivo

### Recomendações para Produção

- [ ] Use HTTPS/TLS em produção
- [ ] Configure `SECURE_SSL_REDIRECT=True`
- [ ] Use banco de dados PostgreSQL ou MySQL
- [ ] Configure backups automáticos
- [ ] Implemente rate limiting
- [ ] Use variáveis de ambiente para senhas
- [ ] Ative logs de segurança
- [ ] Implemente 2FA para admin

## 👨‍💻 Como Usar

### Para Hóspedes

1. Acesse o link de pré-check-in enviado pelo hotel
2. Preencha todos os dados solicitados
3. Envie foto do documento de identificação
4. Assine digitalmente
5. Confirme os dados
6. Receba protocolo e QR Code
7. Chegue ao hotel com o protocolo em mãos

### Para Administradores

1. Acesse `http://localhost:5000/admin/login`
2. Use credenciais padrão:
   - Email: `admin@hotel.com`
   - Senha: `admin123`
3. Navegue para Dashboard para estatísticas
4. Pesquise hóspedes na seção "Hóspedes"
5. Confirme chegada quando hóspede chegar

## 📊 Estatísticas do Dashboard

- Total de check-ins realizados
- Check-ins concluídos vs pendentes
- Hóspedes chegando hoje
- Próximas chegadas (7 dias)
- Tempo economizado em atendimento
- Taxa de ocupação

## 🔄 Fluxo de Dados

```
Hóspede recebe link
    ↓
Preenche formulário
    ↓
Valida dados no servidor
    ↓
Envia documento
    ↓
Assina digitalmente
    ↓
Salva no banco de dados
    ↓
Gera protocolo e QR Code
    ↓
Mostra confirmação
    ↓
Recepcionista valida na chegada
```

## 📈 Benefícios

### Para Hóspedes
- ⏱️ Menos tempo na recepção
- 📱 Comodidade de preencher em casa
- ✅ Processo transparente e rápido
- 📋 Sem filas de espera

### Para Hotel
- 👥 Recepcionistas mais produtivos
- 📊 Dados validados e íntegros
- 🎯 Melhor controle de ocupação
- 📈 Aumento de NPS
- 💾 Registro digital completo
- 🔍 Rastreabilidade total

## 🐛 Problemas Conhecidos

Nenhum no momento. Reporte issues em [GitHub Issues](https://github.com/Sabrinakohlhamer/Site-check-in/issues).

## 🚦 Roadmap Futuro

- [ ] Integração com PMS hoteleiro
- [ ] Envio de e-mails automáticos
- [ ] SMS com link de pré-check-in
- [ ] App mobile nativa
- [ ] Integração com pagamento
- [ ] Multi-idiomas
- [ ] Autenticação com OAuth
- [ ] Relatórios avançados em PDF
- [ ] Integração com WhatsApp Business
- [ ] Machine Learning para previsão de no-shows

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Sabrina Luana Pauli Kohlhamer**
- GitHub: [@Sabrinakohlhamer](https://github.com/Sabrinakohlhamer)
- Email: sabrina.kohlhamer@amf.edu.br

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 💬 Suporte

Tem dúvidas? Abra uma [issue no GitHub](https://github.com/Sabrinakohlhamer/Site-check-in/issues) ou entre em contato.

## 🙏 Agradecimentos

- Flask e comunidade Python
- Bootstrap pelo framework CSS
- Comunidade open-source

---

**Desenvolvido com ❤️ para hotelaria moderna**
