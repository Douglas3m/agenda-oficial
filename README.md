# 📖 Agenda Oficial - Crônica Eclesiástica & Gestão Litúrgica
### Versão 1.1.5 (`Agenda vs 1.1.5`) • PWA Offline-First & APK Android Nativo

![Badge Versão](https://img.shields.io/badge/versão-1.1.5-amber.svg)
![Badge Licença](https://img.shields.io/badge/licença-Proprietária%20Eclesiástica-gold.svg)
![Badge Offline](https://img.shields.io/badge/offline--first-100%25-success.svg)
![Badge Android](https://img.shields.io/badge/Android%20APK-v1.1.5%20(3.05%20MB)-blue.svg)

---

## 📲 Download do Aplicativo Android (APK)

O aplicativo foi empacotado com máxima eficiência, pesando apenas **3.05 MB**, 100% offline-ready e assinado com esquemas v1, v2 e v3 para compatibilidade total do Android 5.0 (Lollipop) ao Android 14 (API 34).

* 📦 **Download Direto do APK:** [`releases/Agenda-v1.1.5.apk`](releases/Agenda-v1.1.5.apk) ou na raiz [`Agenda-v1.1.5.apk`](Agenda-v1.1.5.apk)
* 🔐 **Assinatura:** Assinado com chave SHA-256 e verificado pelo `apksigner`.
* ⚡ **Performance:** WebView acelerada por hardware com interceptação local de assets de latência zero (`https://agenda.local`).

---

## 🏛️ Visão Geral do Sistema

A **Agenda Oficial** é um sistema litúrgico de alta precisão para registro, cronologia e gestão de cultos, eventos solenes, sedes eclesiásticas e acervo patrimonial.

Desenvolvida com uma estética clássica vintage cerimonial (tons preto ônix `#12100e`, café litúrgico `#1a1613` e dourado orvalhado `#d4af37`), unida aos efeitos modernos de **Vidro Líquido (Liquid Glass / Frosted Glass)** e design responsivo universal.

---

## ✨ Principais Funcionalidades

### 1. 📅 Gestão de Cultos & Solenidades
* Cadastro dinâmico de eventos ordinários e solenes com cálculo automático de cronologia litúrgica.
* Sistema de recorrência inteligente (semanal, quinzenal, mensal, etc.).
* Visualização em modo Lista Cronológica, Calendário Mensal e Agenda Diária.
* Busca instantânea por termo, filtro por congregação/sede e status.

### 2. 🏛️ Módulo Completo de Patrimônio (Livro de Tombo)
* Título unificado e minimalista: estritamente **"Patrimônio"** tanto na tela quanto nas atas impressas.
* Registro de bens materiais com código de tombo, número de série, ano de aquisição e quantidade.
* **Upload de Fotos do Bem:** salvamento otimizado em Base64 integrado ao armazenamento do app.
* Controles rápidos: contador de quantidade (+/-) direto nos cartões de acervo.
* Filtros por Sede (Matriz, Filiais), Departamento e ordenação por Ano, Sede ou Nome do Bem.

### 3. 📄 Sistema Analítico de Relatórios Oficiais A4
* Diagramação condensada, item por linha, focada em verificação analítica, auditoria e prestação de contas.
* **Aproveitamento Total da Folha A4:** configurado para **Paisagem (Landscape • 297mm)** por padrão, garantindo que todas as colunas caibam em linha única sem quebras.
* **Seletor de Orientação Dinâmico:** permite alternar entre **Paisagem** e **Retrato (Portrait • 210mm)** com um clique.
* Suporte a impressão via navegador ou geração direta de PDF.

### 4. 🔄 Central de Backup & Transferência entre Dispositivos
* Exportação e importação de dados integrais em arquivo `.json`.
* Inclui: cultos, congregações, categorias, bens tombados (com fotos) e preferências de tema.
* Suporte nativo a envio direto por WhatsApp, Google Drive, E-mail ou Telegram no celular e no computador.
* Opção de colar o código JSON diretamente no aplicativo para transferência imediata sem necessidade de baixar arquivos.

### 5. 🎨 Paletas Cerimoniais Retráteis
* Seletor de cores litúrgicas condensado e retrátil no menu lateral, preservando a elegância e espaço útil da interface.
* Modos Claro, Escuro e Temas Dourados Litúrgicos com persistência em `localStorage`.

---

## 🛠️ Como Executar em Ambiente Local (PC / Servidor)

Basta iniciar qualquer servidor estático HTTP na pasta do projeto:

```bash
# Opção 1: Via script executável do Windows
iniciar_agenda.bat

# Opção 2: Via Python
python -m http.server 8181

# Opção 3: Via Node.js
npx serve -l 8181 .
```

Acesse no seu navegador: `http://localhost:8181`

---

## 📱 Como Recompilar o APK Android

O projeto possui um compilador direto e automatizado em Python que utiliza as ferramentas padrão do Android SDK (`aapt2`, `javac`, `d8`, `zipalign`, `apksigner`):

```bash
python build_apk.py
```

O script:
1. Empacota os arquivos web em `assets/`.
2. Compila os recursos nativos e gera `R.java`.
3. Compila a atividade nativa (`MainActivity.java`).
4. Converte o bytecode para Dalvik (`classes.dex`).
5. Realiza o alinhamento de memória (4 bytes) com `zipalign`.
6. Assina o APK gerado com a chave de produção.
7. Disponibiliza o APK final em `releases/Agenda-v1.1.5.apk` e na raiz.

---

## 🏷️ Histórico de Releases e Tags

* **Tag `v1.1.5`** (`Agenda vs 1.1.5`):
  * Lançamento oficial do APK nativo otimizado (3.05 MB).
  * Adição do módulo de Gestão de Patrimônio com fotos e livro de tombo.
  * Relatórios condensados em A4 Paisagem/Retrato.
  * Central de Backup e Transferência entre Dispositivos.
  * Integração offline com `tailwind.min.js` e interceptor nativo de assets.

---
*Crônica & Agenda Eclesiástica • Desenvolvido para solene uso eclesiástico e litúrgico.*
