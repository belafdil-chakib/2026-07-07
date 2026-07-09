#!/usr/bin/env python
"""
test_dev_install.py
===================

Verifie que l'installation en mode DEVELOPPEUR (voir slide 0 de
"instructions_installation.pptx") est correctement realisee :

    1. Version de Python conforme a pyproject.toml (>=3.12, <3.13)
    2. Toutes les dependances de pyproject.toml sont installees et importables
    3. PyTorch est fonctionnel (le GPU/CUDA est un bonus pour l'option dev)
    4. Les donnees (dossier datasets/) ont ete recuperees et decompressees

Usage :
    python test_dev_install.py

Le script affiche un rapport lisible et se termine avec le code de sortie 0
si tout est OK, 1 sinon.
"""

from __future__ import annotations

import importlib
import importlib.metadata as md
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Petits utilitaires d'affichage
# ---------------------------------------------------------------------------
OK = "[ OK ]"
KO = "[FAIL]"
WARN = "[WARN]"

_results: list[bool] = []


def check(label: str, condition: bool, detail: str = "") -> bool:
    """Enregistre et affiche le resultat d'une verification."""
    status = OK if condition else KO
    line = f"{status}  {label}"
    if detail:
        line += f"  ->  {detail}"
    print(line)
    _results.append(condition)
    return condition


def section(title: str) -> None:
    print()
    print(title)
    print("-" * len(title))


# ---------------------------------------------------------------------------
# 1. Version de Python
# ---------------------------------------------------------------------------
def check_python_version() -> None:
    section("1. Version de Python (pyproject : >=3.12, <3.13)")
    v = sys.version_info
    ok = (v.major, v.minor) == (3, 12)
    check(
        "Python 3.12.x",
        ok,
        f"detecte : {v.major}.{v.minor}.{v.micro}",
    )


# ---------------------------------------------------------------------------
# 2. Dependances (pyproject.toml)
# ---------------------------------------------------------------------------
# Correspondance : nom du paquet (pip/pyproject)  ->  nom du module a importer
DEPENDENCIES: dict[str, str] = {
    # --- Environnement notebooks ---
    "notebook": "notebook",
    "ipykernel": "ipykernel",
    "ipywidgets": "ipywidgets",
    # --- Data / calcul scientifique ---
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
    "scipy": "scipy",
    "scikit-learn": "sklearn",
    "pillow": "PIL",
    # --- Deep Learning (CPU) ---
    "torch": "torch",
    "torchvision": "torchvision",
    # --- NLP / LLM / RAG ---
    "transformers": "transformers",
    "sentence-transformers": "sentence_transformers",
    "datasets": "datasets",
    "chromadb": "chromadb",
    # --- Interface web locale ---
    "open-webui": "open_webui",
}


def check_dependencies() -> None:
    section("2. Dependances installees et importables")
    for pkg, module in DEPENDENCIES.items():
        try:
            importlib.import_module(module)
            try:
                version = md.version(pkg)
            except md.PackageNotFoundError:
                version = "version inconnue"
            check(f"{pkg:<22}", True, f"import '{module}' OK (v{version})")
        except Exception as exc:  # noqa: BLE001 - on veut tout capturer
            check(f"{pkg:<22}", False, f"import '{module}' impossible : {exc}")


# ---------------------------------------------------------------------------
# 3. PyTorch en mode CPU
# ---------------------------------------------------------------------------
def check_torch() -> None:
    section("3. PyTorch fonctionnel")
    try:
        import torch

        # Un petit calcul doit fonctionner (au minimum sur le CPU).
        x = torch.ones(3, 3)
        y = x @ x
        check(
            "Calcul tensoriel (CPU)",
            bool((y == 3).all().item()),
            f"torch {torch.__version__}, produit matriciel 3x3 correct",
        )

        # L'option DEVELOPPEUR est privilegiee si l'on possede une carte
        # graphique : la presence d'un GPU CUDA est un bonus, pas une exigence.
        cuda = torch.cuda.is_available()
        gpu = torch.cuda.get_device_name(0) if cuda else "aucun (CPU only)"
        print(f"{WARN if not cuda else OK}  Acceleration GPU (CUDA)  ->  {gpu}")
    except Exception as exc:  # noqa: BLE001
        check("PyTorch fonctionnel", False, str(exc))


# ---------------------------------------------------------------------------
# 4. Donnees (dossier datasets/)
# ---------------------------------------------------------------------------
# Quelques elements attendus dans datasets/ (recuperes depuis Google Drive).
EXPECTED_DATA = [
    "FashionMNIST",
    "cifar-10-batches-py",
    "housing",
    "lifesat",
    "pokemon_data.csv",
]


def check_datasets() -> None:
    section("4. Donnees recuperees (dossier datasets/)")
    root = Path(__file__).resolve().parent
    datasets = root / "datasets"

    if not check("Dossier datasets/ present", datasets.is_dir(), str(datasets)):
        print(
            f"{WARN}  Recuperez et decompressez les donnees depuis le lien Google "
            "Drive indique sur la slide d'installation."
        )
        return

    for item in EXPECTED_DATA:
        p = datasets / item
        check(f"datasets/{item}", p.exists())


# ---------------------------------------------------------------------------
# Point d'entree
# ---------------------------------------------------------------------------
def main() -> int:
    print("=" * 70)
    print("  Verification de l'installation DEVELOPPEUR - Formation PyTorch")
    print("=" * 70)

    check_python_version()
    check_dependencies()
    check_torch()
    check_datasets()

    total = len(_results)
    passed = sum(_results)
    section("Resultat")
    print(f"{passed}/{total} verifications reussies.")

    if passed == total:
        print("\nInstallation developpeur OK. Vous pouvez lancer les notebooks.")
        return 0

    print(
        "\nInstallation incomplete. Reprenez les etapes de la slide "
        "'OPTION DEVELOPPEUR' :"
    )
    print("  - uv sync            (installe les dependances de pyproject.toml)")
    print("  - recuperez/decompressez les donnees dans datasets/")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
