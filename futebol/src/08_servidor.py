# ----------------------------- SERVIDOR ------------------------------
app = Flask(__name__)

@app.route('/')
def index():
    return Response(HTML, mimetype='text/html')

@app.route('/api/<nome>', methods=['POST'])
def api(nome):
    d = request.get_json(silent=True) or {}
    with LOCK:
        try:
            if nome not in API: return jsonify(erro='Ação desconhecida.')
            if nome not in ('meta', 'novo', 'estado', 'carregar') and not (G and G.coach): return jsonify(erro='Comece um novo jogo.')
            return jsonify(API[nome](d))
        except Exception as e:
            traceback.print_exc(); return jsonify(erro=str(e) or 'Erro interno.')

@app.route('/upload', methods=['POST'])
def upload():
    f = request.files.get('arq')
    if not f or not f.filename: return jsonify(erro='Nenhum arquivo enviado.')
    ext = os.path.splitext(f.filename)[1].lower()
    if ext not in ('.xlsx', '.xlsm', '.csv'): return jsonify(erro='Envie um arquivo .xlsx ou .csv.')
    destino = os.path.abspath('prancheta_dados' + ext); f.save(destino)
    with LOCK:
        try:
            IMPORTADOS[:] = []; gerar_mundo(); res = importar_planilha(destino); gerar_mundo()
            return jsonify(msg='Planilha carregada: %d clubes e %d jogadores importados.' % (res['clubes'], res['jogadores']), **a_meta({}))
        except Exception as e:
            traceback.print_exc(); IMPORTADOS[:] = []; gerar_mundo(); return jsonify(erro='Não consegui ler a planilha: %s' % e)

@app.route('/remover_dados', methods=['POST'])
def remover_dados():
    with LOCK:
        IMPORTADOS[:] = []; gerar_mundo(); return jsonify(msg='Voltando aos dados gerados pelo jogo.', **a_meta({}))

def porta_livre(p):
    import socket
    for q in range(p, p + 50):
        with socket.socket() as s:
            try: s.bind(('0.0.0.0', q)); return q
            except OSError: continue
    return p

def preparar_dados():
    for arq in (DADOS_XLSX, 'prancheta_dados.csv', '/content/drive/MyDrive/' + DADOS_XLSX):
        if os.path.exists(arq) and arq not in IMPORTADOS: IMPORTADOS.append(os.path.abspath(arq)); break
    gerar_mundo()

def iniciar_servidor(porta=PORTA):
    if G is None: preparar_dados()
    import logging; logging.getLogger('werkzeug').setLevel(logging.ERROR)
    porta = porta_livre(porta)
    th = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False, threaded=True), daemon=True)
    th.start()
    print('Prancheta FC: %d ligas, %d clubes, %d jogadores, %d seleções%s.' % (len(G.L), len(clubes()), len(G.P), len(selecoes()),
          (' (dados de ' + ', '.join(os.path.basename(x) for x in IMPORTADOS) + ')') if IMPORTADOS else ''))
    try:
        from google.colab import output   # Google Colab
        output.serve_kernel_port_as_window(porta, anchor_text='>>> CLIQUE AQUI para abrir o Prancheta FC em tela cheia (recomendado) <<<')
        output.serve_kernel_port_as_iframe(porta, height=860)
        return
    except ImportError:
        pass
    url = 'http://127.0.0.1:%d' % porta
    print('Abra no navegador:', url, '(no celular, use o IP deste computador na mesma rede Wi-Fi)')
    try:
        import webbrowser; webbrowser.open(url)
    except Exception:
        pass
    if 'ipykernel' not in sys.modules:
        try: th.join()
        except KeyboardInterrupt: print('Encerrado.')

if __name__ == '__main__':
    iniciar_servidor()
