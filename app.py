"""
Sistema de Pré-Check-in Hoteleiro - SEM BANCO DE DADOS
Aplicação Flask para otimizar o processo de check-in de hóspedes

Autor: Sistema de Hotel
Data: 2024
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import uuid
import qrcode
import base64
from dotenv import load_dotenv
import json

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-super-segura-aqui')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Pastas de upload
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
app.config['DOCUMENT_FOLDER'] = os.path.join('static', 'uploads', 'documents')
app.config['SIGNATURE_FOLDER'] = os.path.join('static', 'uploads', 'signatures')
app.config['QRCODE_FOLDER'] = os.path.join('static', 'uploads', 'qrcodes')
app.config['DATA_FOLDER'] = os.path.join('data')

ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

# Criar pastas se não existirem
for folder in [app.config['UPLOAD_FOLDER'], app.config['DOCUMENT_FOLDER'], 
               app.config['SIGNATURE_FOLDER'], app.config['QRCODE_FOLDER'],
               app.config['DATA_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# ==================== SIMULAÇÃO DE DADOS EM MEMÓRIA ====================

# Dados de usuários (simulando banco de dados)
USUARIOS = {
    'admin@hotel.com': {
        'id': 1,
        'email': 'admin@hotel.com',
        'senha': generate_password_hash('admin123'),
        'nome': 'Administrador',
        'cargo': 'gerente',
        'ativo': True
    }
}

# Dados de hóspedes (simulando banco de dados)
HOSPEDES = {}
HOSPEDES_ID_COUNTER = [1]  # Contador em lista para ser mutável

# Logs (simulando banco de dados)
LOGS = []

# ==================== FUNÇÕES AUXILIARES ====================

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def gerar_protocolo():
    """Gera número de protocolo único para o check-in."""
    return f"CHK-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"


def gerar_qrcode(protocolo, hospede_id):
    """Gera QR Code para o check-in confirmado."""
    try:
        qr_data = f"CHECKIN:{protocolo}:{hospede_id}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#1E3A5F", back_color="#FFFFFF")
        
        # Salvar em arquivo
        filename = f"qrcode_{hospede_id}_{datetime.now().timestamp()}.png"
        filepath = os.path.join(app.config['QRCODE_FOLDER'], filename)
        img.save(filepath)
        
        return f"uploads/qrcodes/{filename}"
    except Exception as e:
        print(f"Erro ao gerar QR Code: {e}")
        return None


def registrar_log(acao, descricao=None, usuario_id=None, hospede_id=None):
    """Registra ações no sistema para auditoria."""
    try:
        log = {
            'usuario_id': usuario_id,
            'hospede_id': hospede_id,
            'acao': acao,
            'descricao': descricao,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'criado_em': datetime.utcnow().isoformat()
        }
        LOGS.append(log)
    except Exception as e:
        print(f"Erro ao registrar log: {e}")


def obter_usuario_por_email(email):
    """Obtém usuário pelo email."""
    return USUARIOS.get(email)


def obter_hospede_por_id(hospede_id):
    """Obtém hóspede pelo ID."""
    return HOSPEDES.get(hospede_id)


def obter_hospede_por_protocolo(protocolo):
    """Obtém hóspede pelo protocolo."""
    for hospede in HOSPEDES.values():
        if hospede.get('protocolo') == protocolo:
            return hospede
    return None


def obter_hospede_por_cpf(cpf):
    """Obtém hóspede pelo CPF."""
    for hospede in HOSPEDES.values():
        if hospede.get('cpf') == cpf:
            return hospede
    return None


def obter_hospede_por_reserva(numero_reserva):
    """Obtém hóspede pelo número de reserva."""
    for hospede in HOSPEDES.values():
        if hospede.get('numero_reserva') == numero_reserva:
            return hospede
    return None


# ==================== ROTAS PÚBLICAS ====================

@app.route('/')
def index():
    """Página inicial do sistema."""
    return render_template('index.html')


@app.route('/pre-checkin/<token>', methods=['GET', 'POST'])
def pre_checkin(token):
    """Página de pré-check-in para hóspedes."""
    from forms import PreCheckinForm
    
    form = PreCheckinForm()
    
    if form.validate_on_submit():
        try:
            # Processar upload de documento
            documento_path = None
            if form.documento.data:
                file = form.documento.data
                if allowed_file(file.filename):
                    filename = secure_filename(f"{form.cpf.data}_{datetime.now().timestamp()}_{file.filename}")
                    filepath = os.path.join(app.config['DOCUMENT_FOLDER'], filename)
                    file.save(filepath)
                    documento_path = f"uploads/documents/{filename}"
            
            # Processar assinatura (Base64 para arquivo)
            assinatura_path = None
            if form.assinatura_base64.data:
                try:
                    assinatura_data = form.assinatura_base64.data.split(',')[1]
                    assinatura_bytes = base64.b64decode(assinatura_data)
                    filename = secure_filename(f"assinatura_{form.cpf.data}_{datetime.now().timestamp()}.png")
                    filepath = os.path.join(app.config['SIGNATURE_FOLDER'], filename)
                    with open(filepath, 'wb') as f:
                        f.write(assinatura_bytes)
                    assinatura_path = f"uploads/signatures/{filename}"
                except Exception as e:
                    print(f"Erro ao salvar assinatura: {e}")
            
            # Gerar protocolo
            protocolo = gerar_protocolo()
            
            # Gerar ID para hóspede
            hospede_id = HOSPEDES_ID_COUNTER[0]
            HOSPEDES_ID_COUNTER[0] += 1
            
            # Criar registro do hóspede em memória
            hospede = {
                'id': hospede_id,
                'numero_reserva': form.numero_reserva.data,
                'nome_completo': form.nome_completo.data,
                'cpf': form.cpf.data,
                'data_nascimento': form.data_nascimento.data.isoformat(),
                'email': form.email.data,
                'telefone': form.telefone.data,
                'nacionalidade': form.nacionalidade.data,
                'endereco': form.endereco.data,
                'cidade': form.cidade.data,
                'estado': form.estado.data,
                'cep': form.cep.data,
                'data_entrada': form.data_entrada.data.isoformat(),
                'data_saida': form.data_saida.data.isoformat(),
                'quantidade_hospedes': form.quantidade_hospedes.data,
                'observacoes': form.observacoes.data,
                'tipo_documento': form.tipo_documento.data,
                'numero_documento': form.numero_documento.data,
                'documento_path': documento_path,
                'assinatura_path': assinatura_path,
                'status': 'concluido',
                'protocolo': protocolo,
                'concluido_em': datetime.utcnow().isoformat(),
                'confirmado_em': None,
                'ip_origem': request.remote_addr,
                'user_agent': request.headers.get('User-Agent'),
                'criado_em': datetime.utcnow().isoformat()
            }
            
            # Adicionar hóspede aos dados
            HOSPEDES[hospede_id] = hospede
            
            # Gerar QR Code
            qrcode_path = gerar_qrcode(protocolo, hospede_id)
            hospede['qrcode_path'] = qrcode_path
            
            registrar_log('PRE_CHECKIN_CONCLUIDO', f'Pré-check-in de {form.nome_completo.data}', hospede_id=hospede_id)
            
            flash('✓ Pré-check-in realizado com sucesso!', 'success')
            return redirect(url_for('confirmacao', protocolo=protocolo))
            
        except Exception as e:
            print(f"Erro ao processar pré-check-in: {e}")
            flash('✗ Erro ao processar seu pré-check-in. Tente novamente.', 'danger')
            registrar_log('PRE_CHECKIN_ERRO', str(e))
    
    return render_template('pre_checkin.html', form=form, token=token)


@app.route('/confirmacao/<protocolo>')
def confirmacao(protocolo):
    """Tela de confirmação após pré-check-in."""
    hospede = obter_hospede_por_protocolo(protocolo)
    
    if not hospede:
        flash('✗ Protocolo não encontrado.', 'danger')
        return redirect(url_for('index'))
    
    return render_template('confirmacao.html', hospede=hospede, protocolo=protocolo)


# ==================== ROTAS ADMINISTRATIVAS ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Login para acesso administrativo."""
    from forms import LoginForm
    
    form = LoginForm()
    
    if form.validate_on_submit():
        usuario = obter_usuario_por_email(form.email.data)
        
        if usuario and check_password_hash(usuario['senha'], form.senha.data) and usuario['ativo']:
            session['usuario_id'] = usuario['id']
            session['usuario_nome'] = usuario['nome']
            flash(f'✓ Bem-vindo, {usuario["nome"]}!', 'success')
            registrar_log('LOGIN_ADMIN', f'Login de {usuario["nome"]}', usuario_id=usuario['id'])
            return redirect(url_for('admin_dashboard'))
        else:
            flash('✗ Email ou senha inválidos.', 'danger')
            registrar_log('LOGIN_FALHO', form.email.data)
    
    return render_template('login.html', form=form)


@app.route('/admin/logout')
def admin_logout():
    """Logout administrativo."""
    usuario_id = session.get('usuario_id')
    usuario_nome = session.get('usuario_nome')
    session.clear()
    registrar_log('LOGOUT_ADMIN', f'Logout de {usuario_nome}', usuario_id=usuario_id)
    flash('✓ Você foi desconectado.', 'info')
    return redirect(url_for('index'))


def login_required(f):
    """Decorator para proteger rotas administrativas."""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            flash('✗ Você precisa fazer login primeiro.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Painel administrativo principal."""
    # Estatísticas
    total_checkins = len(HOSPEDES)
    checkins_concluidos = len([h for h in HOSPEDES.values() if h['status'] == 'concluido'])
    checkins_pendentes = len([h for h in HOSPEDES.values() if h['status'] == 'pendente'])
    
    # Hóspedes chegando hoje
    hoje = datetime.utcnow().date()
    hospedes_hoje = [h for h in HOSPEDES.values() 
                    if h.get('data_entrada') and 
                    datetime.fromisoformat(h['data_entrada']).date() == hoje and 
                    h['status'] == 'concluido']
    
    # Próximas chegadas (próximos 7 dias)
    proximas_sete_dias = []
    for h in HOSPEDES.values():
        if h.get('data_entrada'):
            data_entrada = datetime.fromisoformat(h['data_entrada']).date()
            if hoje <= data_entrada <= hoje + timedelta(days=7):
                proximas_sete_dias.append(h)
    
    proximas_sete_dias = sorted(proximas_sete_dias, 
                                key=lambda x: x['data_entrada'])[:10]
    
    context = {
        'total_checkins': total_checkins,
        'checkins_concluidos': checkins_concluidos,
        'checkins_pendentes': checkins_pendentes,
        'hospedes_hoje': hospedes_hoje,
        'proximas_chegadas': proximas_sete_dias
    }
    
    return render_template('dashboard.html', **context)


@app.route('/admin/hospedes')
@login_required
def admin_hospedes():
    """Lista e busca de hóspedes cadastrados."""
    from forms import PesquisaHospedeForm
    
    form = PesquisaHospedeForm()
    hospedes = list(HOSPEDES.values())
    
    if request.method == 'GET':
        busca = request.args.get('busca')
        if busca:
            hospedes = [h for h in hospedes 
                       if busca.lower() in h['nome_completo'].lower() or 
                       busca.lower() in h['numero_reserva'].lower()]
        
        status = request.args.get('status')
        if status:
            hospedes = [h for h in hospedes if h['status'] == status]
        
        data_entrada = request.args.get('data_entrada')
        if data_entrada:
            hospedes = [h for h in hospedes if h.get('data_entrada') == data_entrada]
        
        # Ordenar por data de criação (mais recentes primeiro)
        hospedes = sorted(hospedes, key=lambda x: x['criado_em'], reverse=True)
    
    return render_template('hospedes.html', hospedes=hospedes, form=form)


@app.route('/admin/hospede/<int:hospede_id>')
@login_required
def admin_detalhes_hospede(hospede_id):
    """Detalhes completos de um hóspede."""
    hospede = obter_hospede_por_id(hospede_id)
    
    if not hospede:
        flash('✗ Hóspede não encontrado.', 'danger')
        return redirect(url_for('admin_hospedes'))
    
    return render_template('detalhes_hospede.html', hospede=hospede)


@app.route('/admin/hospede/<int:hospede_id>/confirmar', methods=['POST'])
@login_required
def confirmar_chegada(hospede_id):
    """Confirma a chegada de um hóspede."""
    hospede = obter_hospede_por_id(hospede_id)
    
    if not hospede:
        flash('✗ Hóspede não encontrado.', 'danger')
        return redirect(url_for('admin_hospedes'))
    
    if hospede['status'] == 'concluido':
        hospede['confirmado_em'] = datetime.utcnow().isoformat()
        
        usuario_id = session.get('usuario_id')
        registrar_log('CHEGADA_CONFIRMADA', f'Chegada de {hospede["nome_completo"]}', 
                     usuario_id=usuario_id, hospede_id=hospede_id)
        
        flash(f'✓ Chegada de {hospede["nome_completo"]} confirmada!', 'success')
    else:
        flash('✗ Apenas check-ins concluídos podem ser confirmados.', 'warning')
    
    return redirect(url_for('admin_detalhes_hospede', hospede_id=hospede_id))


# ==================== ROTAS DE API ====================

@app.route('/api/validar-cpf/<cpf>')
def api_validar_cpf(cpf):
    """API para validar CPF único."""
    hospede_existente = obter_hospede_por_cpf(cpf)
    return jsonify({'disponivel': hospede_existente is None})


@app.route('/api/validar-reserva/<numero_reserva>')
def api_validar_reserva(numero_reserva):
    """API para validar número de reserva."""
    reserva_existente = obter_hospede_por_reserva(numero_reserva)
    return jsonify({'disponivel': reserva_existente is None})


# ==================== PÁGINAS DE ERRO ====================

@app.errorhandler(404)
def nao_encontrado(error):
    """Página 404."""
    return render_template('erro.html', codigo=404, mensagem='Página não encontrada'), 404


@app.errorhandler(500)
def erro_servidor(error):
    """Página 500."""
    return render_template('erro.html', codigo=500, mensagem='Erro interno do servidor'), 500


@app.errorhandler(403)
def acesso_negado(error):
    """Página 403."""
    return render_template('erro.html', codigo=403, mensagem='Acesso negado'), 403


# ==================== CONTEXTO TEMPLATE ====================

@app.context_processor
def inject_user():
    """Injeta informações do usuário nos templates."""
    usuario_id = session.get('usuario_id')
    usuario_nome = session.get('usuario_nome')
    return dict(usuario_logado=usuario_id is not None, usuario_nome=usuario_nome)


if __name__ == '__main__':
    print("=" * 60)
    print("✓ Sistema de Pré-Check-in Hoteleiro")
    print("✓ Modo: SEM BANCO DE DADOS (Em Memória)")
    print("✓ Admin: admin@hotel.com / admin123")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
