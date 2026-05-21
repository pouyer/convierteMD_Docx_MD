"""
Convertidor bidireccional .DOCX ↔ .MD
- Archivos .docx en RUTA_ORIGEN  →  se convierten a .md  en RUTA_DESTINO
- Archivos .md   en RUTA_ORIGEN  →  se convierten a .docx en RUTA_DESTINO
- El archivo original se mueve a RUTA_PROCESADO en ambos casos.
"""

import os
import shutil
import subprocess
import logging
from pathlib import Path
from dotenv import load_dotenv

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ── Configuración ─────────────────────────────────────────────────────────────
def cargar_configuracion() -> tuple[Path, Path, Path]:
    """Lee las rutas desde .env y crea los directorios si no existen."""
    load_dotenv()

    claves = ("RUTA_ORIGEN", "RUTA_PROCESADO", "RUTA_DESTINO")
    valores = {k: os.getenv(k) for k in claves}

    faltantes = [k for k, v in valores.items() if not v]
    if faltantes:
        raise EnvironmentError(f"Faltan variables en .env: {', '.join(faltantes)}")

    rutas = {k: Path(v) for k, v in valores.items()}

    for nombre, ruta in rutas.items():
        ruta.mkdir(parents=True, exist_ok=True)
        log.info(f"{nombre}: {ruta}")

    return rutas["RUTA_ORIGEN"], rutas["RUTA_PROCESADO"], rutas["RUTA_DESTINO"]


# ── Conversión ────────────────────────────────────────────────────────────────
def _ejecutar_pandoc(args: list[str], nombre: str) -> bool:
    """Ejecuta pandoc con los argumentos dados. Retorna True si tuvo éxito."""
    try:
        resultado = subprocess.run(
            ["pandoc"] + args,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if resultado.returncode != 0:
            log.error(f"pandoc falló en '{nombre}': {resultado.stderr.strip()}")
            return False
        return True

    except FileNotFoundError:
        log.error(
            "pandoc no está instalado.\n"
            "  Windows : descarga el instalador desde https://pandoc.org/installing.html\n"
            "  Linux   : sudo apt install pandoc\n"
            "  macOS   : brew install pandoc"
        )
        raise
    except subprocess.TimeoutExpired:
        log.error(f"Tiempo de espera excedido al convertir '{nombre}'")
        return False


def convertir(origen: Path, ruta_destino: Path) -> tuple[bool, Path | None]:
    """
    Detecta la extensión del archivo origen y aplica la conversión correspondiente.
    Retorna (éxito, ruta_del_archivo_generado).
    """
    ext = origen.suffix.lower()

    if ext == ".docx":
        salida = ruta_destino / (origen.stem + ".md")
        args = [
            str(origen), "-o", str(salida),
            "--wrap=none",
            "--markdown-headings=atx",
        ]
        tipo = "DOCX → MD"

    elif ext == ".md":
        salida = ruta_destino / (origen.stem + ".docx")
        args = [
            str(origen), "-o", str(salida),
            "--from=markdown",
            "--to=docx",
        ]
        tipo = "MD → DOCX"

    else:
        log.warning(f"Extensión no soportada, se omite: '{origen.name}'")
        return False, None

    ok = _ejecutar_pandoc(args, origen.name)
    if ok:
        log.info(f"[{tipo}] {origen.name} → {salida.name}")
    return ok, salida if ok else None


# ── Flujo principal ───────────────────────────────────────────────────────────
def procesar_archivos(
    ruta_origen: Path,
    ruta_procesado: Path,
    ruta_destino: Path,
) -> None:
    """Recorre RUTA_ORIGEN, convierte cada .docx y .md encontrado."""

    patrones = ["*.docx", "*.md"]
    archivos = sorted(
        archivo
        for patron in patrones
        for archivo in ruta_origen.glob(patron)
    )

    if not archivos:
        log.info("No se encontraron archivos .docx ni .md en la ruta origen.")
        return

    log.info(f"Archivos encontrados: {len(archivos)}")
    exitos = errores = 0

    for archivo in archivos:
        log.info(f"Procesando: {archivo.name}")
        ok, _ = convertir(archivo, ruta_destino)

        if ok:
            destino_procesado = ruta_procesado / archivo.name
            shutil.move(str(archivo), str(destino_procesado))
            log.info(f"Movido a procesados: {archivo.name}")
            exitos += 1
        else:
            errores += 1

    log.info("─" * 50)
    log.info(f"Resumen → Exitosos: {exitos} | Con error: {errores}")


# ── Entrada ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        origen, procesado, destino = cargar_configuracion()
        procesar_archivos(origen, procesado, destino)
    except EnvironmentError as e:
        log.error(str(e))
        raise SystemExit(1)