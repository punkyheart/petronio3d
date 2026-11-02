# Prancheta FC

Jogo de gerenciamento de futebol: você é técnico de um clube e, se quiser, também de uma seleção. Monta o
elenco, contrata, acompanha as partidas ao vivo num campo 2D e constrói a carreira ao longo das temporadas.

## Como rodar

**Google Colab:** abra `Prancheta_FC.ipynb` (ou cole todo o `prancheta_fc.py` numa célula) e execute.
Clique no link que aparece para abrir em tela cheia.

**No computador:**

```bash
pip install flask openpyxl
python prancheta_fc.py        # abre http://127.0.0.1:8050
```

No celular, use o IP do computador na mesma rede Wi‑Fi.

## Telas

- **Elenco:** tabela compacta colorida por setor, com posição, número, pé, força, físico, potencial, energia,
  salário, valor, características, idade, jogos, gols, assistências, nota média e contrato. Ordena por
  qualquer coluna e marca os craques com ★.
- **Painel lateral nas cores do clube:** caixa, mensagens, confiança da diretoria e da torcida, próximo
  jogo, botões Jogar e Escalar, e ficha do jogador selecionado. A ficha traz estatísticas de temporada,
  carreira e liga, e os botões vender, renovar, emprestar e dispensar.
- **Agenda:** calendário com datas do time atual (clube e seleção), com filtro por competição, placar,
  público e renda. Clicar num jogo disputado abre o relatório completo.
- **Partida ao vivo:** transmissão em campo 2D com a bola, os 22 jogadores se movendo, a situação da jogada
  e a área de pressão.
  - Velocidade: Ultra rápido (padrão), Rápido ou Normal.
  - Abas: Lances, Estatísticas, Gargalos e Outros jogos.
  - Na pausa: substituições, formação e postura.
- **Gargalos:** mostra por qual corredor o adversário ataca, onde seu time perde a bola, as disputas
  vencidas por setor e alertas (cansaço, fora de posição, nota baixa) com sugestões.
- **Relatório pós-jogo**, com 5 abas:
  - Sumário.
  - Estatísticas por tempo: xG, posse, finalizações (no alvo, para fora, bloqueadas, de dentro e de fora
    da área, na trave), chances claras, escanteios, passes e cartões.
  - Formações.
  - Notas dos jogadores.
  - Relato.
- **Tabelas, Estádio, Juniores, Times, Procura, Técnicos, História, Mensagens, Opções e Seleção.**
  - Tabelas: todas as ligas, as copas nacionais e a Copa das Nações.
  - Estádio: capacidade, preço do ingresso e ampliação.
  - Juniores: categoria de base, com promoção ao time principal.
  - Seleção: convocação e escalação da seleção.

## Mundo do jogo

- 40 ligas de primeira divisão e 676 clubes. Cada liga tem o seu calendário real (europeias de agosto a
  maio, sul-americanas no ano civil etc.).
- Copas nacionais com mata-mata e pênaltis, Datas FIFA e Copa das Nações anual com as 16 melhores seleções.
- Contratos com data de término, renovação, empréstimos e público e renda por jogo.
- Confiança da diretoria e da torcida, demissão, propostas de clubes e seleções, e técnicos rivais.
- Envelhecimento, evolução, aposentadoria, novas promessas e histórico de campeões.

## Planilha com dados reais (.xlsx ou .csv)

Em **Opções → Planilha de dados** (ou na tela inicial), carregue uma planilha. Também funciona deixar
`prancheta_dados.xlsx` na pasta do jogo (no Colab, `/content`).

O importador reconhece colunas com nomes variados em português ou inglês:

- **Obrigatórias:** `Clube`, `Jogador`.
- **Recomendadas:** `País`, `Liga`, `Posição`, `Idade` ou `Nascimento`, `Nacionalidade`.
- **Opcionais:** `Pé`, `Força`, `Físico`, `Potencial`, `Características`, `Valor`, `Salário`, `Contrato`,
  `Número`.

Como a planilha é aplicada:

- Atributos ausentes são estimados pela força da liga e do clube ou pelo valor de mercado.
- Uma liga com o mesmo nome (ou a 1ª divisão do país) substitui a liga do jogo. Outras ligas viram novas
  divisões.
- Clubes cuja liga é uma copa (ex.: `Copa do Brasil`) ou está vazia entram só na copa nacional do país.
- Pode haver uma aba só com `País`, `Competição` e `Clube`, sem jogadores. Nesse caso o elenco é gerado.

## Código

- `src/`: o jogo em Python, dividido em partes (dados, mundo, motor de partida, temporada, relatórios, API,
  importador, servidor).
- `web/`: a interface (HTML, CSS e JavaScript).
- `python build.py`: junta tudo em `prancheta_fc.py`, o arquivo único para colar no Colab, e gera
  `Prancheta_FC.ipynb`.
