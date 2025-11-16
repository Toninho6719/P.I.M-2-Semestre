# 🚀 GUIA RÁPIDO - Sistema Acadêmico PIM em Rede LAN

## ⚡ Início Rápido (3 Passos)

### 1️⃣ **Iniciar o Sistema**
```bash
python iniciar.py
```
Um menu interativo será exibido com todas as opções.

---

## 📋 Estrutura de Arquivos Criados

```
PIM/
├── server_proxy.py          # Servidor proxy (máquina servidora)
├── client_proxy.py          # Cliente de rede (biblioteca)
├── config_rede.py           # Configuração de rede
├── iniciar.py               # Menu interativo de inicialização
├── gui_system.py            # Interface gráfica (existente)
├── database.py              # Banco de dados (existente)
├── models.py                # Modelos de dados (existente)
├── README_REDE.md           # Documentação completa
└── COMANDOS_WINDOWS.md      # Comandos úteis do Windows
```

---

## 🎯 Cenários de Uso

### **Cenário 1: Uso Local (Atual - Não precisa mudar nada)**
```bash
python iniciar.py
# Escolha opção 2: Iniciar CLIENTE (Modo Local)
```

### **Cenário 2: Servidor + Cliente na Mesma Máquina (Teste)**

**Terminal 1 (Servidor):**
```bash
python iniciar.py
# Escolha opção 1: Iniciar SERVIDOR PROXY
```

**Terminal 2 (Cliente):**
```bash
python iniciar.py
# Escolha opção 3: Iniciar CLIENTE (Modo Rede)
# IP: localhost (pressione ENTER)
```

### **Cenário 3: Servidor em uma Máquina, Clientes em Outras (Produção)**

**Máquina Servidor (192.168.1.100):**
1. Configurar firewall (executar como Administrador):
   ```powershell
   New-NetFirewallRule -DisplayName "PIM Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
   ```

2. Iniciar servidor:
   ```bash
   python iniciar.py
   # Opção 1: Iniciar SERVIDOR PROXY
   ```

**Máquinas Cliente:**
1. Configurar IP do servidor:
   ```bash
   python iniciar.py
   # Opção 6: Configurar IP do Servidor
   # Digite: 192.168.1.100
   ```

2. Iniciar cliente:
   ```bash
   python iniciar.py
   # Opção 3: Iniciar CLIENTE (Modo Rede)
   ```

---

## 🔧 Configuração do Firewall (Windows)

### Execute como Administrador:

```powershell
# Permitir porta 5000
New-NetFirewallRule -DisplayName "PIM Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

---

## ✅ Testar se Funciona

### 1. Verificar se o servidor está rodando:
```powershell
Test-NetConnection -ComputerName localhost -Port 5000
```

### 2. Usar o script de teste:
```bash
python iniciar.py
# Opção 4: Testar Conexão com Servidor
```

---

## 🌐 Como Descobrir o IP da Máquina

```powershell
ipconfig
```
Procure por **IPv4 Address**, por exemplo: `192.168.1.100`

---

## 📊 Logs do Servidor

Quando o servidor está rodando, você verá logs como:

```
============================================================
🚀 SERVIDOR PROXY - SISTEMA ACADÊMICO PIM
============================================================
📡 Servidor iniciado em: 0.0.0.0:5000
⏰ Data/Hora: 14/11/2025 10:30:45
============================================================
✅ Aguardando conexões de clientes...

✅ [10:35:22] Cliente conectado: 192.168.1.101:54321
   Total de conexões ativas: 1

📨 [10:35:23] 192.168.1.101 -> login
   ✓ Login bem-sucedido: João Silva (ADM)

📨 [10:35:25] 192.168.1.101 -> listar_turmas
```

---

## 🐛 Solução de Problemas Comuns

### ❌ "Não foi possível conectar ao servidor"

**Causas possíveis:**
1. Servidor não está rodando
2. IP incorreto no `config_rede.py`
3. Firewall bloqueando

**Solução:**
```powershell
# 1. Verificar se servidor está rodando
Test-NetConnection -ComputerName IP_DO_SERVIDOR -Port 5000

# 2. Testar ping
ping IP_DO_SERVIDOR

# 3. Verificar firewall
Get-NetFirewallRule -DisplayName "*PIM*"
```

### ❌ "Address already in use"

**Causa:** Já existe outro processo usando a porta 5000

**Solução:**
```powershell
# Ver o processo
netstat -ano | findstr :5000

# Matar o processo (substitua 1234 pelo PID)
Stop-Process -Id 1234 -Force
```

### ❌ "Python não é reconhecido"

**Solução:** Use o caminho completo:
```bash
C:\Users\Assupero\AppData\Local\Programs\Python\Python313\python.exe iniciar.py
```

---

## 🎓 Funcionalidades da Rede

### ✅ O que funciona em rede:
- ✅ Login/Logout
- ✅ Cadastro de usuários, alunos, professores
- ✅ Cadastro de turmas
- ✅ Registro de aulas
- ✅ Registro de atividades
- ✅ Lançamento de notas
- ✅ Registro de chamadas
- ✅ Visualização de dados
- ✅ Múltiplos clientes simultâneos
- ✅ Sessões isoladas por usuário

### 🔒 Segurança:
- Autenticação obrigatória
- Sessões únicas por login
- Validação de permissões
- Professores só acessam suas atividades

---

## 📝 Comparação: Modo Local vs Modo Rede

| Recurso | Modo Local | Modo Rede |
|---------|------------|-----------|
| **Usuários simultâneos** | ❌ Um por vez | ✅ Múltiplos |
| **Centralização** | ❌ Cada máquina tem cópia | ✅ Dados centralizados |
| **Configuração** | ✅ Simples | ⚠️ Requer configuração |
| **Performance** | ✅ Mais rápido | ⚠️ Depende da rede |
| **Backup** | ⚠️ Múltiplos locais | ✅ Um único ponto |
| **Controle** | ❌ Descentralizado | ✅ Monitoramento central |

---

## 💡 Dicas Importantes

1. **Teste localmente primeiro:** Use `localhost` antes de testar na rede
2. **IP estático no servidor:** Evite que o IP mude
3. **Firewall:** Configure corretamente na máquina servidora
4. **Backup regular:** Use o `backup_system.exe` diariamente
5. **Monitore os logs:** Fique de olho no terminal do servidor

---

## 📞 Comandos Essenciais

```powershell
# Ver IP da máquina
ipconfig

# Testar porta
Test-NetConnection -ComputerName IP -Port 5000

# Configurar firewall (como Admin)
New-NetFirewallRule -DisplayName "PIM Server" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow

# Ver processos na porta 5000
netstat -ano | findstr :5000
```

---

## 🎉 Pronto para Usar!

O sistema está completamente configurado. Para começar:

```bash
python iniciar.py
```

Escolha a opção desejada e siga as instruções na tela.

---

**Documentação Completa:** Consulte `README_REDE.md`  
**Comandos Windows:** Consulte `COMANDOS_WINDOWS.md`  

**Versão:** 2.0 - Cliente-Servidor LAN  
**Data:** 14/11/2025
