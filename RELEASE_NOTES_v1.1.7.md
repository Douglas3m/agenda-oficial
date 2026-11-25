# Agenda Oficial v1.1.7 • Crônica Litúrgica & Gestão Patrimonial

Versão oficial com **correção de inicialização, Câmera Nativa sem dependências externas e Spooler A4/PDF do Android**:
1. **🚀 Correção Crítica de Inicialização:**
   - Corrigido fechamento prematuro de bloco de script no código-fonte web embutido no WebView.
   - Removido provider personalizado complexo em favor do **`MediaStore` Nativo Oficial do Android** com `ContentValues` e `content://media/external/images/media/`, eliminando qualquer falha de inicialização em todos os aparelhos Android.
   - Adicionada seção `<queries>` no `AndroidManifest.xml` garantindo visibilidade da câmera e galeria em Android 11, 12, 13 e 14.
2. **📸 Captura Direta de Fotos com a Câmera:**
   - Permissões em tempo de execução (`CAMERA`, `READ_MEDIA_IMAGES`).
   - Opções de **"Tirar Foto (Câmera)"** e **"Galeria / Arquivo"** nos formulários de cadastro e edição de Patrimônio.
   - Compressão de imagem automática em Canvas para alta nitidez e tamanho super leve (~90 KB).
3. **🖨️ Spooler de Impressão A4 & Salvar em PDF:**
   - Integração com `android.print.PrintManager`.
   - Compatível com impressoras físicas e a opção nativa **"Salvar como PDF"** do Android.

### Download do Aplicativo Android (APK)
- **Arquivo:** `Agenda-v1.1.7.apk`
- **Assinatura:** JAR (v1), APK Signature Scheme v2, APK Signature Scheme v3.
- **Tamanho:** ~3.06 MB
