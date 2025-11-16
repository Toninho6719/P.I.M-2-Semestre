"""
Configuração de Rede para Sistema Acadêmico PIM
Define se o sistema opera em modo LOCAL ou REDE
"""

# ===== CONFIGURAÇÃO DO MODO DE OPERAÇÃO =====

# Defina como True para usar modo REDE (cliente-servidor)
# Defina como False para usar modo LOCAL (acesso direto aos arquivos)
MODO_REDE = False

# ===== CONFIGURAÇÃO DO SERVIDOR (usado apenas se MODO_REDE = True) =====

# Endereço IP do servidor proxy
# Use 'localhost' ou '127.0.0.1' se o servidor estiver na mesma máquina
# Use o IP da máquina servidora na rede LAN (ex: '192.168.1.100')
SERVER_HOST = 'localhost'

# Porta do servidor (padrão: 5000)
SERVER_PORT = 5000

# ===== INFORMAÇÕES =====

def get_mode_info():
    """Retorna informações sobre o modo de operação"""
    if MODO_REDE:
        return {
            'modo': 'REDE',
            'descricao': 'Cliente-Servidor via LAN',
            'servidor': f'{SERVER_HOST}:{SERVER_PORT}',
            'info': 'Conectando ao servidor proxy para acesso aos dados'
        }
    else:
        return {
            'modo': 'LOCAL',
            'descricao': 'Acesso direto aos arquivos',
            'servidor': 'N/A',
            'info': 'Lendo e gravando diretamente nos arquivos .txt'
        }

def print_config():
    """Imprime configuração atual"""
    info = get_mode_info()
    print("=" * 60)
    print("CONFIGURAÇÃO DO SISTEMA ACADÊMICO PIM")
    print("=" * 60)
    print(f"Modo de Operação: {info['modo']}")
    print(f"Descrição: {info['descricao']}")
    print(f"Servidor: {info['servidor']}")
    print(f"Info: {info['info']}")
    print("=" * 60)


if __name__ == "__main__":
    print_config()
