# 🚀 GUIA RÁPIDO - USO COM AMBIENTE VIRTUAL

## ✅ AMBIENTE VIRTUAL CONFIGURADO!

O sistema agora usa um ambiente virtual Python isolado, sem precisar de permissões especiais.

---

## 📁 ARQUIVOS .BAT CRIADOS (Duplo Clique)

### **INICIAR_AQUI.bat** ⭐ PRINCIPAL
Abre o menu interativo com todas as opções.

**Use este para:**
- Escolher entre modo LOCAL ou REDE
- Configurar o IP do servidor
- Iniciar servidor ou cliente
- Testar conexões

---

### **GUI.bat**
Inicia diretamente a interface gráfica do sistema.

**Use para acesso rápido ao sistema.**

---

### **SERVIDOR.bat**
Inicia o servidor proxy na porta 5000.

**Use na máquina que será o servidor da rede.**

---

### **DIAGNOSTICO.bat**
Executa verificação completa do sistema.

**Use para verificar se está tudo OK.**

---

## 🎯 COMO USAR

### **Para usar normalmente (MODO LOCAL):**

1. **Duplo clique em:** `GUI.bat`
2. Faça login no sistema
3. Use normalmente

**OU**

1. **Duplo clique em:** `INICIAR_AQUI.bat`
2. Escolha opção **2** (Iniciar Cliente - Modo Local)

---

### **Para usar em REDE (múltiplos computadores):**

#### **Na máquina SERVIDOR:**
1. Descubra o IP da máquina (execute `ipconfig` no cmd)
2. **Duplo clique em:** `SERVIDOR.bat`
3. Deixe rodando

#### **Nas máquinas CLIENTE:**
1. **Duplo clique em:** `INICIAR_AQUI.bat`
2. Escolha opção **6** (Configurar IP do Servidor)
3. Digite o IP do servidor (ex: 192.168.1.100)
4. Escolha opção **3** (Iniciar Cliente - Modo Rede)
5. Faça login

---

## 🔧 VERIFICAR SE ESTÁ TUDO OK

**Duplo clique em:** `DIAGNOSTICO.bat`

Deve mostrar:
```
📊 Total: 7/7 verificações passaram
✅ Sistema está pronto para uso!
```

---

## 📋 ESTRUTURA DE ARQUIVOS

```
PIM/
├── venv/                    ← Ambiente virtual Python
├── INICIAR_AQUI.bat         ⭐ Menu principal
├── GUI.bat                  ⭐ Interface gráfica direta
├── SERVIDOR.bat             ⭐ Inicia servidor proxy
├── DIAGNOSTICO.bat          ⭐ Verificação do sistema
├── iniciar.py               (usado pelos .bat)
├── gui_system.py            (interface Tkinter)
├── server_proxy.py          (servidor de rede)
├── database.py              (acesso aos dados)
└── ... (outros arquivos)
```

---

## 💡 DICAS

1. **Sempre use os arquivos .bat** - Eles cuidam do ambiente virtual automaticamente

2. **Para testar:** Execute `DIAGNOSTICO.bat` primeiro

3. **Atalhos:**
   - Modo Local: `GUI.bat`
   - Servidor: `SERVIDOR.bat`
   - Menu completo: `INICIAR_AQUI.bat`

4. **Sem restrições:** O ambiente virtual roda isolado, sem precisar de permissões administrativas

---

## 🎓 O QUE É O AMBIENTE VIRTUAL?

É uma cópia isolada do Python dentro da pasta `venv/`. 

**Vantagens:**
- ✅ Não precisa de permissões de administrador
- ✅ Não afeta o Python do sistema
- ✅ Funciona mesmo em máquinas restritas
- ✅ Portátil (pode copiar a pasta inteira)

---

## 🚨 SOLUÇÃO DE PROBLEMAS

### Erro ao abrir .bat
**Solução:** Clique com botão direito → "Executar como administrador"

### "Python não encontrado"
**Solução:** Use os arquivos .bat - eles encontram o Python automaticamente

### Sistema não inicia
**Solução:** Execute `DIAGNOSTICO.bat` e veja o que está errado

---

## ✅ RESUMO RÁPIDO

**Para usar o sistema:**
```
Duplo clique: GUI.bat
```

**Para verificar se está OK:**
```
Duplo clique: DIAGNOSTICO.bat
```

**Para usar em rede:**
```
Servidor: SERVIDOR.bat
Cliente:  INICIAR_AQUI.bat → Opção 3
```

---

**Sistema Acadêmico PIM v2.0**  
*Com Ambiente Virtual Python*  
*Pronto para uso sem restrições!* ✅
