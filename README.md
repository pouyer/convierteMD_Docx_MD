# Convertidor Bidireccional DOCX ↔ MD

Convierte automáticamente archivos `.docx` a `.md` y viceversa.  
Detecta la extensión del archivo origen y aplica la conversión correspondiente.
El archivo original se mueve a la carpeta de procesados tras una conversión exitosa.

---

## Estructura del proyecto

```
convertidor/
├── convertidor.py     # Script principal
├── .env               # Configuración de rutas (crearlo manualmente)
├── .env.example       # Plantilla del archivo .env
├── requirements.txt   # Dependencias Python
└── README.md
```

---

## Requisitos previos

### Python

Versión mínima requerida: **Python 3.10**

**Windows**
1. Descarga desde https://www.python.org/downloads/
2. Durante la instalación marca **"Add Python to PATH"**
3. Verifica en PowerShell:
   ```powershell
   python --version
   ```

**Linux**
```bash
sudo apt update && sudo apt install python3 python3-pip   # Debian/Ubuntu
```

---

### Pandoc

Es la herramienta que realiza la conversión. Debe estar instalada y disponible en el PATH.

**Windows**
1. Descarga el instalador `.msi` desde:  
   https://github.com/jgm/pandoc/releases/latest  
   (busca el archivo `pandoc-X.X-windows-x86_64.msi`)
2. Ejecuta el instalador. Agrega pandoc al PATH automáticamente.
3. **Cierra y vuelve a abrir PowerShell** para que tome el cambio.
4. Verifica:
   ```powershell
   pandoc --version
   ```

> **Si pandoc no se reconoce después de instalarlo**, agrega la ruta manualmente:  
> `Inicio` → busca **"variables de entorno"** → `Variables del sistema` → `Path`  
> → `Editar` → `Nuevo` → escribe `C:\Program Files\Pandoc` → Aceptar.  
> Reinicia PowerShell y vuelve a verificar.

**Linux**
```bash
sudo apt install pandoc        # Debian/Ubuntu
sudo dnf install pandoc        # Fedora
```

---

## Instalación del proyecto

### 1. Clona o copia los archivos en una carpeta local

```
C:\proyectos\convertidor\      (Windows)
/home/usuario/convertidor/     (Linux)
```

### 2. Instala la dependencia Python

**Windows**
```powershell
pip install -r requirements.txt
```

**Linux**
```bash
pip3 install -r requirements.txt
```

---

## Configuración

Crea el archivo `.env` en la misma carpeta que `convertidor.py` copiando `.env.example`:

**Windows**
```powershell
copy .env.example .env
```

**Linux**
```bash
cp .env.example .env
```

Edita `.env` con las rutas reales:

**Windows** (usa barras `/` o doble `\\`)
```env
RUTA_ORIGEN=C:/documentos/origen
RUTA_PROCESADO=C:/documentos/procesados
RUTA_DESTINO=C:/documentos/convertidos
```

**Linux**
```env
RUTA_ORIGEN=/home/usuario/documentos/origen
RUTA_PROCESADO=/home/usuario/documentos/procesados
RUTA_DESTINO=/home/usuario/documentos/convertidos
```

> Las carpetas se crean automáticamente si no existen.

---

## Ejecución

Ubícate en la carpeta del proyecto y ejecuta:

**Windows**
```powershell
python convertidor.py
```

**Linux**
```bash
python3 convertidor.py
```

---

## Comportamiento

| Archivo en `RUTA_ORIGEN` | Resultado en `RUTA_DESTINO` |
|---|---|
| `documento.docx` | `documento.md` |
| `nota.md` | `nota.docx` |

- Se procesan **todos** los archivos `.docx` y `.md` encontrados en `RUTA_ORIGEN`.
- Si la conversión es exitosa, el archivo original se **mueve** a `RUTA_PROCESADO`.
- Si la conversión falla, el archivo original **permanece** en `RUTA_ORIGEN`.
- Archivos con otras extensiones son ignorados con una advertencia en el log.

---

## Ejemplo de salida en consola

```
2025-01-15 10:32:01 [INFO] RUTA_ORIGEN: C:/documentos/origen
2025-01-15 10:32:01 [INFO] RUTA_PROCESADO: C:/documentos/procesados
2025-01-15 10:32:01 [INFO] RUTA_DESTINO: C:/documentos/convertidos
2025-01-15 10:32:01 [INFO] Archivos encontrados: 3
2025-01-15 10:32:01 [INFO] Procesando: informe.docx
2025-01-15 10:32:02 [INFO] [DOCX → MD] informe.docx → informe.md
2025-01-15 10:32:02 [INFO] Movido a procesados: informe.docx
2025-01-15 10:32:02 [INFO] Procesando: notas.md
2025-01-15 10:32:03 [INFO] [MD → DOCX] notas.md → notas.docx
2025-01-15 10:32:03 [INFO] Movido a procesados: notas.md
2025-01-15 10:32:03 [INFO] ──────────────────────────────────────────────────
2025-01-15 10:32:03 [INFO] Resumen → Exitosos: 2 | Con error: 0
```

---

## Solución de problemas

**`pandoc` no se reconoce en Windows**  
Agrega `C:\Program Files\Pandoc` al PATH del sistema (ver sección instalación) y reinicia la terminal.

**`ModuleNotFoundError: No module named 'dotenv'`**  
Ejecuta `pip install -r requirements.txt` nuevamente.

**El archivo `.env` no se lee**  
Asegúrate de que `.env` esté en la misma carpeta desde donde ejecutas el script.

**Error de permisos en Linux**  
```bash
chmod +x convertidor.py
```
