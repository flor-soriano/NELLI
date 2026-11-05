#!/usr/bin/env bash
# Instala Prompt Guard 2 (Meta, pesos abiertos) EN LOCAL. El modelo NO entra al repo:
# es gated en Hugging Face (acepta la licencia con TU cuenta) y pesa 1.1 GB.
# Uso:  bash scripts/instalar-prompt-guard.sh
# Requiere: haber aceptado la licencia en
#   https://huggingface.co/meta-llama/Llama-Prompt-Guard-2-86M
# y tener sesión de Hugging Face en el entorno donde se instala (`hf auth login`).
set -euo pipefail
cd "$(dirname "$0")/.."
uv pip install --python .venv/bin/python --index-url https://download.pytorch.org/whl/cpu torch
uv pip install --python .venv/bin/python transformers
mkdir -p modelos
.venv/bin/python - << 'PY'
from huggingface_hub import snapshot_download
ruta = snapshot_download("meta-llama/Llama-Prompt-Guard-2-86M", local_dir="modelos/prompt-guard-2")
print("Modelo en:", ruta)
PY
echo 'Listo. Para usarlo:  NELLI_PROMPT_GUARD=modelos/prompt-guard-2 nelli verificar "..."'
