# Prancheta FC

Jogo de gerenciamento de futebol: técnico de clube e de seleção, com carreira, mercado,
escalação no campinho e partidas ao vivo no modo ultra rápido, com substituições e
mudanças táticas durante o jogo.

## Como rodar

**Google Colab:** abra `Prancheta_FC.ipynb` (ou cole todo o `prancheta_fc.py` numa célula) e
execute. Clique no link que aparece para abrir o jogo em tela cheia; ele também aparece
dentro da própria célula.

**No computador:**

```bash
pip install flask
python prancheta_fc.py      # abre http://127.0.0.1:8050
```

Para jogar no celular, use o IP do computador na mesma rede Wi-Fi (ex.: `http://192.168.0.10:8050`).

## Conteúdo

- 40 ligas de primeira divisão (Europa, Américas, Ásia, África e Oceania), com 676 clubes reais.
- Cerca de 16 mil jogadores com posição, idade, nacionalidade, pé (destro, canhoto ou ambidestro), força,
  força física, potencial, condição e habilidades especiais (finalização, cabeceio, drible, passe,
  velocidade, desarme, marcação, chute de longe, bola parada, pênaltis, liderança, reflexos,
  saída do gol, resistência, cruzamento).
- 47 seleções, montadas a partir da nacionalidade dos jogadores, com convocação manual ou automática,
  amistosos nas Datas FIFA e a Copa das Nações no fim de cada temporada.
- Carreira: reputação, confiança da diretoria, demissão, propostas de clubes e de seleções.
- Envelhecimento, evolução até o potencial, aposentadoria e novas promessas a cada temporada.
- Os jogadores são gerados de acordo com a força de cada clube. Os nomes são fictícios.

## Elencos reais (CSV)

Para colocar elencos reais, crie um CSV separado por `;` e rode `importar_csv('arquivo.csv')`
depois de executar o jogo (os clubes citados têm o elenco substituído):

```
clube;nome;posicao;idade;nacionalidade;forca;fisico;potencial;pe;habilidades
Flamengo;Fulano da Silva;ATA;27;BR;80;75;82;E;FIN DRI
```

Posições: `GOL ZAG LAT VOL MEI ATA`. Pé: `D`, `E` ou `A`. Habilidades: os códigos listados em `HABS`.
Para adicionar outra liga, inclua uma linha em `LIGAS` no formato
`PAIS|Nome da liga|força do melhor|força do pior|Clube 1;Clube 2;...`.
