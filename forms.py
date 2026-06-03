"""
Formulários WTForms para validação de dados do pré-check-in.
Implementa validações do lado do servidor para segurança e integridade.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError, Optional
from wtforms.fields import FileField
from flask_wtf.file import FileAllowed
from models import Hospede
import re


class LoginForm(FlaskForm):
    """Formulário para login administrativo."""
    email = StringField(
        'Email',
        validators=[
            DataRequired(message='Email é obrigatório'),
            Email(message='Email inválido')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'seu.email@hotel.com'
        }
    )
    
    senha = PasswordField(
        'Senha',
        validators=[
            DataRequired(message='Senha é obrigatória'),
            Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': '••••••••'
        }
    )
    
    submit = SubmitField(
        'Entrar',
        render_kw={'class': 'btn btn-primary w-100 py-2'}
    )


class PreCheckinForm(FlaskForm):
    """Formulário principal de pré-check-in para hóspedes."""
    
    # Dados pessoais
    nome_completo = StringField(
        'Nome Completo',
        validators=[
            DataRequired(message='Nome é obrigatório'),
            Length(min=5, max=150, message='Nome deve ter entre 5 e 150 caracteres')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'João da Silva Santos'
        }
    )
    
    cpf = StringField(
        'CPF',
        validators=[
            DataRequired(message='CPF é obrigatório'),
            Regexp(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', message='CPF deve estar no formato: XXX.XXX.XXX-XX')
        ],
        render_kw={
            'class': 'form-control cpf-mask',
            'placeholder': '000.000.000-00',
            'data-mask': '000.000.000-00'
        }
    )
    
    data_nascimento = DateField(
        'Data de Nascimento',
        validators=[DataRequired(message='Data de nascimento é obrigatória')],
        render_kw={
            'class': 'form-control',
            'type': 'date'
        }
    )
    
    email = StringField(
        'E-mail',
        validators=[
            DataRequired(message='Email é obrigatório'),
            Email(message='Email inválido')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'seu.email@exemplo.com'
        }
    )
    
    telefone = StringField(
        'Telefone',
        validators=[
            DataRequired(message='Telefone é obrigatório'),
            Regexp(r'^\(\d{2}\)\s9?\d{4}-\d{4}$', message='Telefone deve estar no formato: (XX) 9XXXX-XXXX')
        ],
        render_kw={
            'class': 'form-control phone-mask',
            'placeholder': '(11) 99999-9999',
            'data-mask': '(00) 00000-0000'
        }
    )
    
    nacionalidade = SelectField(
        'Nacionalidade',
        choices=[('Brasileira', 'Brasileira'), ('Estrangeira', 'Estrangeira')],
        validators=[DataRequired()],
        render_kw={'class': 'form-select'}
    )
    
    # Endereço
    endereco = StringField(
        'Endereço',
        validators=[
            DataRequired(message='Endereço é obrigatório'),
            Length(min=5, max=200, message='Endereço deve ter entre 5 e 200 caracteres')
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Rua das Flores, 123'
        }
    )
    
    cidade = StringField(
        'Cidade',
        validators=[
            DataRequired(message='Cidade é obrigatória'),
            Length(min=2, max=100)
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'São Paulo'
        }
    )
    
    estado = SelectField(
        'Estado',
        choices=[
            ('', 'Selecione...'),
            ('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'),
            ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'),
            ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')
        ],
        validators=[DataRequired(message='Estado é obrigatório')],
        render_kw={'class': 'form-select'}
    )
    
    cep = StringField(
        'CEP',
        validators=[
            Optional(),
            Regexp(r'^\d{5}-\d{3}$', message='CEP deve estar no formato: XXXXX-XXX')
        ],
        render_kw={
            'class': 'form-control cep-mask',
            'placeholder': '01234-567'
        }
    )
    
    # Dados da reserva
    numero_reserva = StringField(
        'Número da Reserva',
        validators=[
            DataRequired(message='Número da reserva é obrigatório'),
            Length(min=3, max=50)
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'HOTEL-2024-123456'
        }
    )
    
    data_entrada = DateField(
        'Data de Entrada',
        validators=[DataRequired(message='Data de entrada é obrigatória')],
        render_kw={
            'class': 'form-control',
            'type': 'date'
        }
    )
    
    data_saida = DateField(
        'Data de Saída',
        validators=[DataRequired(message='Data de saída é obrigatória')],
        render_kw={
            'class': 'form-control',
            'type': 'date'
        }
    )
    
    quantidade_hospedes = IntegerField(
        'Quantidade de Hóspedes',
        validators=[
            DataRequired(message='Quantidade de hóspedes é obrigatória'),
        ],
        default=1,
        render_kw={
            'class': 'form-control',
            'min': '1',
            'max': '10'
        }
    )
    
    observacoes = TextAreaField(
        'Observações Especiais',
        validators=[Optional(), Length(max=500)],
        render_kw={
            'class': 'form-control',
            'rows': '3',
            'placeholder': 'Alergias, restrições, solicitações especiais...'
        }
    )
    
    # Documentação
    tipo_documento = SelectField(
        'Tipo de Documento',
        choices=[('RG', 'RG'), ('Passaporte', 'Passaporte')],
        validators=[DataRequired()],
        render_kw={'class': 'form-select'}
    )
    
    numero_documento = StringField(
        'Número do Documento',
        validators=[
            DataRequired(message='Número do documento é obrigatório'),
            Length(min=3, max=50)
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Digite o número do seu documento'
        }
    )
    
    documento = FileField(
        'Enviar Cópia (RG/Passaporte)',
        validators=[
            DataRequired(message='É obrigatório enviar cópia do documento'),
            FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], message='Apenas PDF, JPG ou PNG permitidos')
        ],
        render_kw={'class': 'form-control'}
    )
    
    # Assinatura será capturada via JavaScript, não precisa validação aqui
    assinatura_base64 = StringField(
        'Assinatura',
        validators=[DataRequired(message='Assinatura é obrigatória')]
    )
    
    termos_aceitos = StringField(
        'Termos Aceitos',
        validators=[DataRequired(message='Você deve aceitar os termos')]
    )
    
    submit = SubmitField(
        'Concluir Pré-Check-in',
        render_kw={'class': 'btn btn-success w-100 py-2'}
    )
    
    def validate_data_saida(self, field):
        """Validação customizada: data de saída deve ser após data de entrada."""
        if self.data_entrada.data >= field.data:
            raise ValidationError('Data de saída deve ser após a data de entrada')
    
    def validate_cpf(self, field):
        """Validação customizada: CPF deve ser único e válido."""
        cpf = field.data.replace('.', '').replace('-', '')
        
        # Validação básica de CPF
        if len(cpf) != 11 or not cpf.isdigit():
            raise ValidationError('CPF inválido')
        
        # Verificar se CPF já existe
        hospede_existente = Hospede.query.filter_by(cpf=field.data).first()
        if hospede_existente:
            raise ValidationError('Este CPF já foi cadastrado no sistema')
    
    def validate_numero_reserva(self, field):
        """Validação customizada: número de reserva deve ser único."""
        reserva_existente = Hospede.query.filter_by(numero_reserva=field.data).first()
        if reserva_existente and reserva_existente.status != 'cancelado':
            raise ValidationError('Número de reserva já cadastrado')


class PesquisaHospedeForm(FlaskForm):
    """Formulário para pesquisa de hóspedes no painel administrativo."""
    busca = StringField(
        'Buscar por Nome ou Reserva',
        validators=[Optional(), Length(min=2)],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Digite nome ou número da reserva...'
        }
    )
    
    status = SelectField(
        'Status',
        choices=[
            ('', 'Todos os status'),
            ('pendente', 'Pendente'),
            ('concluido', 'Concluído'),
            ('cancelado', 'Cancelado')
        ],
        render_kw={'class': 'form-select'}
    )
    
    data_entrada = DateField(
        'Data de Entrada',
        validators=[Optional()],
        render_kw={
            'class': 'form-control',
            'type': 'date'
        }
    )
    
    submit = SubmitField(
        'Pesquisar',
        render_kw={'class': 'btn btn-primary'}
    )
