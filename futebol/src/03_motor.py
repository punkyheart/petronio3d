# ------------------------- MOTOR DA PARTIDA --------------------------
# Cada minuto: posse disputada no meio-campo; o time com a bola tenta uma jogada por um corredor
# (esquerda/centro/direita): saída -> meio-campo -> último terço -> finalização. Cada fase depende da
# força dos setores e dos jogadores daquele corredor (energia, posição, habilidades).
WSH = {'G': 0, 'D': .6, 'M': 2.2, 'A': 5}
WA = {'G': 0, 'D': .25, 'M': .6, 'A': 1.0}     # peso no ataque por corredor
WD = {'G': 0, 'D': 1.0, 'M': .45, 'A': .1}     # peso na defesa por corredor
YL = (18, 50, 82)

def eh_usuario(tid):
    c = G.coach; return bool(c) and tid in (c['club'], c['nt'])

def regeo(S):
    g = geo(S['sl']); S['ax'] = [x[0] for x in g]; S['dp'] = [x[1] for x in g]; S['ln'] = [corredor(x[0]) for x in g]
    S['v'] = S.get('v', 0) + 1

def lado(tid):
    T = G.T[tid]
    (validar_xi if eh_usuario(tid) else auto_xi)(T)
    on, sl = (list(T['xi']), slots(T['form'])) if len(T['xi']) == 11 else arrumar(T['xi'], T['form'])
    bench = sorted([x for x in T['pl'] if x not in on and disp(x, T['nac'])], key=lambda x: -G.P[x]['ovr'])[:12]
    en = {x: (100 if T['nac'] else G.P[x]['cond']) for x in on + bench}
    S = dict(t=tid, on=on, sl=sl, bench=bench, subs=0, en=en, used=set(on), am=set(), sai=set())
    regeo(S); return S

def poder(S, casa):
    T = G.T[S['t']]; d, m, a, fm, fa, fd = FORMS[T['form']]
    soma = {'G': 0, 'D': 0, 'M': 0, 'A': 0}; gk = 30; att = mid = de = 1.0; npas = 0
    la = [0.0] * 3; lan = [0.0] * 3; ld = [0.0] * 3; ldn = [0.0] * 3
    for x, s, l in zip(S['on'], S['sl'], S['ln']):
        p = G.P[x]; hb = p['hab']
        e = p['ovr'] * fit(p['pos'], s) * (.72 + .28 * S['en'][x] / 100)
        if s == 'G': gk = e * (1.06 if 'REF' in hb else 1) * (1.03 if 'SAI' in hb else 1)
        else:
            soma[s] += e; la[l] += e * WA[s]; lan[l] += WA[s]; ld[l] += e * WD[s]; ldn[l] += WD[s]
        for h in hb:
            if h in ('DRI', 'VEL', 'CRU', 'BOL'): att += .012
            elif h == 'PAS': mid += .015; npas += 1
            elif h in ('DES', 'MAR'): de += .012
            elif h == 'LID': att += .004; mid += .004; de += .004
    k = .96 + .08 * T['mor'] / 100; ta, td = TATICAS[T['tac']]
    Dv, Mv, Av = soma['D'] / d, soma['M'] / m, soma['A'] / a
    M = (.7 * Mv + .15 * Dv + .15 * Av) * fm * mid * k * (1.05 if casa else 1)
    A = (.65 * Av + .35 * Mv) * fa * att * k * ta * (1.03 if casa else 1)
    D = (.7 * Dv + .3 * Mv) * fd * de * k * td
    base = max(30, (Dv + Mv + Av) / 3)
    qa = [la[i] / lan[i] if lan[i] else base * .6 for i in range(3)]
    qd = [ld[i] / ldn[i] if ldn[i] else base * .6 for i in range(3)]
    acc = min(.93, max(.6, .72 + (Mv - 65) * .004 + npas * .008))
    return max(M, 1), max(A, 1), max(D, 1), gk, qa, qd, acc

def est0(): return dict(pos=0.0, fin=0, alvo=0, fora=0, blq=0, trv=0, xg=0.0, xgot=0.0, cc=0, esc=0, fal=0, am=0, vm=0,
                        imp=0, den=0, lon=0, pas=0.0, pok=0.0, des=0, dfs=0)
def ps0(s): return dict(s=s, g=0, a=0, f=0, fa=0, d=0, df=0, am=0, vm=0, mi=0, gs=0)
def z0(): return dict(atk=[0, 0, 0], ch=[0, 0, 0], perda=[0, 0, 0], du={'D': [0, 0], 'M': [0, 0], 'A': [0, 0]})

def nova_partida(h, a, tipo, comp, neutro=False, ko=False):
    m = dict(t=[h, a], g=[0, 0], ev=[], s=[lado(h), lado(a)], pen=None, neutro=neutro, us=None, w=None, gm=0, tipo=tipo,
             comp=comp, ko=ko, d=G.hoje, e=[[est0(), est0()], [est0(), est0()]], ps={}, z=[z0(), z0()], fr=None, min=0)
    for s in (0, 1):
        for x in m['s'][s]['on']: m['ps'][x] = ps0(s)
    m['xi0'] = [list(m['s'][0]['on']), list(m['s'][1]['on'])]; m['form0'] = [G.T[h]['form'], G.T[a]['form']]
    m['pub'] = publico(h, a, neutro)
    return m

def ev(m, t, s, k, x, y=''):
    m['ev'].append(dict(m=t, s=s, k=k, x=x, y=y))

def pt(fr, s, depth, l, y=None):
    if fr is None: return
    yy = (YL[l] + R.uniform(-9, 9)) if y is None else y
    fr['b'].append([round(depth if s == 0 else 100 - depth, 1), round(yy if s == 0 else 100 - yy, 1)]); fr['p'] = s

def minuto(m, t, vivo):
    hf = 0 if t <= 45 else 1; E = m['e'][hf]; m['min'] = t
    pw = [poder(m['s'][0], not m['neutro']), poder(m['s'][1], False)]
    a, b = pw[0][0] ** 1.6, pw[1][0] ** 1.6; sh = a / (a + b)
    fr = dict(b=[], k='seg', p=0) if vivo else None
    for s in (0, 1):
        S = m['s'][s]; share = sh if s == 0 else 1 - sh
        E[s]['pos'] += share; npas = share * 10.4 * R.uniform(.85, 1.15); E[s]['pas'] += npas; E[s]['pok'] += npas * pw[s][6]
        for x in S['on']:
            p = G.P[x]; S['en'][x] = max(0, S['en'][x] - (.40 - .0028 * p['fis']) * (.7 if 'RES' in p['hab'] else 1))
            m['ps'][x]['mi'] += 1
    jogada(m, 0 if R.random() < sh else 1, pw, t, E, fr)
    for s in (0, 1):
        if R.random() < .125: falta(m, s, pw, t, E, fr)
        if R.random() < .0018: lesao(m, s, t)
        if m['us'] != s and t >= 56 and R.random() < .09: ai_sub(m, s, t)
    if fr is not None: m['fr'] = fr

def jogada(m, s, pw, t, E, fr):
    o = 1 - s; Z, Zo = m['z'][s], m['z'][o]; M, A = pw[s][0], pw[s][1]; qa, qd = pw[s][4], pw[o][5]
    mods = [min(1.25, max(.8, qa[l] / max(1, qd[2 - l]))) for l in range(3)]
    l = R.choices((0, 1, 2), [(.3, .4, .3)[i] * mods[i] ** 2 for i in range(3)])[0]; md = mods[l] ** .5
    pt(fr, s, R.uniform(18, 36), l)
    if R.random() < .05 * pw[o][0] / M:                        # perde a bola na saída, sob pressão
        Z['perda'][0] += 1; desarme(m, o, ('A', 'M'), 2 - l, E)
        if fr: fr['k'] = 'rec'; fr['p'] = o
        return
    q1 = min(.9, .57 * (M / pw[o][0]) ** .2 * md); Z['du']['M'][1] += 1; Zo['du']['M'][1] += 1
    pt(fr, s, R.uniform(44, 58), l)
    if R.random() > q1:                                        # perde no meio-campo
        Z['perda'][1] += 1; Zo['du']['M'][0] += 1; desarme(m, o, ('M', 'D'), 2 - l, E)
        if fr: fr['k'] = 'seg'; fr['p'] = o
        return
    Z['du']['M'][0] += 1; Z['atk'][l] += 1
    pt(fr, s, R.uniform(68, 80), l)
    if fr: fr['k'] = 'atk'
    q2 = min(.85, .42 * (A / pw[o][2]) ** .5 * md); Z['du']['A'][1] += 1; Zo['du']['D'][1] += 1
    if R.random() > q2:                                        # defesa adversária corta no último terço
        Z['perda'][2] += 1; Zo['du']['D'][0] += 1; r = R.random()
        if r < .25: escanteio(m, s, pw, t, E, fr)
        elif r < .37:
            E[s]['imp'] += 1
            if fr: fr['k'] = 'imp'
        else:
            desarme(m, o, ('D', 'M'), 2 - l, E)
            if fr: fr['k'] = 'seg'; fr['p'] = o
        return
    Z['du']['A'][0] += 1
    if fr: fr['k'] = 'per'
    finalizar(m, s, pw, t, E, fr, l)

def desarme(m, s, grupos, l, E):
    S = m['s'][s]
    c = [(x, sl) for x, sl, ln in zip(S['on'], S['sl'], S['ln']) if sl in grupos and abs(ln - l) <= 1]
    if not c or R.random() < .4: return
    x = R.choices(c, [G.P[x]['ovr'] * (1.4 if {'DES', 'MAR'} & set(G.P[x]['hab']) else 1) * (1.5 if sl == grupos[0] else 1) for x, sl in c])[0][0]
    m['ps'][x]['d'] += 1; E[s]['des'] += 1

def escanteio(m, s, pw, t, E, fr):
    E[s]['esc'] += 1
    if fr: fr['k'] = 'esc'; pt(fr, s, 99.5, 0, R.choice((1.5, 98.5)))
    if R.random() < .1: finalizar(m, s, pw, t, E, fr, 1, 'cab')

def falta(m, f, pw, t, E, fr):
    S = m['s'][f]; E[f]['fal'] += 1
    if len(S['on']) > 7 and R.random() < .15: cartao(m, f, t)
    if R.random() < .065:
        if fr: fr['k'] = 'fal'
        finalizar(m, 1 - f, pw, t, E, fr, 1, 'fk')
    elif fr is not None and fr['k'] == 'seg' and R.random() < .3: fr['k'] = 'fal'

def finalizar(m, s, pw, t, E, fr, l, bp=None):
    o = 1 - s; S = m['s'][s]; A, D, gk = pw[s][1], pw[o][2], pw[o][3]
    cand = [(x, sl) for x, sl in zip(S['on'], S['sl']) if sl != 'G']
    if not cand: return
    pen = bp is None and R.random() < .016
    if pen:
        x = max(S['on'], key=lambda y: G.P[y]['ovr'] + (12 if 'PEN' in G.P[y]['hab'] else 0) - (50 if G.P[y]['pos'] == 'GOL' else 0))
        pg = .76 + (.06 if 'PEN' in G.P[x]['hab'] else 0) - (.05 if gk > A else 0); den = True
    elif bp == 'fk':
        x = max([c[0] for c in cand], key=lambda y: G.P[y]['ovr'] + (15 if 'BOL' in G.P[y]['hab'] else 0) + (8 if 'CHL' in G.P[y]['hab'] else 0))
        pg = (.05 + (.035 if 'BOL' in G.P[x]['hab'] else 0)) * (A / gk) ** .4; den = False
    elif bp == 'cab':
        x = R.choices(cand, [G.P[x]['ovr'] * (2 if 'CAB' in G.P[x]['hab'] else 1) * {'D': 1.2, 'M': .6, 'A': 1.5}[sl] for x, sl in cand])[0][0]
        pg = .08 * (A / D) ** .8 * (A / gk) ** .4 * (1.3 if 'CAB' in G.P[x]['hab'] else 1); den = True
    else:
        w = [WSH[sl] * G.P[x]['ovr'] * (1.6 if 'FIN' in G.P[x]['hab'] else 1) * (1.2 if 'CAB' in G.P[x]['hab'] else 1)
             * (1.2 if 'CHL' in G.P[x]['hab'] else 1) for x, sl in cand]
        x, sl = R.choices(cand, w)[0]; p = G.P[x]
        den = R.random() > (.26 + (.2 if 'CHL' in p['hab'] else 0) + (.12 if sl == 'M' else .1 if sl == 'D' else 0))
        q = p['ovr'] * fit(p['pos'], sl) * (.72 + .28 * S['en'][x] / 100) / A
        pg = .096 * (A / D) ** .8 * (A / gk) ** .4 * q ** 1.2 * (1.12 if 'FIN' in p['hab'] else 1) * (1.25 if den else .42)
    pg = min(.9 if pen else .6, pg); p = G.P[x]; q = m['ps'].setdefault(x, ps0(s))
    E[s]['fin'] += 1; E[s]['xg'] += pg; E[s]['den' if den else 'lon'] += 1; q['f'] += 1; m['z'][s]['ch'][l] += 1
    if pg >= .13: E[s]['cc'] += 1
    pt(fr, s, 88 if den else 74, l)
    if R.random() < pg:
        E[s]['alvo'] += 1; E[s]['xgot'] += min(.97, pg * 1.9); q['fa'] += 1; q['g'] += 1; m['g'][s] += 1; m['gm'] = t
        ast = ''
        if not pen and bp != 'fk' and R.random() < .65:
            c2 = [(y, sl) for y, sl in zip(S['on'], S['sl']) if y != x and sl != 'G']
            if c2:
                y = R.choices(c2, [{'D': 1, 'M': 3, 'A': 2}[sl] * (1.5 if {'PAS', 'CRU'} & set(G.P[y]['hab']) else 1) for y, sl in c2])[0][0]
                m['ps'].setdefault(y, ps0(s))['a'] += 1; ast = G.P[y]['n']
        for z in m['s'][o]['on']: m['ps'].setdefault(z, ps0(o))['gs'] += 1
        ev(m, t, s, 'gol', p['n'] + (' (pênalti)' if pen else ' (falta)' if bp == 'fk' else ' (cabeça)' if bp == 'cab' else ''), ast)
        if fr: fr['k'] = 'gol'; pt(fr, s, 100, 1, 50 + R.uniform(-5, 5))
        return
    r = R.random(); pa = .7 if pen else .3
    if r < pa:
        E[s]['alvo'] += 1; E[s]['xgot'] += min(.95, pg * 1.9); q['fa'] += 1; E[o]['dfs'] += 1
        gl = [z for z, sl in zip(m['s'][o]['on'], m['s'][o]['sl']) if sl == 'G']
        if gl: m['ps'].setdefault(gl[0], ps0(o))['df'] += 1
        k = 'def'; txt = ' parou no goleiro'
        if not pen and R.random() < .3: escanteio(m, s, pw, t, E, fr)
    elif not pen and r < pa + (1 - pa) * .33:
        E[s]['blq'] += 1; desarme(m, o, ('D', 'M'), 2 - l, E); k = 'blq'; txt = ' teve o chute bloqueado'
        if R.random() < .4: escanteio(m, s, pw, t, E, fr)
    elif R.random() < .06:
        E[s]['trv'] += 1; k = 'trv'; txt = ' acertou a trave'
    else:
        E[s]['fora'] += 1; k = 'fora'; txt = R.choice([' chutou para fora', ' bateu por cima', ' perdeu chance clara'])
    if fr:
        if fr['k'] != 'esc': fr['k'] = k
        if k in ('fora', 'trv'): pt(fr, s, 100, 1, 50 + R.choice((-1, 1)) * R.uniform(7, 18))
    if m['us'] is not None and (pen or k == 'trv' or pg >= .25 or R.random() < .25):
        ev(m, t, s, 'quase', p['n'] + (' perdeu o pênalti' if pen else txt))

def expulsar(S, i):
    x = S['on'].pop(i); s = S['sl'].pop(i); S['sai'].add(x)
    if s == 'G' and S['on']: S['on'], S['sl'] = arrumar(S['on'], G.T[S['t']]['form'])
    regeo(S)

def cartao(m, s, t):
    S = m['s'][s]; E = m['e'][0 if t <= 45 else 1][s]
    i = R.choices(range(len(S['on'])), [{'G': .2, 'D': 3, 'M': 2.5, 'A': 1}[sl] for sl in S['sl']])[0]
    x = S['on'][i]; p = G.P[x]; liga = m['tipo'] == 'liga'; q = m['ps'].setdefault(x, ps0(s))
    if x in S['am'] or R.random() < .01:
        dois = x in S['am']; expulsar(S, i); E['vm'] += 1; q['vm'] += 1
        if liga: p['sus'] = 1 if dois else 2
        ev(m, t, s, 'vm', p['n'] + (' (2º amarelo)' if dois else ''))
        if m['us'] == s: m['pausa'] = 'expulsão'
    else:
        S['am'].add(x); E['am'] += 1; q['am'] += 1; ev(m, t, s, 'am', p['n'])
        if liga:
            p['ca'] += 1
            if p['ca'] >= 3: p['ca'] = 0; p['sus'] = 1

def lesao(m, s, t):
    S = m['s'][s]; i = R.randrange(len(S['on'])); x = S['on'][i]; p = G.P[x]
    if p['inj']: return
    p['inj'] = R.randint(6, 40); S['en'][x] = min(S['en'][x], 15)
    ev(m, t, s, 'les', p['n'] + ' (%d dias)' % p['inj'])
    if m['us'] == s: m['pausa'] = 'lesão'
    else: ai_sub(m, s, t, i)

def substituir(m, s, i, xin, t):
    S = m['s'][s]; out = S['on'][i]
    S['on'][i] = xin; S['bench'].remove(xin); S['sai'].add(out); S['used'].add(xin); S['subs'] += 1; S['v'] += 1
    m['ps'].setdefault(xin, ps0(s)); ev(m, t, s, 'sub', G.P[xin]['n'], G.P[out]['n'])

def ai_sub(m, s, t, i=None):
    S = m['s'][s]
    if S['subs'] >= 5 or not S['bench']: return
    if i is None:
        op = [k for k in range(len(S['on'])) if S['sl'][k] != 'G']
        if not op: return
        i = min(op, key=lambda k: S['en'][S['on'][k]])
        if S['en'][S['on'][i]] > 80: return
    g = S['sl'][i]
    c = [x for x in S['bench'] if GRP[G.P[x]['pos']] == g] or ([] if g == 'G' else S['bench'])
    if c: substituir(m, s, i, max(c, key=lambda x: G.P[x]['ovr']), t)

def penaltis(m):
    gols = [0, 0]
    tk = [sorted(m['s'][s]['on'], key=lambda x: -(G.P[x]['ovr'] + (15 if 'PEN' in G.P[x]['hab'] else 0) - (40 if G.P[x]['pos'] == 'GOL' else 0))) for s in (0, 1)]
    for r in range(40):
        for s in (0, 1):
            x = tk[s][r % len(tk[s])]
            if R.random() < .72 + (.08 if 'PEN' in G.P[x]['hab'] else 0): gols[s] += 1
        if r >= 4 and gols[0] != gols[1]: break
        if r < 4 and abs(gols[0] - gols[1]) > 4 - r: break
    m['pen'] = gols

# --------------------------- NOTAS / STATS ---------------------------
def passes_jog(m):
    """divide os passes do time entre os jogadores (peso por setor x minutos em campo)"""
    out = {}
    for s in (0, 1):
        tot = sum(m['e'][h][s]['pas'] for h in (0, 1)); ok = sum(m['e'][h][s]['pok'] for h in (0, 1))
        acc = ok / tot if tot else .8
        S = m['s'][s]; sl = dict(zip(S['on'], S['sl']))
        pesos = {x: {'G': .8, 'D': 2.2, 'M': 3.0, 'A': 1.2}[sl.get(x, GRP[G.P[x]['pos']])] * q['mi']
                 for x, q in m['ps'].items() if q['s'] == s and x in G.P}
        sw = sum(pesos.values()) or 1
        for x, w in pesos.items():
            pa = tot * w / sw; out[x] = (int(pa), int(pa * min(.98, acc * (1 + (G.P[x]['ovr'] - 70) * .004))))
    return out

def nota(m, x, pas=None):
    q = m['ps'].get(x)
    if not q or q['mi'] < 10 or x not in G.P: return None
    p = G.P[x]; s = q['s']; g = GRP[p['pos']]; gf, ga = m['g'][s], m['g'][1 - s]
    n = 6.0 + q['g'] * (.8 if g == 'A' else 1.1) + q['a'] * .55 + q['fa'] * .12 - (q['f'] - q['fa']) * .05 + q['d'] * .12 + q['df'] * .3
    if g == 'G': n += -q['gs'] * .35 + (.5 if q['gs'] == 0 and q['mi'] >= 60 else 0)
    elif g == 'D': n += -q['gs'] * .15 + (.3 if q['gs'] == 0 and q['mi'] >= 60 else 0)
    n += .25 if gf > ga else -.2 if gf < ga else 0
    if pas and x in pas and pas[x][0] > 8: n += (pas[x][1] / pas[x][0] - .8) * 2.5
    n += (p['ovr'] - 70) * .01 - q['am'] * .3 - q['vm'] * 1.5
    return round(max(3, min(10, n)), 1)

def gravar_stats(m):
    """soma a partida nas estatísticas de temporada/carreira/liga dos jogadores"""
    pas = passes_jog(m); ks = ('t', 'c', 'l') if m['tipo'] == 'liga' else ('t', 'c')
    for x, q in m['ps'].items():
        if q['mi'] <= 0 or x not in G.P: continue
        n = nota(m, x, pas); st = G.P[x]['st']
        for k in ks:
            a = st[k]; a[0] += 1; a[1] += q['g']; a[2] += q['a']
            if n is not None: a[3] += n; a[4] += 1

# ---------------------------- SIMULACAO RAPIDA -----------------------
def lado_rapido(tid):
    T = G.T[tid]; k = (G.hoje // 7, T['form'], T['tac'], len(T['pl']), T['mor'] // 10)
    if not eh_usuario(tid):
        c = G.cache.get(tid)
        if c and c[0] == k: return c[1], c[2]
    S = lado(tid); pw = [poder(S, True), poder(S, False)]
    if not eh_usuario(tid): G.cache[tid] = (k, S, pw)
    return S, pw

def gols_esperados(pa, po, share):
    M, A, D, gk = pa[0], pa[1], po[2], po[3]
    q1 = min(.9, .57 * (M / po[0]) ** .2); q2 = min(.85, .42 * (A / D) ** .5)
    pg = min(.45, .096 * (A / D) ** .8 * (A / gk) ** .4 * (.73 * 1.25 + .27 * .42))
    return 90 * share * .95 * q1 * q2 * (.984 * pg + .016 * .78) + .1

def rapido(h, a, neutro=False, tipo='liga'):
    """simulação instantânea (jogos sem o usuário). Atualiza estatísticas dos jogadores."""
    (Sh, pwh), (Sa, pwa) = lado_rapido(h), lado_rapido(a)
    ph, pa = pwh[0 if not neutro else 1], pwa[1]
    x, y = ph[0] ** 1.6, pa[0] ** 1.6; sh = x / (x + y)
    gols = [poisson(gols_esperados(ph, pa, sh)), poisson(gols_esperados(pa, ph, 1 - sh))]
    ks = ('t', 'c', 'l') if tipo == 'liga' else ('t', 'c')
    for s, S in ((0, Sh), (1, Sa)):
        gf, ga = gols[s], gols[1 - s]; marc = {}; ast = {}
        c = [(x, sl) for x, sl in zip(S['on'], S['sl']) if sl != 'G']
        if not c: continue
        for _ in range(gf):
            z = R.choices(c, [WSH[sl] * G.P[x]['ovr'] * (1.6 if 'FIN' in G.P[x]['hab'] else 1) for x, sl in c])[0][0]
            marc[z] = marc.get(z, 0) + 1
            if R.random() < .6:
                w = R.choice(c)[0]
                if w != z: ast[w] = ast.get(w, 0) + 1
        res = .3 if gf > ga else -.25 if gf < ga else 0
        for z, sl in zip(S['on'], S['sl']):
            p = G.P[z]; g = marc.get(z, 0); aa = ast.get(z, 0)
            n = 6.15 + R.gauss(0, .45) + res + g * .9 + aa * .5 + (p['ovr'] - 70) * .01
            if sl in 'GD': n += .4 if ga == 0 else -.2 * ga
            n = round(max(3, min(10, n)), 1)
            for k in ks:
                st = p['st'][k]; st[0] += 1; st[1] += g; st[2] += aa; st[3] += n; st[4] += 1
    return gols[0], gols[1]

def poisson(l):
    lim, k, p = math.exp(-l), 0, 1.0
    while True:
        p *= R.random()
        if p < lim: return k
        k += 1

# ------------------------- PARTIDA AO VIVO ---------------------------
def iniciar(tipo, jogos, comp, ko=False, neutro=False, extra=None):
    c = G.coach; meu = c['nt'] if tipo in ('sel', 'cn') else c['club']; ms = []; u = None
    for i, (h, a) in enumerate(jogos):
        m = nova_partida(h, a, tipo, comp, neutro, ko)
        if meu in (h, a): m['us'] = 0 if h == meu else 1; u = i
        ms.append(m)
    if u: ms.insert(0, ms.pop(u)); u = 0
    G.live = dict(tipo=tipo, comp=comp, min=0, ms=ms, u=u, ko=ko, fim=False, ne=0, lv=[-1, -1], extra=extra or {})

def lineups(m):
    out = []
    for s in (0, 1):
        S = m['s'][s]
        out.append([[x, round(ax, 1), dp, G.P[x]['num'], G.P[x]['n'], sl] for x, ax, dp, sl in zip(S['on'], S['ax'], S['dp'], S['sl'])])
    return out

def passo(n):
    L = G.live; frames = []
    if L['fim']: return frames
    um = L['ms'][L['u']] if L['u'] is not None else None
    for _ in range(max(1, min(n, 10))):
        if L['min'] >= 90: break
        L['min'] += 1; t = L['min']
        for m in L['ms']: minuto(m, t, m is um)
        f = dict(min=t, g=[list(m['g']) for m in L['ms']], gols=[i for i, m in enumerate(L['ms']) if m['gm'] == t], ev=[])
        if um:
            f['ev'] = um['ev'][L['ne']:]; L['ne'] = len(um['ev']); f['fr'] = um['fr']
            vs = [um['s'][0]['v'], um['s'][1]['v']]
            if vs != L['lv']: f['lu'] = lineups(um); L['lv'] = vs
            if um.get('pausa'):
                pz = um.pop('pausa')
                if t < 90: f['pausa'] = pz
        frames.append(f)
        if 'pausa' in f: break
    if L['min'] >= 90: encerrar()
    return frames

def resultado_lado(m, s):
    a, b = m['pen'] or m['g']
    if a == b: return 'E'
    return 'V' if (a > b) == (s == 0) else 'D'

def encerrar():
    L = G.live; L['fim'] = True; c = G.coach
    for m in L['ms']:
        if m['ko'] and m['g'][0] == m['g'][1]: penaltis(m)
        a, b = m['pen'] or m['g']; m['w'] = 0 if a > b else 1 if b > a else None
        gravar_stats(m)
        for s in (0, 1):
            S = m['s'][s]; T = G.T[S['t']]
            if T['nac']: continue
            if m['tipo'] == 'liga':
                for x in T['pl']:
                    if G.P[x]['sus'] > 0 and x not in S['used']: G.P[x]['sus'] -= 1
            if eh_usuario(T['id']):
                for x in S['used'] | S['sai']: G.P[x]['cond'] = int(S['en'].get(x, 100))
            G.cache.pop(T['id'], None)
        if m['us'] is not None:
            r = resultado_lado(m, m['us']); c[{'V': 'v', 'E': 'e', 'D': 'd'}[r]] += 1
            eu, ele = G.T[m['t'][m['us']]], G.T[m['t'][1 - m['us']]]
            if not eu['nac']:
                esp = max(.3, min(2.6, 1.35 + (forca(eu) - forca(ele) + (2 if m['us'] == 0 else -2)) * .09))
                pts = {'V': 3, 'E': 1, 'D': 0}[r]; peso = 4 if m['tipo'] == 'liga' else 3
                c['conf'] = max(0, min(100, c['conf'] + (pts - esp) * peso)); c['rep'] = max(1, min(99, c['rep'] + (pts - esp) * .25))
            else:
                c['rep'] = max(1, min(99, c['rep'] + {'V': .8, 'E': .1, 'D': -.6}[r]))
            arquivar(m)
    concluir_evento(L)

def arquivar(m):
    """guarda o relatório completo da partida do usuário (para rever na Agenda)"""
    G.narq += 1; k = 'j%d' % G.narq; G.arq[k] = relatorio(m); m['arq'] = k; G.ult = k
    if len(G.arq) > 160: del G.arq[min(G.arq, key=lambda z: int(z[1:]))]
    return k
