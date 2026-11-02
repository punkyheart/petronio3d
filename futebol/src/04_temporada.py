# ----------------------- TEMPORADA E CALENDARIO ----------------------
def noticia(txt, tipo='info', of=None):
    G.nmsg += 1; G.msgs.insert(0, dict(id=G.nmsg, d=G.hoje, x=txt, k=tipo, lida=False, of=of)); del G.msgs[80:]

def liga_usuario():
    c = G.coach; T = G.T.get(c['club']) if c and c['club'] else None
    return G.L[T['lg']] if T and T['lg'] is not None else None

def turno(ids):
    ids = ids[:]; R.shuffle(ids)
    if len(ids) % 2: ids.append(None)
    n = len(ids); rodadas = []
    for r in range(n - 1):
        rd = [(ids[i], ids[n-1-i]) if r % 2 == 0 else (ids[n-1-i], ids[i]) for i in range(n // 2)]
        rodadas.append([j for j in rd if j[0] and j[1]]); ids = [ids[0], ids[-1]] + ids[1:-1]
    return rodadas

def agendar_liga(L, ini):
    rodadas = turno(L['clubs'])
    if len(L['clubs']) <= 20: rodadas += [[(b, a) for a, b in rd] for rd in rodadas]   # turno e returno
    d0 = proximo_dia(ini, 6)
    L['fx'] = [dict(d=d0 + 7 * i, j=rd, ok=False) for i, rd in enumerate(rodadas)]; L['r'] = 0
    L['ini_o'] = d0; L['fim_o'] = L['fx'][-1]['d']; L['res'] = {}; L['tab'] = {t: [0] * 7 for t in L['clubs']}
    y = ano_de(d0); L['temp'] = '%d/%s' % (y, str(y + 1)[2:]) if dt.date.fromordinal(d0).month >= 7 else str(y)

def inicio_ciclo(L):
    """primeira rodada da temporada: zera estatísticas e sorteia a copa nacional"""
    for t in L['clubs']:
        for x in G.T[t]['pl']: G.P[x]['st']['t'] = st0(); G.P[x]['st']['l'] = st0()
    C = G.C.get(L['cc'])
    if C and next(x for x in G.L if x['cc'] == L['cc']) is L:
        while C['rd'] and not C.get('ok'): rodada_copa_rapida(C)
        agendar_copa(C, L)
    if liga_usuario() is L:
        G.coach['conf'] = max(G.coach['conf'], 50); noticia('Começa a temporada %s da %s!' % (L['temp'], L['n']))

def classificacao(L):
    tb = L['tab']; return sorted(L['clubs'], key=lambda t: (-tb[t][6], -(tb[t][4] - tb[t][5]), -tb[t][4], G.T[t]['n']))

def moral(T, saldo, adv=None):
    T['mor'] = max(25, min(100, T['mor'] + (7 if saldo > 0 else 1 if saldo == 0 else -6)))
    dif = (forca(adv) - forca(T)) if adv else 0
    T['tor'] = max(15, min(100, T.get('tor', 60) + (3 + (2 if dif > 3 else 0) if saldo > 0 else -3 - (2 if dif < -3 else 0) if saldo < 0 else 0)))

def publico(h, a, neutro=False):
    T, O = G.T[h], G.T[a]
    if T['nac'] or neutro or 'est' not in T:
        pub = int(min(70000, 15000 + (forca(T) + forca(O) - 120) * 900 * R.uniform(.8, 1.1))); return max(5000, pub), int(max(5000, pub) * .045)
    e = T['est']; s = T['str']
    dem = (3000 + 1.08 ** (s - 40) * 2600) * (.55 + .8 * T.get('tor', 60) / 100) * max(.6, 1 + (forca(O) - forca(T)) / 60)
    dem *= (e['ref'] / max(.5, e['preco'])) ** 1.1 * R.uniform(.9, 1.08)
    pub = int(max(300, min(e['cap'], dem))); return pub, int(pub * e['preco'] / 1000)

def registrar(L, h, a, gh, ga, pub=0, renda=0, arq=None):
    for t, gp, gc in ((L['tab'][h], gh, ga), (L['tab'][a], ga, gh)):
        t[0] += 1; t[4] += gp; t[5] += gc
        if gp > gc: t[1] += 1; t[6] += 3
        elif gp == gc: t[2] += 1; t[6] += 1
        else: t[3] += 1
    L['res'][(h, a)] = (gh, ga, pub, renda, arq)
    moral(G.T[h], gh - ga, G.T[a]); moral(G.T[a], ga - gh, G.T[h])
    receita_usuario(h, renda)

def receita_usuario(h, renda):
    c = G.coach
    if c and h == c['club'] and renda: G.T[h]['bud'] += renda

def jogar_rodada_rapida(L, r):
    rd = L['fx'][r]
    for h, a in rd['j']:
        gh, ga = rapido(h, a); pub, renda = publico(h, a); registrar(L, h, a, gh, ga, pub, renda)
    rd['ok'] = True; L['r'] = r + 1
    if L['r'] >= len(L['fx']): fim_liga(L)

def fim_liga(L):
    c = G.coach; tb = classificacao(L); camp = G.T[tb[0]]
    L['champ'].append((L['temp'], camp['n']))
    art = sorted([G.P[x] for t in L['clubs'] for x in G.T[t]['pl']], key=lambda p: -p['st']['l'][1])[:5]
    L['ult'] = dict(temp=L['temp'], tab=[(t, list(L['tab'][t])) for t in tb], art=[(p['n'], G.T[p['club']]['n'], p['st']['l'][1]) for p in art])
    if camp.get('tec') in G.TEC: G.TEC[camp['tec']]['tit'] += 1
    for t in tb[-2:]:                                   # clubes da IA trocam de técnico
        if not eh_usuario(t): trocar_tecnico_ia(G.T[t])
    if c['club'] in L['clubs']:
        T = G.T[c['club']]; pos = tb.index(T['id']) + 1
        esp = sorted(L['clubs'], key=lambda t: -forca(G.T[t])).index(T['id']) + 1
        c['rep'] = max(1, min(99, c['rep'] + max(-10, min(12, (esp - pos) * 1.2)) + (8 if pos == 1 else 0)))
        T['bud'] += int(T['rev'] * 8 * (len(tb) - pos + 1) / len(tb))
        c['hist'].append(dict(s=L['temp'], t=T['n'], l=L['n'], pos=pos, pts=L['tab'][T['id']][6], tit=pos == 1))
        if pos == 1: c['tit'].append('%s %s (%s)' % (L['n'], L['temp'], T['n']))
        noticia(('🏆 CAMPEÃO! ' if pos == 1 else '') + '%s terminou a %s %s em %dº lugar (expectativa: %dº).' % (T['n'], L['n'], L['temp'], pos, esp), 'bom' if pos <= esp else 'info')
        if pos > esp + 5 and c['conf'] < 45:
            noticia('A diretoria do %s não renovou com você.' % T['n'], 'mau'); sair_do_clube()
    agendar_liga(L, od(ano_de(L['ini_o']) + 1, L['ini']))

# ------------------------------- COPAS -------------------------------
def fase_nome(n, k):
    return {2: 'Final', 4: 'Semifinal', 8: 'Quartas de final', 16: 'Oitavas de final', 32: '16 avos de final'}.get(n, '%dª fase' % (k + 1))

def agendar_copa(C, L):
    times = [t for X in G.L if X['cc'] == C['cc'] for t in X['clubs']] + [T['id'] for T in clubes() if T['lg'] is None and T.get('cup') == C['cc']]
    n = len(times); size = 1 << (n - 1).bit_length()
    ordem = sorted(times, key=lambda t: -G.T[t]['str']); byes = ordem[:size - n]; resto = ordem[size - n:]
    nrod = int(math.log2(size)); esp = max(3, min(6, (len(L['fx']) - 6) // max(1, nrod)))
    C.update(temp=L['temp'], vivos=list(byes), rd=[], ok=False, d0=L['ini_o'], esp=esp, times=times, size=size)
    C['rd'].append(rodada_copa(C, resto if resto else ordem, 0))

def rodada_copa(C, times, k):
    times = list(times); R.shuffle(times)
    return dict(d=proximo_dia(C['d0'] + 7 * (4 + C['esp'] * k), 2), j=[(times[i], times[i + 1]) for i in range(0, len(times) - 1, 2)],
                ok=False, r=[], nome=fase_nome(C['size'] >> k, k))

def vencedor_ko(h, a, gh, ga, pen):
    if gh != ga: return h if gh > ga else a
    return h if pen[0] > pen[1] else a

def pen_rapido():
    a = sum(R.random() < .75 for _ in range(5)); b = sum(R.random() < .75 for _ in range(5))
    while a == b: a += R.random() < .75; b += R.random() < .75
    return [a, b]

def rodada_copa_rapida(C):
    rd = C['rd'][-1]; rd['r'] = []
    for h, a in rd['j']:
        gh, ga = rapido(h, a, tipo='copa'); pen = pen_rapido() if gh == ga else None
        pub, renda = publico(h, a); receita_usuario(h, renda)
        rd['r'].append((gh, ga, pen, pub, renda, None))
    concluir_rodada_copa(C)

def concluir_rodada_copa(C):
    rd = C['rd'][-1]; rd['ok'] = True; c = G.coach
    venc = [vencedor_ko(h, a, r[0], r[1], r[2]) for (h, a), r in zip(rd['j'], rd['r'])]
    if c and c['club']:
        for (h, a), w in zip(rd['j'], venc):
            if c['club'] in (h, a) and w != c['club']:
                noticia('%s foi eliminado da %s (%s).' % (G.T[c['club']]['n'], C['n'], rd['nome']), 'mau')
    vivos = C['vivos'] + venc; C['vivos'] = []
    if len(vivos) == 1:
        T = G.T[vivos[0]]; C['ok'] = True; C['champ'].append((C['temp'], T['n']))
        noticia('🏆 %s conquista a %s %s!' % (T['n'], C['n'], C['temp']), 'bom' if eh_usuario(T['id']) else 'info')
        if c and vivos[0] == c['club']:
            c['rep'] = min(99, c['rep'] + 5); T['bud'] += T['rev'] * 4; c['tit'].append('%s %s (%s)' % (C['n'], C['temp'], T['n']))
        if T.get('tec') in G.TEC: G.TEC[T['tec']]['tit'] += 1
        return
    C['rd'].append(rodada_copa(C, vivos, len(C['rd'])))

# ------------------------- SELECOES NACIONAIS ------------------------
def montar_cn():
    for T in selecoes():
        if not eh_usuario(T['id']): convocar_auto(T)
    top = sorted(selecoes(), key=lambda T: -forca(T))[:16]
    ordem = [0, 15, 7, 8, 3, 12, 4, 11, 1, 14, 6, 9, 2, 13, 5, 10]; y = ano_de(G.hoje)
    G.cn = dict(ano=y, vivos=[top[i]['id'] for i in ordem], rd=[], ok=False)
    rodada_cn(); noticia('Sorteio da Copa das Nações %d: as 16 melhores seleções já conhecem seus adversários.' % y)

def rodada_cn():
    k = len(G.cn['rd']); t = G.cn['vivos']
    G.cn['rd'].append(dict(d=od(G.cn['ano'], DATAS_CN[k]), j=list(zip(t[0::2], t[1::2])), ok=False, r=[], nome=FASES_CN[k]))

def rodada_cn_rapida():
    rd = G.cn['rd'][-1]; rd['r'] = []
    for h, a in rd['j']:
        gh, ga = rapido(h, a, True, 'cn'); rd['r'].append((gh, ga, pen_rapido() if gh == ga else None, 0, 0, None))
    concluir_rodada_cn()

def concluir_rodada_cn():
    rd = G.cn['rd'][-1]; rd['ok'] = True; c = G.coach
    venc = [vencedor_ko(h, a, r[0], r[1], r[2]) for (h, a), r in zip(rd['j'], rd['r'])]
    if c['nt'] in G.cn['vivos'] and c['nt'] not in venc:
        noticia(('%s ficou com o vice da Copa das Nações.' if rd['nome'] == 'Final' else '%s foi eliminada da Copa das Nações (' + rd['nome'] + ').') % G.T[c['nt']]['n'], 'mau')
    G.cn['vivos'] = venc
    if len(venc) == 1:
        T = G.T[venc[0]]; G.cn['ok'] = True; G.cnhist.append((G.cn['ano'], T['n']))
        noticia('🏆 %s é campeã da Copa das Nações %d!' % (T['n'], G.cn['ano']), 'bom')
        if venc[0] == c['nt']:
            c['rep'] = min(99, c['rep'] + 15); c['tit'].append('Copa das Nações %d (%s)' % (G.cn['ano'], T['n']))
        return
    rodada_cn()

def agendar_amistosos():
    c = G.coach
    if not c or not c['nt']: return
    ns = sorted(selecoes(), key=lambda T: -forca(T)); ids = [T['id'] for T in ns]; i = ids.index(c['nt'])
    for y in (ano_de(G.hoje), ano_de(G.hoje) + 1):
        for md in DATAS_FIFA:
            d = od(y, md)
            if G.hoje <= d <= G.hoje + 400 and d not in G.ntopp:
                G.ntopp[d] = dict(adv=R.choice([x for x in ids[max(0, i - 8): i + 9] if x != c['nt']]), casa=R.random() < .5, ok=False, r=None, nt=c['nt'])

# ---------------------------- DIA A DIA ------------------------------
def processar_dia(d, pular=()):
    for L in G.L:
        r = L['r']
        if r < len(L['fx']) and L['fx'][r]['d'] == d:
            if r == 0: inicio_ciclo(L)
            if ('liga', L['i'], r) not in pular: jogar_rodada_rapida(L, r)
    for C in G.C.values():
        if C['rd'] and not C['rd'][-1]['ok'] and C['rd'][-1]['d'] == d and ('copa', C['cc'], len(C['rd']) - 1) not in pular:
            rodada_copa_rapida(C)
    if G.cn and not G.cn['ok'] and G.cn['rd'][-1]['d'] == d and ('cn', len(G.cn['rd']) - 1) not in pular: rodada_cn_rapida()
    md = dt.date.fromordinal(d).strftime('%m-%d')
    if md == '07-01': anual()
    if md == '06-01': montar_cn()
    for p in G.P.values():
        if p['inj']: p['inj'] = max(0, p['inj'] - 1)
        if p['cond'] < 100: p['cond'] = min(100, p['cond'] + 3)
    if dia_sem(d) == 0: semanal(d)

def avancar_ate(alvo, pular=()):
    while G.hoje < alvo:
        G.hoje += 1; processar_dia(G.hoje, pular)

def semanal(d):
    c = G.coach
    for p in list(G.P.values()):
        if p['emp'] and p['empf'] <= d:                                    # fim de empréstimo
            O = p['emp']; p['emp'] = None
            if O in G.T: mover_jogador(p, O); noticia('%s voltou de empréstimo.' % p['n']) if O == c['club'] else None
        elif p['ct'] < d and not p['jr']:                                   # contrato vencido
            T = G.T.get(p['club'])
            if T and T['id'] == c['club']:
                dest = R.choice([C for C in clubes() if C['lg'] is not None and C['id'] != T['id'] and abs(C['str'] - p['ovr']) < 8] or clubes())
                mover_jogador(p, dest['id']); p['ct'] = od(ano_de(d) + R.randint(1, 3), '06-30')
                noticia('%s saiu de graça para o %s: o contrato terminou.' % (p['n'], dest['n']), 'mau')
            else:
                p['ct'] = od(ano_de(d) + R.randint(1, 3), '06-30')
    if c['club']:
        T = G.T[c['club']]
        T['bud'] += T['rev'] - folha(T)
        for x in T['pl']:
            p = G.P[x]
            if not p['aviso'] and p['ct'] - d <= 120 and not p['emp']:
                p['aviso'] = True; noticia('O contrato de %s termina em %s. Renove na ficha do jogador.' % (p['n'], fdata(p['ct'])))
        L = liga_usuario()
        if L and L['r'] >= 6 and c['conf'] < 12:
            noticia('A diretoria do %s demitiu você após a sequência de maus resultados.' % T['n'], 'mau')
            sair_do_clube(); c['rep'] = max(1, c['rep'] - 6)
    c['ofs'] = [o for o in c['ofs'] if o['w'] >= d]
    if R.random() < (.35 if not c['club'] else .05): gerar_proposta()
    if not c['nt'] and c['rep'] >= 45 and R.random() < .03: gerar_proposta(sel=True)

def folha(T): return sum(G.P[x]['sal'] for x in T['pl'] if not G.P[x]['emp'])

def anual():
    c = G.coach; aposentados = 0; G.cache.clear()
    for p in list(G.P.values()):
        p['age'] += 1; a = p['age']
        if a <= 23: p['ovr'] = min(max(p['pot'], p['ovr']), p['ovr'] + R.randint(1, 5 if not p['jr'] else 7))
        elif a <= 29: p['ovr'] = min(max(p['pot'], p['ovr']), p['ovr'] + R.randint(-1, 2))
        elif a <= 32: p['ovr'] -= R.randint(0, 3); p['fis'] -= R.randint(0, 3)
        else: p['ovr'] -= R.randint(1, 5); p['fis'] -= R.randint(1, 4)
        p['ovr'] = max(30, min(95, p['ovr'])); p['fis'] = max(30, p['fis'])
        p['pot'] = p['ovr'] if a >= 30 else max(p['pot'], p['ovr'])
        if not p['jr'] and (a >= 38 or (a >= 34 and R.random() < .4)): aposentar(p); aposentados += 1
        else: valor(p)
    for T in G.T.values():
        if T['nac']:
            T['pl'] = [x for x in T['pl'] if x in G.P]
            if T['id'] != c['nt'] or len(T['pl']) < 16: convocar_auto(T)
        else:
            if T['id'] != c['club']: auto_xi(T)
            else: validar_xi(T)
            T['str'] = round(forca(T))
    if c['club']: juniores_anual(G.T[c['club']])
    noticia('Virada do ano esportivo: %d jogadores se aposentaram e novas promessas surgiram.' % aposentados)
    agendar_amistosos()

def aposentar(p):
    T = G.T.get(p['club'])
    for N in selecoes():
        if p['id'] in N['pl']: tirar_do_xi(N, p['id']); N['pl'].remove(p['id'])
    if not T: G.P.pop(p['id'], None); return
    if p['id'] in T['pl']: T['pl'].remove(p['id'])
    O = G.T.get(p['emp']) if p['emp'] else None
    if O and p['id'] in O['pl']: O['pl'].remove(p['id'])
    D = O or T; cc = D['cc']
    nat = cc if R.random() < LOCAL.get(cc, .72) else R.choice([x[:2] for x in ESTRANG.split()])
    q = novo_jogador(p['pos'], R.gauss(D['str'] - 12, 4), nat, D['id'], age=R.randint(17, 19))
    q['pot'] = min(97, q['ovr'] + R.randint(8, 26)); valor(q); D['pl'].append(q['id']); q['num'] = numero_livre(D, q['pos'])
    if p['id'] in D['xi']: D['xi'][D['xi'].index(p['id'])] = q['id']
    if p['id'] in T['xi']: tirar_do_xi(T, p['id'])
    G.P.pop(p['id'], None)

# ------------------------------ JUNIORES -----------------------------
def novo_junior(T, idade=None):
    pos = R.choice(POSICOES); cc = T['cc'] if R.random() < .85 else R.choice([x[:2] for x in ESTRANG.split()])
    p = novo_jogador(pos, R.gauss(T['str'] - 24, 5), cc, T['id'], age=idade or R.randint(15, 18), jr=True)
    p['pot'] = min(95, p['ovr'] + R.randint(14, 36)); p['sal'] = 1; p['val'] = max(20, p['val']); p['ct'] = od(ano_de(G.hoje) + 3, '06-30')
    p['st'] = {'t': st0(), 'l': st0(), 'c': st0()}; T['jr'].append(p['id'])

def juniores_inicio(T):
    while len(T['jr']) < 8: novo_junior(T)

def juniores_anual(T):
    for x in list(T['jr']):
        p = G.P.get(x)
        if not p: T['jr'].remove(x); continue
        if p['age'] >= 19:
            T['jr'].remove(x); del G.P[x]; noticia('%s (juniores, %d anos) deixou o clube por idade.' % (p['n'], p['age']))
    for _ in range(4): novo_junior(T, R.randint(15, 16))

# --------------------------- TECNICOS / CARREIRA ---------------------
def trocar_tecnico_ia(T):
    velho = G.TEC.get(T.get('tec'))
    if velho: velho['t'] = None
    livres = [x for x in G.TEC.values() if x['t'] is None and x['id'] != (velho or {}).get('id')]
    novo = max(R.sample(livres, min(6, len(livres))), key=lambda x: x['rep']) if livres else G.TEC[novo_tecnico(T['cc'], T['str'] - 25)]
    novo['t'] = T['id']; T['tec'] = novo['id']

def sair_do_clube():
    c = G.coach
    if not c['club']: return
    T = G.T[c['club']]; c['club'] = None
    for x in T['jr']: G.P.pop(x, None)
    T['jr'] = []; trocar_tecnico_ia(T); auto_xi(T)

def assumir_clube(T):
    c = G.coach
    if c['club']: noticia('Você deixou o %s.' % G.T[c['club']]['n']); sair_do_clube()
    c['club'] = T['id']; c['conf'] = 60; velho = G.TEC.get(T.get('tec'))
    if velho: velho['t'] = None
    T['tec'] = 'eu'; auto_xi(T); juniores_inicio(T)

def assumir_selecao(T):
    c = G.coach
    if c['nt']: N = G.T[c['nt']]; trocar_tecnico_ia(N)
    velho = G.TEC.get(T.get('tec'))
    if velho: velho['t'] = None
    c['nt'] = T['id']; T['tec'] = 'eu'; convocar_auto(T); agendar_amistosos()

def gerar_proposta(sel=False):
    c = G.coach; rep = c['rep']
    if sel:
        cand = [T for T in selecoes() if T['id'] != c['nt'] and 45 + rep * .25 <= forca(T) <= 55 + rep * .35]
    else:
        mx = 60 + rep * .32
        cand = [T for T in clubes() if T['lg'] is not None and T['id'] != c['club'] and mx - 10 <= T['str'] <= mx]
    if not cand: return
    T = R.choice(cand)
    if any(o['t'] == T['id'] for o in c['ofs']): return
    o = dict(t=T['id'], tipo='sel' if sel else 'clube', w=G.hoje + 28); c['ofs'].append(o)
    noticia('Proposta: %s quer você como técnico! Responda em Mensagens.' % T['n'], 'bom', of=T['id'])

# ---------------------------- PROXIMO EVENTO -------------------------
def eventos_usuario():
    c = G.coach; evs = []
    if c['club']:
        T = G.T[c['club']]
        if T['lg'] is not None:
            L = G.L[T['lg']]; r = L['r']
            if r < len(L['fx']):
                jj = [j for j in L['fx'][r]['j'] if c['club'] in j]
                if jj: evs.append((L['fx'][r]['d'], 0, dict(tipo='liga', k=('liga', L['i'], r), h=jj[0][0], a=jj[0][1], comp='%s · %dª rodada' % (L['n'], r + 1))))
        C = G.C.get(T['cup'])
        if C and C['rd'] and not C['rd'][-1]['ok']:
            rd = C['rd'][-1]; jj = [j for j in rd['j'] if c['club'] in j]
            if jj: evs.append((rd['d'], 1, dict(tipo='copa', k=('copa', C['cc'], len(C['rd']) - 1), h=jj[0][0], a=jj[0][1], comp='%s · %s' % (C['n'], rd['nome']))))
    if c['nt']:
        if G.cn and not G.cn['ok']:
            rd = G.cn['rd'][-1]; jj = [j for j in rd['j'] if c['nt'] in j]
            if jj: evs.append((rd['d'], 2, dict(tipo='cn', k=('cn', len(G.cn['rd']) - 1), h=jj[0][0], a=jj[0][1], comp='Copa das Nações · ' + rd['nome'])))
        for d in sorted(G.ntopp):
            e = G.ntopp[d]
            if d >= G.hoje and not e['ok'] and e['nt'] == c['nt']:
                h, a = (c['nt'], e['adv']) if e['casa'] else (e['adv'], c['nt'])
                evs.append((d, 3, dict(tipo='sel', k=('sel', d), h=h, a=a, comp='Amistoso internacional (Data FIFA)'))); break
    evs = [e for e in evs if e[0] >= G.hoje]
    return sorted(evs, key=lambda e: (e[0], e[1]))

def proximo():
    evs = eventos_usuario()
    if not evs: return dict(tipo='semana', k=None, d=G.hoje + 7, comp='Sem jogos marcados: avançar uma semana')
    d, _, e = evs[0]; e['d'] = d; return e

def concluir_evento(L):
    ex = L['extra']; k = ex.get('k')
    if L['tipo'] == 'liga':
        Lg = G.L[k[1]]; r = k[2]
        for m in L['ms']:
            h, a = m['t']; registrar(Lg, h, a, m['g'][0], m['g'][1], m['pub'][0], m['pub'][1], m.get('arq'))
        Lg['fx'][r]['ok'] = True; Lg['r'] = r + 1
        if Lg['r'] >= len(Lg['fx']): fim_liga(Lg)
    elif L['tipo'] in ('copa', 'cn'):
        rd = G.C[k[1]]['rd'][-1] if L['tipo'] == 'copa' else G.cn['rd'][-1]
        rs = {tuple(m['t']): m for m in L['ms']}; rd['r'] = []
        for j in rd['j']:
            m = rs[tuple(j)]
            if L['tipo'] == 'copa': receita_usuario(j[0], m['pub'][1])
            rd['r'].append((m['g'][0], m['g'][1], m['pen'], m['pub'][0], m['pub'][1], m.get('arq')))
        concluir_rodada_copa(G.C[k[1]]) if L['tipo'] == 'copa' else concluir_rodada_cn()
    elif L['tipo'] == 'sel':
        m = L['ms'][0]; e = G.ntopp[k[1]]; e['ok'] = True; e['r'] = (m['g'][0], m['g'][1], m['pub'][0], m.get('arq'))

def iniciar_jogo_usuario(pr):
    k = pr['k']
    if pr['tipo'] == 'liga':
        Lg = G.L[k[1]]; iniciar('liga', Lg['fx'][k[2]]['j'], pr['comp'], extra=dict(k=k))
    elif pr['tipo'] == 'copa':
        iniciar('copa', G.C[k[1]]['rd'][-1]['j'], pr['comp'], ko=True, extra=dict(k=k))
    elif pr['tipo'] == 'cn':
        iniciar('cn', G.cn['rd'][-1]['j'], pr['comp'], ko=True, neutro=True, extra=dict(k=k))
    else:
        iniciar('sel', [(pr['h'], pr['a'])], pr['comp'], extra=dict(k=k))

def simular_pendente(k):
    """se o evento do usuário deixou de valer (demissão etc.), simula normalmente"""
    if not k: return
    if k[0] == 'liga':
        L = G.L[k[1]]
        if L['r'] == k[2]: jogar_rodada_rapida(L, k[2])
    elif k[0] == 'copa':
        C = G.C[k[1]]
        if len(C['rd']) - 1 == k[2] and not C['rd'][-1]['ok']: rodada_copa_rapida(C)
    elif k[0] == 'cn':
        if G.cn and not G.cn['ok'] and len(G.cn['rd']) - 1 == k[1]: rodada_cn_rapida()

# ------------------------------ INICIO -------------------------------
def preparar_calendario(lg_usuario):
    """define a data inicial (1 semana antes da 1ª rodada da liga do usuário) e coloca cada liga no ponto certo"""
    ref = od(ANO_BASE, '07-01')
    s = od(ANO_BASE, G.L[lg_usuario]['ini'])
    if s < ref: s = od(ANO_BASE + 1, G.L[lg_usuario]['ini'])
    G.hoje = proximo_dia(s, 6) - 7; y = ano_de(G.hoje)
    for L in G.L:
        nr = (len(L['clubs']) - 1) * (2 if len(L['clubs']) <= 20 else 1)
        ini = od(y, L['ini'])
        if ini > G.hoje:
            prev = od(y - 1, L['ini'])
            if proximo_dia(prev, 6) + 7 * (nr - 1) >= G.hoje: ini = prev
        elif proximo_dia(ini, 6) + 7 * (nr - 1) < G.hoje: ini = od(y + 1, L['ini'])
        agendar_liga(L, ini)
    # simula o que já aconteceu antes da data inicial (só partidas)
    d0 = min(L['ini_o'] for L in G.L); hoje = G.hoje
    for d in range(d0, hoje + 1):
        for L in G.L:
            r = L['r']
            if r < len(L['fx']) and L['fx'][r]['d'] == d:
                if r == 0: inicio_ciclo(L)
                jogar_rodada_rapida(L, r)
        for C in G.C.values():
            if C['rd'] and not C['rd'][-1]['ok'] and C['rd'][-1]['d'] == d: rodada_copa_rapida(C)
    G.base = G.hoje; G.iniciado = True
