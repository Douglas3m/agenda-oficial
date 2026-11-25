import os
import sys
import shutil
import subprocess
import glob

SDK_DIR = r"C:\Users\Casa\AppData\Local\Android\Sdk"
BUILD_TOOLS_DIR = os.path.join(SDK_DIR, "build-tools", "34.0.0")
ANDROID_JAR = os.path.join(SDK_DIR, "platforms", "android-34", "android.jar")

AAPT2 = os.path.join(BUILD_TOOLS_DIR, "aapt2.exe")
D8 = os.path.join(BUILD_TOOLS_DIR, "d8.bat")
ZIPALIGN = os.path.join(BUILD_TOOLS_DIR, "zipalign.exe")
APKSIGNER = os.path.join(BUILD_TOOLS_DIR, "apksigner.bat")

ROOT_DIR = r"D:\agenda_app"
BUILD_DIR = os.path.join(ROOT_DIR, "android_build")
OUTPUT_DIR = os.path.join(ROOT_DIR, "releases")
APK_NAME = "Agenda-v1.1.6.apk"
KEYSTORE = os.path.join(ROOT_DIR, "agenda_release.keystore")
KEYSTORE_PASS = "agenda2026"
KEY_ALIAS = "agenda_key"

def run_cmd(cmd, cwd=None, check=True):
    print(f">> Executing: {' '.join(cmd) if isinstance(cmd, list) else cmd}")
    res = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding='utf-8', errors='replace')
    if res.stdout:
        print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    if check and res.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {res.returncode}")
    return res

def setup_dirs():
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)
    os.makedirs(os.path.join(BUILD_DIR, "res", "values"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "res", "xml"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "res", "mipmap-hdpi"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "res", "mipmap-xhdpi"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "res", "mipmap-xxhdpi"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "res", "mipmap-xxxhdpi"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "src", "br", "com", "agendaoficial", "app"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "gen"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "bin", "classes"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "bin", "dex"), exist_ok=True)
    os.makedirs(os.path.join(BUILD_DIR, "assets"), exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def copy_assets():
    print(">> Copiando assets web para a pasta assets/ do APK...")
    asset_files = [
        "index.html",
        "tailwind.min.js",
        "manifest.json",
        "sw.js",
        "logos_b64.js",
        "favicon.ico",
        "icon-192.png",
        "icon-512.png",
        "icon-transparent-512.png",
        "logo_dark.png",
        "logo_light.png",
        "logo_vazado.png",
        "logo_vazado_gold.png"
    ]
    for af in asset_files:
        src = os.path.join(ROOT_DIR, af)
        if os.path.exists(src):
            dst = os.path.join(BUILD_DIR, "assets", af)
            shutil.copy2(src, dst)
            print(f"   [OK] Copiado {af} ({os.path.getsize(src):,} bytes)")
        else:
            print(f"   [AVISO] {af} não encontrado na raiz.")

    # Copiar ícones de launcher
    icon_src = os.path.join(ROOT_DIR, "icon-192.png")
    for d in ["mipmap-hdpi", "mipmap-xhdpi", "mipmap-xxhdpi", "mipmap-xxxhdpi"]:
        shutil.copy2(icon_src, os.path.join(BUILD_DIR, "res", d, "ic_launcher.png"))

def create_manifest():
    manifest_content = """<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="br.com.agendaoficial.app"
    android:versionCode="10106"
    android:versionName="1.1.6">

    <uses-sdk
        android:minSdkVersion="21"
        android:targetSdkVersion="34" />

    <!-- Conectividade -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <!-- Câmera Nativa para Fotos de Patrimônio e Eventos -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" android:required="false" />
    <uses-feature android:name="android.hardware.camera.autofocus" android:required="false" />

    <!-- Armazenamento & Galeria -->
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" android:maxSdkVersion="29" />
    <uses-permission android:name="android.permission.READ_MEDIA_IMAGES" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher"
        android:supportsRtl="true"
        android:hardwareAccelerated="true"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|screenLayout|keyboardHidden"
            android:windowSoftInputMode="adjustResize">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <!-- Provider Seguro para Compartilhamento de Fotos da Câmera -->
        <provider
            android:name=".AppFileProvider"
            android:authorities="br.com.agendaoficial.app.fileprovider"
            android:exported="false"
            android:grantUriPermissions="true">
            <meta-data
                android:name="android.support.FILE_PROVIDER_PATHS"
                android:resource="@xml/file_paths" />
        </provider>

    </application>
</manifest>
"""
    with open(os.path.join(BUILD_DIR, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)

    strings_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Agenda Oficial</string>
</resources>
"""
    with open(os.path.join(BUILD_DIR, "res", "values", "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_content)

    styles_content = """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="@android:style/Theme.Material.NoActionBar">
        <item name="android:statusBarColor">#1a1613</item>
        <item name="android:navigationBarColor">#12100e</item>
        <item name="android:windowBackground">#12100e</item>
    </style>
</resources>
"""
    with open(os.path.join(BUILD_DIR, "res", "values", "styles.xml"), "w", encoding="utf-8") as f:
        f.write(styles_content)

    file_paths = """<?xml version="1.0" encoding="utf-8"?>
<paths>
    <external-files-path name="my_images" path="." />
    <cache-path name="my_cache" path="." />
</paths>
"""
    with open(os.path.join(BUILD_DIR, "res", "xml", "file_paths.xml"), "w", encoding="utf-8") as f:
        f.write(file_paths)

def create_java_source():
    # 1. AppFileProvider.java (ContentProvider nativo sem dependência externa)
    file_provider_code = """package br.com.agendaoficial.app;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.Cursor;
import android.database.MatrixCursor;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.provider.OpenableColumns;
import java.io.File;
import java.io.FileNotFoundException;

public class AppFileProvider extends ContentProvider {
    public static final String AUTHORITY = "br.com.agendaoficial.app.fileprovider";

    public static Uri getUriForFile(File file) {
        return Uri.parse("content://" + AUTHORITY + "/" + file.getName());
    }

    @Override
    public boolean onCreate() {
        return true;
    }

    @Override
    public ParcelFileDescriptor openFile(Uri uri, String mode) throws FileNotFoundException {
        File cacheDir = getContext() != null ? getContext().getCacheDir() : null;
        if (cacheDir == null) {
            throw new FileNotFoundException("Diretório de cache indisponível");
        }
        File file = new File(cacheDir, uri.getLastPathSegment());
        if (!file.exists()) {
            try {
                file.createNewFile();
            } catch (Exception e) {
                throw new FileNotFoundException("Erro ao criar arquivo: " + e.getMessage());
            }
        }
        int modeFlag = ParcelFileDescriptor.MODE_READ_WRITE;
        if ("r".equals(mode)) {
            modeFlag = ParcelFileDescriptor.MODE_READ_ONLY;
        }
        return ParcelFileDescriptor.open(file, modeFlag);
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        File cacheDir = getContext() != null ? getContext().getCacheDir() : null;
        if (cacheDir == null) return null;
        File file = new File(cacheDir, uri.getLastPathSegment());
        MatrixCursor cursor = new MatrixCursor(new String[]{OpenableColumns.DISPLAY_NAME, OpenableColumns.SIZE});
        cursor.addRow(new Object[]{file.getName(), file.length()});
        return cursor;
    }

    @Override
    public String getType(Uri uri) {
        String name = uri.getLastPathSegment();
        if (name != null && name.toLowerCase().endsWith(".png")) {
            return "image/png";
        }
        if (name != null && name.toLowerCase().endsWith(".pdf")) {
            return "application/pdf";
        }
        return "image/jpeg";
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) { return null; }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        File cacheDir = getContext() != null ? getContext().getCacheDir() : null;
        if (cacheDir == null) return 0;
        File file = new File(cacheDir, uri.getLastPathSegment());
        if (file.exists()) {
            return file.delete() ? 1 : 0;
        }
        return 0;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) { return 0; }
}
"""
    with open(os.path.join(BUILD_DIR, "src", "br", "com", "agendaoficial", "app", "AppFileProvider.java"), "w", encoding="utf-8") as f:
        f.write(file_provider_code)

    # 2. MainActivity.java (WebView com Câmera, Seletor Chooser e PrintManager A4 / PDF)
    java_content = """package br.com.agendaoficial.app;

import android.app.Activity;
import android.os.Bundle;
import android.os.Build;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.ConsoleMessage;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.JavascriptInterface;
import android.net.Uri;
import android.content.Intent;
import android.content.Context;
import android.content.pm.PackageManager;
import android.provider.MediaStore;
import android.print.PrintManager;
import android.print.PrintDocumentAdapter;
import android.print.PrintAttributes;
import android.graphics.Color;
import android.widget.Toast;
import android.Manifest;
import java.io.InputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.util.HashMap;
import java.util.Map;

public class MainActivity extends Activity {
    private WebView mWebView;
    private ValueCallback<Uri[]> mFilePathCallback;
    private Uri mCameraPhotoUri;
    private final static int FILECHOOSER_RESULTCODE = 101;
    private final static int CAMERA_PERMISSION_CODE = 202;

    private static final Map<String, String> MIME_TYPES = new HashMap<String, String>() {{
        put("html", "text/html");
        put("htm", "text/html");
        put("js", "application/javascript");
        put("css", "text/css");
        put("json", "application/json");
        put("png", "image/png");
        put("jpg", "image/jpeg");
        put("jpeg", "image/jpeg");
        put("ico", "image/x-icon");
        put("svg", "image/svg+xml");
        put("woff", "font/woff");
        put("woff2", "font/woff2");
        put("ttf", "font/ttf");
    }};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Status bar & Navigation bar styling
        Window window = getWindow();
        window.clearFlags(WindowManager.LayoutParams.FLAG_TRANSLUCENT_STATUS);
        window.addFlags(WindowManager.LayoutParams.FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS);
        window.setStatusBarColor(Color.parseColor("#1a1613"));
        window.setNavigationBarColor(Color.parseColor("#12100e"));

        mWebView = new WebView(this);
        mWebView.setBackgroundColor(Color.parseColor("#12100e"));
        setContentView(mWebView);

        WebSettings settings = mWebView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setAllowFileAccess(true);
        settings.setAllowContentAccess(true);
        settings.setAllowFileAccessFromFileURLs(true);
        settings.setAllowUniversalAccessFromFileURLs(true);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(true);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setSupportZoom(true);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        // WebApp Bridge para câmera, impressão nativa, backup e compartilhamento
        mWebView.addJavascriptInterface(new WebAppInterface(), "AndroidBridge");

        // WebChromeClient avançado com suporte a Câmera + Galeria
        mWebView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView webView, ValueCallback<Uri[]> filePathCallback,
                                             FileChooserParams fileChooserParams) {
                if (mFilePathCallback != null) {
                    mFilePathCallback.onReceiveValue(null);
                    mFilePathCallback = null;
                }
                mFilePathCallback = filePathCallback;

                // Solicita permissão de câmera se necessário em tempo de execução
                checkAndRequestCameraPermission();

                boolean isCaptureExplicit = false;
                if (fileChooserParams != null && fileChooserParams.isCaptureEnabled()) {
                    isCaptureExplicit = true;
                }

                // 1. Prepara Intent da Câmera Nativa do Android
                Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
                try {
                    File photoFile = new File(getCacheDir(), "foto_patrimonio_" + System.currentTimeMillis() + ".jpg");
                    mCameraPhotoUri = AppFileProvider.getUriForFile(photoFile);
                    takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, mCameraPhotoUri);
                    takePictureIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
                } catch (Exception e) {
                    mCameraPhotoUri = null;
                }

                // Se capture="camera" foi especificado no HTML, abre direto a câmera
                if (isCaptureExplicit && mCameraPhotoUri != null && takePictureIntent.resolveActivity(getPackageManager()) != null) {
                    try {
                        startActivityForResult(takePictureIntent, FILECHOOSER_RESULTCODE);
                        return true;
                    } catch (Exception e) {}
                }

                // 2. Prepara Intent de Seleção de Galeria / Documentos
                Intent contentSelectionIntent = new Intent(Intent.ACTION_GET_CONTENT);
                contentSelectionIntent.addCategory(Intent.CATEGORY_OPENABLE);
                String mimeType = "image/*";
                if (fileChooserParams != null && fileChooserParams.getAcceptTypes() != null && fileChooserParams.getAcceptTypes().length > 0 && !fileChooserParams.getAcceptTypes()[0].isEmpty()) {
                    mimeType = fileChooserParams.getAcceptTypes()[0];
                }
                contentSelectionIntent.setType(mimeType);

                // 3. Monta o Seletor Unificado (Tirar Foto com a Câmera OU Escolher da Galeria)
                Intent chooserIntent = new Intent(Intent.ACTION_CHOOSER);
                chooserIntent.putExtra(Intent.EXTRA_INTENT, contentSelectionIntent);
                chooserIntent.putExtra(Intent.EXTRA_TITLE, "Capturar com Câmera ou Selecionar Foto");

                if (mCameraPhotoUri != null && takePictureIntent.resolveActivity(getPackageManager()) != null) {
                    chooserIntent.putExtra(Intent.EXTRA_INITIAL_INTENTS, new Intent[]{takePictureIntent});
                }

                try {
                    startActivityForResult(chooserIntent, FILECHOOSER_RESULTCODE);
                    return true;
                } catch (Exception e) {
                    if (mFilePathCallback != null) {
                        mFilePathCallback.onReceiveValue(null);
                        mFilePathCallback = null;
                    }
                    return false;
                }
            }

            @Override
            public boolean onConsoleMessage(ConsoleMessage consoleMessage) {
                return super.onConsoleMessage(consoleMessage);
            }
        });

        mWebView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String scheme = uri.getScheme();
                if ("tel".equals(scheme) || "mailto".equals(scheme) || "whatsapp".equals(scheme)) {
                    try {
                        Intent intent = new Intent(Intent.ACTION_VIEW, uri);
                        startActivity(intent);
                        return true;
                    } catch (Exception e) {
                        return false;
                    }
                }
                return false;
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                Uri uri = request.getUrl();
                String host = uri.getHost();
                if ("agenda.local".equals(host) || "localhost".equals(host)) {
                    String path = uri.getPath();
                    if (path == null || path.equals("/") || path.isEmpty()) {
                        path = "/index.html";
                    }
                    if (path.startsWith("/")) {
                        path = path.substring(1);
                    }

                    try {
                        InputStream is = getAssets().open(path);
                        String ext = "";
                        int lastDot = path.lastIndexOf('.');
                        if (lastDot > 0) {
                            ext = path.substring(lastDot + 1).toLowerCase();
                        }
                        String mimeType = MIME_TYPES.containsKey(ext) ? MIME_TYPES.get(ext) : "application/octet-stream";
                        Map<String, String> headers = new HashMap<>();
                        headers.put("Access-Control-Allow-Origin", "*");
                        headers.put("Cache-Control", "no-cache");
                        return new WebResourceResponse(mimeType, "UTF-8", 200, "OK", headers, is);
                    } catch (Exception e) {
                        // fallback to default
                    }
                }
                return super.shouldInterceptRequest(view, request);
            }
        });

        // Inicia a aplicação usando domínio seguro com assets interceptados localmente
        mWebView.loadUrl("https://agenda.local/index.html");
    }

    private void checkAndRequestCameraPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{Manifest.permission.CAMERA}, CAMERA_PERMISSION_CODE);
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        if (requestCode == CAMERA_PERMISSION_CODE) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permissão de câmera concedida!", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Permissão de câmera necessária para capturar fotos do acervo.", Toast.LENGTH_LONG).show();
            }
        }
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == FILECHOOSER_RESULTCODE) {
            if (mFilePathCallback != null) {
                Uri[] results = null;
                if (resultCode == Activity.RESULT_OK) {
                    // 1. Caso a foto tenha sido tirada pela CÂMERA
                    if (data == null || data.getData() == null) {
                        if (mCameraPhotoUri != null) {
                            File photoFile = new File(getCacheDir(), mCameraPhotoUri.getLastPathSegment());
                            if (photoFile.exists() && photoFile.length() > 0) {
                                results = new Uri[]{mCameraPhotoUri};
                            }
                        }
                    } else {
                        // 2. Caso a foto venha da GALERIA ou gerenciador de arquivos
                        if (data.getData() != null) {
                            results = new Uri[]{data.getData()};
                        } else if (data.getClipData() != null) {
                            int count = data.getClipData().getItemCount();
                            results = new Uri[count];
                            for (int i = 0; i < count; i++) {
                                results[i] = data.getClipData().getItemAt(i).getUri();
                            }
                        }
                    }
                }
                mFilePathCallback.onReceiveValue(results);
                mFilePathCallback = null;
            }
        }
        super.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    public void onBackPressed() {
        if (mWebView != null) {
            mWebView.evaluateJavascript(
                "(function() { if (typeof window.handleAndroidBack === 'function') { return window.handleAndroidBack(); } return false; })()",
                new ValueCallback<String>() {
                    @Override
                    public void onReceiveValue(String value) {
                        if (!"true".equals(value)) {
                            if (mWebView.canGoBack()) {
                                mWebView.goBack();
                            } else {
                                MainActivity.super.onBackPressed();
                            }
                        }
                    }
                }
            );
        } else {
            super.onBackPressed();
        }
    }

    public class WebAppInterface {
        @JavascriptInterface
        public void showToast(final String message) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(MainActivity.this, message, Toast.LENGTH_SHORT).show();
                }
            });
        }

        @JavascriptInterface
        public String getAppVersion() {
            return "1.1.6";
        }

        @JavascriptInterface
        public void requestCamera() {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    checkAndRequestCameraPermission();
                }
            });
        }

        @JavascriptInterface
        public void printDocument(final String documentName) {
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    try {
                        PrintManager printManager = (PrintManager) getSystemService(Context.PRINT_SERVICE);
                        String jobName = (documentName != null && !documentName.trim().isEmpty())
                                ? documentName.trim()
                                : "Relatorio_Agenda_Oficial_A4";

                        PrintDocumentAdapter printAdapter = mWebView.createPrintDocumentAdapter(jobName);
                        PrintAttributes.Builder builder = new PrintAttributes.Builder();
                        builder.setMediaSize(PrintAttributes.MediaSize.ISO_A4);
                        builder.setColorMode(PrintAttributes.COLOR_MODE_COLOR);

                        printManager.print(jobName, printAdapter, builder.build());
                    } catch (Exception e) {
                        Toast.makeText(MainActivity.this, "Erro ao abrir spooler de impressão/PDF: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                }
            });
        }

        @JavascriptInterface
        public void shareBackup(final String jsonContent, final String fileName) {
            try {
                Intent sendIntent = new Intent();
                sendIntent.setAction(Intent.ACTION_SEND);
                sendIntent.putExtra(Intent.EXTRA_TEXT, jsonContent);
                sendIntent.putExtra(Intent.EXTRA_SUBJECT, fileName);
                sendIntent.setType("text/plain");
                startActivity(Intent.createChooser(sendIntent, "Exportar / Compartilhar Backup"));
            } catch (final Exception e) {
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        Toast.makeText(MainActivity.this, "Erro ao compartilhar: " + e.getMessage(), Toast.LENGTH_SHORT).show();
                    }
                });
            }
        }
    }
}
"""
    with open(os.path.join(BUILD_DIR, "src", "br", "com", "agendaoficial", "app", "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write(java_content)

def build_apk():
    setup_dirs()
    copy_assets()
    create_manifest()
    create_java_source()

    print("\n--- 1. Compilando Recursos com AAPT2 ---")
    res_zip = os.path.join(BUILD_DIR, "compiled_res.zip")
    res_dir = os.path.join(BUILD_DIR, "res")
    run_cmd([AAPT2, "compile", "--dir", res_dir, "-o", res_zip])

    print("\n--- 2. Vinculando Recursos e Gerando APK Não Alinhado ---")
    unaligned_apk = os.path.join(BUILD_DIR, "unaligned.apk")
    manifest_xml = os.path.join(BUILD_DIR, "AndroidManifest.xml")
    gen_dir = os.path.join(BUILD_DIR, "gen")
    assets_dir = os.path.join(BUILD_DIR, "assets")

    run_cmd([
        AAPT2, "link",
        "-I", ANDROID_JAR,
        res_zip,
        "--manifest", manifest_xml,
        "-o", unaligned_apk,
        "--java", gen_dir,
        "-A", assets_dir
    ])

    print("\n--- 3. Compilando Código Fonte Java com javac ---")
    classes_dir = os.path.join(BUILD_DIR, "bin", "classes")
    java_files = glob.glob(os.path.join(BUILD_DIR, "src", "**", "*.java"), recursive=True)
    gen_java_files = glob.glob(os.path.join(gen_dir, "**", "*.java"), recursive=True)
    all_java = java_files + gen_java_files

    run_cmd([
        "javac",
        "-encoding", "UTF-8",
        "-cp", f"{ANDROID_JAR};{gen_dir}",
        "-d", classes_dir,
        *all_java
    ])

    print("\n--- 4. Convertendo Bytecode para Dalvik Executable (classes.dex) com d8 ---")
    class_files = glob.glob(os.path.join(classes_dir, "**", "*.class"), recursive=True)
    dex_dir = os.path.join(BUILD_DIR, "bin", "dex")
    run_cmd([
        D8,
        "--min-api", "21",
        "--lib", ANDROID_JAR,
        "--output", dex_dir,
        *class_files
    ])

    print("\n--- 5. Adicionando classes.dex ao APK ---")
    classes_dex = os.path.join(dex_dir, "classes.dex")
    run_cmd(["jar", "uf", unaligned_apk, "-C", dex_dir, "classes.dex"])

    print("\n--- 6. Alinhando APK com zipalign (4 bytes) ---")
    aligned_apk = os.path.join(BUILD_DIR, "aligned.apk")
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    run_cmd([ZIPALIGN, "-f", "-p", "4", unaligned_apk, aligned_apk])

    print("\n--- 7. Criando Keystore de Assinatura (se não existir) ---")
    if not os.path.exists(KEYSTORE):
        run_cmd([
            "keytool",
            "-genkeypair", "-v",
            "-keystore", KEYSTORE,
            "-alias", KEY_ALIAS,
            "-keyalg", "RSA",
            "-keysize", "2048",
            "-validity", "10000",
            "-storepass", KEYSTORE_PASS,
            "-keypass", KEYSTORE_PASS,
            "-dname", "CN=Agenda Oficial, OU=Liturgica, O=Ecclesiastica, L=Sao Paulo, ST=SP, C=BR"
        ])
        print(f"   [OK] Keystore criado em {KEYSTORE}")
    else:
        print(f"   [OK] Keystore existente em {KEYSTORE}")

    print("\n--- 8. Assinando APK com apksigner ---")
    final_apk = os.path.join(OUTPUT_DIR, APK_NAME)
    if os.path.exists(final_apk):
        os.remove(final_apk)
    run_cmd([
        APKSIGNER, "sign",
        "--ks", KEYSTORE,
        "--ks-pass", f"pass:{KEYSTORE_PASS}",
        "--ks-key-alias", KEY_ALIAS,
        "--key-pass", f"pass:{KEYSTORE_PASS}",
        "--out", final_apk,
        aligned_apk
    ])

    # Copiar também para raiz de agenda_app para acesso direto
    root_apk = os.path.join(ROOT_DIR, APK_NAME)
    shutil.copy2(final_apk, root_apk)

    print("\n--- 9. Verificando Assinatura do APK ---")
    verify_res = run_cmd([APKSIGNER, "verify", "-v", final_apk])

    size_mb = os.path.getsize(final_apk) / (1024 * 1024)
    print("\n" + "="*60)
    print(f"SUCESSO ABSOLUTO! APK GERADO COM SUCESSO:")
    print(f"Caminho: {final_apk}")
    print(f"Cópia Raiz: {root_apk}")
    print(f"Tamanho: {size_mb:.2f} MB")
    print(f"Versão: 1.1.6 (Agenda vs 1.1.6)")
    print("="*60)

if __name__ == "__main__":
    build_apk()
