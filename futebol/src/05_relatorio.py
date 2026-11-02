# ------------------------------ JSON ---------------------------------
def jt(T):
    return dict(id=T['id'], n=T['n'], sig=T['sig'], cor=T['cor'], f=forca(T), fl=bandeira(T['cc']) if T['nac'] else '')

def media(a): return round(a[3] / a[4], 2) if a[4] else None

def jp(p):
    d = {k: p[k] for k in ('id', 'n', 'pos', 'age', 'nat', 'ovr', 'pot', 'fis', 'pe', 'hab', 'cond', 'inj', 'sus', 'val', 'sal', 'num', 'jr')}
    T = G.T.get(p['club']); st = p['st']
    d.update(fl=bandeira(p['nat']), cl=T['n'] if T else 'Sem clube', ct=fdata(p['ct']), j=st['t'][0], g=st['t'][1], a=st['t'][2],
             nm=media(st['t']), st={k: [v[0], v[1], v[2], media(v)] for k, v in st.items()},
             emp=(G.T[p['club']]['n'] if p['emp'] else None), empf=(fdata(p['empf']) if p['emp'] else None))
    return d

# ---------------------------- RELATORIO ------------------------------
def soma_est(m, hs, s):
    d = est0()
    for h in hs:
        for k, v in m['e'][h][s].items(): d[k] += v
    return d

def linhas_est(a, b):
    tp = (a['pos'] + b['pos']) or 1; pa, pb = round(100 * a['pos'] / tp), 100 - round(100 * a['pos'] / tp)
    pz = lambda e: '%d%% (%d/%d)' % (round(100 * e['pok'] / e['pas']) if e['pas'] else 0, e['pok'], e['pas'])
    R2 = lambda n, x, y, fx=None: dict(n=n, a=fx(x) if fx else x, b=fx(y) if fx else y,
                                       va=float(x if not isinstance(x, dict) else x['pok']), vb=float(y if not isinstance(y, dict) else y['pok']))
    f2 = lambda v: '%.2f' % v
    dest = [R2('Gols esperados (xG)', a['xg'], b['xg'], f2), dict(n='Posse de bola', a='%d%%' % pa, b='%d%%' % pb, va=pa, vb=pb),
            R2('Total de finalizações', a['fin'], b['fin']), R2('Finalizações no alvo', a['alvo'], b['alvo']),
            R2('Chances claras', a['cc'], b['cc']), R2('Escanteios', a['esc'], b['esc']),
            dict(n='Passes', a=pz(a), b=pz(b), va=a['pok'], vb=b['pok']), R2('Cartões amarelos', a['am'], b['am'])]
    fin = [R2('Gols esperados (xG)', a['xg'], b['xg'], f2), R2('xG das finalizações no alvo (xGOT)', a['xgot'], b['xgot'], f2),
           R2('Total de finalizações', a['fin'], b['fin']), R2('Finalizações no alvo', a['alvo'], b['alvo']),
           R2('Finalizações para fora', a['fora'], b['fora']), R2('Finalizações bloqueadas', a['blq'], b['blq']),
           R2('Finalizações de dentro da área', a['den'], b['den']), R2('Finalizações de fora da área', a['lon'], b['lon']),
           R2('Bolas na trave', a['trv'], b['trv'])]
    out = [R2('Desarmes', a['des'], b['des']), R2('Defesas do goleiro', a['dfs'], b['dfs']), R2('Faltas cometidas', a['fal'], b['fal']),
           R2('Impedimentos', a['imp'], b['imp']), R2('Cartões vermelhos', a['vm'], b['vm'])]
    return [dict(t='Destaques', l=dest), dict(t='Finalizações', l=fin), dict(t='Defesa e disciplina', l=out)]

def relatorio(m):
    pas = passes_jog(m)
    est = {nome: linhas_est(soma_est(m, hs, 0), soma_est(m, hs, 1)) for nome, hs in (('jogo', (0, 1)), ('1t', (0,)), ('2t', (1,)))}
    jog = [[], []]
    for s in (0, 1):
        ordem = list(m['xi0'][s]) + [x for x in m['ps'] if m['ps'][x]['s'] == s and x not in m['xi0'][s]]
        for x in ordem:
            q = m['ps'].get(x); p = G.P.get(x)
            if not q or not p: continue
            pa, pk = pas.get(x, (0, 0))
            jog[s].append(dict(id=x, num=p['num'], n=p['n'], pos=p['pos'], tit=x in m['xi0'][s], mi=q['mi'], g=q['g'], a=q['a'], f=q['f'],
                               fa=q['fa'], pa=pa, pk=pk, d=q['d'], df=q['df'], am=q['am'], vm=q['vm'], nt=nota(m, x, pas)))
    form = []
    for s in (0, 1):
        sl = slots(m['form0'][s]); g = geo(sl)
        form.append(dict(f=m['form0'][s], xi=[dict(id=x, num=G.P[x]['num'] if x in G.P else 0, n=G.P[x]['n'] if x in G.P else '?',
                                                     ax=g[i][0], dp=g[i][1], nt=nota(m, x, pas)) for i, x in enumerate(m['xi0'][s][:len(g)])]))
    return dict(comp=m['comp'], data=fdata(m['d']), min=m['min'], h=jt(G.T[m['t'][0]]), a=jt(G.T[m['t'][1]]), g=list(m['g']),
                pen=m['pen'], pub=m['pub'][0], renda=m['pub'][1], est=est, jog=jog, form=form, ev=m['ev'],
                sum=[e for e in m['ev'] if e['k'] in ('gol', 'am', 'vm', 'sub', 'les')])

LADOS = ['esquerdo', 'central', 'direito']
def gargalos(m, s):
    o = 1 - s; Zs, Zo = m['z'][s], m['z'][o]; S = m['s'][s]
    atk = [Zo['atk'][2 - l] for l in range(3)]; ch = [Zo['ch'][2 - l] for l in range(3)]
    meu = [Zs['atk'][l] for l in range(3)]
    du = {k: (round(100 * w / t) if t else None) for k, (w, t) in Zs['du'].items()}
    alertas = []
    for x, sl in zip(S['on'], S['sl']):
        p = G.P[x]; e = S['en'][x]; n = nota(m, x)
        if p['inj']: alertas.append('%s está lesionado' % p['n'])
        if e < 55: alertas.append('%s está cansado (%d%% de energia)' % (p['n'], e))
        if fit(p['pos'], sl) < 1: alertas.append('%s (%s) está fora de posição' % (p['n'], p['pos']))
        if x in S['am']: alertas.append('%s tem cartão amarelo' % p['n'])
        if n is not None and n < 5.8 and m['ps'][x]['mi'] >= 25: alertas.append('%s vai mal no jogo (nota %.1f)' % (p['n'], n))
    sug = []; tot = sum(atk)
    if tot >= 5:
        i = max(range(3), key=lambda k: atk[k])
        if atk[i] / tot >= .42:
            fraco = [G.P[x]['n'] for x, l, sl in zip(S['on'], S['ln'], S['sl']) if l == i and sl in 'DM']
            sug.append('O adversário ataca mais pelo seu lado %s (%d de %d ataques, %d finalizações). Reforce esse corredor%s.'
                       % (LADOS[i], atk[i], tot, ch[i], (' ou substitua ' + ', '.join(fraco[:2])) if fraco else ''))
    if du['M'] is not None and du['M'] < 46 and Zs['du']['M'][1] >= 8:
        sug.append('Seu meio-campo vence só %d%% das disputas: use mais um meia (4-2-3-1 / 4-5-1) ou troque um volante cansado.' % du['M'])
    if du['D'] is not None and du['D'] < 48 and Zs['du']['D'][1] >= 6:
        sug.append('Sua defesa barra só %d%% dos ataques no último terço: postura Defensiva ou 5-3-2 podem ajudar.' % du['D'])
    if du['A'] is not None and du['A'] < 40 and Zs['du']['A'][1] >= 6:
        sug.append('Seu ataque chega mas não finaliza (%d%%): tente postura Ofensiva ou um atacante com Drible/Velocidade.' % du['A'])
    if Zs['perda'][0] >= 3: sug.append('Muitas perdas de bola na saída sob pressão (%d).' % Zs['perda'][0])
    if any(S['en'][x] < 50 for x in S['on']): sug.append('Há jogadores com menos de 50% de energia: faça substituições.')
    if not sug: sug.append('Time equilibrado. Mantenha a estratégia.')
    return dict(atk=atk, ch=ch, meu=meu, perda=Zs['perda'], du=du, dun={k: v[1] for k, v in Zs['du'].items()}, alertas=alertas[:8], sug=sug)
