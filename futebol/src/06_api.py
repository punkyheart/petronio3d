# ------------------------------ API ----------------------------------
API = {}
def acao(f): API[f.__name__[2:]] = f; return f

def time_do(d):
    c = G.coach; tid = c['nt'] if d.get('t') == 'sel' else c['club']
    if not tid: raise ValueError('Você não comanda esse time no momento.')
    return G.T[tid]

def sem_live():
    if G.live and not G.live['fim']: raise ValueError('Termine a partida em andamento primeiro.')

def sl_de(T):
    if len(T['xi']) == 11: return slots(T['form'])
    T['xi'], sl = arrumar(T['xi'], T['form']); return sl

def craques(T):
    top = sorted(T['pl'], key=lambda x: -G.P[x]['ovr'])[:3]
    return [x for x in top if G.P[x]['ovr'] >= forca(T) + 2]

@acao
def a_meta(d):
    return dict(save=os.path.exists(SAVE), dados=[os.path.basename(x) for x in IMPORTADOS],
                ligas=[dict(i=L['i'], n=L['n'], pais=PAISES[L['cc']][0], fl=bandeira(L['cc']),
                            clubs=[dict(id=t, n=G.T[t]['n'], f=G.T[t]['str'], sig=G.T[t]['sig'], cor=G.T[t]['cor']) for t in L['clubs']]) for L in G.L],
                sels=[dict(id=T['id'], n=T['n'], fl=bandeira(T['cc']), f=forca(T)) for T in sorted(selecoes(), key=lambda T: -forca(T))])

@acao
def a_novo(d):
    if G.iniciado or G.coach: gerar_mundo()
    T = G.T.get(d.get('clube'))
    if not T or T['nac'] or T['lg'] is None: raise ValueError('Escolha um clube.')
    G.coach = dict(n=(d.get('nome') or 'Técnico').strip()[:30], rep=50, club=None, nt=None, conf=60, v=0, e=0, d=0, hist=[], ofs=[], tit=[])
    assumir_clube(T); preparar_calendario(T['lg'])
    if d.get('sel') in G.T and G.T[d['sel']]['nac']: assumir_selecao(G.T[d['sel']])
    noticia('Bem-vindo, %s! Você é o novo técnico do %s%s. A temporada começa em %s.' % (G.coach['n'], T['n'],
            (' e da seleção da ' + G.T[G.coach['nt']]['n']) if G.coach['nt'] else '', fdata(liga_usuario()['ini_o'])), 'bom')
    return a_estado(d)

@acao
def a_estado(d):
    if not G or not G.coach: return dict(jogo=False)
    c = G.coach; T = G.T.get(c['club']) if c['club'] else None; pr = proximo()
    meu = c['nt'] if pr['tipo'] in ('sel', 'cn') else c['club']
    out = dict(jogo=True, live=bool(G.live and not G.live['fim']), data=fdata(G.hoje), dsem=['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][dia_sem(G.hoje)],
               tecnico=dict(n=c['n'], rep=round(c['rep']), conf=round(c['conf']), v=c['v'], e=c['e'], d=c['d']),
               clube=jt(T) if T else None, sel=jt(G.T[c['nt']]) if c['nt'] else None, nmsg=sum(1 for x in G.msgs if not x['lida']),
               prox=dict(tipo=pr['tipo'], comp=pr['comp'], data=fdata(pr['d']), h=jt(G.T[pr['h']]) if 'h' in pr else None,
                         a=jt(G.T[pr['a']]) if 'a' in pr else None, casa=pr.get('h') == meu), ult=G.ult,
               ofs=[dict(t=jt(G.T[o['t']]), tipo=o['tipo'], liga=G.L[G.T[o['t']]['lg']]['n'] if o['tipo'] == 'clube' else 'Seleção nacional') for o in c['ofs']])
    if T:
        L = liga_usuario(); pos = classificacao(L).index(T['id']) + 1 if L else 0
        out.update(bud=T['bud'], tor=T['tor'], mor=T['mor'], liga=L['n'] if L else '', temp=L['temp'] if L else '', pos=pos,
                   nel=len(T['pl']), folha=folha(T), rev=T['rev'])
    return out

@acao
def a_elenco(d):
    T = time_do(d)
    if not (G.live and not G.live['fim']): validar_xi(T)
    sl = sl_de(T); emp = [p for p in G.P.values() if p['emp'] == T['id']] if not T['nac'] else []
    pl = [jp(G.P[x]) for x in sorted(T['pl'], key=lambda x: (POSICOES.index(G.P[x]['pos']), -G.P[x]['ovr']))]
    return dict(t=jt(T), nac=T['nac'], form=T['form'], tac=T['tac'], xi=T['xi'], sl=sl, forms=list(FORMS), pl=pl,
                emp=[jp(p) for p in emp], craques=craques(T), n=len(T['pl']))

@acao
def a_jogador(d):
    p = G.P.get(int(d['pid']))
    if not p: raise ValueError('Jogador não encontrado.')
    out = jp(p); c = G.coach
    out['meu'] = p['club'] == c['club'] or p['emp'] == c['club']; out['craque'] = p['club'] in G.T and p['id'] in craques(G.T[p['club']])
    return out

@acao
def a_trocar(d):
    sem_live(); T = time_do(d); xi = T['xi']; a, b = d['a'], d['b']
    if a not in T['pl'] or b not in T['pl']: raise ValueError('Jogador inválido.')
    if a in xi and b in xi: i, j = xi.index(a), xi.index(b); xi[i], xi[j] = xi[j], xi[i]
    elif a in xi or b in xi:
        x, y = (a, b) if a in xi else (b, a)
        if not disp(y, T['nac']): raise ValueError('%s está indisponível (lesão/suspensão).' % G.P[y]['n'])
        xi[xi.index(x)] = y
    return a_elenco(d)

@acao
def a_escalar(d):
    sem_live(); T = time_do(d)
    if d.get('form') in FORMS and d['form'] != T['form']:
        T['form'] = d['form']; T['xi'] = arrumar(T['xi'], T['form'])[0] if T['xi'] else T['xi']
    if d.get('tac') in TATICAS: T['tac'] = d['tac']
    return a_elenco(d)

@acao
def a_auto(d):
    sem_live(); auto_xi(time_do(d)); return a_elenco(d)

# ------------------------------ AGENDA -------------------------------
def linha_ag(d, h, a, comp, res=None, pub=None, renda=None, arq=None, pen=None, tipo='clube'):
    return dict(d=fdata(d), o=d, h=jt(G.T[h]) if h else None, a=jt(G.T[a]) if a else None, comp=comp, res=res, pen=pen,
                pub=pub, renda=renda, arq=arq, tipo=tipo)

@acao
def a_agenda(d):
    c = G.coach; rows = []; f = d.get('f') or 'todos'
    if c['club']:
        T = G.T[c['club']]; L = liga_usuario()
        if L:
            for rd in L['fx']:
                for h, a in rd['j']:
                    if T['id'] in (h, a):
                        r = L['res'].get((h, a))
                        rows.append(linha_ag(rd['d'], h, a, L['n'], [r[0], r[1]] if r else None, r[2] if r else None, r[3] if r else None, r[4] if r else None))
        C = G.C.get(T['cup'])
        if C:
            for rd in C['rd']:
                for i, (h, a) in enumerate(rd['j']):
                    if T['id'] in (h, a):
                        r = rd['r'][i] if rd['ok'] and i < len(rd['r']) else None
                        rows.append(linha_ag(rd['d'], h, a, '%s · %s' % (C['n'], rd['nome']), [r[0], r[1]] if r else None,
                                             r[3] if r else None, r[4] if r else None, r[5] if r else None, r[2] if r else None))
            if not C.get('ok') and T['id'] in C['vivos']:
                rows.append(linha_ag(proximo_dia(C['d0'] + 7 * (4 + C['esp'] * len(C['rd'])), 2), T['id'], None, '%s · próxima fase' % C['n']))
    if c['nt']:
        for dd in sorted(G.ntopp):
            e = G.ntopp[dd]
            if e['nt'] != c['nt']: continue
            h, a = (c['nt'], e['adv']) if e['casa'] else (e['adv'], c['nt'])
            r = e['r']; rows.append(linha_ag(dd, h, a, 'Amistoso internacional', [r[0], r[1]] if r else None, r[2] if r else None, None, r[3] if r else None, tipo='sel'))
        if G.cn:
            for rd in G.cn['rd']:
                for i, (h, a) in enumerate(rd['j']):
                    if c['nt'] in (h, a):
                        r = rd['r'][i] if rd['ok'] and i < len(rd['r']) else None
                        rows.append(linha_ag(rd['d'], h, a, 'Copa das Nações · ' + rd['nome'], [r[0], r[1]] if r else None, r[3] if r else None,
                                             None, r[5] if r else None, r[2] if r else None, tipo='sel'))
    comps = sorted({r['comp'].split(' · ')[0] for r in rows})
    if f == 'clube': rows = [r for r in rows if r['tipo'] == 'clube']
    elif f == 'sel': rows = [r for r in rows if r['tipo'] == 'sel']
    elif f != 'todos': rows = [r for r in rows if r['comp'].split(' · ')[0] == f]
    rows.sort(key=lambda r: r['o'])
    return dict(rows=rows, comps=comps, hoje=G.hoje, titulo=(G.T[c['club']]['n'] if c['club'] else '') + (' / ' + G.T[c['nt']]['n'] if c['nt'] else ''))

@acao
def a_partida(d):
    k = d.get('id')
    if k not in G.arq: raise ValueError('Relatório desta partida não está disponível.')
    return G.arq[k]

@acao
def a_estat_live(d):
    L = G.live
    if not L or L['u'] is None: raise ValueError('Nenhuma partida em andamento.')
    m = L['ms'][L['u']]; return dict(rel=relatorio(m), garg=gargalos(m, m['us']))

# --------------------------- TABELAS / COPAS -------------------------
@acao
def a_tabela(d):
    lg = d.get('lg'); L = G.L[int(lg)] if lg not in (None, '') else (liga_usuario() or G.L[0])
    art = sorted([G.P[x] for t in L['clubs'] for x in G.T[t]['pl']], key=lambda p: -p['st']['l'][1])[:10]
    u = L.get('ult')
    return dict(lg=L['i'], n=L['n'], fl=bandeira(L['cc']), temp=L['temp'], rows=[dict(t=jt(G.T[t]), d=L['tab'][t]) for t in classificacao(L)],
                rod=L['r'], tot=len(L['fx']), art=[jp(p) for p in art if p['st']['l'][1]], champ=L['champ'][-5:][::-1],
                ult=dict(temp=u['temp'], tab=[dict(t=jt(G.T[t]), d=r) for t, r in u['tab'][:5]], art=u['art']) if u else None,
                ligas=[dict(i=x['i'], n=x['n'], fl=bandeira(x['cc']), pais=PAISES[x['cc']][0]) for x in G.L],
                copas=[dict(cc=C['cc'], n=C['n'], fl=bandeira(C['cc'])) for C in G.C.values()])

@acao
def a_copa(d):
    cc = d.get('cc')
    if cc == 'CN':
        if not G.cn: return dict(n='Copa das Nações', rd=[], champ=[(str(a), b) for a, b in G.cnhist[::-1]])
        C = dict(n='Copa das Nações %d' % G.cn['ano'], rd=G.cn['rd']); champ = [(str(a), b) for a, b in G.cnhist[::-1]]
    else:
        C = G.C[cc]; champ = C['champ'][::-1]
    rds = []
    for rd in C['rd']:
        js = []
        for i, (h, a) in enumerate(rd['j']):
            r = rd['r'][i] if i < len(rd['r']) else None
            js.append(dict(h=jt(G.T[h]), a=jt(G.T[a]), r=[r[0], r[1]] if r else None, pen=r[2] if r else None))
        rds.append(dict(nome=rd['nome'], d=fdata(rd['d']), ok=rd['ok'], j=js))
    return dict(n=C['n'], rd=rds, champ=champ[:8], temp=C.get('temp', ''))

# ------------------------- ESTADIO / JUNIORES ------------------------
@acao
def a_estadio(d):
    T = time_do({}); e = T['est']; L = liga_usuario(); jogos = []
    if L:
        for rd in L['fx']:
            for h, a in rd['j']:
                if h == T['id'] and (h, a) in L['res']:
                    r = L['res'][(h, a)]; jogos.append(dict(d=fdata(rd['d']), adv=G.T[a]['n'], pub=r[2], renda=r[3], oc=round(100 * r[2] / e['cap'])))
    custo = int(2500 + e['cap'] * .05)
    return dict(n=e['n'], cap=e['cap'], preco=e['preco'], ref=e['ref'], tor=T['tor'], jogos=jogos[::-1], custo=custo, bud=T['bud'],
                media=int(sum(j['pub'] for j in jogos) / len(jogos)) if jogos else 0)

@acao
def a_estadio_preco(d):
    T = time_do({}); e = T['est']; v = float(d.get('preco', e['preco']))
    e['preco'] = round(max(e['ref'] * .3, min(e['ref'] * 3, v)), 1); return dict(a_estadio(d), msg='Ingresso agora custa € %.1f' % e['preco'])

@acao
def a_estadio_ampliar(d):
    sem_live(); T = time_do({}); e = T['est']; custo = int(2500 + e['cap'] * .05)
    if e['cap'] >= 100000: raise ValueError('O estádio já está na capacidade máxima.')
    if T['bud'] < custo: raise ValueError('Dinheiro insuficiente para a ampliação.')
    T['bud'] -= custo; e['cap'] += 5000; noticia('%s ampliado para %d lugares.' % (e['n'], e['cap']), 'bom')
    return dict(a_estadio(d), msg='Estádio ampliado!')

@acao
def a_juniores(d):
    T = time_do({}); return dict(lista=[jp(G.P[x]) for x in sorted(T['jr'], key=lambda x: -G.P[x]['pot']) if x in G.P], n=len(T['pl']))

@acao
def a_promover(d):
    sem_live(); T = time_do({}); x = int(d['pid'])
    if x not in T['jr']: raise ValueError('Jogador não está nos juniores.')
    if len(T['pl']) >= 35: raise ValueError('Elenco principal cheio (máx. 35).')
    p = G.P[x]; T['jr'].remove(x); T['pl'].append(x); p['jr'] = False; p['num'] = numero_livre(T, p['pos']); p['sal'] = max(2, p['val'] // 300)
    p['ct'] = od(ano_de(G.hoje) + 3, '06-30'); noticia('%s foi promovido ao time principal.' % p['n'], 'bom')
    return dict(a_juniores(d), msg='%s promovido!' % p['n'])

@acao
def a_dispensar_jr(d):
    sem_live(); T = time_do({}); x = int(d['pid'])
    if x in T['jr']: T['jr'].remove(x); G.P.pop(x, None)
    return a_juniores(d)

# ------------------------------ TIMES --------------------------------
@acao
def a_times(d):
    lg = d.get('lg'); out = dict(ligas=[dict(i=L['i'], n=L['n'], fl=bandeira(L['cc'])) for L in G.L], lg=None, clubs=[])
    if lg == 'copa': ts = [T for T in clubes() if T['lg'] is None]
    elif lg == 'sel': ts = sorted(selecoes(), key=lambda T: -forca(T))
    else:
        L = G.L[int(lg)] if lg not in (None, '') else (liga_usuario() or G.L[0]); out['lg'] = L['i']; ts = [G.T[t] for t in L['clubs']]
    for T in ts:
        tec = G.TEC.get(T.get('tec')); out['clubs'].append(dict(jt(T), tec=G.coach['n'] if T.get('tec') == 'eu' else (tec['n'] if tec else '—'),
                                                               cap=T['est']['cap'] if 'est' in T else None, nj=len(T['pl'])))
    return out

@acao
def a_time(d):
    T = G.T[d['tid']]; tec = G.TEC.get(T.get('tec'))
    return dict(t=jt(T), tec=G.coach['n'] if T.get('tec') == 'eu' else (tec['n'] if tec else '—'), est=T.get('est'), craques=craques(T),
                pl=[jp(G.P[x]) for x in sorted(T['pl'], key=lambda x: (POSICOES.index(G.P[x]['pos']), -G.P[x]['ovr'])) if x in G.P])

# ---------------------------- MERCADO --------------------------------
@acao
def a_procura(d):
    c = G.coach; meu = c['club']; pos = d.get('pos') or ''; q = (d.get('q') or '').lower().strip()
    mx = int(d.get('max') or 10 ** 9); lg = d.get('lg'); mn = int(d.get('min') or 0); ida = int(d.get('idade') or 99)
    clubes_ = set(G.L[int(lg)]['clubs']) if lg not in (None, '') else None
    res = [p for p in G.P.values() if p['club'] != meu and p['club'] in G.T and not p['jr'] and not p['emp'] and (not pos or p['pos'] == pos)
           and int(p['val'] * 1.15) <= mx and p['ovr'] >= mn and p['age'] <= ida and (not q or q in p['n'].lower())
           and (clubes_ is None or p['club'] in clubes_) and not G.T[p['club']]['nac']]
    res = sorted(res, key=lambda p: -p['ovr'])[:80]
    return dict(lista=[dict(jp(p), preco=int(p['val'] * 1.15)) for p in res], bud=G.T[meu]['bud'] if meu else 0,
                ligas=[dict(i=x['i'], n=x['n'], fl=bandeira(x['cc'])) for x in G.L])

@acao
def a_comprar(d):
    sem_live(); T = time_do({}); p = G.P[int(d['pid'])]; S = G.T[p['club']]; preco = int(p['val'] * 1.15)
    if S is T: raise ValueError('Esse jogador já é seu.')
    if p['emp'] or p['jr']: raise ValueError('Jogador não está disponível para venda.')
    if len(S['pl']) <= 18: raise ValueError('O %s não quer vender: elenco curto.' % S['n'])
    if len(T['pl']) >= 35: raise ValueError('Seu elenco está cheio (máx. 35).')
    if T['bud'] < preco: raise ValueError('Dinheiro insuficiente.')
    mover_jogador(p, T['id']); T['bud'] -= preco; S['bud'] += preco
    p['ct'] = max(p['ct'], od(ano_de(G.hoje) + 3, '06-30')); p['aviso'] = False
    if p['ovr'] >= forca(T) + 3: T['tor'] = min(100, T['tor'] + 4)
    noticia('Contratação: %s (%s) chega do %s.' % (p['n'], p['pos'], S['n']), 'bom')
    return dict(msg='%s contratado!' % p['n'])

def destino_ia(p, T, faixa=6):
    cand = [C for C in clubes() if C is not T and C['lg'] is not None and abs(C['str'] - p['ovr']) <= faixa and len(C['pl']) < 32]
    return R.choice(cand or [C for C in clubes() if C is not T and len(C['pl']) < 32])

@acao
def a_vender(d):
    sem_live(); T = time_do({}); pid = int(d['pid']); p = G.P[pid]
    if pid not in T['pl']: raise ValueError('Jogador não está no seu elenco.')
    if len(T['pl']) <= 16: raise ValueError('Elenco mínimo de 16 jogadores.')
    C = destino_ia(p, T); preco = int(p['val'] * R.uniform(.85, 1.0))
    if pid in craques(T): T['tor'] = max(15, T['tor'] - 5)
    mover_jogador(p, C['id']); T['bud'] += preco; noticia('%s foi vendido ao %s.' % (p['n'], C['n']))
    return dict(msg='%s vendido ao %s por € %s mil' % (p['n'], C['n'], format(preco, ',d').replace(',', '.')))

@acao
def a_renovar(d):
    sem_live(); T = time_do({}); pid = int(d['pid']); p = G.P[pid]
    if pid not in T['pl']: raise ValueError('Jogador não está no seu elenco.')
    anos = 3 if p['age'] < 30 else 1 if p['age'] >= 33 else 2
    if 'ok' not in d:
        fim = od(ano_de(G.hoje) + anos, '06-30')
        p['_ren'] = (int(max(p['sal'], p['val'] / 260) * R.uniform(1.05, 1.3)), fim if fim > p['ct'] else od(ano_de(p['ct']) + 1, '06-30'))
        return dict(prop=dict(sal=p['_ren'][0], ate=fdata(p['_ren'][1]), atual=p['sal']))
    if not d['ok'] or '_ren' not in p: p.pop('_ren', None); return dict(msg='Negociação cancelada.')
    if T['mor'] < 35 and R.random() < .4: p.pop('_ren'); raise ValueError('%s recusou renovar: o clima no elenco está ruim.' % p['n'])
    p['sal'], p['ct'] = p.pop('_ren'); p['aviso'] = False
    noticia('%s renovou até %s.' % (p['n'], fdata(p['ct'])), 'bom'); return dict(msg='Contrato renovado até %s' % fdata(p['ct']))

@acao
def a_emprestar(d):
    sem_live(); T = time_do({}); pid = int(d['pid']); p = G.P[pid]
    if pid not in T['pl']: raise ValueError('Jogador não está no seu elenco.')
    if len(T['pl']) <= 16: raise ValueError('Elenco mínimo de 16 jogadores.')
    C = destino_ia(p, T, 8); fim = od(ano_de(G.hoje) + (1 if dt.date.fromordinal(G.hoje).month >= 7 else 0), '06-30')
    if fim - G.hoje < 60: fim = od(ano_de(fim) + 1, '06-30')
    mover_jogador(p, C['id']); p['emp'] = T['id']; p['empf'] = fim
    noticia('%s foi emprestado ao %s até %s.' % (p['n'], C['n'], fdata(fim))); return dict(msg='%s emprestado ao %s' % (p['n'], C['n']))

@acao
def a_dispensar(d):
    sem_live(); T = time_do({}); pid = int(d['pid']); p = G.P[pid]
    if pid not in T['pl']: raise ValueError('Jogador não está no seu elenco.')
    if len(T['pl']) <= 16: raise ValueError('Elenco mínimo de 16 jogadores.')
    C = destino_ia(p, T, 10); multa = int(p['sal'] * max(0, (p['ct'] - G.hoje)) / 7 * .5)
    mover_jogador(p, C['id']); T['bud'] -= multa
    noticia('%s foi dispensado (rescisão de € %d mil) e assinou com o %s.' % (p['n'], multa, C['n']))
    return dict(msg='%s dispensado' % p['n'])

# ---------------------------- SELECAO --------------------------------
@acao
def a_elegiveis(d):
    T = time_do({'t': 'sel'})
    el = sorted([p for p in G.P.values() if p['nat'] == T['cc'] and not p['jr']], key=lambda p: -p['ovr'])[:90]
    return dict(t=jt(T), conv=T['pl'], lista=[jp(p) for p in el])

@acao
def a_convocar(d):
    sem_live(); T = time_do({'t': 'sel'}); ids = [int(x) for x in d.get('ids', [])][:23]
    if len(ids) < 16: raise ValueError('Convoque pelo menos 16 jogadores.')
    if any(G.P[x]['nat'] != T['cc'] for x in ids): raise ValueError('Jogador de outra nacionalidade.')
    T['pl'] = ids; T['xi'] = [x for x in T['xi'] if x in ids]
    if len(T['xi']) < 11: auto_xi(T)
    return dict(a_elegiveis(d), msg='Convocação salva (%d jogadores).' % len(ids))

@acao
def a_conv_auto(d):
    sem_live(); convocar_auto(time_do({'t': 'sel'})); return a_elegiveis(d)

@acao
def a_ranking(d):
    return dict(lista=[jt(T) for T in sorted(selecoes(), key=lambda T: -forca(T))][:47])

# ----------------------- TECNICOS / HISTORIA -------------------------
@acao
def a_tecnicos(d):
    f = d.get('f') or 'todos'; c = G.coach
    ts = [dict(n=x['n'], fl=bandeira(x['nat']), t=G.T[x['t']]['n'] if x['t'] in G.T else None, rep=x['rep'], tit=x['tit']) for x in G.TEC.values()]
    T = G.T.get(c['club']); N = G.T.get(c['nt'])
    ts.append(dict(n=c['n'] + ' (você)', fl='', t=' / '.join(x['n'] for x in (T, N) if x) or None, rep=round(c['rep']), tit=len(c['tit']), eu=True))
    if f == 'livres': ts = [x for x in ts if not x['t']]
    elif f == 'empregados': ts = [x for x in ts if x['t']]
    return dict(lista=sorted(ts, key=lambda x: -x['rep'])[:300])

@acao
def a_historia(d):
    c = G.coach
    return dict(ligas=[dict(n=L['n'], fl=bandeira(L['cc']), champ=L['champ'][::-1][:10]) for L in G.L if L['champ']],
                copas=[dict(n=C['n'], fl=bandeira(C['cc']), champ=C['champ'][::-1][:10]) for C in G.C.values() if C['champ']],
                cn=[(str(a), b) for a, b in G.cnhist[::-1]], hist=c['hist'][::-1], tit=c['tit'][::-1], n=c['n'], rep=round(c['rep']),
                v=c['v'], e=c['e'], d=c['d'])

# ----------------------------- MENSAGENS -----------------------------
@acao
def a_mensagens(d):
    c = G.coach; vivas = {o['t'] for o in c['ofs']}
    return dict(lista=[dict(id=x['id'], d=fdata(x['d']), x=x['x'], k=x['k'], lida=x['lida'], of=x['of'] if x['of'] in vivas else None) for x in G.msgs])

@acao
def a_ler(d):
    for x in G.msgs:
        if d.get('id') in (None, x['id']): x['lida'] = True
    return dict(ok=True)

@acao
def a_aceitar(d):
    sem_live(); c = G.coach; o = next((o for o in c['ofs'] if o['t'] == d.get('t')), None)
    if not o: raise ValueError('Proposta expirada.')
    c['ofs'].remove(o); T = G.T[o['t']]
    if o['tipo'] == 'clube':
        assumir_clube(T); L = liga_usuario()
        if L and L['r'] > 0 and L['r'] < len(L['fx']): pass
    else: assumir_selecao(T)
    noticia('Você assinou com %s!' % T['n'], 'bom'); return a_estado(d)

@acao
def a_recusar(d):
    c = G.coach; c['ofs'] = [o for o in c['ofs'] if o['t'] != d.get('t')]; return dict(msg='Proposta recusada.')

@acao
def a_demitir(d):
    sem_live(); c = G.coach
    if d.get('t') == 'sel' and c['nt']:
        N = G.T[c['nt']]; noticia('Você deixou a seleção da %s.' % N['n']); c['nt'] = None; trocar_tecnico_ia(N)
    elif c['club']:
        noticia('Você pediu demissão do %s.' % G.T[c['club']]['n']); sair_do_clube(); c['rep'] = max(1, c['rep'] - 3)
    return a_estado(d)

# ----------------------------- PARTIDA -------------------------------
@acao
def a_jogar(d):
    if G.live and not G.live['fim']: return snap()
    G.live = None; pr = proximo(); k = pr['k']
    avancar_ate(pr['d'], {k} if k else ())
    if pr['tipo'] == 'semana': return dict(live=False, msg='Semana avançada: hoje é %s.' % fdata(G.hoje))
    p2 = proximo()
    if p2.get('k') != k or p2['d'] != G.hoje:
        simular_pendente(k); return dict(live=False, msg='Sua situação mudou antes do jogo. Confira as mensagens.')
    iniciar_jogo_usuario(pr); return snap()

def lado_usuario():
    L = G.live; m = L['ms'][L['u']]; S = m['s'][m['us']]; T = G.T[S['t']]
    f = lambda x, sl=None: dict(id=x, n=G.P[x]['n'], pos=G.P[x]['pos'], num=G.P[x]['num'], sl=sl, ovr=G.P[x]['ovr'], en=int(S['en'].get(x, 100)),
                                am=x in S['am'], les=G.P[x]['inj'] > 0, nt=nota(m, x))
    return dict(on=[f(x, sl) for x, sl in zip(S['on'], S['sl'])], bench=[f(x) for x in S['bench']], subs=S['subs'], form=T['form'], tac=T['tac'])

def snap():
    L = G.live; u = L['u']
    d = dict(live=True, tipo=L['tipo'], comp=L['comp'], min=L['min'], u=u, fim=L['fim'], data=fdata(G.hoje),
             ms=[dict(h=jt(G.T[m['t'][0]]), a=jt(G.T[m['t'][1]]), g=m['g'], pen=m['pen']) for m in L['ms']])
    if u is not None:
        m = L['ms'][u]; d.update(us=m['us'], ev=m['ev'], lado=lado_usuario(), lu=lineups(m), pub=m['pub'][0])
        L['ne'] = len(m['ev']); L['lv'] = [m['s'][0]['v'], m['s'][1]['v']]
    return d

@acao
def a_passo(d):
    if not G.live: raise ValueError('Nenhuma partida em andamento.')
    fr = passo(int(d.get('n', 4))); L = G.live; out = dict(frames=fr, fim=L['fim'], min=L['min'])
    if L['fim']:
        out['final'] = [dict(h=jt(G.T[m['t'][0]]), a=jt(G.T[m['t'][1]]), g=m['g'], pen=m['pen'], w=m['w']) for m in L['ms']]
        if L['u'] is not None: m = L['ms'][L['u']]; out['res'] = resultado_lado(m, m['us']); out['arq'] = m.get('arq')
    return out

@acao
def a_snap(d):
    if not G.live: raise ValueError('Nenhuma partida em andamento.')
    return snap()

def lado_live():
    L = G.live
    if not L or L['fim'] or L['u'] is None: raise ValueError('Nenhuma partida em andamento.')
    m = L['ms'][L['u']]; return L, m, m['us'], m['s'][m['us']]

@acao
def a_sub(d):
    L, m, s, S = lado_live(); out, xin = int(d['out']), int(d['in'])
    if S['subs'] >= 5: raise ValueError('Limite de 5 substituições atingido.')
    if out not in S['on'] or xin not in S['bench']: raise ValueError('Substituição inválida.')
    substituir(m, s, S['on'].index(out), xin, L['min'])
    return dict(lado=lado_usuario(), garg=gargalos(m, s))

@acao
def a_tatica(d):
    L, m, s, S = lado_live(); T = G.T[S['t']]
    if d.get('form') in FORMS and d['form'] != T['form']:
        T['form'] = d['form']; S['on'], S['sl'] = arrumar(S['on'], T['form']); regeo(S)
        if len(T['xi']) == 11: T['xi'] = arrumar(T['xi'], T['form'])[0]
        ev(m, L['min'], s, 'tat', 'Nova formação: ' + T['form'])
    if d.get('tac') in TATICAS and d['tac'] != T['tac']:
        T['tac'] = d['tac']; ev(m, L['min'], s, 'tat', 'Postura: ' + {'D': 'Defensiva', 'E': 'Equilibrada', 'O': 'Ofensiva'}[d['tac']])
    return dict(lado=lado_usuario(), garg=gargalos(m, s))

@acao
def a_salvar(d):
    sem_live()
    with open(SAVE, 'wb') as f: pickle.dump(G, f)
    return dict(msg='Jogo salvo em ' + os.path.abspath(SAVE))

@acao
def a_carregar(d):
    global G
    if not os.path.exists(SAVE): raise ValueError('Nenhum jogo salvo.')
    with open(SAVE, 'rb') as f: G = pickle.load(f)
    return a_estado(d)
