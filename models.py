"""
Modelos de banco de dados para o sistema de pré-check-in hoteleiro.
Usa SQLAlchemy para gerenciar as entidades principais do sistema.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

db = SQLAlchemy()


class Usuario(db.Model):
    """
    Modelo para usuários administrativos (recepcionistas e gerentes).
    Armazena credenciais de acesso ao painel administrativo.
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    senha = db.Column(db.String(255), nullable=False)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(50), default='recepcionista')  # recepcionista, gerente
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Usuario {self.nome}>'


class Hospede(db.Model):
    """
    Modelo para hóspedes que realizam pré-check-in.
    Armazena todos os dados pessoais e de reserva.
    """
    __tablename__ = 'hospedes'
    
    id = db.Column(db.Integer, primary_key=True)
    numero_reserva = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Dados pessoais
    nome_completo = db.Column(db.String(150), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False, index=True)
    data_nascimento = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    telefone = db.Column(db.String(20), nullable=False)
    nacionalidade = db.Column(db.String(50), default='Brasileira')
    
    # Endereço
    endereco = db.Column(db.String(200), nullable=False)
    cidade = db.Column(db.String(100), nullable=False)
    estado = db.Column(db.String(2), nullable=False)
    cep = db.Column(db.String(10), nullable=True)
    
    # Dados da hospedagem
    data_entrada = db.Column(db.Date, nullable=False, index=True)
    data_saida = db.Column(db.Date, nullable=False)
    quantidade_hospedes = db.Column(db.Integer, default=1)
    observacoes = db.Column(db.Text, nullable=True)
    
    # Documentação
    documento_path = db.Column(db.String(255), nullable=True)  # Caminho do RG/Passaporte
    tipo_documento = db.Column(db.String(20), default='RG')  # RG ou Passaporte
    numero_documento = db.Column(db.String(50), nullable=True)
    
    # Assinatura
    assinatura_path = db.Column(db.String(255), nullable=True)  # Caminho da assinatura
    
    # Status do check-in
    status = db.Column(db.String(20), default='pendente')  # pendente, concluido, cancelado
    protocolo = db.Column(db.String(20), unique=True, nullable=True, index=True)
    qrcode_path = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    concluido_em = db.Column(db.DateTime, nullable=True)
    confirmado_em = db.Column(db.DateTime, nullable=True)
    
    # Controle
    ip_origem = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Hospede {self.nome_completo}>'
    
    def get_dias_hospedagem(self):
        """Calcula a quantidade de noites de hospedagem."""
        return (self.data_saida - self.data_entrada).days
    
    def esta_atrasado(self):
        """Verifica se o hóspede está atrasado (data de entrada já passou)."""
        return datetime.utcnow().date() > self.data_entrada


class ConfiguracaoSistema(db.Model):
    """
    Modelo para armazenar configurações globais do sistema.
    Permite customização sem alterar código.
    """
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), unique=True, nullable=False)
    valor = db.Column(db.Text, nullable=True)
    tipo = db.Column(db.String(20), default='string')  # string, boolean, number
    descricao = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Configuracao {self.chave}>'


class LogAcesso(db.Model):
    """
    Modelo para auditoria de acessos ao sistema.
    Registra quem acessou o quê, quando e de onde.
    """
    __tablename__ = 'logs_acesso'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    hospede_id = db.Column(db.Integer, db.ForeignKey('hospedes.id'), nullable=True)
    acao = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    ip_address = db.Column(db.String(50), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<LogAcesso {self.acao} em {self.criado_em}>'


def init_db(app):
    """
    Inicializa o banco de dados e cria as tabelas.
    
    Args:
        app: Instância da aplicação Flask
    """
    with app.app_context():
        db.create_all()
        print("✓ Banco de dados inicializado com sucesso!")
