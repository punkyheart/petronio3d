# -------------- IMPORTAR LIGAS / CLUBES / JOGADORES (XLSX/CSV) --------------
def norm(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower().strip()
    return re.sub(r'[^a-z0-9/ ]+', ' ', s).strip()

SIN = {'pais': 'pais|country|pais da liga|league country', 'liga': 'liga|league|divisao|competicao|campeonato|division|torneio|serie',
       'clube': 'clube|club|time|equipe|team|squad|agremiacao', 'nome': 'jogador|nome|name|player|atleta|nome do jogador|player name|nome completo',
       'pos': 'posicao|pos|position|p|funcao|pos.', 'idade': 'idade|age|anos', 'nasc': 'nascimento|data de nascimento|dob|birth|birthdate|date of birth|nasc|data nasc',
       'nat': 'nacionalidade|nac|nationality|nat|nacao|selecao', 'pe': 'pe|foot|lado|preferred foot|perna|l|pe preferido',
       'forca': 'forca|overall|ovr|rating|f|nivel|geral|forca atual|ca', 'fis': 'fisico|physical|phy|forca fisica|fis|fisico atual',
       'pot': 'potencial|potential|pot|pa', 'hab': 'habilidades|caracteristicas|car|skills|traits|car.|habilidade|caracteristica',
       'val': 'valor|value|passe|market value|valor de mercado|preco|valor mercado', 'sal': 'salario|wage|salary|ordenado|salario semanal',
       'ct': 'contrato|contract|fim do contrato|contract end|vinculo|contrato ate|fim contrato|contract expires',
       'num': 'numero|camisa|number|shirt|n|no|num', 'tipo': 'tipo|type|status|categoria'}
SIN = {k: set(v.split('|')) for k, v in SIN.items()}
POSMAP = {'GOL': 'gk gol g goleiro goalkeeper por portero keeper arqueiro',
          'ZAG': 'cb zag z zagueiro centre back center back defensor central dc zagueiro central defesa central df d',
          'LAT': 'lb rb lat lateral lwb rwb fullback full back ld le lateral direito lateral esquerdo ala',
          'VOL': 'dm cdm vol volante defensive midfielder defensive midfield primeiro volante',
          'MEI': 'cm mc mei m meia am cam mid midfielder mf lm rm meio campo meio campista armador central midfield attacking midfield mid',
          'ATA': 'st cf fw ata a atacante centroavante lw rw ponta winger forward ss centre forward striker extremo pd pe'}
POSMAP = {w: k for k, v in POSMAP.items() for w in v.split()}
HABMAP = {'fin': 'FIN', 'finalizacao': 'FIN', 'finishing': 'FIN', 'cab': 'CAB', 'cabeceio': 'CAB', 'heading': 'CAB', 'dri': 'DRI',
          'drible': 'DRI', 'dribbling': 'DRI', 'pas': 'PAS', 'passe': 'PAS', 'passing': 'PAS', 'arm': 'PAS', 'armacao': 'PAS',
          'vel': 'VEL', 'velocidade': 'VEL', 'pace': 'VEL', 'speed': 'VEL', 'des': 'DES', 'desarme': 'DES', 'tackling': 'DES',
          'mar': 'MAR', 'marcacao': 'MAR', 'marking': 'MAR', 'chu': 'CHL', 'chl': 'CHL', 'chute': 'CHL', 'chute de longe': 'CHL',
          'long shots': 'CHL', 'bpa': 'BOL', 'bol': 'BOL', 'bola parada': 'BOL', 'set pieces': 'BOL', 'free kick': 'BOL', 'pen': 'PEN',
          'penaltis': 'PEN', 'penalties': 'PEN', 'lid': 'LID', 'lideranca': 'LID', 'leadership': 'LID', 'ref': 'REF', 'reflexos': 'REF',
          'reflexes': 'REF', 'sgo': 'SAI', 'sai': 'SAI', 'saida do gol': 'SAI', 'one on ones': 'SAI', 'res': 'RES', 'resistencia': 'RES',
          'stamina': 'RES', 'cru': 'CRU', 'cruzamento': 'CRU', 'crossing': 'CRU', 'dpe': 'SAI', 'cob': 'BOL'}
MARCA_COPA = ('copa', 'cup', 'taca', 'coupe', 'pokal', 'coppa', 'beker', 'sem liga', 'nenhuma', 'pokalen', 'cupen', 'puchar')

def mapear_cabecalho(linha):
    mp = {}
    for j, c in enumerate(linha):
        if c is None: continue
        n = norm(c)
        for k, alts in SIN.items():
            if n in alts and k not in mp: mp[k] = j; break
    return mp

def ler_planilha(caminho):
    ext = os.path.splitext(caminho)[1].lower(); folhas = []
    if ext in ('.xlsx', '.xlsm'):
        try: import openpyxl
        except ImportError:
            import subprocess; subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'openpyxl']); import openpyxl
        wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
        for ws in wb.worksheets: folhas.append((ws.title, [list(r) for r in ws.iter_rows(values_only=True)]))
    else:
        txt = open(caminho, encoding='utf-8-sig', errors='replace').read()
        sep = ';' if txt.count(';') > txt.count(',') else ','
        folhas.append((os.path.splitext(os.path.basename(caminho))[0], list(csv.reader(txt.splitlines(), delimiter=sep))))
    jog, cls = [], []
    for nome, linhas in folhas:
        hi = mapa = None
        for i, ln in enumerate(linhas[:20]):
            mp = mapear_cabecalho(ln)
            if 'clube' in mp and ('nome' in mp or 'liga' in mp or 'pais' in mp): hi, mapa = i, mp; break
        if hi is None: continue
        ult = {}
        for ln in linhas[hi + 1:]:
            r = {k: ln[j] for k, j in mapa.items() if j < len(ln) and ln[j] not in (None, '')}
            for k in ('pais', 'liga', 'clube'):
                if k in r: ult[k] = r[k]
                elif k in ult and ('nome' in r): r[k] = ult[k]
            if 'clube' not in r: continue
            r['_folha'] = nome
            (jog if 'nome' in mapa and 'nome' in r else cls).append(r)
    return jog, cls

def num(v, padrao=None):
    if v is None: return padrao
    if isinstance(v, (int, float)): return float(v)
    s = unicodedata.normalize('NFKD', str(v)).encode('ascii', 'ignore').decode().lower()
    m = re.search(r'-?\d+(?:[.,]\d+)*', s)
    if not m: return padrao
    t = m.group(); resto = s[m.end():].strip()
    if '.' in t and ',' in t: t = t.replace('.', '').replace(',', '.') if t.rfind(',') > t.rfind('.') else t.replace(',', '')
    elif ',' in t: t = t.replace(',', '') if re.fullmatch(r'-?\d{1,3}(,\d{3})+', t) else t.replace(',', '.')
    elif re.fullmatch(r'-?\d{1,3}(\.\d{3}){2,}', t) or (re.fullmatch(r'-?\d{1,3}\.\d{3}', t) and not resto[:1].isalpha()): t = t.replace('.', '')
    x = float(t)
    if re.match(r'(bi|bn|bilh)', resto): x *= 1e9
    elif re.match(r'(m\b|mi\b|mi |mio|mill|milh|mln)', resto + ' ') or resto == 'm': x *= 1e6
    elif re.match(r'(k\b|mil\b|mil )', resto + ' ') or resto == 'k': x *= 1e3
    return x

def euros_mil(v):
    x = num(v)
    if x is None: return None
    return x / 1000 if x >= 2000 else x * 1000 if x < 300 else x

def pais_codigo(v):
    if v in (None, ''): return None
    s = str(v).strip(); n = norm(s)
    if len(s) == 2 and s.upper() in PAISES: return s.upper()
    for cc, (nome, _) in PAISES.items():
        if norm(nome) == n: return cc
    if n in NOMES_PAIS_EN: return NOMES_PAIS_EN[n]
    ISO3 = {'bra': 'BR', 'arg': 'AR', 'eng': 'EN', 'esp': 'ES', 'ita': 'IT', 'ger': 'DE', 'deu': 'DE', 'fra': 'FR', 'por': 'PT', 'ned': 'NL',
            'usa': 'US', 'mex': 'MX', 'uru': 'UY', 'col': 'CO', 'chi': 'CL', 'par': 'PY', 'per': 'PE', 'ecu': 'EC', 'bel': 'BE', 'sco': 'SC'}
    if n in ISO3: return ISO3[n]
    cc = re.sub('[^A-Z]', '', n.upper())[:2] or 'XX'
    while cc in PAISES and norm(PAISES[cc][0]) != n: cc = cc[0] + chr((ord(cc[1]) - 64) % 26 + 65)
    PAISES[cc] = (s.title(), 'en'); return cc

def idade_de(r):
    v = r.get('idade')
    if v not in (None, ''):
        x = num(v)
        if x and 14 <= x <= 45: return int(x)
    v = r.get('nasc')
    if isinstance(v, (dt.date, dt.datetime)): return max(15, ANO_BASE - v.year)
    if v:
        m = re.search(r'(19|20)\d\d', str(v))
        if m: return max(15, ANO_BASE - int(m.group()))
    return None

def escala(v):
    x = num(v)
    if x is None: return None
    return x * 5 if x <= 20 else x

def ct_de(v):
    if isinstance(v, (dt.date, dt.datetime)): return dt.date(v.year, v.month, v.day).toordinal()
    m = re.search(r'(20\d\d)', str(v or ''))
    return od(int(m.group()), '06-30') if m else None

def ovr_por_valor(val, idade):
    f = 1.3 if idade <= 21 else 1.12 if idade <= 25 else 1.0 if idade <= 29 else .7 if idade <= 32 else .4
    return 50 + math.log(max(25, val) / (50 * f)) / math.log(1.2)

def jogador_importado(r, T, s, idx):
    pos = POSMAP.get(norm(str(r.get('pos', ''))).split('/')[0].strip()) or POSMAP.get(norm(str(r.get('pos', ''))).split(' ')[0]) or 'MEI'
    idade = idade_de(r) or int(R.triangular(18, 34, 25)); val = euros_mil(r.get('val'))
    ovr = escala(r.get('forca'))
    if ovr is None: ovr = ovr_por_valor(val, idade) if val else R.gauss(s + 1 - 1.8 * idx, 3)
    nat = pais_codigo(r.get('nat')) or T['cc']
    p = novo_jogador(pos, ovr, nat, T['id'], idade); p['n'] = str(r['nome']).strip()[:40]
    if r.get('fis') is not None: p['fis'] = int(max(30, min(99, escala(r['fis']) or p['fis'])))
    if r.get('pot') is not None: p['pot'] = int(max(p['ovr'], min(99, escala(r['pot']) or p['pot'])))
    pe = norm(r.get('pe', ''))
    if pe: p['pe'] = 'E' if pe[0] in 'el' or 'canh' in pe or 'left' in pe or 'esq' in pe else 'A' if pe[0] == 'a' or 'both' in pe else 'D'
    if r.get('hab'):
        hs = []
        for tok in re.split(r'[/,;|+]', norm(r['hab'])):
            h = HABMAP.get(tok.strip())
            if h and h not in hs: hs.append(h)
        p['hab'] = hs[:4]
    if val: p['val'] = int(val)
    sal = euros_mil(r.get('sal'))
    if sal: p['sal'] = max(1, int(sal / (52 if sal > p['val'] / 40 else 1)))
    else: p['sal'] = max(1, p['val'] // 260)
    ct = ct_de(r.get('ct'))
    if ct: p['ct'] = ct
    n = num(r.get('num'))
    if n and 0 < n < 100: p['num'] = int(n)
    return p

def completar_elenco(T, s):
    falta = {pos: qt for pos, qt in (('GOL', 2), ('ZAG', 4), ('LAT', 3), ('VOL', 2), ('MEI', 3), ('ATA', 3))}
    for x in T['pl']:
        if falta.get(G.P[x]['pos'], 0) > 0: falta[G.P[x]['pos']] -= 1
    for pos, qt in falta.items():
        for i in range(qt):
            p = novo_jogador(pos, R.gauss(s - 6, 3), T['cc'], T['id']); p['num'] = numero_livre(T, pos); T['pl'].append(p['id'])

def remover_clube(tid):
    T = G.T.pop(tid)
    for x in T['pl']: G.P.pop(x, None)
    if T.get('tec') in G.TEC: G.TEC[T['tec']]['t'] = None

def montar_clube(nome, cc, linhas, s, lg=None):
    T = criar_clube(nome, cc, s, lg=lg, cup=cc, jogadores=not linhas)
    cont = {}
    for r in linhas:
        pos = POSMAP.get(norm(str(r.get('pos', ''))).split('/')[0].strip(), 'MEI'); cont[pos] = cont.get(pos, 0) + 1
        p = jogador_importado(r, T, s, cont[pos] - 1)
        if not p['num']: p['num'] = numero_livre(T, p['pos'])
        T['pl'].append(p['id'])
    if linhas:
        completar_elenco(T, s)
        top = sorted((G.P[x]['ovr'] for x in T['pl']), reverse=True)[:14]; T['str'] = round(sum(top) / len(top) - 1)
        financas_iniciais(T)
    auto_xi(T); return T

def importar_planilha(caminho):
    jog, cls = ler_planilha(caminho)
    if not jog and not cls: raise ValueError('Não encontrei colunas reconhecíveis (ex.: Clube, Jogador, Posição, Liga, País).')
    if caminho not in IMPORTADOS: IMPORTADOS.append(caminho)
    por_liga = {norm(L['n']): L for L in G.L}; por_copa = {norm(v): k for k, v in COPAS.items()}
    antigos = {norm(T['n']): T for T in clubes()}
    grupos = {}                      # (tipo, cc, liga) -> {clube: [linhas]}
    for r in jog + cls:
        liga = str(r.get('liga') or ('' if norm(r['_folha']) in ('sheet1', 'planilha1', 'plan1', 'jogadores', 'players', 'dados', 'clubes') else r['_folha'])).strip()
        nl = norm(liga); tipo = norm(r.get('tipo', ''))
        copa = any(w in nl for w in MARCA_COPA) or any(w in tipo for w in ('copa', 'cup')) or not liga
        cc = pais_codigo(r.get('pais')) or (por_liga[nl]['cc'] if nl in por_liga else None) or por_copa.get(nl) or \
             (antigos[norm(r['clube'])]['cc'] if norm(r['clube']) in antigos else None) or pais_codigo(r.get('nat')) or 'BR'
        g = grupos.setdefault(('copa' if copa else 'liga', cc, '' if copa else liga), {})
        lst = g.setdefault(str(r['clube']).strip(), [])
        if 'nome' in r: lst.append(r)
    n_cl = n_jog = 0; ligas_pais = {}
    for (tipo, cc, liga) in grupos:
        if tipo == 'liga': ligas_pais.setdefault(cc, []).append(liga)
    for (tipo, cc, liga), cl in grupos.items():
        if tipo != 'liga': continue
        L = por_liga.get(norm(liga))
        if not L:
            do_pais = [x for x in G.L if x['cc'] == cc]
            topo = any(w in norm(liga).split() for w in ('a', '1', 'primeira', 'premier', 'primera', 'first', 'superliga', 'super', 'pro'))
            if do_pais and (len(ligas_pais[cc]) == 1 or topo) and not any(x.get('importada') for x in do_pais): L = do_pais[0]
        if L:
            for t in list(L['clubs']): remover_clube(t)
            L['clubs'] = []; L['n'] = liga or L['n']
        else:
            base = next((x for x in G.L if x['cc'] == cc), None)
            L = dict(i=len(G.L), cc=cc, n=liga, ini=base['ini'] if base else '08-16', clubs=[], fx=[], tab={}, res={}, champ=[], temp='',
                     top=(base['bot'] if base else 66), bot=(base['bot'] - 10 if base else 55)); G.L.append(L)
        L['importada'] = True; nomes = list(cl)
        for k, nome in enumerate(nomes):
            antigo = antigos.get(norm(nome))
            s = antigo['str'] if antigo else L['top'] - (L['top'] - L['bot']) * (k / max(1, len(nomes) - 1))
            T = montar_clube(nome, cc, cl[nome], s, lg=L['i']); L['clubs'].append(T['id']); n_cl += 1; n_jog += len(cl[nome])
        if len(L['clubs']) < 2: raise ValueError('A liga %s precisa de pelo menos 2 clubes.' % liga)
    for (tipo, cc, liga), cl in grupos.items():
        if tipo != 'copa': continue
        ref = next((x for x in G.L if x['cc'] == cc), None); s0 = (ref['bot'] - 8) if ref else 55
        for nome, linhas in cl.items():
            if norm(nome) in {norm(G.T[t]['n']) for L in G.L for t in L['clubs']}: continue
            montar_clube(nome, cc, linhas, R.gauss(s0, 3)); n_cl += 1; n_jog += len(linhas)
        if cc not in G.C and ref is None:
            pass
    return dict(clubes=n_cl, jogadores=n_jog)
