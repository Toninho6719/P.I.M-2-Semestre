# Sistema Acadêmico PIM - Modo Cliente-Servidor (LAN)

## 📋 Visão Geral

O sistema foi expandido para suportar dois modos de operação:

1. **MODO LOCAL**: Acesso direto aos arquivos .txt (modo atual)
2. **MODO REDE**: Arquitetura cliente-servidor via LAN com servidor proxy

---

## 🏗️ Arquitetura de Rede

```
┌─────────────────────────────────────────────────────────────┐
│                    REDE LOCAL (LAN)                          │
│                                                               │
│  ┌─────────────┐          ┌─────────────────────────┐       │
│  │  Cliente 1  │          │                         │       │
│  │  (GUI)      │◄────────►│   SERVIDOR PROXY        │       │
│  └─────────────┘          │   (server_proxy.py)     │       │
│                           │                         │       │
│  ┌─────────────┐          │   - Gerencia conexões   │       │
│  │  Cliente 2  │◄────────►│   - Valida sessões      │       │
│  │  (GUI)      │          │   - Processa requisições│       │
│  └─────────────┘          │   - Acessa banco dados  │       │
│                           │                         │       │
│  ┌─────────────┐          └────────────┬────────────┘       │
│  │  Cliente N  │◄────────────────────┘                      │
│  │  (GUI)      │                                             │
│  └─────────────┘                                             │
│                                                               │
│                    ┌────────────────────────┐                │
│                    │   ARQUIVOS DE DADOS    │                │
│                    │   - usuarios.txt       │                │
│                    │   - alunos.txt         │                │
│                    │   - professores.txt    │                │
│                    │   - turmas.txt         │                │
│                    │   - aulas.txt          │                │
│                    │   - atividades.txt     │                │
│                    │   - notas.txt          │                │
│                    │   - chamadas.txt       │                │
│                    └────────────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Como Configurar e Usar

### **1. Configurar o Modo de Operação**

Edite o arquivo `config_rede.py`:

```python
# Para usar modo LOCAL (acesso direto aos arquivos)
MODO_REDE = False

# Para usar modo REDE (cliente-servidor)
MODO_REDE = True
SERVER_HOST = '192.168.1.100'  # IP do servidor na rede
SERVER_PORT = 5000
```

---

### **2. Modo LOCAL (Atual)**

Não requer configuração adicional. Execute diretamente:

```bash
python gui_system.py
```

O sistema acessa os arquivos .txt diretamente.

---

### **3. Modo REDE - Configuração do Servidor**

#### **Passo 1: Preparar a máquina servidora**

Na máquina que será o servidor:

1. Certifique-se de que todos os arquivos .txt estão na pasta correta
2. Verifique o IP da máquina:
   ```bash
   ipconfig
   ```
   Anote o IPv4 (ex: 192.168.1.100)

#### **Passo 2: Configurar Firewall**

**Windows Firewall:**

```powershell
# Permitir porta 5000 (execute como Administrador)
New-NetFirewallRule -DisplayName "Sistema Academico PIM" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

#### **Passo 3: Iniciar o servidor**

```bash
python server_proxy.py
```

Você verá algo como:

```
╔════════════════════════════════════════════════════════════╗
║     SERVIDOR PROXY - SISTEMA ACADÊMICO PIM                ║
║            Modelo Cliente-Servidor com Proxy              ║
╚════════════════════════════════════════════════════════════╝

📝 Configuração:
   Host: 0.0.0.0 (todas as interfaces)
   Porta: 5000
   Protocolo: TCP/IP

============================================================
🚀 SERVIDOR PROXY - SISTEMA ACADÊMICO PIM
============================================================
📡 Servidor iniciado em: 0.0.0.0:5000
⏰ Data/Hora: 14/11/2025 10:30:45
============================================================
✅ Aguardando conexões de clientes...
```

---

### **4. Modo REDE - Configuração dos Clientes**

#### **Passo 1: Configurar cada cliente**

Em cada máquina cliente, edite `config_rede.py`:

```python
MODO_REDE = True
SERVER_HOST = '192.168.1.100'  # IP do servidor
SERVER_PORT = 5000
```

#### **Passo 2: Executar a interface**

```bash
python gui_system.py
```

---

## 🧪 Testar a Conexão

Use o script de teste incluído no `client_proxy.py`:

```bash
python client_proxy.py
```

Será solicitado:
- IP do servidor
- Username
- Password

O teste verificará:
- ✅ Conexão com servidor
- ✅ Autenticação
- ✅ Listagem de dados

---

## 📊 Monitoramento do Servidor

O servidor exibe logs em tempo real:

```
✅ [10:35:22] Cliente conectado: 192.168.1.101:54321
   Total de conexões ativas: 1

📨 [10:35:23] 192.168.1.101 -> login
   ✓ Login bem-sucedido: João Silva (ADM)

📨 [10:35:25] 192.168.1.101 -> listar_turmas

🔌 [10:40:15] Cliente desconectado: 192.168.1.101:54321
   Total de conexões ativas: 0
```

---

## 🔒 Segurança

O sistema implementa:

- **Autenticação**: Login obrigatório antes de qualquer operação
- **Sessões**: Cada cliente tem uma sessão única (SHA-256)
- **Validação**: Todas as requisições validam a sessão
- **Isolamento**: Professores só acessam suas próprias atividades

---

## 🛠️ Arquivos do Sistema

### **Servidor**
- `server_proxy.py` - Servidor proxy principal
- `database.py` - Acesso aos arquivos .txt
- `models.py` - Modelos de dados
- Arquivos .txt (usuarios, alunos, etc.)

### **Cliente**
- `gui_system.py` - Interface gráfica
- `client_proxy.py` - Cliente de rede
- `config_rede.py` - Configuração do modo

---

## 🐛 Solução de Problemas

### **Erro: "Não foi possível conectar ao servidor"**

1. Verifique se o servidor está rodando
2. Confirme o IP e porta em `config_rede.py`
3. Verifique o firewall
4. Teste com `ping` do cliente ao servidor

### **Erro: "Sessão inválida ou expirada"**

1. Faça logout e login novamente
2. Reinicie o cliente
3. Se persistir, reinicie o servidor

### **Servidor não aceita conexões**

1. Verifique se já não há outro processo usando a porta 5000:
   ```powershell
   netstat -ano | findstr :5000
   ```
2. Configure firewall corretamente
3. Verifique se `HOST = '0.0.0.0'` no servidor

---

## 📈 Vantagens do Modo REDE

✅ **Centralização**: Dados em um único servidor  
✅ **Concorrência**: Múltiplos usuários simultâneos  
✅ **Controle**: Monitoramento de acessos  
✅ **Segurança**: Autenticação centralizada  
✅ **Backup**: Um único ponto para backup  
✅ **Manutenção**: Atualizações apenas no servidor  

---

## 🔄 Protocolo de Comunicação

### **Formato de Requisição (JSON)**

```json
{
  "action": "login",
  "data": {
    "username": "admin",
    "password": "admin123"
  }
}
```

### **Formato de Resposta (JSON)**

```json
{
  "status": "success",
  "data": {
    "session_id": "abc123...",
    "id_usuario": "1",
    "nome": "Administrador",
    "papel": "ADM"
  }
}
```

---

## 💡 Dicas de Uso

1. **Desenvolvimento**: Use MODO_REDE = False para testes locais
2. **Produção**: Use MODO_REDE = True com servidor dedicado
3. **Backup**: Sempre faça backup dos arquivos .txt do servidor
4. **Performance**: Servidor suporta até 10 conexões simultâneas (configurável)
5. **Segurança**: Mantenha o servidor em rede privada (não expor à internet)

---

## 📞 Suporte

Em caso de dúvidas:

1. Verifique os logs do servidor
2. Use o script de teste (`python client_proxy.py`)
3. Confirme as configurações em `config_rede.py`
4. Teste a conectividade de rede (ping, telnet)

---

## 📝 Comandos Úteis

### **Verificar porta aberta no servidor**
```powershell
netstat -ano | findstr :5000
```

### **Verificar IP da máquina**
```powershell
ipconfig
```

### **Testar conexão de um cliente**
```powershell
Test-NetConnection -ComputerName 192.168.1.100 -Port 5000
```

### **Liberar porta no firewall**
```powershell
New-NetFirewallRule -DisplayName "PIM Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## 🎯 Próximos Passos

Para implementar em produção:

1. Configure o servidor em uma máquina dedicada
2. Configure MODO_REDE = True em todos os clientes
3. Distribua o `config_rede.py` com o IP correto
4. Teste com 2-3 clientes antes de distribuir amplamente
5. Configure backup automático dos arquivos .txt
6. Monitore logs do servidor regularmente

---

**Sistema Acadêmico PIM v2.0 - Modo Cliente-Servidor**  
*Desenvolvido com Python 3 + Tkinter + Socket*
