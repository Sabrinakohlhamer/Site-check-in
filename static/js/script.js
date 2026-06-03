/**
 * Scripts JavaScript para o Sistema de Pré-Check-in Hoteleiro
 * Funcionalidades de interatividade, validação e UI
 */

// ===== MÁSCARAS DE ENTRADA =====

$(document).ready(function() {
    // Máscara de CPF
    if ($('.cpf-mask').length) {
        $('.cpf-mask').mask('000.000.000-00', {
            placeholder: '000.000.000-00'
        });
    }

    // Máscara de Telefone
    if ($('.phone-mask').length) {
        $('.phone-mask').mask('(00) 00000-0000', {
            placeholder: '(00) 00000-0000'
        });
    }

    // Máscara de CEP
    if ($('.cep-mask').length) {
        $('.cep-mask').mask('00000-000', {
            placeholder: '00000-000'
        });
    }
});

// ===== VALIDAÇÕES DE FORMULÁRIO =====

/**
 * Valida CPF localmente
 */
function validarCPF(cpf) {
    // Remove formatação
    cpf = cpf.replace(/\D/g, '');

    // Verifica se tem 11 dígitos
    if (cpf.length !== 11) return false;

    // Verifica se são todos dígitos iguais
    if (/^(\d)\1{10}$/.test(cpf)) return false;

    // Cálculo do primeiro dígito verificador
    let soma = 0;
    let resto;

    for (let i = 1; i <= 9; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (11 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(9, 10))) return false;

    // Cálculo do segundo dígito verificador
    soma = 0;
    for (let i = 1; i <= 10; i++) {
        soma += parseInt(cpf.substring(i - 1, i)) * (12 - i);
    }

    resto = (soma * 10) % 11;
    if (resto === 10 || resto === 11) resto = 0;
    if (resto !== parseInt(cpf.substring(10, 11))) return false;

    return true;
}

/**
 * Valida email
 */
function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Valida data
 */
function validarData(data) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;
    if (!regex.test(data)) return false;
    const date = new Date(data);
    return date instanceof Date && !isNaN(date);
}

// ===== SIGNATURE PAD =====

let signaturePad;

/**
 * Inicializa o Signature Pad quando o DOM está pronto
 */
function initSignaturePad() {
    const canvas = document.getElementById('signaturePad');
    if (!canvas) return;

    signaturePad = new SignaturePad(canvas, {
        backgroundColor: 'rgb(255, 255, 255)',
        penColor: '#1E3A5F',
        minWidth: 1,
        maxWidth: 3
    });

    // Redimensionar canvas
    function resizeCanvas() {
        const ratio = Math.max(window.devicePixelRatio || 1, 1);
        canvas.width = canvas.offsetWidth * ratio;
        canvas.height = canvas.offsetHeight * ratio;
        canvas.getContext('2d').scale(ratio, ratio);
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
}

/**
 * Limpa a assinatura
 */
function limparAssinatura() {
    if (signaturePad) {
        signaturePad.clear();
    }
}

/**
 * Salva a assinatura como Base64
 */
function salvarAssinatura() {
    if (signaturePad && !signaturePad.isEmpty()) {
        return signaturePad.toDataURL('image/png');
    }
    return null;
}

// ===== BUSCA DE PROTOCOLO =====

/**
 * Copia protocolo para a área de transferência
 */
function copiarProtocolo() {
    const protocolo = document.querySelector('[data-protocolo]')?.dataset.protocolo || 
                      document.querySelector('.fw-bold')?.textContent;
    
    if (protocolo) {
        navigator.clipboard.writeText(protocolo).then(() => {
            alert('✓ Protocolo copiado para a área de transferência!');
        }).catch(() => {
            alert('Erro ao copiar o protocolo');
        });
    }
}

/**
 * Acessar check-in com token
 */
function acessarCheckin() {
    const token = document.getElementById('tokenCheckin')?.value;
    
    if (!token || !token.trim()) {
        alert('Por favor, digite o código de acesso');
        return;
    }

    window.location.href = `/pre-checkin/${token.trim()}`;
}

// ===== IMPRESSORA =====

/**
 * Imprime a página
 */
function imprimirConfirmacao() {
    window.print();
}

// ===== VALIDAÇÕES DE FORMULÁRIO AVANZADA =====

/**
 * Valida formulário de check-in antes de enviar
 */
function validarFormularioCheckin() {
    const form = document.getElementById('formCheckin');
    if (!form) return true;

    // Validar CPF
    const cpfInput = form.querySelector('input[name="cpf"]');
    if (cpfInput && !validarCPF(cpfInput.value)) {
        alert('CPF inválido');
        return false;
    }

    // Validar email
    const emailInput = form.querySelector('input[name="email"]');
    if (emailInput && !validarEmail(emailInput.value)) {
        alert('Email inválido');
        return false;
    }

    // Validar assinatura
    if (signaturePad && signaturePad.isEmpty()) {
        alert('Por favor, assine digitalmente antes de enviar');
        return false;
    }

    // Validar termos
    const termos = form.querySelector('input[id="checkTermos"]');
    if (termos && !termos.checked) {
        alert('Você deve aceitar os termos e condições');
        return false;
    }

    // Salvar assinatura
    const assinaturaBase64 = salvarAssinatura();
    if (assinaturaBase64) {
        const assinaturaInput = form.querySelector('input[name="assinatura_base64"]');
        if (assinaturaInput) {
            assinaturaInput.value = assinaturaBase64;
        }
    }

    return true;
}

// ===== ATTACH LISTENERS =====

// Inicializar quando documento carregar
document.addEventListener('DOMContentLoaded', function() {
    initSignaturePad();

    // Validar formulário ao enviar
    const formCheckin = document.getElementById('formCheckin');
    if (formCheckin) {
        formCheckin.addEventListener('submit', function(e) {
            if (!validarFormularioCheckin()) {
                e.preventDefault();
            }
        });
    }
});

// ===== UTILIDADES =====

/**
 * Anima um elemento
 */
function animar(elemento, animacao, duracao = 600) {
    elemento.style.animation = `${animacao} ${duracao}ms ease-in-out`;
    setTimeout(() => {
        elemento.style.animation = '';
    }, duracao);
}

/**
 * Formata data para BR
 */
function formatarDataBR(data) {
    const d = new Date(data);
    const dia = String(d.getDate()).padStart(2, '0');
    const mes = String(d.getMonth() + 1).padStart(2, '0');
    const ano = d.getFullYear();
    return `${dia}/${mes}/${ano}`;
}

/**
 * Formata moeda brasileira
 */
function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(valor);
}
