const $=s=>document.querySelector(s),V=()=>$('#view');
const S={v:'elenco',st:null,meta:null,t:'clube',sel:null,el:null,pk:null,ord:null,card:null,agf:'todos',lg:null,tlg:null,
  mf:{pos:'',q:'',max:'',lg:'',min:'',idade:''},vel:lsg('vel')||'u',tecf:'todos'};
const GRP={GOL:'G',ZAG:'D',LAT:'D',VOL:'M',MEI:'M',ATA:'A'},PE={D:'Destro',E:'Canhoto',A:'Ambidestro'},PEC={D:'D',E:'E',A:'A'};
const POSN={GOL:'Goleiro',ZAG:'Zagueiro',LAT:'Lateral',VOL:'Volante',MEI:'Meia',ATA:'Atacante'};
const HB={FIN:'Finalização',CAB:'Cabeceio',DRI:'Drible',PAS:'Passe',VEL:'Velocidade',DES:'Desarme',MAR:'Marcação',CHL:'Chute de longe',BOL:'Bola parada',PEN:'Pênaltis',LID:'Liderança',REF:'Reflexos',SAI:'Saída do gol',RES:'Resistência',CRU:'Cruzamento'};
const AB={FIN:'Fin',CAB:'Cab',DRI:'Dri',PAS:'Pas',VEL:'Vel',DES:'Des',MAR:'Mar',CHL:'Chu',BOL:'Bpa',PEN:'Pen',LID:'Lid',REF:'Ref',SAI:'Sgo',RES:'Res',CRU:'Cru'};
const FORMS=['4-4-2','4-3-3','4-2-3-1','3-5-2','5-3-2','3-4-3','4-5-1'],TAC=[['D','Defensiva'],['E','Equilibrada'],['O','Ofensiva']];
const VEL={u:['Ultra rápido',85,5],r:['Rápido',320,3],n:['Normal',950,2]};
function lsg(k){try{return localStorage.getItem('pfc_'+k)}catch(e){return null}}
function lss(k,v){try{localStorage.setItem('pfc_'+k,v)}catch(e){}}
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>'&#'+c.charCodeAt(0)+';');
const mob=()=>matchMedia('(max-width:900px)').matches;
function api(a,b){return fetch('api/'+a,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})}).then(r=>r.json()).then(j=>{if(j.erro){toast(j.erro,1);throw new Error(j.erro)}if(j.msg)toast(j.msg);return j})}
function toast(m,bad){const t=$('#toast');t.textContent=m;t.className='show'+(bad?' bad':'');clearTimeout(t._t);t._t=setTimeout(()=>t.className='',3000)}
function modal(html,cls=''){$('#modal').innerHTML=`<div class="mbox ${cls}">${html}</div>`;$('#modal').onclick=e=>{if(e.target.id=='modal')fechar()}}
function fechar(){$('#modal').innerHTML=''}
function ask(m){return new Promise(r=>{modal(`<p>${esc(m)}</p><div class="row"><button class="btn sec" id="mn">Cancelar</button><button class="btn" id="ms">Confirmar</button></div>`,'peq');$('#mn').onclick=()=>{fechar();r(false)};$('#ms').onclick=()=>{fechar();r(true)}})}
const mo=k=>k==null?'–':(k<0?'-':'')+(Math.abs(k)>=1000?'€ '+(Math.abs(k)/1000).toLocaleString('pt-BR',{maximumFractionDigits:1})+' mi':'€ '+Math.round(Math.abs(k))+' mil');
const bdg=(t,c='')=>`<span class="bdg ${c}" style="background:${t.cor[0]};color:${t.cor[1]}">${t.fl||esc(t.sig)}</span>`;
const ov=v=>`<span class="ov ${v>=85?'o5':v>=78?'o4':v>=70?'o3':v>=60?'o2':'o1'}">${Math.round(v)}</span>`;
const bar=(v,c)=>`<div class="bar"><i style="width:${Math.max(0,Math.min(100,v))}%;background:${c||(v>66?'var(--pri)':v>40?'var(--yel)':'var(--red)')}"></i></div>`;
const corv=v=>v>66?'#0e9f6e':v>40?'#f5b301':'#e5484d';
const cbar=v=>`<div class="cbar"><i style="width:${v}%;background:${corv(v)}"></i><span>${Math.round(v)}%</span></div>`;
const energia=v=>`<span class="en"><i style="width:${v}%;background:${corv(v)}"></i><span>${Math.round(v)}%</span></span>`;
const habs=(h,full)=>h.map(x=>`<span class="chip" title="${HB[x]}">${full?HB[x]:AB[x]}</span>`).join('');
const notaH=n=>n==null?'<span class="mut">–</span>':`<span class="nota ${n<5.5?'n1':n<6.3?'n2':n<7?'n3':n<8?'n4':'n5'}">${(+n).toFixed(1)}</span>`;
const tacs=(cur,fn)=>TAC.map(([k,l])=>`<button class="${cur==k?'on':''}" onclick="${fn}({tac:'${k}'})">${l}</button>`).join('');
const fsel=(cur,fn)=>`<select onchange="${fn}({form:this.value})">${FORMS.map(f=>`<option ${f==cur?'selected':''}>${f}</option>`).join('')}</select>`;
const vazio=m=>`<div class="card"><p class="mut">${m}</p></div>`;
function luz(h){const c=h.replace('#','');const r=parseInt(c.substr(0,2),16),g=parseInt(c.substr(2,2),16),b=parseInt(c.substr(4,2),16);return (.299*r+.587*g+.114*b)/255}
const IC={elenco:'<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.5.6 4 2.8 4 6"/>',
agenda:'<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',selecao:'<path d="M5 21V4h11l-2 4 2 4H5"/>',
tabelas:'<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M3 14h18M9 9v11"/>',estadio:'<ellipse cx="12" cy="12" rx="9.5" ry="6"/><ellipse cx="12" cy="12" rx="4.5" ry="2.6"/>',
juniores:'<path d="M12 21v-8M12 13c0-4 3-6 7-6 0 4-3 6-7 6zM12 15c0-3-2.5-5-6-5 0 3 2.5 5 6 5z"/>',times:'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/>',
procura:'<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',tecnicos:'<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 4-6 8-6s8 2 8 6M8 5h8"/>',
historia:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 3"/>',mensagens:'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
opcoes:'<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/>'};
const MENU=[['elenco','Elenco'],['agenda','Agenda'],['selecao','Seleção'],['tabelas','Tabelas'],['estadio','Estádio'],['juniores','Juniores'],['times','Times'],['procura','Procura'],['tecnicos','Técnicos'],['historia','História'],['mensagens','Mensagens'],['opcoes','Opções']];
function menu(){const n=S.st?.nmsg||0;$('#menu').innerHTML=MENU.map(([k,l])=>`<button class="${S.v==k||(S.v=='escalar'&&k=='elenco')?'on':''}" onclick="go('${k}')"><svg viewBox="0 0 24 24">${IC[k]}</svg>${l}${k=='mensagens'&&n?`<span class="badge">${n}</span>`:''}</button>`).join('')}
const R={};
async function go(v){if(LV&&!LV.done){toast('Partida em andamento!',1);return}S.v=v;fechar();menu();scrollTo(0,0);try{await R[v]()}catch(e){console.error(e)}}
async function refresh(){S.st=await api('estado');topo();painel()}
function topo(){const s=S.st;$('#hoje').innerHTML=s&&s.jogo?`${s.dsem}, ${s.data}<small>${s.prox.h?'Próximo: '+s.prox.data:''}</small>`:'';
 $('#bjogar').textContent=s&&s.jogo&&s.prox.h?'▶ Jogar':'⏩ Avançar';menu()}
async function boot(){S.st=await api('estado');if(!S.st.jogo){S.meta=await api('meta');return novo()}document.body.classList.remove('nogame');topo();painel();if(S.st.live)return startLive(await api('snap'));go('elenco')}
/* ---------------- painel lateral ---------------- */
function painel(){const s=S.st,P=$('#painel');if(!s||!s.jogo){P.innerHTML='';return}
 const T=s.clube||s.sel,cor=T?T.cor:['#0e9f6e','#fff'];P.style.setProperty('--pc',cor[0]);P.style.setProperty('--pt',cor[1]);P.classList.toggle('claro',luz(cor[0])>.62);
 const p=s.prox,adv=p.h?(p.casa?p.a:p.h):null;
 P.innerHTML=`<div class="pn-top" onclick="$('#painel').classList.toggle('aberto')">${T?bdg(T,'lg'):''}<div><b class="pn-nome">${T?esc(T.n):'Sem time'}</b><small>${esc(s.tecnico.n)}${s.clube&&s.sel?' · '+s.sel.fl+' '+esc(s.sel.n):''}</small></div><span class="pn-seta">▾</span></div>
 <div class="pn-corpo">
  ${s.clube?`<div class="pn-linha pn-sempre"><span>💰 <b>${mo(s.bud)}</b></span><button class="pn-msg" onclick="event.stopPropagation();go('mensagens')">✉ ${s.nmsg}</button></div>
  <div><small>${esc(s.liga)} ${s.temp?'· '+s.temp:''} · <b>${s.pos}º lugar</b></small></div>
  <div class="pn-conf"><div><small>Confiança diretoria</small>${cbar(s.tecnico.conf)}</div><div><small>Confiança torcida</small>${cbar(s.tor)}</div></div>`
  :`<div class="pn-box"><small>Você está sem clube. Veja as propostas em Mensagens.</small></div>`}
  <div class="pn-box pn-sempre"><div class="pn-prox-t">${p.h?'Próximo jogo – '+(p.casa?'Casa':'Fora'):'Agenda'}</div>
   ${adv?`<div class="pn-adv">${bdg(adv)}<div><b>${esc(adv.n)}</b><small>${esc(p.comp)}<br>${p.data}</small></div></div>`:`<small>${esc(p.comp)}</small>`}</div>
  <div class="pn-bts"><button class="btn jogar" onclick="jogar()">${p.h?'▶ Jogar':'⏩ Avançar'}</button><button class="btn sec2" onclick="go('escalar')">Escalar time</button></div>
  <div id="card"></div>
  ${s.clube?`<div class="pn-rod"><span>👥 ${s.nel}/35</span><span>Folha ${mo(s.folha)}/sem</span></div>`:''}
 </div>`;desenharCard()}
function htmlCard(p){if(!p)return '<div class="cardj vazio"><small>Toque num jogador para ver a ficha.</small></div>';
 const st=p.st,f=v=>v==null?'–':v;let ac='';
 if(p.meu&&!p.emp&&!p.jr)ac=`<button onclick="acaoJ('vender',${p.id})">💰 Vender</button><button onclick="renovar(${p.id})">✍️ Renovar</button><button onclick="acaoJ('emprestar',${p.id})">🔁 Emprestar</button><button class="red" onclick="acaoJ('dispensar',${p.id})">Dispensar</button>`;
 else if(!p.meu&&!p.jr&&!p.emp&&S.st.clube)ac=`<button onclick="comprar(${p.id},'${esc(p.n).replace(/&#39;/g,'')}',${Math.round(p.val*1.15)})">🛒 Comprar ${mo(Math.round(p.val*1.15))}</button>`;
 return `<div class="cardj"><div class="cj-h">${p.fl} <b>${esc(p.n)}</b>${p.craque?'<span class="estrela">★</span>':''}<span class="cj-f">F:${p.ovr}</span></div>
 ${ac?`<div class="cj-acoes">${ac}</div>`:''}<small>${POSN[p.pos]} · ${PE[p.pe]} · ${p.age} anos · Nº ${p.num||'–'} · ${esc(p.cl)}</small>
 <small>Contrato até ${p.ct}${p.emp?` · emprestado até ${p.empf}`:''}</small>
 <div class="cj-v"><span>Valor <b>${mo(p.val)}</b></span><span>Salário <b>${mo(p.sal)}</b>/sem</span></div>
 <div class="cj-v"><span>Físico <b>${p.fis}</b></span><span>Potencial <b>${p.pot}</b></span><span>Energia <b>${p.cond}%</b></span></div>
 <div>${habs(p.hab,1)||'<small>Sem habilidades especiais</small>'}</div>
 ${p.inj?`<small class="red">Lesionado: ${p.inj} dias</small>`:''}${p.sus?'<small class="red">Suspenso</small>':''}
 <table class="cj-st"><tr><th></th><th>Temporada</th><th>Carreira</th><th>Liga</th></tr>
 ${[['Jogos',0],['Gols',1],['Assistências',2],['Nota média',3]].map(([n,i])=>`<tr><td>${n}</td>${['t','c','l'].map(k=>`<td>${f(st[k][i])}</td>`).join('')}</tr>`).join('')}</table></div>`}
function desenharCard(){const el=$('#card');if(el)el.innerHTML=htmlCard(S.card)}
async function verJogador(id,local){const p=local||await api('jogador',{pid:id});S.card=p;desenharCard();
 if(mob())modal(`<div class="mhead"><h2>Ficha do jogador</h2><button class="x" onclick="fechar()">✕</button></div>${htmlCard(p)}`,'peq');}
async function acaoJ(a,id){const nomes={vender:'Vender',emprestar:'Emprestar',dispensar:'Dispensar (com multa rescisória)'};
 if(!await ask(nomes[a]+' '+(S.card?.n||'o jogador')+'?'))return;await api(a,{pid:id});S.card=null;fechar();await refresh();if(R[S.v])R[S.v]()}
async function renovar(id){const r=await api('renovar',{pid:id});const p=r.prop;
 const ok=await ask(`Renovar até ${p.ate}? Salário pedido: ${mo(p.sal)}/semana (atual ${mo(p.atual)}).`);await api('renovar',{pid:id,ok});await refresh();verJogador(id)}
async function comprar(pid,n,v){if(await ask(`Contratar ${n} por ${mo(v)}?`)){await api('comprar',{pid});await refresh();verJogador(pid);if(S.v=='procura')R.procura()}}
/* ---------------- novo jogo ---------------- */
function novo(){document.body.classList.add('nogame');$('#painel').innerHTML='';const m=S.meta;S.sel=null;
 V().innerHTML=`<div class="hero"><div class="logo xl">P</div><h1>Prancheta FC</h1><p>Assuma um clube (e, se quiser, uma seleção), monte o time, acompanhe as partidas ao vivo e construa sua carreira de técnico.</p></div>
 <div class="card"><div class="form"><label>Seu nome<input id="nm" value="Professor" maxlength="30"></label>
 <label>Liga<select id="lg" onchange="clubesNovo()">${m.ligas.map(l=>`<option value="${l.i}">${l.fl} ${esc(l.pais)} — ${esc(l.n)}</option>`).join('')}</select></label>
 <label>Seleção (opcional)<select id="ns"><option value="">Nenhuma</option>${m.sels.map(x=>`<option value="${x.id}">${x.fl} ${esc(x.n)} (${Math.round(x.f)})</option>`).join('')}</select></label></div>
 <h3 style="margin:16px 0 10px">Escolha seu clube</h3><div id="cls" class="clubs"></div>
 <div class="row" style="margin-top:16px"><button class="btn big" onclick="comecar()">Começar carreira ▶</button>${m.save?'<button class="btn sec big" onclick="carregar()">Carregar jogo salvo</button>':''}</div></div>
 <div class="card"><h3>Dados dos jogadores</h3><p class="hint mut" style="margin-bottom:10px">${m.dados.length?'Usando a planilha <b>'+esc(m.dados.join(', '))+'</b>.':'Usando jogadores gerados pelo jogo.'} Para usar ligas, clubes e jogadores reais, carregue uma planilha .xlsx/.csv (colunas como País, Liga, Clube, Jogador, Posição, Idade, Força...).</p>
 <div class="tools"><input type="file" id="arq" accept=".xlsx,.xlsm,.csv"><button class="btn sec" onclick="enviarPlanilha()">Carregar planilha</button>${m.dados.length?'<button class="btn red" onclick="removerDados()">Usar dados do jogo</button>':''}</div></div>`;clubesNovo()}
function clubesNovo(){const l=S.meta.ligas[$('#lg').value];$('#cls').innerHTML=l.clubs.map(c=>`<button class="club ${S.sel==c.id?'on':''}" onclick="S.sel='${c.id}';clubesNovo()">${bdg(c)}<span>${esc(c.n)}</span>${ov(c.f)}</button>`).join('')}
async function comecar(){if(!S.sel)return toast('Escolha um clube',1);toast('Preparando a temporada...');S.st=await api('novo',{nome:$('#nm').value,clube:S.sel,sel:$('#ns').value});
 document.body.classList.remove('nogame');S.card=null;topo();painel();go('elenco')}
async function carregar(){S.st=await api('carregar');document.body.classList.remove('nogame');LV=null;S.card=null;topo();painel();go('elenco')}
async function novoJogo(){if(!await ask('Começar um novo jogo? O progresso não salvo será perdido.'))return;S.meta=await api('meta');novo()}
async function enviarPlanilha(){const f=$('#arq').files[0];if(!f)return toast('Escolha um arquivo .xlsx ou .csv',1);
 if(S.st&&S.st.jogo&&!await ask('Carregar a planilha cria um novo mundo e encerra o jogo atual (salve antes). Continuar?'))return;
 const fd=new FormData();fd.append('arq',f);toast('Lendo a planilha...');const r=await fetch('upload',{method:'POST',body:fd}).then(r=>r.json());
 if(r.erro)return toast(r.erro,1);toast(r.msg);S.meta=r;S.st=null;novo()}
async function removerDados(){const r=await fetch('remover_dados',{method:'POST'}).then(r=>r.json());toast(r.msg);S.meta=r;novo()}
/* ---------------- elenco (tabela) ---------------- */
const COLS=[['pos','P'],['n','Nome'],['num','Nº','hm'],['pe','L','hm'],['ovr','F'],['fis','Fís','hm'],['pot','Pot','hm'],['cond','Energia'],['sal','Salário','hm'],['val','Valor','hm'],['hab','Car.'],['age','Idade','hm'],['j','J','hm'],['g','G','hm'],['a','A','hm'],['nm','NM','hm'],['ct','Contrato','hm']];
const PORD=['GOL','LAT','ZAG','VOL','MEI','ATA'];
function chave(p,k){if(k=='pos')return PORD.indexOf(p.pos)*1000-p.ovr;if(k=='ct')return p.ct.split('/').reverse().join('');if(k=='hab')return p.hab.join();return p[k]??-1}
function ordenar(k){S.ord=S.ord&&S.ord.k==k?{k,d:-S.ord.d}:{k,d:['n','pos','hab','ct'].includes(k)?1:-1};drawElenco()}
R.elenco=async()=>{await refresh();const s=S.st;if(!s.clube&&!s.sel){V().innerHTML=vazio('Você está sem time. Veja as propostas em Mensagens.');return}
 if(S.t=='clube'&&!s.clube)S.t='sel';if(S.t=='sel'&&!s.sel)S.t='clube';S.el=await api('elenco',{t:S.t});drawElenco()}
function linhaJog(p,e,emp){const cr=e.craques.includes(p.id),tit=e.xi.includes(p.id);
 return `<tr class="p-${p.pos} ${tit?'tit':''} ${S.card&&S.card.id==p.id?'selj':''}" onclick="selJog(${p.id})"><td><b>${p.pos[0]}</b></td>
 <td>${cr?'<span class="estrela">★</span> ':''}<b>${esc(p.n)}</b> ${p.inj?'🩹':''}${p.sus?'🟥':''}${emp?` <small class="mut">→ ${esc(p.emp)}</small>`:''}</td>
 <td class="hm">${p.num||''}</td><td class="hm">${PEC[p.pe]}</td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td>${energia(p.cond)}</td>
 <td class="hm">${mo(p.sal)}</td><td class="hm">${mo(p.val)}</td><td>${p.hab.slice(0,2).map(x=>AB[x]).join('/')||'–'}</td><td class="hm">${p.age}</td>
 <td class="hm">${p.j}</td><td class="hm">${p.g}</td><td class="hm">${p.a}</td><td class="hm">${p.nm??'–'}</td><td class="hm">${p.ct}</td></tr>`}
function drawElenco(){const e=S.el,s=S.st;let pl=e.pl.slice();
 if(S.ord)pl.sort((a,b)=>{const x=chave(a,S.ord.k),y=chave(b,S.ord.k);return (x>y?1:x<y?-1:0)*S.ord.d});else pl.sort((a,b)=>chave(a,'pos')-chave(b,'pos'));
 const th=COLS.map(([k,t,c])=>`<th class="${c||''}" onclick="ordenar('${k}')">${t}${S.ord&&S.ord.k==k?(S.ord.d>0?' ▲':' ▼'):''}</th>`).join('');
 V().innerHTML=`<div class="barra-v"><h2>${e.t.fl||''} ${esc(e.t.n)}<small>${e.n} jogadores · força ${Math.round(e.t.f)} · ${e.form}</small></h2>
 ${s.clube&&s.sel?`<div class="seg">${[['clube','Clube'],['sel','Seleção']].map(([k,l])=>`<button class="${S.t==k?'on':''}" onclick="S.t='${k}';R.elenco()">${l}</button>`).join('')}</div>`:''}
 <div class="sp"></div><button class="btn" onclick="go('escalar')">⚽ Escalar time</button></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr>${th}</tr></thead><tbody>${pl.map(p=>linhaJog(p,e)).join('')}</tbody></table></div>
 ${e.emp.length?`<h3 class="sub">Emprestados</h3><div class="tabela-wrap"><table class="dens"><tbody>${e.emp.map(p=>linhaJog(p,e,1)).join('')}</tbody></table></div>`:''}
 <p class="hint mut" style="margin-top:8px">★ craque do elenco · barra verde à esquerda = titular · toque no jogador para ver a ficha · toque no título da coluna para ordenar</p>`}
function selJog(id){const p=[...S.el.pl,...S.el.emp].find(x=>x.id==id);if(!p)return;p.meu=!S.el.nac;p.craque=S.el.craques.includes(id);verJogador(id,p);
 document.querySelectorAll('tr.selj').forEach(t=>t.classList.remove('selj'));}
/* ---------------- escalação ---------------- */
function coords(sl){const r={G:[],D:[],M:[],A:[]},o=[];sl.forEach((s,i)=>r[s].push(i));
 for(const g of 'GDMA'){const ids=r[g],n=ids.length;if(g=='M'&&n>=5){ids.slice(0,2).forEach((k,j)=>o[k]=[(j+1)*100/3,60]);const a=ids.slice(2);a.forEach((k,j)=>o[k]=[(j+1)*100/(a.length+1),39])}
 else ids.forEach((k,j)=>o[k]=[(j+1)*100/(n+1),{G:91,D:73,M:49,A:19}[g]])}return o}
R.escalar=async()=>{await refresh();const s=S.st;if(!s.clube&&!s.sel){V().innerHTML=vazio('Você está sem time.');return}
 if(S.t=='clube'&&!s.clube)S.t='sel';if(S.t=='sel'&&!s.sel)S.t='clube';S.el=await api('elenco',{t:S.t});S.pk=null;drawEsc()}
function drawEsc(){const e=S.el,P={},s=S.st;e.pl.forEach(p=>P[p.id]=p);const c=coords(e.sl),res=e.pl.filter(p=>!e.xi.includes(p.id)).sort((a,b)=>chave(a,'pos')-chave(b,'pos'));
 const li=p=>`<tr class="p-${p.pos} ${S.pk==p.id?'selj':''}" onclick="pick(${p.id})"><td><b>${p.pos}</b></td><td><b>${esc(p.n)}</b> ${p.inj?'🩹':''}${p.sus?'🟥':''}</td><td>${ov(p.ovr)}</td><td>${energia(p.cond)}</td><td>${p.hab.slice(0,2).map(x=>AB[x]).join('/')}</td></tr>`;
 V().innerHTML=`<div class="barra-v"><h2>Escalar ${esc(e.t.n)}</h2>${s.clube&&s.sel?`<div class="seg">${[['clube','Clube'],['sel','Seleção']].map(([k,l])=>`<button class="${S.t==k?'on':''}" onclick="S.t='${k}';R.escalar()">${l}</button>`).join('')}</div>`:''}
 ${fsel(e.form,'escl')}<div class="seg">${tacs(e.tac,'escl')}</div><button class="btn sec" onclick="autoEl()">Automático</button><div class="sp"></div><button class="btn sec" onclick="go('elenco')">✕ Fechar</button></div>
 <p class="hint mut" style="margin-bottom:10px">Toque em dois jogadores (no campo ou na lista) para trocá-los de lugar.</p>
 <div class="two"><div><div class="pitch" style="--kit:${e.t.cor[0]}"><div class="area t"></div><div class="area b"></div>${e.xi.map((id,i)=>{const p=P[id],bad=GRP[p.pos]!=e.sl[i];return `<div class="pp ${S.pk==id?'sel':''} ${bad?'bad':''}" style="left:${c[i][0]}%;top:${c[i][1]}%" onclick="pick(${id})"><div class="c">${p.ovr}</div><div class="nm">${esc(p.n)}</div><div class="ps">${p.pos}${bad?' ⚠':''}</div></div>`}).join('')}</div>
 <p class="hint mut" style="text-align:center;margin-top:8px">Força do time: <b>${Math.round(e.t.f)}</b> · ⚠ fora de posição</p></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th>Pos</th><th>Titulares</th><th>F</th><th>Energia</th><th>Car.</th></tr></thead><tbody>${e.xi.map(id=>li(P[id])).join('')}</tbody>
 <thead><tr><th>Pos</th><th>Reservas</th><th>F</th><th>Energia</th><th>Car.</th></tr></thead><tbody>${res.map(li).join('')}</tbody></table></div></div>`}
async function pick(id){if(S.pk==null){S.pk=id;return drawEsc()}if(S.pk==id){S.pk=null;return drawEsc()}const a=S.pk;S.pk=null;S.el=await api('trocar',{t:S.t,a,b:id}).catch(()=>S.el);drawEsc()}
async function escl(o){S.el=await api('escalar',{t:S.t,...o});drawEsc()}
async function autoEl(){S.el=await api('auto',{t:S.t});drawEsc();toast('Time escalado automaticamente')}
/* ---------------- agenda ---------------- */
function meuId(){return [S.st.clube?.id,S.st.sel?.id]}
R.agenda=async()=>{const d=await api('agenda',{f:S.agf});const ids=meuId();let prox=false;
 const linhas=d.rows.map(r=>{let cls='',cel='x';
  if(r.res){const eu=ids.includes(r.h?.id)?0:1,a=r.res[eu],b=r.res[1-eu],pa=r.pen?r.pen[eu]:0,pb=r.pen?r.pen[1-eu]:0;
   const k=a>b||(a==b&&pa>pb)?'V':a<b||(a==b&&pa<pb)?'D':'E';cel=`<span class="res ${k}">${r.res[0]} x ${r.res[1]}${r.pen?` <small>(${r.pen[0]}-${r.pen[1]})</small>`:''}</span>`}
  else if(!prox&&r.o>=d.hoje&&r.h&&r.a){prox=true;cls='prox'}
  return `<tr class="${cls} ${r.arq?'click':''}" ${r.arq?`onclick="abrirRelatorio('${r.arq}')"`:''}><td>${r.d}</td><td class="r">${r.h?esc(r.h.n)+' '+bdg(r.h,'sm'):''}</td><td style="text-align:center">${cel}</td>
  <td>${r.a?bdg(r.a,'sm')+' '+esc(r.a.n):'<span class="mut">a definir</span>'}</td><td>${esc(r.comp)}</td><td class="hm">${r.pub?r.pub.toLocaleString('pt-BR'):''}</td><td class="hm">${r.renda!=null?mo(r.renda):''}</td></tr>`}).join('');
 V().innerHTML=`<div class="janela"><div class="jan-h"><h2>📅 Calendário – ${esc(d.titulo)}</h2><select onchange="S.agf=this.value;R.agenda()">
 <option value="todos">Mostrar todos</option>${S.st.clube&&S.st.sel?`<option value="clube" ${S.agf=='clube'?'selected':''}>Somente clube</option><option value="sel" ${S.agf=='sel'?'selected':''}>Somente seleção</option>`:''}
 ${d.comps.map(c=>`<option ${S.agf==c?'selected':''}>${esc(c)}</option>`).join('')}</select><button class="x" onclick="go('elenco')">✕</button></div>
 <div class="tw"><table class="ag"><thead><tr><th>Data</th><th style="text-align:right">Mandante</th><th></th><th>Visitante</th><th>Competição</th><th class="hm">Público</th><th class="hm">Renda</th></tr></thead><tbody>${linhas||'<tr><td colspan="7" class="mut">Nenhum jogo marcado.</td></tr>'}</tbody></table></div></div>
 <p class="hint mut" style="margin-top:8px">Toque num jogo já disputado para ver as estatísticas completas.</p>`};
/* ---------------- relatório pós-jogo ---------------- */
async function abrirRelatorio(id,rel){const r=rel||await api('partida',{id});S.rel=r;S.ra='est';S.rp='jogo';drawRel()}
function cmpRow(x,h,a){const t=(x.va+x.vb)||1;return `<div class="cmp"><div class="l"><b>${x.a}</b><span>${esc(x.n)}</span><b>${x.b}</b></div>
 <div class="bb"><div><i style="width:${100*x.va/t}%;background:${h.cor[0]=='#f8fafc'?'#94a3b8':h.cor[0]}"></i></div><div><i style="width:${100*x.vb/t}%;background:${a.cor[0]=='#f8fafc'?'#94a3b8':a.cor[0]}"></i></div></div></div>`}
function estHTML(r,per){return r.est[per].map(sec=>`<div class="secao">${sec.t}</div>${sec.l.map(x=>cmpRow(x,r.h,r.a)).join('')}`).join('')}
const EVT={gol:'⚽',am:'🟨',vm:'🟥',les:'🩹',sub:'🔁',quase:'💨',tat:'📋'};
function evTxt(e){return e.k=='gol'?'<b>GOL!</b> '+esc(e.x)+(e.y?` <small class="mut">(assist. ${esc(e.y)})</small>`:''):e.k=='sub'?`Entra <b>${esc(e.x)}</b>, sai ${esc(e.y)}`:e.k=='am'?'Amarelo: '+esc(e.x):e.k=='vm'?'Expulso: '+esc(e.x):e.k=='les'?'Lesão: '+esc(e.x):esc(e.x)}
function evLista(r,evs){return evs.slice().reverse().map(e=>{const t=e.s?r.a:r.h;return `<div class="nw"><b style="min-width:30px">${e.m}'</b><span class="dot" style="background:${t.cor[0]};margin-top:5px"></span><span>${EVT[e.k]||''} ${evTxt(e)}</span></div>`}).join('')||'<p class="mut">Sem lances.</p>'}
function jogTab(r,s){return `<table class="dens"><thead><tr><th>Nº</th><th>Jogador</th><th>Min</th><th>G</th><th>A</th><th class="hm">Fin (alvo)</th><th class="hm">Passes</th><th class="hm">Des</th><th class="hm">Def</th><th>Nota</th></tr></thead><tbody>
 ${r.jog[s].map(j=>`<tr class="p-${j.pos}"><td>${j.num}</td><td>${j.tit?'':'🔁 '}<b>${esc(j.n)}</b> <small class="mut">${j.pos}</small>${j.am?' 🟨':''}${j.vm?' 🟥':''}</td><td>${j.mi}'</td><td>${j.g||''}</td><td>${j.a||''}</td><td class="hm">${j.f} (${j.fa})</td><td class="hm">${j.pk}/${j.pa}</td><td class="hm">${j.d}</td><td class="hm">${j.df||''}</td><td>${notaH(j.nt)}</td></tr>`).join('')}</tbody></table>`}
function formHTML(r,s){const f=r.form[s],t=s?r.a:r.h;return `<div><h3>${esc(t.n)} · ${f.f}</h3><div class="pitch" style="--kit:${t.cor[0]};max-width:300px">${f.xi.map(p=>`<div class="pp" style="left:${p.ax}%;top:${100-p.dp-4}%"><div class="c">${p.num}</div><div class="nm">${esc(p.n)}</div><div class="ps">${p.nt!=null?(+p.nt).toFixed(1):''}</div></div>`).join('')}</div></div>`}
function drawRel(){const r=S.rel,a=S.ra,ab=[['sum','Sumário'],['est','Estatísticas'],['form','Formações'],['jog','Jogadores'],['rel','Relato']];
 let c='';if(a=='est')c=`<div class="seg" style="margin-bottom:8px">${[['jogo','Jogo'],['1t','1º tempo'],['2t','2º tempo']].map(([k,l])=>`<button class="${S.rp==k?'on':''}" onclick="S.rp='${k}';drawRel()">${l}</button>`).join('')}</div>${estHTML(r,S.rp)}`;
 else if(a=='sum')c=evLista(r,r.sum);else if(a=='rel')c=evLista(r,r.ev);
 else if(a=='form')c=`<div class="two w" style="grid-template-columns:1fr 1fr">${formHTML(r,0)}${formHTML(r,1)}</div>`;
 else c=`<h3>${esc(r.h.n)}</h3><div class="tw">${jogTab(r,0)}</div><h3 class="sub">${esc(r.a.n)}</h3><div class="tw">${jogTab(r,1)}</div>`;
 modal(`<div class="mhead"><h2>${esc(r.comp)} <small class="mut">· ${r.data}${r.min<90?' · '+r.min+"'":''}</small></h2><button class="x" onclick="fechar()">✕</button></div>
 <div class="placar" style="margin:6px 0 10px"><div class="tm">${bdg(r.h,'lg')}<span>${esc(r.h.n)}</span></div><div><div class="pl">${r.g[0]} - ${r.g[1]}</div>${r.pen?`<small class="mut">Pênaltis ${r.pen[0]}-${r.pen[1]}</small>`:''}<div class="hint mut">Público ${(r.pub||0).toLocaleString('pt-BR')}</div></div><div class="tm">${bdg(r.a,'lg')}<span>${esc(r.a.n)}</span></div></div>
 <div class="abas">${ab.map(([k,l])=>`<button class="${a==k?'on':''}" onclick="S.ra='${k}';drawRel()">${l}</button>`).join('')}</div>${c}`)}
/* ---------------- tabelas / copas ---------------- */
R.tabelas=async(sel)=>{if(sel!==undefined)S.lg=sel;const ehC=typeof S.lg=='string'&&S.lg.startsWith('c:');
 const d=ehC?await api('copa',{cc:S.lg.slice(2)}):await api('tabela',{lg:S.lg});const ref=ehC?await api('tabela',{}):d;const me=S.st.clube?.id;
 const opts=`<optgroup label="Ligas">${ref.ligas.map(l=>`<option value="${l.i}" ${!ehC&&l.i==d.lg?'selected':''}>${l.fl} ${esc(l.pais)} — ${esc(l.n)}</option>`).join('')}</optgroup>
 <optgroup label="Copas">${ref.copas.map(c=>`<option value="c:${c.cc}" ${S.lg=='c:'+c.cc?'selected':''}>${c.fl} ${esc(c.n)}</option>`).join('')}<option value="c:CN" ${S.lg=='c:CN'?'selected':''}>🌍 Copa das Nações</option></optgroup>`;
 const sel_=`<select onchange="R.tabelas(this.value.startsWith('c:')?this.value:+this.value)">${opts}</select>`;
 if(ehC){V().innerHTML=`<div class="barra-v">${sel_}<h2>${esc(d.n)} <small>${esc(d.temp||'')}</small></h2></div><div class="two w"><div>${d.rd.length?d.rd.slice().reverse().map(rd=>`<div class="card"><h3>${esc(rd.nome)} · ${rd.d}</h3>${rd.j.map(j=>`<div class="og ${[j.h.id,j.a.id].includes(me)?'hit':''}"><span>${esc(j.h.n)} ${bdg(j.h,'sm')}</span><b>${j.r?j.r[0]+' - '+j.r[1]+(j.pen?` (${j.pen[0]}-${j.pen[1]})`:''):'x'}</b><span>${bdg(j.a,'sm')} ${esc(j.a.n)}</span></div>`).join('')}</div>`).join(''):vazio('A competição ainda não começou.')}</div>
 <div class="card"><h3>Campeões</h3>${d.champ.length?d.champ.map(c=>`<div class="nw">${c[0]} — <b>${esc(c[1])}</b></div>`).join(''):'<p class="mut">Ainda sem campeões.</p>'}</div></div>`;return}
 V().innerHTML=`<div class="barra-v">${sel_}<h2>${d.fl} ${esc(d.n)} <small>${d.temp} · rodada ${d.rod} de ${d.tot}</small></h2></div>
 <div class="two w"><div class="tabela-wrap"><table><thead><tr><th>#</th><th></th><th style="width:100%">Clube</th><th>P</th><th>J</th><th>V</th><th class="hm">E</th><th class="hm">D</th><th class="hm">GP</th><th class="hm">GC</th><th>SG</th></tr></thead><tbody>
 ${d.rows.map((r,i)=>`<tr class="${r.t.id==me?'me':''}"><td>${i+1}</td><td>${bdg(r.t)}</td><td><a href="#" onclick="verTime('${r.t.id}');return false" style="color:inherit;text-decoration:none">${esc(r.t.n)}</a></td><td><b>${r.d[6]}</b></td><td>${r.d[0]}</td><td>${r.d[1]}</td><td class="hm">${r.d[2]}</td><td class="hm">${r.d[3]}</td><td class="hm">${r.d[4]}</td><td class="hm">${r.d[5]}</td><td>${r.d[4]-r.d[5]}</td></tr>`).join('')}</tbody></table></div>
 <div><div class="card"><h3>Artilharia</h3>${d.art.length?`<table>${d.art.map((p,i)=>`<tr onclick="verJogador(${p.id})" style="cursor:pointer"><td>${i+1}</td><td><b>${esc(p.n)}</b><br><small class="mut">${esc(p.cl)}</small></td><td><b>${p.st.l[1]}</b></td></tr>`).join('')}</table>`:'<p class="mut">Nenhum gol ainda.</p>'}</div>
 ${d.ult?`<div class="card"><h3>Temporada ${esc(d.ult.temp)}</h3>${d.ult.tab.map((r,i)=>`<div class="nw"><b>${i+1}º</b> ${bdg(r.t,'sm')} ${esc(r.t.n)} <span class="sp"></span><b>${r.d[6]} pts</b></div>`).join('')}${d.ult.art[0]?`<p class="hint mut" style="margin-top:6px">Artilheiro: ${esc(d.ult.art[0][0])} (${esc(d.ult.art[0][1])}), ${d.ult.art[0][2]} gols</p>`:''}</div>`:''}
 ${d.champ.length?`<div class="card"><h3>Campeões</h3>${d.champ.map(c=>`<div class="nw">${c[0]} — <b>${esc(c[1])}</b></div>`).join('')}</div>`:''}</div></div>`};
/* ---------------- estádio ---------------- */
R.estadio=async()=>{if(!S.st.clube){V().innerHTML=vazio('Você precisa estar num clube.');return}const d=await api('estadio');
 V().innerHTML=`<div class="grid"><div class="card"><h3>🏟️ ${esc(d.n)}</h3><div class="kv"><span>Capacidade</span><b>${d.cap.toLocaleString('pt-BR')} lugares</b>
 <span>Público médio</span><b>${d.media.toLocaleString('pt-BR')} (${d.cap?Math.round(100*d.media/d.cap):0}%)</b><span>Confiança da torcida</span>${bar(d.tor)}<span>Caixa</span><b>${mo(d.bud)}</b></div></div>
 <div class="card"><h3>Ingresso</h3><p class="hint mut" style="margin-bottom:8px">Preço de referência € ${d.ref}. Mais caro aumenta a renda por torcedor, mas afasta o público.</p>
 <div class="tools"><input id="preco" type="number" step="0.5" min="0" value="${d.preco}" style="width:120px"><button class="btn" onclick="api('estadio_preco',{preco:+$('#preco').value}).then(()=>R.estadio())">Salvar preço</button></div></div>
 <div class="card"><h3>Ampliação</h3><p style="margin-bottom:10px">+5.000 lugares por <b>${mo(d.custo)}</b></p><button class="btn" onclick="ask('Ampliar o estádio por ${mo(d.custo)}?').then(ok=>ok&&api('estadio_ampliar').then(()=>{refresh();R.estadio()}))">Ampliar estádio</button></div></div>
 <div class="tabela-wrap" style="margin-top:14px"><table><thead><tr><th>Data</th><th>Adversário</th><th>Público</th><th>Ocupação</th><th>Renda</th></tr></thead><tbody>${d.jogos.map(j=>`<tr><td>${j.d}</td><td>${esc(j.adv)}</td><td>${j.pub.toLocaleString('pt-BR')}</td><td>${j.oc}%</td><td>${mo(j.renda)}</td></tr>`).join('')||'<tr><td colspan="5" class="mut">Nenhum jogo em casa nesta temporada.</td></tr>'}</tbody></table></div>`};
/* ---------------- juniores ---------------- */
R.juniores=async()=>{if(!S.st.clube){V().innerHTML=vazio('Você precisa estar num clube.');return}const d=await api('juniores');
 V().innerHTML=`<div class="barra-v"><h2>🌱 Juniores<small>${d.lista.length} jogadores · elenco principal ${d.n}/35</small></h2></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th>P</th><th>Nome</th><th>Idade</th><th>F</th><th>Pot</th><th class="hm">Fís</th><th class="hm">Pé</th><th>Car.</th><th></th></tr></thead><tbody>
 ${d.lista.map(p=>`<tr class="p-${p.pos}"><td><b>${p.pos}</b></td><td><b>${esc(p.n)}</b> ${p.fl}</td><td>${p.age}</td><td>${ov(p.ovr)}</td><td>${ov(p.pot)}</td><td class="hm">${p.fis}</td><td class="hm">${PE[p.pe]}</td><td>${p.hab.map(x=>AB[x]).join('/')||'–'}</td>
 <td style="white-space:nowrap"><button class="btn" onclick="api('promover',{pid:${p.id}}).then(()=>{refresh();R.juniores()})">Promover</button> <button class="btn red" onclick="api('dispensar_jr',{pid:${p.id}}).then(()=>R.juniores())">Dispensar</button></td></tr>`).join('')}</tbody></table></div>
 <p class="hint mut" style="margin-top:8px">Todo 1º de julho chegam novos garotos da base. Jogadores com 19 anos que não forem promovidos deixam o clube.</p>`};
/* ---------------- times ---------------- */
R.times=async(lg)=>{if(lg!==undefined)S.tlg=lg;const d=await api('times',{lg:S.tlg});
 V().innerHTML=`<div class="barra-v"><select onchange="R.times(this.value)">${d.ligas.map(l=>`<option value="${l.i}" ${d.lg==l.i?'selected':''}>${l.fl} ${esc(l.n)}</option>`).join('')}<option value="copa" ${S.tlg=='copa'?'selected':''}>Clubes só de copa</option><option value="sel" ${S.tlg=='sel'?'selected':''}>Seleções</option></select></div>
 <div class="clubs" style="max-height:none">${d.clubs.map(t=>`<button class="club" onclick="verTime('${t.id}')">${bdg(t)}<span>${esc(t.n)}<br><small class="mut">${esc(t.tec)}${t.cap?' · '+t.cap.toLocaleString('pt-BR')+' lug.':''}</small></span>${ov(t.f)}</button>`).join('')||'<p class="mut">Nenhum clube.</p>'}</div>`};
async function verTime(tid){const d=await api('time',{tid});S.v='times';menu();
 V().innerHTML=`<div class="barra-v">${bdg(d.t,'lg')}<h2>${esc(d.t.n)}<small>Técnico: ${esc(d.tec)}${d.est?' · '+esc(d.est.n)+' ('+d.est.cap.toLocaleString('pt-BR')+')':''} · força ${Math.round(d.t.f)}</small></h2><div class="sp"></div><button class="btn sec" onclick="R.times()">✕ Voltar</button></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th>P</th><th>Nome</th><th>Idade</th><th>F</th><th class="hm">Fís</th><th class="hm">Pot</th><th class="hm">Pé</th><th>Car.</th><th class="hm">Valor</th><th class="hm">J</th><th class="hm">G</th><th class="hm">NM</th></tr></thead><tbody>
 ${d.pl.map(p=>`<tr class="p-${p.pos}" onclick="verJogador(${p.id})"><td><b>${p.pos[0]}</b></td><td>${d.craques.includes(p.id)?'<span class="estrela">★</span> ':''}<b>${esc(p.n)}</b> ${p.fl}</td><td>${p.age}</td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td class="hm">${PEC[p.pe]}</td><td>${p.hab.slice(0,2).map(x=>AB[x]).join('/')||'–'}</td><td class="hm">${mo(p.val)}</td><td class="hm">${p.j}</td><td class="hm">${p.g}</td><td class="hm">${p.nm??'–'}</td></tr>`).join('')}</tbody></table></div>`}
/* ---------------- procura ---------------- */
R.procura=async()=>{if(!S.st.clube){V().innerHTML=vazio('Você precisa estar num clube para contratar.');return}const f=S.mf,d=await api('procura',f);
 V().innerHTML=`<div class="card tools"><select id="fp"><option value="">Todas as posições</option>${['GOL','ZAG','LAT','VOL','MEI','ATA'].map(x=>`<option ${f.pos==x?'selected':''}>${x}</option>`).join('')}</select>
 <select id="fl"><option value="">Todas as ligas</option>${d.ligas.map(l=>`<option value="${l.i}" ${f.lg===String(l.i)?'selected':''}>${l.fl} ${esc(l.n)}</option>`).join('')}</select>
 <select id="fm"><option value="">Qualquer preço</option>${[1000,5000,10000,25000,50000,100000].map(v=>`<option value="${v}" ${f.max==v?'selected':''}>até ${mo(v)}</option>`).join('')}</select>
 <input id="fmin" type="number" placeholder="Força mín." value="${esc(f.min)}" style="width:110px"><input id="fid" type="number" placeholder="Idade máx." value="${esc(f.idade)}" style="width:110px">
 <input id="fq" placeholder="Nome do jogador" value="${esc(f.q)}"><button class="btn" onclick="filtrar()">🔎 Procurar</button><div class="sp"></div><b>Caixa ${mo(d.bud)}</b></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th>P</th><th>Nome</th><th>Clube</th><th>Idade</th><th>F</th><th class="hm">Fís</th><th class="hm">Pot</th><th class="hm">Pé</th><th>Car.</th><th>Preço</th><th></th></tr></thead><tbody>
 ${d.lista.map(p=>`<tr class="p-${p.pos}" onclick="verJogador(${p.id})"><td><b>${p.pos}</b></td><td><b>${esc(p.n)}</b> ${p.fl}</td><td>${esc(p.cl)}</td><td>${p.age}</td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td class="hm">${PEC[p.pe]}</td><td>${p.hab.slice(0,2).map(x=>AB[x]).join('/')||'–'}</td><td><b>${mo(p.preco)}</b></td>
 <td><button class="btn" onclick="event.stopPropagation();comprar(${p.id},'${esc(p.n).replace(/&#39;/g,'')}',${p.preco})">Comprar</button></td></tr>`).join('')}</tbody></table>${d.lista.length?'':'<p class="mut" style="padding:12px">Nenhum jogador encontrado.</p>'}</div>`};
function filtrar(){S.mf={pos:$('#fp').value,lg:$('#fl').value,max:$('#fm').value,min:$('#fmin').value,idade:$('#fid').value,q:$('#fq').value};R.procura()}
/* ---------------- técnicos / história ---------------- */
R.tecnicos=async(f)=>{if(f)S.tecf=f;const d=await api('tecnicos',{f:S.tecf});
 V().innerHTML=`<div class="barra-v"><h2>Técnicos</h2><div class="seg">${[['todos','Todos'],['empregados','Empregados'],['livres','Sem time']].map(([k,l])=>`<button class="${S.tecf==k?'on':''}" onclick="R.tecnicos('${k}')">${l}</button>`).join('')}</div></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th>#</th><th>Técnico</th><th>Time</th><th>Reputação</th><th>Títulos</th></tr></thead><tbody>
 ${d.lista.map((t,i)=>`<tr class="${t.eu?'me':''}"><td>${i+1}</td><td>${t.fl} <b>${esc(t.n)}</b></td><td>${t.t?esc(t.t):'<span class="mut">sem time</span>'}</td><td style="min-width:120px">${bar(t.rep,'var(--blue)')}</td><td>${t.tit}</td></tr>`).join('')}</tbody></table></div>`};
R.historia=async()=>{const d=await api('historia');const lista=(t,c)=>`<div class="card"><h3>${t}</h3>${c.length?c.map(x=>`<div class="nw">${esc(x[0])} — <b>${esc(x[1])}</b></div>`).join(''):'<p class="mut">Ainda sem campeões.</p>'}</div>`;
 V().innerHTML=`<div class="grid"><div class="card"><h3>Sua carreira</h3><div class="kv"><span>Técnico</span><b>${esc(d.n)}</b><span>Reputação</span>${bar(d.rep,'var(--blue)')}<span>Campanha</span><b>${d.v}V ${d.e}E ${d.d}D</b><span>Títulos</span><b>${d.tit.length}</b></div>
 ${d.tit.length?`<div style="margin-top:8px">${d.tit.map(t=>`<div class="nw">🏆 ${esc(t)}</div>`).join('')}</div>`:''}</div>
 <div class="card tw"><h3>Temporadas</h3>${d.hist.length?`<table><tr><th>Ano</th><th>Time</th><th>Competição</th><th>Pos.</th><th>Pts</th></tr>${d.hist.map(h=>`<tr><td>${h.s}</td><td>${h.tit?'🏆 ':''}<b>${esc(h.t)}</b></td><td>${esc(h.l)}</td><td>${h.pos}º</td><td>${h.pts}</td></tr>`).join('')}</table>`:'<p class="mut">Sua primeira temporada está em andamento.</p>'}</div>
 ${lista('🌍 Copa das Nações',d.cn)}${d.ligas.map(l=>lista(l.fl+' '+esc(l.n),l.champ)).join('')}${d.copas.map(l=>lista(l.fl+' '+esc(l.n),l.champ)).join('')}</div>`};
/* ---------------- mensagens ---------------- */
R.mensagens=async()=>{const d=await api('mensagens');
 V().innerHTML=`<div class="barra-v"><h2>✉️ Mensagens</h2><div class="sp"></div><button class="btn sec" onclick="api('ler').then(()=>{refresh();R.mensagens()})">Marcar todas como lidas</button></div>
 <div class="card">${d.lista.map(m=>`<div class="nw ${m.k} ${m.lida?'':'nova'}"><small>${m.d}</small><div style="flex:1">${esc(m.x)}${m.of?`<div class="tools" style="margin-top:6px"><button class="btn" onclick="aceitarOf('${m.of}')">Aceitar</button><button class="btn sec" onclick="api('recusar',{t:'${m.of}'}).then(()=>R.mensagens())">Recusar</button></div>`:''}</div></div>`).join('')||'<p class="mut">Nenhuma mensagem.</p>'}</div>`;
 api('ler').then(()=>refresh())};
async function aceitarOf(t){if(!await ask('Aceitar esta proposta?'))return;await api('aceitar',{t});S.card=null;await refresh();go('elenco')}
/* ---------------- seleção ---------------- */
R.selecao=async()=>{await refresh();if(!S.st.sel){const r=await api('ranking');V().innerHTML=`<div class="card"><h3>Seleções</h3><p class="mut">Você não comanda uma seleção. Convites chegam conforme sua reputação cresce — fique de olho nas Mensagens.</p></div><div class="tabela-wrap"><table><thead><tr><th>#</th><th>Seleção</th><th>Força</th></tr></thead><tbody>${r.lista.map((t,i)=>`<tr onclick="verTime('${t.id}')" style="cursor:pointer"><td>${i+1}</td><td>${t.fl} <b>${esc(t.n)}</b></td><td>${ov(t.f)}</td></tr>`).join('')}</tbody></table></div>`;return}
 const d=await api('elegiveis');S.cv=new Set(d.conv);
 V().innerHTML=`<div class="barra-v"><h2>${d.t.fl} ${esc(d.t.n)}<small>Convocados: <b id="cvn">${S.cv.size}</b>/23</small></h2><div class="sp"></div><button class="btn sec" onclick="api('conv_auto').then(()=>R.selecao())">Automática</button><button class="btn" onclick="api('convocar',{ids:[...S.cv]})">Salvar convocação</button><button class="btn sec" onclick="S.t='sel';go('escalar')">Escalar</button></div>
 <div class="tabela-wrap"><table class="dens"><thead><tr><th></th><th>P</th><th>Jogador</th><th>Clube</th><th>Idade</th><th>F</th><th class="hm">Fís</th><th class="hm">Pot</th><th>Car.</th><th class="hm">NM</th></tr></thead><tbody>
 ${d.lista.map(p=>`<tr class="p-${p.pos} ${S.cv.has(p.id)?'tit':''}" onclick="tg(${p.id},this)"><td><input type="checkbox" ${S.cv.has(p.id)?'checked':''} style="pointer-events:none"></td><td><b>${p.pos}</b></td><td><b>${esc(p.n)}</b>${p.inj?' 🩹':''}</td><td>${esc(p.cl)}</td><td>${p.age}</td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td>${p.hab.slice(0,2).map(x=>AB[x]).join('/')}</td><td class="hm">${p.nm??'–'}</td></tr>`).join('')}</tbody></table></div>`};
function tg(id,tr){if(S.cv.has(id))S.cv.delete(id);else{if(S.cv.size>=23)return toast('Máximo de 23 convocados',1);S.cv.add(id)}tr.classList.toggle('tit',S.cv.has(id));tr.querySelector('input').checked=S.cv.has(id);$('#cvn').textContent=S.cv.size}
/* ---------------- opções ---------------- */
R.opcoes=async()=>{const m=await api('meta');
 V().innerHTML=`<div class="grid"><div class="card"><h3>Jogo</h3><div class="row"><button class="btn" onclick="api('salvar')">💾 Salvar</button><button class="btn sec" onclick="carregar()" ${m.save?'':'disabled'}>Carregar</button><button class="btn sec" onclick="novoJogo()">Novo jogo</button></div>
 <p class="hint mut" style="margin-top:10px">No Colab, o arquivo salvo fica em /content e é apagado quando a sessão termina.</p></div>
 <div class="card"><h3>Velocidade das partidas</h3><div class="seg">${Object.entries(VEL).map(([k,v])=>`<button class="${S.vel==k?'on':''}" onclick="S.vel='${k}';lss('vel','${k}');R.opcoes()">${v[0]}</button>`).join('')}</div>
 <p class="hint mut" style="margin-top:10px">O padrão é Ultra rápido. Use Normal para acompanhar a movimentação dos jogadores no campo.</p></div>
 <div class="card"><h3>Planilha de dados</h3><p class="hint mut" style="margin-bottom:10px">${m.dados.length?'Planilha em uso: <b>'+esc(m.dados.join(', '))+'</b>':'Usando dados gerados pelo jogo.'}<br>Carregar uma planilha cria um novo mundo e começa um novo jogo.</p>
 <div class="tools"><input type="file" id="arq" accept=".xlsx,.xlsm,.csv"><button class="btn" onclick="enviarPlanilha()">Carregar planilha</button>${m.dados.length?'<button class="btn red" onclick="removerDados()">Remover</button>':''}</div></div>
 <div class="card"><h3>Carreira</h3><div class="row">${S.st.clube?`<button class="btn red" onclick="sair('clube')">Sair do clube</button>`:''}${S.st.sel?`<button class="btn red" onclick="sair('sel')">Sair da seleção</button>`:''}</div></div></div>`};
async function sair(t){if(await ask('Tem certeza?')){await api('demitir',{t});S.card=null;await refresh();go('elenco')}}
/* ---------------- partida ao vivo + transmissão 2D ---------------- */
let LV=null;
const STX={seg:'Bola segura',rec:'Recuperou a bola',atk:'Ataque',per:'Ataque perigoso',gol:'GOL!',esc:'Escanteio',imp:'Impedimento',fal:'Falta',def:'Defesa do goleiro',blq:'Chute bloqueado',trv:'Na trave!',fora:'Chute para fora'};
async function jogar(){if(LV&&!LV.done)return;const r=await api('jogar');if(!r.live){await refresh();if(R[S.v])R[S.v]();return}startLive(r)}
function startLive(r){LV={...r,q:[],busy:false,pause:false,hold:false,done:false,evs:r.ev||[],so:null,ball:[50,50],aba:'lances',vert:mob()};S.v='jogo';fechar();menu();drawLive();loop()}
function campoSVG(v){const W=v?68:105,H=v?105:68,T=(x,y)=>v?[y,105-x]:[x,y];
 const rc=(x,y,w,h,f='none',o='')=>{const [a,b]=T(x,v?y:y),p=v?[y,105-x-w,h,w]:[x,y,w,h];return `<rect x="${p[0]}" y="${p[1]}" width="${p[2]}" height="${p[3]}" fill="${f}" ${o}/>`};
 let s=`<svg viewBox="0 0 ${W} ${H}" preserveAspectRatio="none">`;
 for(let i=0;i<10;i++)s+=rc(i*10.5,0,10.5,68,i%2?'#5aa543':'#4f9a3a');
 const st='stroke="rgba(255,255,255,.8)" stroke-width=".45"';
 s+=rc(.6,.6,103.8,66.8,'none',st)+rc(.6,13.84,15.9,40.32,'none',st)+rc(88.5,13.84,15.9,40.32,'none',st)+rc(.6,24.84,4.9,18.32,'none',st)+rc(99.5,24.84,4.9,18.32,'none',st);
 const [mx1,my1]=T(52.5,.6),[mx2,my2]=T(52.5,67.4),[cx,cy]=T(52.5,34);
 s+=`<line x1="${mx1}" y1="${my1}" x2="${mx2}" y2="${my2}" ${st}/><circle cx="${cx}" cy="${cy}" r="9.15" fill="none" ${st}/><circle cx="${cx}" cy="${cy}" r=".6" fill="#fff"/>`;
 for(const px of [11,94]){const [a,b]=T(px,34);s+=`<circle cx="${a}" cy="${b}" r=".55" fill="#fff"/>`}
 return s+'</svg>'}
function pctPos(x,y){return LV.vert?[y,100-x]:[x,y]}
function drawLive(){const L=LV,m=L.ms[0];
 V().innerHTML=`<div class="card"><div class="tools" style="justify-content:space-between"><span class="comp">${esc(L.comp)} · ${L.data}</span><div class="seg" id="vel">${Object.entries(VEL).map(([k,v])=>`<button class="${S.vel==k?'on':''}" onclick="S.vel='${k}';lss('vel','${k}');document.querySelectorAll('#vel button').forEach(b=>b.classList.toggle('on',b.dataset.k=='${k}'))" data-k="${k}">${v[0]}</button>`).join('')}</div></div>
 <div class="placar" style="margin:8px 0"><div class="tm">${bdg(m.h,'lg')}<span>${esc(m.h.n)}</span></div><div><div class="pl" id="pl">${m.g[0]} - ${m.g[1]}</div><span class="min" id="mn">${L.min}'</span><div id="pe" class="mut hint"></div></div><div class="tm">${bdg(m.a,'lg')}<span>${esc(m.a.n)}</span></div></div>
 <div class="bar prog"><i id="pg" style="width:${L.min/.9}%"></i></div><div class="ctl" id="ctl"><button class="btn" id="bp" onclick="pausar()">❚❚ Pausar</button><button class="btn sec" onclick="painelSub()">🔁 Substituições (<span id="sc">${L.lado.subs}</span>/5)</button></div></div>
 <div id="pn"></div>
 <div class="aovivo"><div class="card" style="padding:10px"><div class="campo ${L.vert?'v':''}" id="campo">${campoSVG(L.vert)}<div class="sombra" id="sombra"></div><div id="jds"></div><div class="bola" id="bola" style="left:50%;top:50%"></div><div class="status" id="stt">${esc(m.h.n)} × ${esc(m.a.n)}</div></div>
 <p class="hint mut" style="margin-top:6px;text-align:center">Público: ${(L.pub||0).toLocaleString('pt-BR')} · bolinhas = jogadores (número da camisa)</p></div>
 <div class="card"><div class="abas" id="abas"></div><div id="abac"></div></div></div>`;
 montarJogadores();abas()}
function montarJogadores(){const L=LV,m=L.ms[0],cH=m.h.cor,cA=m.a.cor,ig=cH[0]==cA[0];
 $('#jds').innerHTML=L.lu.map((lado,s)=>lado.map(([id,ax,dp,num,n,sl])=>{const c=s?(ig?[cA[1],cA[0]]:cA):cH;
  return `<div class="jd" id="j${id}" title="${esc(n)}" style="background:${c[0]};color:${c[1]}">${num||''}</div>`}).join('')).join('');
 posJog({b:[L.ball],p:0},0)}
function posJog(fr,dur){const L=LV,b=fr.b.length?fr.b[fr.b.length-1]:L.ball;L.ball=b;
 L.lu.forEach((lado,s)=>lado.forEach(([id,ax,dp,num,n,sl])=>{const el=document.getElementById('j'+id);if(!el)return;
  const bd=s==0?b[0]:100-b[0],by=s==0?b[1]:100-b[1],atk=fr.p==s;
  let d=sl=='G'?dp+(bd-50)*.08:dp+(atk?(bd-45)*.5+8:(bd-55)*.45-8);const lim={G:[2,16],D:[6,64],M:[18,84],A:[30,95]}[sl];d=Math.max(lim[0],Math.min(lim[1],d));
  let w=Math.max(4,Math.min(96,ax+(by-50)*.3+(Math.random()-.5)*5));const [px,py]=pctPos(s==0?d:100-d,s==0?w:100-w);
  el.style.transitionDuration=dur+'ms';el.style.left=px+'%';el.style.top=py+'%'}))}
function animarBola(pts,dur){const el=$('#bola');if(!el||!pts.length)return;const st=dur/pts.length;
 pts.forEach((p,i)=>setTimeout(()=>{if(!LV)return;const [x,y]=pctPos(p[0],p[1]);el.style.transitionDuration=st+'ms';el.style.left=x+'%';el.style.top=y+'%'},i*st))}
function sombra(fr){const el=$('#sombra');if(!el)return;const b=LV.ball[0];
 if(LV.vert){el.style.left='0';el.style.width='100%';if(fr.p==0){el.style.top=(100-b-6)+'%';el.style.height=(b+6)+'%';el.style.background='linear-gradient(0deg,rgba(0,0,0,.28),rgba(0,0,0,.08))'}else{el.style.top='0';el.style.height=(100-b+6)+'%';el.style.background='linear-gradient(180deg,rgba(0,0,0,.28),rgba(0,0,0,.08))'}}
 else if(fr.p==0){el.style.left='0';el.style.width=Math.min(100,b+6)+'%';el.style.background='linear-gradient(90deg,rgba(0,0,0,.28),rgba(0,0,0,.08))'}
 else{el.style.left=Math.max(0,b-6)+'%';el.style.width=(100-Math.max(0,b-6))+'%';el.style.background='linear-gradient(270deg,rgba(0,0,0,.28),rgba(0,0,0,.08))'}}
function abas(){const L=LV,ab=[['lances','Lances'],['est','Estatísticas'],['garg','Gargalos'],['outros','Outros jogos']];
 $('#abas').innerHTML=ab.map(([k,l])=>`<button class="${L.aba==k?'on':''}" onclick="LV.aba='${k}';abas()">${l}</button>`).join('');
 if(L.aba=='lances')feed();else if(L.aba=='outros')outros([]);else{$('#abac').innerHTML='<p class="mut">Carregando...</p>';atualizarEst()}}
async function atualizarEst(){if(!LV||LV.done)return;const r=await api('estat_live');LV.rel=r.rel;LV.garg=r.garg;if(LV.aba=='est')$('#abac').innerHTML=estHTML(r.rel,'jogo');else if(LV.aba=='garg')$('#abac').innerHTML=gargHTML(r.garg)}
function gargHTML(g){const L=['Esquerdo','Centro','Direito'],tot=g.atk.reduce((a,b)=>a+b,0)||1,pz=['Saída de bola','Meio-campo','Último terço'],ptot=g.perda.reduce((a,b)=>a+b,0)||1;
 const du=(k,n)=>`<div class="cmp"><div class="l"><span>${n}</span><b>${g.du[k]==null?'–':g.du[k]+'%'}</b></div>${bar(g.du[k]||0)}</div>`;
 return `<div class="garg"><h3>Por onde o adversário ataca (seu lado)</h3><div class="lane">${g.atk.map((v,i)=>`<div style="background:rgba(229,72,77,${.08+.5*v/tot})"><b>${Math.round(100*v/tot)}%</b><small>${L[i]} · ${g.ch[i]} fin.</small></div>`).join('')}</div>
 <h3>Onde seu time perde a bola</h3><div class="lane">${g.perda.map((v,i)=>`<div style="background:rgba(245,179,1,${.08+.5*v/ptot})"><b>${v}</b><small>${pz[i]}</small></div>`).join('')}</div>
 <h3>Disputas vencidas por setor</h3>${du('D','Defesa (barra ataques no último terço)')}${du('M','Meio-campo (passa da marcação)')}${du('A','Ataque (chega a finalizar)')}
 ${g.alertas.length?`<h3 style="margin-top:10px">Alertas</h3><ul>${g.alertas.map(a=>`<li>${esc(a)}</li>`).join('')}</ul>`:''}
 <div class="sug"><b>Sugestões</b><ul>${g.sug.map(a=>`<li>${esc(a)}</li>`).join('')}</ul></div></div>`}
function feed(){if(!LV||LV.aba!='lances')return;const L=LV,m=L.ms[0];$('#abac').innerHTML=`<div class="feed">${L.evs.slice().reverse().map(e=>{const t=e.s?m.a:m.h;return `<div class="${e.k=='gol'?'gol':''}"><b style="min-width:28px">${e.m}'</b><span class="dot" style="background:${t.cor[0]}"></span><span>${EVT[e.k]||''} ${evTxt(e)}</span></div>`}).join('')||'<p class="mut">A bola vai rolar...</p>'}</div>`}
function outros(gl){if(!LV||LV.aba!='outros')return;const o=LV.ms.slice(1);$('#abac').innerHTML=o.length?o.map((m,i)=>`<div class="og ${gl.includes(i+1)?'hit':''}"><span>${esc(m.h.n)} ${bdg(m.h,'sm')}</span><b>${m.g[0]} - ${m.g[1]}${m.pen?` (${m.pen[0]}-${m.pen[1]})`:''}</b><span>${bdg(m.a,'sm')} ${esc(m.a.n)}</span></div>`).join(''):'<p class="mut">Sem outros jogos nesta rodada.</p>'}
function loop(){const L=LV;if(!L||L.done)return;const v=VEL[S.vel]||VEL.u;let w=v[1];
 if(!L.fim&&!L.busy&&!L.hold&&!L.pause&&L.q.length<v[2]+1){L.busy=true;api('passo',{n:v[2]}).then(r=>{L.busy=false;L.q.push(...r.frames);if(r.frames.some(f=>f.pausa))L.hold=true;if(r.fim){L.fim=true;L.final=r.final;L.res=r.res;L.arq=r.arq}}).catch(()=>{L.busy=false})}
 if(!L.pause&&L.q.length){const f=L.q.shift();aplicar(f,w);if(f.gols.includes(0))w=Math.max(w,900);else if(f.min==45){w=Math.max(w,1000);toast('Intervalo')}
  if(f.pausa){pausar(1);toast(f.pausa=='lesão'?'Jogador lesionado! Faça a substituição.':'Jogador expulso! Reorganize o time.',1)}}
 else if(L.fim&&!L.q.length&&!L.pause)return fimJogo();
 L.tm=setTimeout(loop,w)}
function aplicar(f,dur){const L=LV,m=L.ms[0];L.min=f.min;f.g.forEach((g,i)=>L.ms[i].g=g);L.evs.push(...f.ev);
 $('#pl').textContent=`${f.g[0][0]} - ${f.g[0][1]}`;$('#mn').textContent=f.min+"'";$('#pg').style.width=(f.min/.9)+'%';
 if(f.lu){L.lu=f.lu;montarJogadores()}
 if(f.fr){animarBola(f.fr.b,dur*.8);posJog(f.fr,dur);sombra(f.fr);const t=f.fr.p?m.a:m.h,st=$('#stt');
  st.className='status'+(f.fr.k=='gol'?' gol':'');st.innerHTML=`${esc(t.n)} <small>– ${STX[f.fr.k]||''}</small>`}
 if(f.gols.includes(0)){const e=$('#pl');e.classList.remove('flash');void e.offsetWidth;e.classList.add('flash')}
 if(f.ev.length)feed();outros(f.gols);if(f.min%10==0&&(L.aba=='est'||L.aba=='garg'))atualizarEst()}
function pausar(auto){const L=LV;if(!L||L.done)return;if(L.pause&&!auto){L.pause=false;L.hold=false;L.so=null;$('#pn').innerHTML='';$('#bp').textContent='❚❚ Pausar';return}
 if(L.pause)return;L.pause=true;$('#bp').textContent='▶ Continuar';painelSub()}
async function painelSub(){if(!LV||LV.done||(LV.fim&&!LV.q.length))return;if(!LV.pause)return pausar();const r=await api('tatica',{});LV.lado=r.lado;LV.garg=r.garg;drawPn()}
function drawPn(){const l=LV.lado;$('#sc').textContent=l.subs;const g=LV.garg;
 $('#pn').innerHTML=`<div class="card"><div class="tools">${fsel(l.form,'tat')}<div class="seg">${tacs(l.tac,'tat')}</div><div class="sp"></div><button class="btn" onclick="pausar()">▶ Continuar</button></div>
 <p class="hint mut" style="margin:8px 0">Toque em quem sai e depois em quem entra · ${5-l.subs} substituições restantes</p>
 <div class="two w"><div><h3>Em campo</h3>${l.on.map(p=>prow(p,1)).join('')}</div><div><h3>Banco</h3>${l.bench.map(p=>prow(p,0)).join('')||'<p class="mut">Banco vazio.</p>'}</div></div>
 ${g?`<div class="garg"><div class="sug"><b>Leitura do jogo</b><ul>${g.sug.map(a=>`<li>${esc(a)}</li>`).join('')}${g.alertas.slice(0,4).map(a=>`<li>${esc(a)}</li>`).join('')}</ul></div></div>`:''}</div>`}
function prow(p,on){return `<div class="pr ${LV.so==p.id?'pk':''}" onclick="${on?`LV.so=${p.id};drawPn()`:`entra(${p.id})`}"><span class="pos ${GRP[p.pos]}">${p.pos}</span><b>${esc(p.n)}</b>${p.am?'🟨':''}${p.les?'🩹':''}${on&&p.sl&&GRP[p.pos]!=p.sl?'⚠':''}<span class="sp"></span>${notaH(p.nt)} ${ov(p.ovr)}<div style="width:50px">${bar(p.en)}</div></div>`}
async function entra(id){if(!LV.so)return toast('Escolha primeiro quem sai',1);const r=await api('sub',{out:LV.so,in:id});LV.so=null;LV.lado=r.lado;LV.garg=r.garg;drawPn()}
async function tat(o){const r=await api('tatica',o);LV.lado=r.lado;LV.garg=r.garg;drawPn()}
function fimJogo(){const L=LV;L.done=true;const m=L.final[0];L.ms=L.final;if(m.pen)$('#pe').textContent=`Pênaltis: ${m.pen[0]} - ${m.pen[1]}`;$('#ctl').innerHTML='';
 $('#stt').className='status';$('#stt').innerHTML='Fim de jogo';
 $('#pn').innerHTML=`<div class="card fim ${L.res}"><h2>${L.res=='V'?'Vitória!':L.res=='E'?'Empate':'Derrota'}</h2><p>${esc(m.h.n)} ${m.g[0]} - ${m.g[1]} ${esc(m.a.n)}${m.pen?` (pên. ${m.pen[0]}-${m.pen[1]})`:''}</p>
 <div class="row"><button class="btn sec big" onclick="abrirRelatorio('${L.arq}')">📊 Estatísticas da partida</button><button class="btn big" onclick="sairJogo()">Continuar</button></div></div>`;
 if(L.aba=='outros')outros([]);scrollTo({top:0,behavior:'smooth'});if(L.arq)abrirRelatorio(L.arq)}
async function sairJogo(){LV=null;fechar();S.card=null;await refresh();go('elenco')}
addEventListener('resize',()=>{if(LV&&!LV.done&&LV.vert!=mob()){LV.vert=mob();drawLive()}});
boot().catch(e=>{V().innerHTML=vazio('Erro ao iniciar: '+esc(e.message))});
