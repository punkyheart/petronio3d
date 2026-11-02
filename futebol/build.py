"""Gera prancheta_fc.py (arquivo único para o Colab/PC) e Prancheta_FC.ipynb a partir de src/ e web/."""
import os, json, glob
AQUI = os.path.dirname(os.path.abspath(__file__))
def ler(p): return open(os.path.join(AQUI, p), encoding='utf-8').read()
partes = sorted(glob.glob(os.path.join(AQUI, 'src', '*.py')))
html = ler('web/index.html').replace('/*CSS*/', ler('web/app.css')).replace('/*JS*/', ler('web/app.js'))
assert "'''" not in html
codigo = ''
for p in partes:
    if p.endswith('08_servidor.py'): codigo += "\n# --------------------------- INTERFACE -------------------------------\nHTML = r'''" + html + "'''\n\n"
    codigo += open(p, encoding='utf-8').read().rstrip() + '\n\n'
open(os.path.join(AQUI, 'prancheta_fc.py'), 'w', encoding='utf-8').write(codigo)
nb = {"nbformat": 4, "nbformat_minor": 5, "metadata": {"colab": {"name": "Prancheta_FC.ipynb"}, "kernelspec": {"name": "python3", "display_name": "Python 3"}},
      "cells": [{"cell_type": "markdown", "metadata": {}, "source": ["# ⚽ Prancheta FC\n", "Execute a célula abaixo (Shift+Enter) e clique no link que aparecer para abrir o jogo em tela cheia.\n\n",
                 "Para usar jogadores reais: no jogo, vá em **Opções → Carregar planilha (.xlsx)**, ou envie `prancheta_dados.xlsx` para a pasta `/content` antes de executar."]},
                {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": codigo.splitlines(keepends=True)}]}
json.dump(nb, open(os.path.join(AQUI, 'Prancheta_FC.ipynb'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('prancheta_fc.py: %d KB, %d linhas' % (len(codigo.encode()) // 1024, codigo.count('\n')))
