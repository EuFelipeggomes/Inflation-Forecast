import sys

dependencias = [
    "pandas",
    "numpy",
    "matplotlib",
    "seaborn",
    "statsmodels",
    "prophet",
    "sklearn",
    "bcb",
    "pmdarima"
]

print(f"Python: {sys.version}\n")

todas_ok = True

for lib in dependencias:
    try:
        mod = __import__(lib)
        versao = getattr(mod, "__version__", "OK")
        print(f"  ✓ {lib} — {versao}")
    except ImportError:
        print(f"  ✗ {lib} — NÃO ENCONTRADA")
        todas_ok = False

print()
if todas_ok:
    print("Tudo certo! Ambiente configurado com sucesso.")
else:
    print("Algumas dependências estão faltando. Rode: pip install -r requirements.txt")