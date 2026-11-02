# ------------------------- CRIACAO DO MUNDO --------------------------
class Mundo: pass
G = None
LOCK = threading.RLock()
IMPORTADOS = []          # planilhas (.xlsx/.csv) aplicadas a cada novo mundo

def od(y, md):
    m, d = map(int, md.split('-')); return dt.date(y, m, d).toordinal()
def fdata(o): return dt.date.fromordinal(o).strftime('%d/%m/%Y')
def dia_sem(o): return dt.date.fromordinal(o).weekday()          # 0=segunda ... 6=domingo
def ano_de(o): return dt.date.fromordinal(o).year
def proximo_dia(o, wd): return o + (wd - dia_sem(o)) % 7

def bandeira(cc):
    if cc in ('EN', 'SC', 'WA'):
        tag = {'EN': 'gbeng', 'SC': 'gbsct', 'WA': 'gbwls'}[cc]
        return '\U0001F3F4' + ''.join(chr(0xE0000 + ord(c)) for c in tag) + '\U000E007F'
    if cc == 'NI': return '\U0001F1EC\U0001F1E7'
    return ''.join(chr(0x1F1E6 + ord(c) - 65) for c in cc if 'A' <= c <= 'Z')

def sigla(n):
    w = [x for x in n.replace('-', ' ').replace('.', ' ').split() if len(x) > 2 and x.lower() not in ('club','de','del','des','fc','cf','sc','ac','the')] or [n]
    return (w[0][:3] if len(w) == 1 else w[0][0] + w[1][:2]).upper()

def valor(p):
    a = p['age']; f = 1.3 if a <= 21 else 1.12 if a <= 25 else 1.0 if a <= 29 else .7 if a <= 32 else .4
    p['val'] = int(max(20, 50 * 1.2 ** (p['ovr'] - 50) * f * (1 + max(0, p['pot'] - p['ovr']) / 30)))  # mil EUR
    if not p.get('sal'): p['sal'] = max(1, p['val'] // 260)                                          # mil EUR/semana

def st0(): return [0, 0, 0, 0.0, 0]       # jogos, gols, assistências, soma das notas, nº de notas

def carreira_inicial(p):
    j = int(max(0, p['age'] - 18) * R.uniform(16, 32) * (.6 + p['ovr'] / 150))
    tg = {'GOL': 0, 'ZAG': .04, 'LAT': .05, 'VOL': .07, 'MEI': .17, 'ATA': .36}[p['pos']] * p['ovr'] / 70
    ta = {'GOL': .003, 'ZAG': .03, 'LAT': .1, 'VOL': .08, 'MEI': .17, 'ATA': .12}[p['pos']]
    nm = 6.2 + (p['ovr'] - 60) * .025 + R.uniform(-.2, .2)
    p['st'] = {'t': st0(), 'l': st0(), 'c': [j, int(j * tg * R.uniform(.6, 1.3)), int(j * ta * R.uniform(.6, 1.3)), round(nm * j, 1), j]}

def nome_pessoa(cc):
    first, last = NOMES[PAISES.get(cc, ('', 'en'))[1]].split('|')
    return (R.choice(first.split()) + ' ' + R.choice(last.split())).replace('_', ' ')

def novo_jogador(pos, ovr, cc, club=None, age=None, jr=False):
    age = age or int(R.triangular(17, 35, 25)); ovr = max(30, min(94, int(round(ovr))))
    if cc not in PAISES: cc = 'BR'
    nome = R.choice(APELIDOS) if cc == 'BR' and R.random() < .2 else nome_pessoa(cc)
    nh = (ovr >= 68) + (ovr >= 77) + (ovr >= 84) + (R.random() < .3)
    hab = R.sample(HAB_POS[pos].split(), min(nh, 3))
    if age >= 29 and 'LID' not in hab and R.random() < .2: hab.append('LID')
    if R.random() < .07 and 'RES' not in hab: hab.append('RES')
    p = dict(id=G.nid, n=nome, pos=pos, age=age, nat=cc, ovr=ovr, club=club, hab=hab, jr=jr, num=0, emp=None, empf=0,
             pot=min(97, ovr + int(max(0, 27 - age) * R.uniform(.4, 2.2))), aviso=False,
             fis=max(30, min(99, int(R.gauss(ovr - 4 + (5 if pos in ('ZAG', 'VOL', 'ATA') else 0) - max(0, age - 31) * 2, 7)))),
             pe=R.choices('DEA', (72, 22, 6))[0], cond=100, inj=0, sus=0, ca=0, sal=0,
             ct=od(ANO_BASE + (R.randint(1, 5) if age < 33 else R.randint(1, 2)), '06-30'))
    valor(p); carreira_inicial(p); G.P[G.nid] = p; G.nid += 1
    return p

NUMS = {'GOL': [1, 12, 23], 'ZAG': [3, 4, 13, 14, 15], 'LAT': [2, 6, 16, 17], 'VOL': [5, 8, 18, 19], 'MEI': [10, 7, 20, 21], 'ATA': [9, 11, 22, 24]}
def numero_livre(T, pos=None):
    usados = {G.P[x]['num'] for x in T['pl'] if x in G.P}
    for n in (NUMS.get(pos, []) + list(range(25, 100))):
        if n not in usados: return n
    return 99

def novo_tecnico(cc, rep, tid=None):
    i = 't%d' % len(G.TEC)
    G.TEC[i] = dict(id=i, n=nome_pessoa(cc), nat=cc, rep=int(max(15, min(95, rep))), t=tid, tit=0)
    return i

def criar_clube(nome, cc, s, lg=None, cup=None, jogadores=True):
    tid = 'c%d' % G.ntid; G.ntid += 1; h = sum(map(ord, nome))
    T = dict(id=tid, n=nome, lg=lg, cup=cup or cc, cc=cc, str=round(s), pl=[], xi=[], form=R.choice(list(FORMS)[:4]), tac='E',
             mor=60, tor=60, sig=sigla(nome), cor=CORES_CLUBES.get(nome, CORES[h % len(CORES)]), nac=False, jr=[], bud=0, rev=0)
    G.T[tid] = T
    if jogadores:
        loc = LOCAL.get(cc, .72); fk = [x[:2] for x in ESTRANG.split()]; fw = [int(x[2:]) for x in ESTRANG.split()]
        for pos, qt in ELENCO:
            for i in range(qt):
                nat = cc if R.random() < loc else R.choices(fk, fw)[0]
                p = novo_jogador(pos, R.gauss(s + 1 - 11 * i / qt, 3.2), nat, tid); T['pl'].append(p['id']); p['num'] = NUMS[pos][i]
    financas_iniciais(T)
    T['tec'] = novo_tecnico(cc, s - 25 + R.gauss(0, 6), tid)
    return T

def financas_iniciais(T):
    s = T['str']; folha = max(5, sum(G.P[x]['sal'] for x in T['pl']))
    cap = int(min(95000, max(4000, (3000 + 1.08 ** (s - 40) * 2200) * R.uniform(.85, 1.15))) // 500 * 500)
    T['est'] = dict(n='Estádio ' + ('do ' if not T['n'].split()[0].endswith('a') else 'da ') + T['n'], cap=cap,
                    ref=round(max(3, 1.6 * folha * 1000 / cap), 1))
    T['est']['preco'] = T['est']['ref']
    T['rev'] = int(folha * .45); T['bud'] = int(sum(G.P[x]['val'] for x in T['pl']) * .12)

def gerar_mundo(seed=None):
    global G
    if seed is not None: R.seed(seed)
    G = Mundo(); G.P = {}; G.T = {}; G.L = []; G.C = {}; G.TEC = {}; G.nid = 1; G.ntid = 0; G.msgs = []; G.nmsg = 0
    G.hoje = od(ANO_BASE, '07-01'); G.base = G.hoje; G.live = None; G.coach = None; G.ntopp = {}; G.cn = None
    G.cnhist = []; G.arq = {}; G.narq = 0; G.ult = None; G.cache = {}; G.iniciado = False
    for li, linha in enumerate(LIGAS.strip().split('\n')):
        cc, nome, top, bot, ini, cl = linha.split('|'); top, bot = int(top), int(bot); clubes = cl.split(';')
        L = dict(i=li, cc=cc, n=nome, ini=ini, clubs=[], fx=[], tab={}, res={}, champ=[], temp='', top=top, bot=bot)
        G.L.append(L); n = len(clubes)
        for k, cn in enumerate(clubes):
            s = top - (top - bot) * (k / max(1, n - 1)) ** .8 + R.uniform(-1.2, 1.2)
            T = criar_clube(cn, cc, s, lg=li); auto_xi(T); L['clubs'].append(T['id'])
    for arq in IMPORTADOS:
        try: importar_planilha(arq)
        except Exception as e: print('Falha ao importar', arq, '->', e)
    for L in G.L: G.C[L['cc']] = dict(cc=L['cc'], n=COPAS.get(L['cc'], 'Copa ' + PAISES[L['cc']][0]), rd=[], champ=[], temp='', vivos=[])
    montar_selecoes()

def montar_selecoes():
    por = {}
    for p in G.P.values():
        if not p['jr']: por.setdefault(p['nat'], []).append(p['id'])
    for cc, ids in por.items():
        tid = 'n' + cc
        if len(ids) < 22 or tid in G.T: continue
        G.T[tid] = dict(id=tid, n=PAISES[cc][0], cc=cc, pl=[], xi=[], form='4-3-3', tac='E', mor=60, tor=60, sig=cc,
                        cor=CORES_PAIS.get(cc, CORES[sum(map(ord, cc)) % len(CORES)]), nac=True, str=60, lg=None, jr=[])
        convocar_auto(G.T[tid]); G.T[tid]['tec'] = novo_tecnico(cc, forca(G.T[tid]) - 20, tid)

def selecoes(): return [T for T in G.T.values() if T['nac']]
def clubes(): return [T for T in G.T.values() if not T['nac']]

def convocar_auto(T):
    el = sorted([p for p in G.P.values() if p['nat'] == T['cc'] and p['inj'] == 0 and not p['jr']], key=lambda p: -p['ovr'])
    conv = []
    for g, q in (('G', 3), ('D', 8), ('M', 7), ('A', 5)):
        conv += [p['id'] for p in el if GRP[p['pos']] == g][:q]
    T['pl'] = conv; auto_xi(T)

# -------------------------- ESCALACAO --------------------------------
def disp(pid, nac=False):
    p = G.P[pid]; return p['inj'] == 0 and (nac or p['sus'] == 0)

def fit(pos, slot):
    a, b = 'GDMA'.index(GRP[pos]), 'GDMA'.index(slot)
    if a == b: return 1.0
    if a == 0 or b == 0: return .35
    return .85 if abs(a - b) == 1 else .7

def slots(form):
    d, m, a = FORMS[form][:3]; return ['G'] + ['D'] * d + ['M'] * m + ['A'] * a

def geo(sl):
    """coordenadas-base de cada posição: (largura 0-100, profundidade 0-100 a partir do próprio gol)"""
    r = {'G': [], 'D': [], 'M': [], 'A': []}; out = [None] * len(sl)
    for i, s in enumerate(sl): r[s].append(i)
    for g in 'GDMA':
        ids = r[g]; n = len(ids)
        if g == 'M' and n >= 5:
            for j, k in enumerate(ids[:2]): out[k] = ((j + 1) * 100 / 3, 40)
            adv = ids[2:]
            for j, k in enumerate(adv): out[k] = ((j + 1) * 100 / (len(adv) + 1), 60)
        else:
            for j, k in enumerate(ids): out[k] = ((j + 1) * 100 / (n + 1), {'G': 5, 'D': 24, 'M': 48, 'A': 75}[g])
    return out

def corredor(ax): return 0 if ax < 32 else 2 if ax > 68 else 1

def arrumar(ids, form):
    sl = slots(form)
    while len(sl) > len(ids): sl.remove('A' if 'A' in sl else 'M' if 'M' in sl else 'D' if 'D' in sl else 'G')
    resto = list(ids); out = [None] * len(sl)
    for g in 'GDMA':
        cand = sorted([x for x in resto if GRP[G.P[x]['pos']] == g], key=lambda x: -G.P[x]['ovr'])
        for i, s in enumerate(sl):
            if s == g and cand: c = cand.pop(0); out[i] = c; resto.remove(c)
    for i, s in enumerate(sl):
        if out[i] is None:
            c = max(resto, key=lambda x: G.P[x]['ovr'] * fit(G.P[x]['pos'], s)); out[i] = c; resto.remove(c)
    return out, sl

def auto_xi(T):
    d, m, a = FORMS[T['form']][:3]
    av = sorted([x for x in T['pl'] if disp(x, T['nac'])], key=lambda x: -G.P[x]['ovr'] * (.7 + .3 * G.P[x]['cond'] / 100))
    if len(av) < 11: av += sorted([x for x in T['pl'] if x not in av], key=lambda x: -G.P[x]['ovr'])[:11 - len(av)]
    pick = []
    for g, q in (('G', 1), ('D', d), ('M', m), ('A', a)):
        pick += [x for x in av if GRP[G.P[x]['pos']] == g][:q]
    for x in av:
        if len(pick) >= 11: break
        if x not in pick: pick.append(x)
    T['xi'] = arrumar(pick, T['form'])[0] if pick else []
    T['f'] = round(sum(G.P[x]['ovr'] for x in T['xi']) / max(1, len(T['xi'])), 1)
    if T['nac']: T['str'] = T['f']
    return T['xi']

def forca(T):
    if 'f' not in T: auto_xi(T)
    return T['f']

def validar_xi(T):
    """troca lesionados/suspensos/saídos da escalação do usuário pelo melhor substituto"""
    xi = [x for x in T['xi'] if x in T['pl']]
    if len(xi) < 11: return auto_xi(T)
    for i, x in enumerate(xi):
        if not disp(x, T['nac']):
            g = GRP[G.P[x]['pos']]
            c = [y for y in T['pl'] if y not in xi and disp(y, T['nac'])]
            if c: xi[i] = max(c, key=lambda y: G.P[y]['ovr'] * (1.2 if GRP[G.P[y]['pos']] == g else 1))
    T['xi'] = xi
    T['f'] = round(sum(G.P[x]['ovr'] for x in xi) / 11, 1)
    return xi

def tirar_do_xi(T, pid):
    if pid not in T['xi']: return
    i = T['xi'].index(pid); g = GRP[G.P[pid]['pos']]
    c = [y for y in T['pl'] if y != pid and y not in T['xi'] and disp(y, T['nac'])]
    if c: T['xi'][i] = max(c, key=lambda y: G.P[y]['ovr'] * (1.2 if GRP[G.P[y]['pos']] == g else 1))
    else: T['xi'].pop(i)

def mover_jogador(p, destino, msg=None):
    """transfere/empresta o jogador p para o clube destino (id)"""
    O = G.T.get(p['club'])
    if O:
        if p['id'] in O['pl']: O['pl'].remove(p['id'])
        tirar_do_xi(O, p['id'])
    D = G.T[destino]; D['pl'].append(p['id']); p['club'] = destino; p['sus'] = 0; p['num'] = numero_livre(D, p['pos'])
    G.cache.pop(destino, None); G.cache.pop(O['id'] if O else None, None)
