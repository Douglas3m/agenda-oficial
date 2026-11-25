# 📌 Notas de Lançamento: Agenda Oficial vs 1.1.5

**Data de Lançamento:** 25 de Novembro de 2026  
**Identificador da Tag:** `v1.1.5`  
**Nome do Pacote:** `br.com.agendaoficial.app`  
**Versão do APK:** 1.1.5 (Build 10105)  
**Tamanho do APK:** 3.05 MB  
**Arquivo do APK:** [`Agenda-v1.1.5.apk`](releases/Agenda-v1.1.5.apk)

---

### 🚀 Destaques da Versão 1.1.5

1. **Empacotamento Nativo em APK de Alta Eficiência:**
   - Compilação direta e limpa com Android SDK 34 (Android 14) com retrocompatibilidade até Android 5.0 (Lollipop).
   - Pacote leve de apenas 3.05 MB com carregamento instantâneo.
   - Navegação offline completa sem necessidade de internet: todos os recursos (`index.html`, `tailwind.min.js`, logomarcas, ícones) são interceptados e servidos instantaneamente pelo `AssetManager` da aplicação nativa.
   - Suporte nativo ao seletor de arquivos (`WebChromeClient.onShowFileChooser`) para tirar fotos ou anexar imagens no Patrimônio e importar backups.
   - Gerenciamento inteligente do botão "Voltar" do Android (`onBackPressed`), fechando drawers e modais abertos antes de sair do app.

2. **Módulo de Gestão de Patrimônio Eclesiástico (Livro de Tombo):**
   - Cadastro completo de patrimônio: código de tombo, nome do bem, congregação/sede, departamento responsável, ano de aquisição e quantidade.
   - Anexação de fotos do bem com visualização imediata e armazenamento otimizado em Base64.
   - Incremento e decremento rápido de quantidade (+/-) nos cartões do acervo.
   - Filtros dinâmicos por congregação e departamento com busca instantânea.
   - Título estritamente unificado para "Patrimônio" tanto na interface quanto nas atas e relatórios.

3. **Sistema Analítico de Relatórios A4 com Seletor de Orientação:**
   - Formatação condensada de alta densidade analítica, com um item por linha para conferência e inventário rápido.
   - Padrão **Paisagem (Landscape • 297mm)** para total aproveitamento da largura da folha A4.
   - Seletor dinâmico para alternar entre **Paisagem** e **Retrato (Portrait • 210mm)**.
   - Otimização CSS `@media print` para corte e margens perfeitas na impressão e exportação em PDF.

4. **Central de Backup & Transferência entre Dispositivos:**
   - Exportação completa dos dados da aplicação em formato JSON estruturado (cultos, congregações, categorias, bens tombados com fotos e temas).
   - Compartilhamento direto via folha nativa do Android (WhatsApp, Drive, Email, Bluetooth).
   - Importação via arquivo `.json` ou colagem direta de texto para transferências rápidas entre PC e celular.

5. **Menu Lateral com Paletas Retráteis:**
   - Paletas de cores compactadas em gaveta retrátil no drawer, liberando espaço útil para navegação.

---
*Assinado e verificado digitalmente para distribuição oficial.*
