# =====================================================================
#  PRANCHETA FC - jogo de gerenciamento de futebol (Python + HTML/JS)
#  Google Colab: cole TUDO numa celula e execute (Shift+Enter).
#  PC: pip install flask  &&  python prancheta_fc.py  -> abre o navegador
# =====================================================================
import random, math, os, sys, threading, pickle, csv, traceback
try:
    from flask import Flask, request, jsonify, Response
except ImportError:
    import subprocess; subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'flask'])
    from flask import Flask, request, jsonify, Response

PORTA = 8050
SAVE = 'prancheta_save.pkl'
R = random.Random()

# ----------------------------- DADOS ---------------------------------
# pais|liga|forca do melhor|forca do pior|clubes (em ordem aproximada de forca)
LIGAS = """EN|Premier League|87|72|Arsenal;Manchester City;Liverpool;Chelsea;Newcastle;Tottenham;Aston Villa;Manchester United;Nottingham Forest;Brighton;Crystal Palace;Bournemouth;Brentford;Fulham;Everton;West Ham;Sunderland;Leeds United;Wolverhampton;Burnley
ES|La Liga|87|68|Real Madrid;Barcelona;Atlético de Madrid;Athletic Bilbao;Villarreal;Real Betis;Real Sociedad;Sevilla;Celta de Vigo;Girona;Valencia;Osasuna;Rayo Vallecano;Mallorca;Getafe;Espanyol;Alavés;Elche;Levante;Real Oviedo
IT|Serie A|84|67|Inter de Milão;Napoli;Juventus;Milan;Atalanta;Roma;Como;Lazio;Bologna;Fiorentina;Torino;Udinese;Genoa;Sassuolo;Cagliari;Parma;Lecce;Verona;Cremonese;Pisa
DE|Bundesliga|87|67|Bayern de Munique;Bayer Leverkusen;Borussia Dortmund;RB Leipzig;Eintracht Frankfurt;VfB Stuttgart;SC Freiburg;Hoffenheim;Mainz 05;Wolfsburg;Werder Bremen;Borussia Mönchengladbach;Union Berlin;Augsburg;Colônia;Hamburgo;St. Pauli;Heidenheim
FR|Ligue 1|86|64|Paris Saint-Germain;Olympique de Marseille;Monaco;Lille;Lyon;Nice;Lens;Strasbourg;Rennes;Toulouse;Brest;Nantes;Auxerre;Le Havre;Angers;Paris FC;Lorient;Metz
BR|Brasileirão Série A|80|68|Flamengo;Palmeiras;Botafogo;Cruzeiro;Fluminense;São Paulo;Atlético Mineiro;Internacional;Corinthians;Bahia;Grêmio;Red Bull Bragantino;Vasco da Gama;Santos;Mirassol;Vitória;Athletico Paranaense;Coritiba;Chapecoense;Remo
PT|Liga Portugal|81|60|Benfica;Porto;Sporting;Braga;Vitória de Guimarães;Famalicão;Santa Clara;Gil Vicente;Moreirense;Rio Ave;Estoril;Casa Pia;Arouca;Nacional;Estrela da Amadora;Tondela;AVS;Alverca
NL|Eredivisie|79|60|PSV;Feyenoord;Ajax;AZ Alkmaar;Twente;Utrecht;NEC Nijmegen;Go Ahead Eagles;Heerenveen;Sparta Rotterdam;Groningen;Fortuna Sittard;PEC Zwolle;Heracles;NAC Breda;Excelsior;Telstar;Volendam
AR|Liga Profesional|77|63|River Plate;Boca Juniors;Racing Club;Vélez Sarsfield;Estudiantes;Talleres;Independiente;San Lorenzo;Rosario Central;Argentinos Juniors;Lanús;Huracán;Defensa y Justicia;Belgrano;Newell's Old Boys;Unión de Santa Fe;Platense;Tigre;Instituto;Godoy Cruz;Banfield;Gimnasia La Plata;Barracas Central;Independiente Rivadavia;Sarmiento;Central Córdoba;Atlético Tucumán;Aldosivi;Deportivo Riestra;Gimnasia de Mendoza
TR|Süper Lig|78|62|Galatasaray;Fenerbahçe;Beşiktaş;Trabzonspor;Başakşehir;Samsunspor;Göztepe;Eyüpspor;Kasımpaşa;Antalyaspor;Konyaspor;Alanyaspor;Kayserispor;Gaziantep;Rizespor;Kocaelispor;Gençlerbirliği;Fatih Karagümrük
BE|Pro League|77|61|Club Brugge;Union Saint-Gilloise;Anderlecht;Genk;Gent;Antwerp;Standard Liège;Mechelen;Westerlo;Charleroi;Sint-Truiden;OH Leuven;Cercle Brugge;Dender;Zulte Waregem;La Louvière
SC|Scottish Premiership|75|59|Celtic;Rangers;Hearts;Aberdeen;Hibernian;Motherwell;Dundee United;St Mirren;Kilmarnock;Falkirk;Dundee;Livingston
SA|Saudi Pro League|80|60|Al-Hilal;Al-Nassr;Al-Ittihad;Al-Ahli;Al-Qadsiah;Al-Ettifaq;Al-Shabab;Al-Taawoun;Al-Fateh;Al-Khaleej;Al-Fayha;Al-Kholood;Al-Riyadh;Damac;Al-Hazem;Al-Okhdood;Al-Najma;NEOM
US|MLS|74|62|Inter Miami;LAFC;Columbus Crew;FC Cincinnati;Seattle Sounders;LA Galaxy;Philadelphia Union;Vancouver Whitecaps;Orlando City;Atlanta United;New York City FC;New York Red Bulls;Minnesota United;Nashville SC;San Diego FC;Charlotte FC;Austin FC;Portland Timbers;Real Salt Lake;Houston Dynamo;Sporting Kansas City;FC Dallas;Chicago Fire;New England Revolution;Colorado Rapids;St. Louis City;San Jose Earthquakes;D.C. United;CF Montréal;Toronto FC
MX|Liga MX|75|62|América;Toluca;Tigres UANL;Monterrey;Cruz Azul;Guadalajara;Pumas UNAM;Pachuca;León;Atlas;Santos Laguna;Tijuana;Juárez;Necaxa;Puebla;Querétaro;Mazatlán;Atlético San Luis
JP|J1 League|70|60|Kashima Antlers;Vissel Kobe;Sanfrecce Hiroshima;Kashiwa Reysol;Kyoto Sanga;Machida Zelvia;Urawa Reds;Kawasaki Frontale;Gamba Osaka;Cerezo Osaka;FC Tokyo;Yokohama F. Marinos;Nagoya Grampus;Avispa Fukuoka;Shimizu S-Pulse;Tokyo Verdy;Fagiano Okayama;V-Varen Nagasaki;Mito HollyHock;JEF United Chiba
KR|K League 1|68|59|Jeonbuk Hyundai;Ulsan HD;Pohang Steelers;FC Seoul;Gangwon FC;Daejeon Hana Citizen;Gimcheon Sangmu;Gwangju FC;Jeju SK;FC Anyang;Suwon FC;Incheon United
CN|Super League|67|56|Shanghai Port;Shanghai Shenhua;Chengdu Rongcheng;Beijing Guoan;Shandong Taishan;Tianjin Jinmen Tiger;Zhejiang FC;Henan FC;Qingdao West Coast;Yunnan Yukun;Dalian Yingbo;Wuhan Three Towns;Shenzhen Peng City;Qingdao Hainiu;Chongqing Tonglianglong;Liaoning Tieren
RU|Premier Liga|75|61|Zenit;Krasnodar;Spartak Moscou;CSKA Moscou;Lokomotiv Moscou;Dínamo Moscou;Rubin Kazan;Rostov;Akhmat Grozny;Krylia Sovetov;Baltika;Dinamo Makhachkala;Akron Tolyatti;Pari NN;Orenburg;Sochi
UA|Premier Liga|71|57|Shakhtar Donetsk;Dínamo de Kiev;Polissya Zhytomyr;Kryvbas;LNZ Cherkasy;Oleksandriya;Karpaty Lviv;Zorya Luhansk;Kolos Kovalivka;Veres Rivne;Rukh Lviv;Obolon Kyiv;Metalist 1925;Kudrivka;Epitsentr;Poltava
GR|Super League|75|60|Olympiacos;PAOK;AEK Atenas;Panathinaikos;Aris;OFI Creta;Asteras Tripolis;Atromitos;Volos;Levadiakos;Panetolikos;Kifisia;Panserraikos;AEL Larissa
CH|Super League|73|61|Basel;Young Boys;Servette;Lugano;Luzern;St. Gallen;Lausanne-Sport;Zürich;Sion;Thun;Grasshoppers;Winterthur
AT|Bundesliga|74|60|Red Bull Salzburg;Sturm Graz;Rapid Viena;Austria Viena;LASK;Wolfsberger AC;Hartberg;Rheindorf Altach;Blau-Weiß Linz;WSG Tirol;Grazer AK;Ried
DK|Superliga|73|60|Copenhague;Midtjylland;Brøndby;AGF Aarhus;Nordsjælland;Randers;Silkeborg;Viborg;OB Odense;Sønderjyske;Vejle;Fredericia
NO|Eliteserien|72|58|Bodø/Glimt;Molde;Brann;Rosenborg;Viking;Vålerenga;Sarpsborg 08;Fredrikstad;Tromsø;Lillestrøm;Sandefjord;HamKam;Kristiansund;KFUM Oslo;Start;Aalesund
SE|Allsvenskan|70|58|Malmö FF;Mjällby;Hammarby;AIK;Djurgården;IFK Göteborg;Häcken;Elfsborg;GAIS;Sirius;Brommapojkarna;Halmstad;Degerfors;Västerås SK;Kalmar FF;Örgryte
PL|Ekstraklasa|70|58|Lech Poznań;Raków Częstochowa;Jagiellonia;Legia Varsóvia;Pogoń Szczecin;Górnik Zabrze;Cracovia;Widzew Łódź;Motor Lublin;GKS Katowice;Piast Gliwice;Zagłębie Lubin;Korona Kielce;Radomiak;Lechia Gdańsk;Wisła Płock;Arka Gdynia;Bruk-Bet Termalica
CZ|Chance Liga|74|58|Slavia Praga;Sparta Praga;Viktoria Plzeň;Baník Ostrava;Jablonec;Sigma Olomouc;Hradec Králové;Slovan Liberec;Bohemians 1905;Mladá Boleslav;Teplice;Karviná;Pardubice;Dukla Praga;Zlín;Slovácko
HR|HNL|73|57|Dinamo Zagreb;Hajduk Split;Rijeka;Osijek;Varaždin;Lokomotiva Zagreb;Slaven Belupo;Istra 1961;Gorica;Vukovar 1991
RS|SuperLiga|73|55|Estrela Vermelha;Partizan;Vojvodina;Čukarički;TSC Bačka Topola;Novi Pazar;Radnički 1923;OFK Beograd;Železničar Pančevo;Spartak Subotica;IMT Belgrado;Mladost Lučani;Radnički Niš;Napredak;Javor;Radnik Surdulica
CO|Liga BetPlay|71|58|Atlético Nacional;Millonarios;América de Cali;Junior Barranquilla;Independiente Santa Fe;Deportes Tolima;Independiente Medellín;Deportivo Cali;Once Caldas;Atlético Bucaramanga;Deportivo Pereira;Águilas Doradas;Alianza FC;Fortaleza CEIF;Llaneros;Boyacá Chicó;Internacional de Bogotá;Cúcuta Deportivo;Jaguares de Córdoba;Envigado
CL|Primera División|69|57|Colo-Colo;Universidad de Chile;Universidad Católica;Coquimbo Unido;O'Higgins;Palestino;Audax Italiano;Huachipato;Everton de Viña;Cobresal;Unión La Calera;Ñublense;Deportes Iquique;Deportes La Serena;Deportes Limache;Deportes Concepción
UY|Primera División|69|56|Peñarol;Nacional;Defensor Sporting;Liverpool;Danubio;Racing Montevideo;Cerro Largo;Boston River;Montevideo Wanderers;Progreso;Plaza Colonia;Juventud;Cerro;River Plate Montevideo;Central Español;Montevideo City Torque
PY|División de Honor|68|56|Olimpia;Cerro Porteño;Libertad;Guaraní;Nacional Asunción;Sportivo Luqueño;Sportivo Trinidense;2 de Mayo;Sportivo Ameliano;Tacuary;Recoleta;General Caballero JLM
EC|LigaPro|71|56|Independiente del Valle;LDU Quito;Barcelona SC;Emelec;Universidad Católica;Aucas;Deportivo Cuenca;Orense;Macará;Técnico Universitario;Mushuc Runa;Delfín;El Nacional;Libertad FC;Manta;Vinotinto
PE|Liga 1|67|55|Universitario;Alianza Lima;Sporting Cristal;Cusco FC;Melgar;Cienciano;ADT;Sport Huancayo;Alianza Atlético;Deportivo Garcilaso;Atlético Grau;Juan Pablo II;Los Chankas;Sport Boys;Comerciantes Unidos;UTC;Ayacucho FC;Binacional
AU|A-League|66|56|Melbourne City;Auckland FC;Western Sydney Wanderers;Sydney FC;Melbourne Victory;Adelaide United;Central Coast Mariners;Macarthur FC;Brisbane Roar;Wellington Phoenix;Newcastle Jets;Perth Glory
EG|Premier League|70|55|Al Ahly;Pyramids;Zamalek;Al Masry;Ceramica Cleopatra;Modern Sport;ZED;Smouha;ENPPI;Ismaily;Al Ittihad;Talaea El Gaish;El Gouna;Ghazl El Mahalla;Petrojet;National Bank;Haras El Hodoud;Pharco
MA|Botola Pro|69|55|RS Berkane;Wydad Casablanca;Raja Casablanca;FAR Rabat;FUS Rabat;MAS Fès;Hassania Agadir;Olympic Safi;Difaâ El Jadida;Union Touarga;IR Tanger;Renaissance Zemamra;CODM Meknès;Kawkab Marrakech;Olympique Dcheira;Yacoub El Mansour
ZA|Premiership|68|55|Mamelodi Sundowns;Orlando Pirates;Kaizer Chiefs;Stellenbosch;Sekhukhune United;TS Galaxy;AmaZulu;Polokwane City;Golden Arrows;Chippa United;Richards Bay;Durban City;Siwelele;Magesi;Marumo Gallants;Orbit College"""

PAISES = {'BR':('Brasil','br'),'AR':('Argentina','es'),'UY':('Uruguai','es'),'CL':('Chile','es'),'CO':('Colômbia','es'),
 'PY':('Paraguai','es'),'PE':('Peru','es'),'EC':('Equador','es'),'MX':('México','es'),'ES':('Espanha','es'),
 'US':('Estados Unidos','en'),'EN':('Inglaterra','en'),'SC':('Escócia','en'),'AU':('Austrália','en'),
 'IT':('Itália','it'),'DE':('Alemanha','de'),'AT':('Áustria','de'),'CH':('Suíça','de'),'FR':('França','fr'),
 'BE':('Bélgica','nl'),'NL':('Holanda','nl'),'PT':('Portugal','pt'),'TR':('Turquia','tr'),'JP':('Japão','jp'),
 'KR':('Coreia do Sul','kr'),'CN':('China','cn'),'SA':('Arábia Saudita','ar'),'EG':('Egito','ar'),'MA':('Marrocos','ar'),
 'DZ':('Argélia','ar'),'RU':('Rússia','ru'),'UA':('Ucrânia','ru'),'DK':('Dinamarca','nd'),'NO':('Noruega','nd'),
 'SE':('Suécia','nd'),'PL':('Polônia','sl'),'CZ':('Tchéquia','sl'),'HR':('Croácia','sl'),'RS':('Sérvia','sl'),
 'GR':('Grécia','gr'),'ZA':('África do Sul','af'),'SN':('Senegal','af'),'NG':('Nigéria','af'),'GH':('Gana','af'),
 'CI':('Costa do Marfim','af'),'CM':('Camarões','af'),'ML':('Mali','af')}
# peso de cada nacionalidade entre os estrangeiros
ESTRANG = 'BR9 AR7 FR6 ES5 PT4 NL3 EN3 DE3 IT3 BE3 UY3 CO3 SN3 NG3 CI3 MA3 GH2 CM2 ML2 DZ2 HR2 RS2 JP2 KR2 US2 MX2 DK2 PL2 EC2 SE1 NO1 TR1 CL1 PY1 CH1 AT1 CZ1 UA1 EG1 SC1 GR1 RU1 PE1 AU1 CN1 SA1 ZA1'
LOCAL = {'EN':.38,'IT':.45,'DE':.5,'FR':.55,'ES':.6,'SA':.55,'US':.55,'TR':.55,'PT':.5,'BE':.45,'NL':.6,'BR':.86,'AR':.86}
NOMES = {
'br':"Gabriel Lucas Matheus Pedro João Rafael Vinícius Gustavo Felipe Bruno Thiago Diego Rodrigo Caio André Igor Danilo Wesley Luan Arthur Davi Renan Marcos Everton|Silva Santos Oliveira Souza Lima Pereira Costa Ferreira Almeida Ribeiro Carvalho Gomes Martins Rocha Barbosa Araújo Moraes Cardoso Teixeira Nascimento Moreira Mendes Freitas Barros Pinheiro",
'es':"Juan Carlos Luis Miguel Javier Diego Sergio Pablo Alejandro Andrés Martín Facundo Nicolás Santiago Matías Gonzalo Iván Rodrigo Tomás Lautaro Joaquín Emiliano Mateo Cristian|García Rodríguez González Fernández López Martínez Sánchez Pérez Gómez Díaz Torres Ramírez Romero Álvarez Ruiz Herrera Medina Castro Vargas Ríos Suárez Ortega Molina Rojas Acosta",
'en':"James Jack Harry Oliver Charlie George Thomas Daniel Ryan Callum Luke Kyle Mason Jordan Lewis Tyler Ben Sam Connor Jamie|Smith Jones Taylor Brown Williams Wilson Johnson Davies Robinson Wright Thompson Evans Walker White Roberts Green Hall Wood Jackson Clarke Hughes Morgan Cooper Bennett",
'it':"Marco Luca Andrea Matteo Lorenzo Alessandro Davide Federico Simone Nicolò Riccardo Giacomo Stefano Daniele Francesco Gianluca Tommaso Filippo|Rossi Russo Ferrari Esposito Bianchi Romano Colombo Ricci Marino Greco Bruno Gallo Conti De Luca Costa Mancini Giordano Rizzo Lombardi Moretti Barbieri Fontana",
'de':"Lukas Leon Jonas Felix Maximilian Niklas Tim Jan Paul Florian Julian Kevin Marcel Tobias Moritz Fabian Luca David|Müller Schmidt Schneider Fischer Weber Meyer Wagner Becker Schulz Hoffmann Koch Richter Klein Wolf Schröder Neumann Braun Zimmermann Krüger Hartmann Lange Werner",
'fr':"Lucas Hugo Théo Nathan Mathis Enzo Louis Raphaël Antoine Maxime Kylian Clément Adrien Yanis Baptiste Jules Mathéo Noah|Martin Bernard Dubois Thomas Robert Richard Petit Durand Leroy Moreau Simon Laurent Lefebvre Michel Garcia David Bertrand Roux Vincent Fournier Morel Girard",
'pt':"João Diogo Rúben Tiago Rafael Gonçalo Bruno André Nuno Pedro Ricardo Miguel Francisco Rodrigo Vítor Hugo Fábio Duarte|Silva Santos Ferreira Pereira Oliveira Costa Rodrigues Martins Sousa Fernandes Gonçalves Gomes Lopes Marques Alves Almeida Ribeiro Pinto Carvalho Teixeira Moreira",
'nl':"Daan Sem Thijs Lars Jesse Bram Luuk Milan Stijn Ruben Tim Joey Kevin Sven Jordy Wout Jens Niels|de Jong de Vries van Dijk Bakker Janssen Visser Smit Meijer de Boer Mulder de Groot Bos Vos Peters Hendriks van Leeuwen Dekker Brouwer de Wit Dijkstra Maes Peeters",
'tr':"Mehmet Mustafa Ahmet Emre Burak Can Kerem Arda Yusuf Ömer Hakan Cenk Oğuz Mert Eren Berkay Okay Kaan|Yılmaz Kaya Demir Şahin Çelik Yıldız Aydın Öztürk Arslan Doğan Kılıç Aslan Çetin Kara Koç Kurt Özdemir Polat Erdoğan Güler",
'jp':"Takumi Kaoru Daichi Ritsu Hiroki Yuto Shota Kento Ryota Kota Wataru Junya Ayase Yuki Sota Kaito Haruto Ren|Sato Suzuki Takahashi Tanaka Watanabe Ito Yamamoto Nakamura Kobayashi Kato Yoshida Yamada Sasaki Matsumoto Inoue Kimura Hayashi Shimizu Mori Ikeda",
'kr':"Min-jae Hee-chan Kang-in Seung-ho Jae-sung Woo-young Gue-sung In-beom Jun-ho Tae-hwan Ji-sung Young-woo Hyun-woo Dong-gyeong Sang-ho|Kim Lee Park Choi Jung Kang Cho Yoon Jang Lim Han Oh Seo Shin Kwon Hwang Ahn Song Hong",
'cn':"Wei Lei Hao Jie Yang Tao Peng Bin Chao Long Xin Jun Ming Qiang Yu Fei Kai|Wang Li Zhang Liu Chen Yang Huang Zhao Wu Zhou Xu Sun Ma Zhu Hu Guo He Lin Gao Luo",
'ar':"Mohamed Ahmed Ali Omar Youssef Khalid Abdullah Salem Hamza Karim Yassine Sofiane Ismail Bilal Nabil Amine Ayoub Saud Fahad Tarek|Hassan Ibrahim Mansour El-Sayed Benali Haddad Khalil Nasser Fathi Saleh Rahman Aziz Kamal Tahir Hamdan Zaki Rashid Al-Harbi Al-Otaibi Al-Qahtani Al-Ghamdi Bennani",
'ru':"Aleksandr Dmitri Sergei Andrei Artem Ivan Maksim Nikita Mikhail Kirill Denis Roman Vladislav Oleksandr Mykola Viktor Ilya Yegor|Ivanov Smirnov Kuznetsov Popov Sokolov Lebedev Kozlov Novikov Morozov Petrov Volkov Fedorov Mironov Zaitsev Pavlov Kovalenko Bondarenko Shevchuk Tkachenko Melnyk",
'nd':"Erik Lars Anders Magnus Mikkel Jonas Oscar Emil William Kasper Mathias Henrik Sander Kristoffer Rasmus Viktor Isak Elias|Hansen Johansen Olsen Larsen Andersen Nielsen Pedersen Jensen Eriksson Karlsson Nilsson Lindqvist Berg Haugen Dahl Lund Holm Strand Bakke Solberg",
'sl':"Jakub Kacper Mateusz Tomáš Ondřej Luka Ivan Marko Nikola Filip Stefan Petar Dominik Adam Michal Josip Mario Lovro|Nowak Kowalski Wiśniewski Novák Svoboda Dvořák Horvat Kovačević Babić Marić Jovanović Petrović Nikolić Marković Đorđević Popović Zieliński Wójcik Krejčí Lukić",
'gr':"Giorgos Dimitris Kostas Nikos Giannis Christos Panagiotis Vasilis Thanasis Michalis Stelios Lazaros Anastasios Tasos|Papadopoulos Pappas Oikonomou Georgiou Vlachos Angelopoulos Nikolaidis Karagiannis Dimitriou Konstantinou Makris Alexiou Ioannidis Antoniou Fotiou",
'af':"Moussa Ibrahima Mamadou Cheikh Victor Samuel Emmanuel Kelechi Wilfried Franck Seko Yves Thomas Bongani Themba Sipho Kwame Kofi|Diallo Ndiaye Diop Traoré Koné Touré Mensah Osei Boateng Okafor Eze Adeyemi Mbeki Dlamini Nkosi Kamara Fofana Camara Mbemba Sissoko Bamba"}
APELIDOS = 'Dudu Juninho Paulinho Neto Pedrinho Fabinho Marquinhos Tiaguinho Luizinho Bruninho Carlinhos Didi Nenê Serginho Ronaldinho Robinho'.split()

POSICOES = ['GOL', 'ZAG', 'LAT', 'VOL', 'MEI', 'ATA']
GRP = {'GOL':'G', 'ZAG':'D', 'LAT':'D', 'VOL':'M', 'MEI':'M', 'ATA':'A'}
ELENCO = (('GOL',3), ('ZAG',5), ('LAT',4), ('VOL',4), ('MEI',4), ('ATA',4))
HABS = {'FIN':'Finalização','CAB':'Cabeceio','DRI':'Drible','PAS':'Passe','VEL':'Velocidade','DES':'Desarme',
        'MAR':'Marcação','CHL':'Chute de longe','BOL':'Bola parada','PEN':'Pênaltis','LID':'Liderança',
        'REF':'Reflexos','SAI':'Saída do gol','RES':'Resistência','CRU':'Cruzamento'}
HAB_POS = {'GOL':'REF SAI LID', 'ZAG':'CAB DES MAR LID', 'LAT':'VEL CRU DES RES', 'VOL':'DES MAR PAS RES CHL',
           'MEI':'PAS DRI CHL BOL FIN', 'ATA':'FIN CAB DRI VEL PEN'}
# formacao: (defensores, meias, atacantes, mult. meio, mult. ataque, mult. defesa)
FORMS = {'4-4-2':(4,4,2,1.0,1.0,1.0), '4-3-3':(4,3,3,.96,1.07,.97), '4-2-3-1':(4,5,1,1.05,.97,1.0),
         '3-5-2':(3,5,2,1.06,1.02,.92), '5-3-2':(5,3,2,.95,.93,1.12), '3-4-3':(3,4,3,1.0,1.1,.9), '4-5-1':(4,5,1,1.07,.9,1.03)}
TATICAS = {'D':(.88,1.12), 'E':(1.0,1.0), 'O':(1.12,.9)}   # (ataque, defesa)
CORES = [('#d62828','#fff'),('#1d4ed8','#fff'),('#111827','#fff'),('#15803d','#fff'),('#facc15','#111'),('#7c3aed','#fff'),
         ('#0ea5e9','#fff'),('#ea580c','#fff'),('#be123c','#fff'),('#0f766e','#fff'),('#f8fafc','#111'),('#1e3a8a','#facc15')]
DATAS_FIFA = (5, 12, 19, 26)

# ------------------------- CRIACAO DO MUNDO --------------------------
class Mundo: pass
G = None
LOCK = threading.RLock()

def bandeira(cc):
    if cc in ('EN', 'SC'):
        return '\U0001F3F4' + ''.join(chr(0xE0000 + ord(c)) for c in ('gbeng' if cc == 'EN' else 'gbsct')) + '\U000E007F'
    return ''.join(chr(0x1F1E6 + ord(c) - 65) for c in cc)

def sigla(n):
    w = [x for x in n.replace('-', ' ').replace('.', ' ').split() if len(x) > 2 and x.lower() not in ('club','de','del','des','fc','cf','sc','ac','the')] or [n]
    return (w[0][:3] if len(w) == 1 else w[0][0] + w[1][:2]).upper()

def valor(p):
    a = p['age']; f = 1.3 if a <= 21 else 1.12 if a <= 25 else 1.0 if a <= 29 else .7 if a <= 32 else .4
    p['val'] = int(max(20, 50 * 1.2 ** (p['ovr'] - 50) * f * (1 + max(0, p['pot'] - p['ovr']) / 30)))  # mil EUR
    p['sal'] = max(1, p['val'] // 260)                                                                   # mil EUR/semana

def novo_jogador(pos, ovr, cc, club=None, age=None):
    age = age or int(R.triangular(17, 35, 25)); ovr = max(35, min(94, int(round(ovr))))
    first, last = NOMES[PAISES[cc][1]].split('|')
    nome = R.choice(APELIDOS) if cc == 'BR' and R.random() < .2 else R.choice(first.split()) + ' ' + R.choice(last.split())
    nh = (ovr >= 68) + (ovr >= 77) + (ovr >= 84) + (R.random() < .3)
    hab = R.sample(HAB_POS[pos].split(), min(nh, 3))
    if age >= 29 and 'LID' not in hab and R.random() < .2: hab.append('LID')
    if R.random() < .07 and 'RES' not in hab: hab.append('RES')
    p = dict(id=G.nid, n=nome, pos=pos, age=age, nat=cc, ovr=ovr, club=club, hab=hab,
             pot=min(97, ovr + int(max(0, 27 - age) * R.uniform(.4, 2.2))),
             fis=max(30, min(99, int(R.gauss(ovr - 4 + (5 if pos in ('ZAG','VOL','ATA') else 0) - max(0, age - 31) * 2, 7)))),
             pe=R.choices('DEA', (72, 22, 6))[0], cond=100, inj=0, sus=0, ca=0, gol=0, jg=0)
    valor(p); G.P[G.nid] = p; G.nid += 1
    return p

def gerar_mundo(seed=None):
    global G
    if seed is not None: R.seed(seed)
    G = Mundo(); G.P = {}; G.T = {}; G.L = []; G.nid = 1; G.news = []; G.week = 0; G.season = 2026
    G.live = None; G.phase = 'liga'; G.coach = None; G.ntdone = set(); G.ntopp = {}; G.copa = None; G.ult = None
    fk = [x[:2] for x in ESTRANG.split()]; fw = [int(x[2:]) for x in ESTRANG.split()]
    for li, linha in enumerate(LIGAS.strip().split('\n')):
        cc, nome, top, bot, cl = linha.split('|'); top, bot = int(top), int(bot); clubes = cl.split(';')
        L = dict(i=li, cc=cc, n=nome, clubs=[], fx=[], tab={}, champ=[])
        G.L.append(L); n = len(clubes); loc = LOCAL.get(cc, .72)
        for k, cn in enumerate(clubes):
            s = top - (top - bot) * (k / (n - 1)) ** .8 + R.uniform(-1.2, 1.2)
            tid = 'c%d' % len(G.T); h = sum(map(ord, cn))
            T = dict(id=tid, n=cn, lg=li, cc=cc, str=round(s), pl=[], xi=[], form=R.choice(list(FORMS)[:4]), tac='E',
                     mor=60, sig=sigla(cn), cor=CORES[h % len(CORES)], nac=False)
            G.T[tid] = T; L['clubs'].append(tid)
            for pos, qt in ELENCO:
                for i in range(qt):
                    nat = cc if R.random() < loc else R.choices(fk, fw)[0]
                    T['pl'].append(novo_jogador(pos, R.gauss(s + 1 - 11 * i / qt, 3.2), nat, tid)['id'])
            folha = sum(G.P[x]['sal'] for x in T['pl'])
            T['rev'] = int(folha * 1.15); T['bud'] = int(sum(G.P[x]['val'] for x in T['pl']) * .12)
            auto_xi(T)
        novo_calendario(L)
    montar_selecoes()
    for arq in IMPORTADOS: importar_csv(arq)

def montar_selecoes():
    por = {}
    for p in G.P.values(): por.setdefault(p['nat'], []).append(p['id'])
    for cc, ids in por.items():
        tid = 'n' + cc
        if len(ids) < 22 or tid in G.T: continue
        G.T[tid] = dict(id=tid, n=PAISES[cc][0], cc=cc, pl=[], xi=[], form='4-3-3', tac='E', mor=60, sig=cc,
                        cor=CORES[sum(map(ord, cc)) % len(CORES)], nac=True, str=60)
        convocar_auto(G.T[tid])

def selecoes(): return [T for T in G.T.values() if T['nac']]

def convocar_auto(T):
    el = sorted([p for p in G.P.values() if p['nat'] == T['cc'] and p['inj'] == 0], key=lambda p: -p['ovr'])
    conv = []
    for g, q in (('G', 3), ('D', 8), ('M', 7), ('A', 5)):
        conv += [p['id'] for p in el if GRP[p['pos']] == g][:q]
    T['pl'] = conv; auto_xi(T)

def novo_calendario(L):
    ids = L['clubs'][:]; R.shuffle(ids)
    if len(ids) % 2: ids.append(None)
    n = len(ids); rodadas = []
    for r in range(n - 1):
        rd = [(ids[i], ids[n-1-i]) if (r + i) % 2 == 0 else (ids[n-1-i], ids[i]) for i in range(n // 2)]
        rodadas.append([j for j in rd if j[0] and j[1]])
        ids = [ids[0], ids[-1]] + ids[1:-1]
    if len(L['clubs']) <= 20: rodadas += [[(b, a) for a, b in rd] for rd in rodadas]   # turno e returno
    L['fx'] = rodadas; L['res'] = {}
    L['tab'] = {t: [0]*7 for t in L['clubs']}   # J V E D GP GC Pts

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

def arrumar(ids, form):
    sl = slots(form)
    while len(sl) > len(ids): sl.remove('A' if 'A' in sl else 'M')
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
    """troca lesionados/suspensos da escalacao do usuario pelo melhor substituto"""
    xi = [x for x in T['xi'] if x in T['pl']]
    if len(xi) < 11: return auto_xi(T)
    for i, x in enumerate(xi):
        if not disp(x, T['nac']):
            g = GRP[G.P[x]['pos']]
            c = [y for y in T['pl'] if y not in xi and disp(y, T['nac'])]
            if c:
                xi[i] = max(c, key=lambda y: G.P[y]['ovr'] * (1.2 if GRP[G.P[y]['pos']] == g else 1))
    T['xi'] = xi
    return xi

# ------------------------- MOTOR DA PARTIDA --------------------------
WSH = {'G': 0, 'D': .6, 'M': 2.2, 'A': 5}

def eh_usuario(tid):
    c = G.coach; return bool(c) and tid in (c['club'], c['nt'])

def lado(tid):
    T = G.T[tid]
    (validar_xi if eh_usuario(tid) else auto_xi)(T)
    on, sl = (list(T['xi']), slots(T['form'])) if len(T['xi']) == 11 else arrumar(T['xi'], T['form'])
    bench = sorted([x for x in T['pl'] if x not in on and disp(x, T['nac'])], key=lambda x: -G.P[x]['ovr'])[:12]
    en = {x: (100 if T['nac'] else G.P[x]['cond']) for x in on + bench}
    return dict(t=tid, on=on, sl=sl, bench=bench, subs=0, en=en, used=set(on), am=set(), sai=set())

def poder(S, casa):
    T = G.T[S['t']]; d, m, a, fm, fa, fd = FORMS[T['form']]
    soma = {'G': 0, 'D': 0, 'M': 0, 'A': 0}; gk = 30; att = mid = de = 1.0
    for x, s in zip(S['on'], S['sl']):
        p = G.P[x]; hb = p['hab']
        e = p['ovr'] * fit(p['pos'], s) * (.72 + .28 * S['en'][x] / 100)
        if s == 'G': gk = e * (1.06 if 'REF' in hb else 1) * (1.03 if 'SAI' in hb else 1)
        else: soma[s] += e
        for h in hb:
            if h in ('DRI', 'VEL', 'CRU', 'BOL'): att += .012
            elif h == 'PAS': mid += .015
            elif h in ('DES', 'MAR'): de += .012
            elif h == 'LID': att += .004; mid += .004; de += .004
    k = .96 + .08 * T['mor'] / 100; ta, td = TATICAS[T['tac']]
    Dv, Mv, Av = soma['D'] / d, soma['M'] / m, soma['A'] / a
    M = (.7 * Mv + .15 * Dv + .15 * Av) * fm * mid * k * (1.05 if casa else 1)
    A = (.65 * Av + .35 * Mv) * fa * att * k * ta * (1.03 if casa else 1)
    D = (.7 * Dv + .3 * Mv) * fd * de * k * td
    return max(M, 1), max(A, 1), max(D, 1), gk

def ev(m, t, s, k, x, y=''):
    m['ev'].append(dict(m=t, s=s, k=k, x=x, y=y))

def minuto(m, t, L):
    pw = [poder(m['s'][0], not m['neutro']), poder(m['s'][1], False)]
    a, b = pw[0][0] ** 2.2, pw[1][0] ** 2.2; sh = a / (a + b)
    for s in (0, 1):
        S = m['s'][s]
        for x in S['on']:
            p = G.P[x]; S['en'][x] = max(0, S['en'][x] - (.40 - .0028 * p['fis']) * (.7 if 'RES' in p['hab'] else 1))
        if R.random() < .26 * (sh if s == 0 else 1 - sh): chance(m, s, pw, t, L)
        if R.random() < .018: cartao(m, s, t, L)
        if R.random() < .0018: lesao(m, s, t)
        if m['us'] != s and t >= 56 and R.random() < .09: ai_sub(m, s, t)

def chance(m, s, pw, t, L):
    o = 1 - s; S = m['s'][s]; A, D, gk = pw[s][1], pw[o][2], pw[o][3]
    cand = [(x, sl) for x, sl in zip(S['on'], S['sl']) if sl != 'G']
    if not cand: return
    if R.random() < .015:
        x = max(S['on'], key=lambda y: G.P[y]['ovr'] + (12 if 'PEN' in G.P[y]['hab'] else 0) - (50 if G.P[y]['pos'] == 'GOL' else 0))
        pg = .74 + (.08 if 'PEN' in G.P[x]['hab'] else 0) - (.05 if gk > A else 0); pen = True
    else:
        w = [WSH[sl] * G.P[x]['ovr'] * (1.6 if 'FIN' in G.P[x]['hab'] else 1) * (1.2 if 'CAB' in G.P[x]['hab'] else 1)
             * (1.2 if 'CHL' in G.P[x]['hab'] else 1) for x, sl in cand]
        x, sl = R.choices(cand, w)[0]; p = G.P[x]
        q = p['ovr'] * fit(p['pos'], sl) * (.72 + .28 * S['en'][x] / 100) / A
        pg = min(.45, .092 * (A / D) ** 1.6 * (A / gk) ** .4 * q ** 1.2 * (1.12 if 'FIN' in p['hab'] else 1)); pen = False
    p = G.P[x]
    if R.random() < pg:
        m['g'][s] += 1; m['gm'] = t
        if L['tipo'] == 'liga': p['gol'] += 1
        ast = ''
        if not pen and R.random() < .65:
            c2 = [(y, sl) for y, sl in zip(S['on'], S['sl']) if y != x and sl != 'G']
            if c2:
                ast = G.P[R.choices(c2, [{'D': 1, 'M': 3, 'A': 2}[sl] * (1.5 if {'PAS', 'CRU'} & set(G.P[y]['hab']) else 1) for y, sl in c2])[0][0]]['n']
        ev(m, t, s, 'gol', p['n'] + (' (pênalti)' if pen else ''), ast)
    elif m['us'] is not None and R.random() < .3:
        ev(m, t, s, 'quase', p['n'] + R.choice([' chutou para fora', ' parou no goleiro', ' acertou a trave', ' perdeu chance clara', ' bateu por cima']))

def expulsar(S, i):
    x = S['on'].pop(i); s = S['sl'].pop(i); S['sai'].add(x)
    if s == 'G' and S['on']: S['on'], S['sl'] = arrumar(S['on'], G.T[S['t']]['form'])

def cartao(m, s, t, L):
    S = m['s'][s]
    if len(S['on']) <= 7: return
    i = R.choices(range(len(S['on'])), [{'G': .2, 'D': 3, 'M': 2.5, 'A': 1}[sl] for sl in S['sl']])[0]
    x = S['on'][i]; p = G.P[x]; liga = L['tipo'] == 'liga'
    if x in S["am"] or R.random() < .015:
        dois = x in S['am']; expulsar(S, i)
        if liga: p['sus'] = 1 if dois else 2
        ev(m, t, s, 'vm', p['n'] + (' (2º amarelo)' if dois else ''))
        if m['us'] == s: m['pausa'] = 'expulsão'
    else:
        S['am'].add(x); ev(m, t, s, 'am', p['n'])
        if liga:
            p['ca'] += 1
            if p['ca'] >= 3: p['ca'] = 0; p['sus'] = 1

def lesao(m, s, t):
    S = m['s'][s]; i = R.randrange(len(S['on'])); x = S['on'][i]; p = G.P[x]
    if p['inj']: return
    p['inj'] = R.randint(2, 6); S['en'][x] = min(S['en'][x], 15)
    ev(m, t, s, 'les', p['n'] + ' (%d sem.)' % (p['inj'] - 1))
    if m['us'] == s: m['pausa'] = 'lesão'
    else: ai_sub(m, s, t, i)

def substituir(m, s, i, xin, t):
    S = m['s'][s]; out = S['on'][i]
    S['on'][i] = xin; S['bench'].remove(xin); S['sai'].add(out); S['used'].add(xin); S['subs'] += 1
    ev(m, t, s, 'sub', G.P[xin]['n'], G.P[out]['n'])

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

def poisson(l):
    lim, k, p = math.exp(-l), 0, 1.0
    while True:
        p *= R.random()
        if p < lim: return k
        k += 1

def rapido(h, a, neutro=False, liga=False):
    """simulacao instantanea (outras ligas / jogos sem o usuario)"""
    S = [lado(h), lado(a)]; pw = [poder(S[0], not neutro), poder(S[1], False)]
    x, y = pw[0][0] ** 2.2, pw[1][0] ** 2.2; sh = x / (x + y); gols = []
    for s, share in ((0, sh), (1, 1 - sh)):
        o = 1 - s; A, D, gk = pw[s][1], pw[o][2], pw[o][3]
        pg = min(.45, .092 * (A / D) ** 1.6 * (A / gk) ** .4)
        n = poisson(90 * .26 * share * (.985 * pg + .015 * .76)); gols.append(n)
        if liga and n:
            c = [(x, sl) for x, sl in zip(S[s]['on'], S[s]['sl']) if sl != 'G']
            for _ in range(n):
                G.P[R.choices(c, [WSH[sl] * G.P[x]['ovr'] * (1.6 if 'FIN' in G.P[x]['hab'] else 1) for x, sl in c])[0][0]]['gol'] += 1
    return gols[0], gols[1]

def moral(T, saldo):
    T['mor'] = max(25, min(100, T['mor'] + (7 if saldo > 0 else 1 if saldo == 0 else -6)))

def registrar(L, h, a, gh, ga):
    for t, gp, gc in ((L['tab'][h], gh, ga), (L['tab'][a], ga, gh)):
        t[0] += 1; t[4] += gp; t[5] += gc
        if gp > gc: t[1] += 1; t[6] += 3
        elif gp == gc: t[2] += 1; t[6] += 1
        else: t[3] += 1
    L['res'][(h, a)] = (gh, ga)
    moral(G.T[h], gh - ga); moral(G.T[a], ga - gh)

def classificacao(L):
    tb = L['tab']; return sorted(L['clubs'], key=lambda t: (-tb[t][6], -(tb[t][4] - tb[t][5]), -tb[t][4], G.T[t]['n']))

# ------------------------- PARTIDA AO VIVO ---------------------------
def iniciar(tipo, jogos, comp, ko=False, neutro=False):
    c = G.coach; meu = c['nt'] if tipo in ('sel', 'copa') else c['club']; ms = []; u = None
    for i, (h, a) in enumerate(jogos):
        m = dict(t=[h, a], g=[0, 0], ev=[], s=[lado(h), lado(a)], pen=None, neutro=neutro, us=None, w=None, gm=0)
        if meu in (h, a): m['us'] = 0 if h == meu else 1; u = i
        ms.append(m)
    if u is not None and u: ms.insert(0, ms.pop(u)); u = 0
    G.live = dict(tipo=tipo, comp=comp, min=0, ms=ms, u=u, ko=ko, fim=False, ne=0)

def passo(n):
    L = G.live; frames = []
    if L['fim']: return frames
    um = L['ms'][L['u']] if L['u'] is not None else None
    for _ in range(max(1, min(n, 10))):
        if L['min'] >= 90: break
        L['min'] += 1; t = L['min']
        for m in L['ms']: minuto(m, t, L)
        f = dict(min=t, g=[list(m['g']) for m in L['ms']], gols=[i for i, m in enumerate(L['ms']) if m['gm'] == t], ev=[])
        if um:
            f['ev'] = um['ev'][L['ne']:]; L['ne'] = len(um['ev'])
            if um.get('pausa'):
                pz = um.pop('pausa')
                if t < 90: f['pausa'] = pz
        frames.append(f)
        if 'pausa' in f: break
    if L['min'] >= 90: encerrar()
    return frames

def resultado_usuario(m):
    s = m['us']; a, b = m['pen'] or m['g']
    return 'V' if (a > b) == (s == 0) and a != b else 'E' if a == b else 'D'

def encerrar():
    L = G.live; L['fim'] = True; c = G.coach; venc = []
    for m in L['ms']:
        if L['ko'] and m['g'][0] == m['g'][1]: penaltis(m)
        a, b = m['pen'] or m['g']; m['w'] = 0 if a > b else 1 if b > a else None
        venc.append(m['t'][m['w'] if m['w'] is not None else R.randint(0, 1)])
        for s in (0, 1):
            S = m['s'][s]; T = G.T[S['t']]
            if T['nac']: continue
            for x in S['used']: G.P[x]['jg'] += 1
            if L['tipo'] == 'liga':
                for x in T['pl']:
                    if G.P[x]['sus'] > 0 and x not in S['used']: G.P[x]['sus'] -= 1
            if eh_usuario(T['id']):
                for x in S['used']: G.P[x]['cond'] = int(S['en'].get(x, 100))
        if L['tipo'] != 'liga': moral(G.T[m['t'][0]], m['g'][0] - m['g'][1]); moral(G.T[m['t'][1]], m['g'][1] - m['g'][0])
        if m['us'] is not None:
            r = resultado_usuario(m); c[{'V': 'v', 'E': 'e', 'D': 'd'}[r]] += 1
            eu, ele = G.T[m['t'][m['us']]], G.T[m['t'][1 - m['us']]]
            if L['tipo'] == 'liga':
                esp = max(.3, min(2.6, 1.35 + (forca(eu) - forca(ele) + (2 if m['us'] == 0 else -2)) * .09))
                pts = {'V': 3, 'E': 1, 'D': 0}[r]
                c['conf'] = max(0, min(100, c['conf'] + (pts - esp) * 4)); c['rep'] = max(1, min(99, c['rep'] + (pts - esp) * .25))
            else:
                c['rep'] = max(1, min(99, c['rep'] + {'V': .8, 'E': .1, 'D': -.6}[r]))
    if L['tipo'] == 'liga':
        lg = G.L[G.T[c['club']]['lg']]
        for m in L['ms']: registrar(lg, m['t'][0], m['t'][1], m['g'][0], m['g'][1])
        fim_semana(ja=lg)
    elif L['tipo'] == 'sel':
        G.ntdone.add(G.week)
    elif L['tipo'] == 'copa':
        avancar_copa(venc)

# ----------------------- TEMPORADA E CARREIRA ------------------------
FASES = ['Oitavas de final', 'Quartas de final', 'Semifinal', 'Final']

def noticia(txt, tipo='info'):
    G.news.insert(0, dict(s=G.season, w=G.week + 1, x=txt, k=tipo)); del G.news[40:]

def liga_usuario():
    c = G.coach; return G.L[G.T[c['club']]['lg']] if c and c['club'] else None

def semanas_temporada():
    L = liga_usuario(); return len(L['fx']) if L else max(len(x['fx']) for x in G.L)

def fim_semana(ja=None):
    w = G.week; c = G.coach
    for L in G.L:
        if L is ja or w >= len(L['fx']): continue
        for h, a in L['fx'][w]: registrar(L, h, a, *rapido(h, a, liga=True))
    if c['club']:
        T = G.T[c['club']]; L = G.L[T['lg']]
        casa = w < len(L['fx']) and any(h == T['id'] for h, a in L['fx'][w])
        T['bud'] += T['rev'] - sum(G.P[x]['sal'] for x in T['pl']) + (int(T['rev'] * .6) if casa else 0)
    for p in G.P.values():
        if p['inj']: p['inj'] -= 1
        if p['cond'] < 100: p['cond'] = min(100, p['cond'] + 16)
    G.week += 1
    c['ofs'] = [o for o in c['ofs'] if G.week - o['w'] <= 4]
    if R.random() < (.35 if not c['club'] else .05): gerar_proposta()
    if not c['nt'] and c['rep'] >= 45 and R.random() < .03: gerar_proposta(sel=True)
    if c['club'] and G.week >= 6 and c['conf'] < 12:
        noticia('A diretoria do %s demitiu você após a sequência de maus resultados.' % G.T[c['club']]['n'], 'mau')
        c['club'] = None; c['rep'] = max(1, c['rep'] - 6)
    if G.week >= semanas_temporada(): fim_liga()

def gerar_proposta(sel=False):
    c = G.coach; rep = c['rep']
    if sel:
        cand = [T for T in selecoes() if T['id'] != c['nt'] and 45 + rep * .25 <= forca(T) <= 55 + rep * .35]
    else:
        mx = 60 + rep * .32
        cand = [T for T in G.T.values() if not T['nac'] and T['id'] != c['club'] and mx - 10 <= T['str'] <= mx]
    if not cand: return
    T = R.choice(cand)
    if any(o['t'] == T['id'] for o in c['ofs']): return
    c['ofs'].append(dict(t=T['id'], tipo='sel' if sel else 'clube', w=G.week))
    noticia('Proposta: %s quer você como técnico! Veja em Carreira.' % T['n'], 'bom')

def fim_liga():
    c = G.coach
    for L in G.L:
        for w in range(G.week, len(L['fx'])):
            for h, a in L['fx'][w]: registrar(L, h, a, *rapido(h, a, liga=True))
        L['champ'].append((G.season, classificacao(L)[0]))
    if c['club']:
        T = G.T[c['club']]; L = G.L[T['lg']]; tb = classificacao(L); pos = tb.index(T['id']) + 1
        esp = sorted(L['clubs'], key=lambda t: -forca(G.T[t])).index(T['id']) + 1
        c['rep'] = max(1, min(99, c['rep'] + max(-10, min(12, (esp - pos) * 1.2)) + (8 if pos == 1 else 0)))
        T['bud'] += int(T['rev'] * 8 * (len(tb) - pos + 1) / len(tb))
        c['hist'].append(dict(s=G.season, t=T['n'], l=L['n'], pos=pos, pts=L['tab'][T['id']][6], tit=pos == 1))
        noticia(('🏆 CAMPEÃO! ' if pos == 1 else '') + '%s terminou a %s em %dº lugar (expectativa: %dº).' % (T['n'], L['n'], pos, esp), 'bom' if pos <= esp else 'info')
        if pos > esp + 5 and c['conf'] < 45:
            noticia('A diretoria do %s não renovou com você.' % T['n'], 'mau'); c['club'] = None
    for T in selecoes():
        if T['id'] != c['nt']: convocar_auto(T)
    top = sorted(selecoes(), key=lambda T: -forca(T))[:16]
    ordem = [0, 15, 7, 8, 3, 12, 4, 11, 1, 14, 6, 9, 2, 13, 5, 10]
    G.copa = dict(stage=0, teams=[top[i]['id'] for i in ordem])
    G.phase = 'copa'
    noticia('Fim da temporada nas ligas! Começa a Copa das Nações com as 16 melhores seleções.')

def simular_copa():
    while G.phase == 'copa':
        t = G.copa['teams']; venc = []
        for h, a in zip(t[0::2], t[1::2]):
            gh, ga = rapido(h, a, neutro=True)
            venc.append(h if gh > ga else a if ga > gh else R.choice((h, a)))
        avancar_copa(venc)

def avancar_copa(venc):
    c = G.coach
    if c['nt'] in G.copa['teams'] and c['nt'] not in venc:
        noticia(('%s ficou com o vice da Copa das Nações.' if G.copa['stage'] == 3 else '%s foi eliminada da Copa das Nações (' + FASES[G.copa['stage']] + ').') % G.T[c['nt']]['n'], 'mau')
    G.copa['teams'] = venc; G.copa['stage'] += 1
    if len(venc) == 1:
        T = G.T[venc[0]]; noticia('🏆 %s é campeã da Copa das Nações %d!' % (T['n'], G.season), 'bom')
        if venc[0] == c['nt']:
            c['rep'] = min(99, c['rep'] + 15); c['hist'].append(dict(s=G.season, t=T['n'], l='Copa das Nações', pos=1, pts='-', tit=True))
        nova_temporada()

def aposentar(p):
    T = G.T.get(p['club']); del G.P[p['id']]
    if not T: return
    T['pl'].remove(p['id']); cc = T['cc']
    nat = cc if R.random() < LOCAL.get(cc, .72) else R.choice([x[:2] for x in ESTRANG.split()])
    q = novo_jogador(p['pos'], R.gauss(T['str'] - 12, 4), nat, T['id'], age=R.randint(17, 19))
    q['pot'] = min(97, q['ovr'] + R.randint(8, 26)); valor(q); T['pl'].append(q['id'])
    if p['id'] in T['xi']: T['xi'][T['xi'].index(p['id'])] = q['id']

def nova_temporada():
    c = G.coach; G.season += 1; G.week = 0; G.ntdone = set(); G.ntopp = {}; G.phase = 'liga'; G.copa = None; aposentados = 0
    for p in list(G.P.values()):
        p['age'] += 1; a = p['age']
        if a <= 23: p['ovr'] = min(max(p['pot'], p['ovr']), p['ovr'] + R.randint(1, 5))
        elif a <= 29: p['ovr'] = min(max(p['pot'], p['ovr']), p['ovr'] + R.randint(-1, 2))
        elif a <= 32: p['ovr'] -= R.randint(0, 3); p['fis'] -= R.randint(0, 3)
        else: p['ovr'] -= R.randint(1, 5); p['fis'] -= R.randint(1, 4)
        p['ovr'] = max(35, min(95, p['ovr'])); p['fis'] = max(30, p['fis'])
        p['pot'] = p['ovr'] if a >= 30 else max(p['pot'], p['ovr'])
        p.update(gol=0, jg=0, ca=0, sus=0, cond=100)
        if a >= 38 or (a >= 34 and R.random() < .4): aposentar(p); aposentados += 1
        else: valor(p)
    for L in G.L: novo_calendario(L)
    for T in G.T.values():
        T['mor'] = 60
        if T['nac']:
            T['pl'] = [x for x in T['pl'] if x in G.P]
            if T['id'] != c['nt'] or len(T['pl']) < 16: convocar_auto(T)
        else:
            if T['id'] != c['club']: auto_xi(T)
            T['str'] = round(forca(T))
    if c['club']: c['conf'] = max(c['conf'], 50)
    noticia('Começa a temporada %d! %d jogadores se aposentaram e novas promessas surgiram.' % (G.season, aposentados))
    for _ in range(2): gerar_proposta()
    if c['rep'] >= 55 and not c['nt']: gerar_proposta(sel=True)

def proximo():
    c = G.coach
    if G.phase == 'copa':
        st = G.copa; nome = 'Copa das Nações · ' + FASES[st['stage']]
        if c['nt'] in st['teams']:
            i = st['teams'].index(c['nt']); j = i ^ 1
            return dict(tipo='copa', comp=nome, h=st['teams'][min(i, j)], a=st['teams'][max(i, j)])
        return dict(tipo='copa_sim', comp=nome)
    if c['nt'] and G.week in DATAS_FIFA and G.week not in G.ntdone and G.week < semanas_temporada():
        if G.week not in G.ntopp:
            ns = sorted(selecoes(), key=lambda T: -forca(T)); i = [T['id'] for T in ns].index(c['nt'])
            G.ntopp[G.week] = (R.choice([T['id'] for T in ns[max(0, i - 8): i + 9] if T['id'] != c['nt']]), R.random() < .5)
        adv, casa = G.ntopp[G.week]
        return dict(tipo='sel', comp='Amistoso internacional (Data FIFA)', h=c['nt'] if casa else adv, a=adv if casa else c['nt'])
    if c['club']:
        L = liga_usuario()
        if G.week < len(L['fx']):
            for h, a in L['fx'][G.week]:
                if c['club'] in (h, a): return dict(tipo='liga', comp='%s · Rodada %d' % (L['n'], G.week + 1), h=h, a=a)
    return dict(tipo='semana', comp='Semana %d (sem jogo seu)' % (G.week + 1))

# ------------------------------ JSON ---------------------------------
def jt(T):
    return dict(id=T['id'], n=T['n'], sig=T['sig'], cor=T['cor'], f=forca(T), fl=bandeira(T['cc']) if T['nac'] else '')

def jp(p):
    d = {k: p[k] for k in ('id', 'n', 'pos', 'age', 'nat', 'ovr', 'pot', 'fis', 'pe', 'hab', 'cond', 'inj', 'sus', 'val', 'sal', 'gol', 'jg')}
    d['fl'] = bandeira(p['nat']); d['cl'] = G.T[p['club']]['n'] if p['club'] in G.T else 'Sem clube'
    return d

def tabela_json(L, n=None):
    tb = L['tab']
    return [dict(t=jt(G.T[t]), d=tb[t]) for t in classificacao(L)[:n]]

def lado_usuario():
    L = G.live; m = L['ms'][L['u']]; S = m['s'][m['us']]; T = G.T[S['t']]
    f = lambda x, sl=None: dict(id=x, n=G.P[x]['n'], pos=G.P[x]['pos'], sl=sl, ovr=G.P[x]['ovr'], en=int(S['en'].get(x, 100)),
                                am=x in S['am'], les=G.P[x]['inj'] > 0, hab=G.P[x]['hab'])
    return dict(on=[f(x, sl) for x, sl in zip(S['on'], S['sl'])], bench=[f(x) for x in S['bench']], subs=S['subs'], form=T['form'], tac=T['tac'])

def snap():
    L = G.live; u = L['u']
    d = dict(live=True, tipo=L['tipo'], comp=L['comp'], min=L['min'], u=u, fim=L['fim'],
             ms=[dict(h=jt(G.T[m['t'][0]]), a=jt(G.T[m['t'][1]]), g=m['g'], pen=m['pen']) for m in L['ms']])
    if u is not None: d.update(us=L['ms'][u]['us'], ev=L['ms'][u]['ev'], lado=lado_usuario()); L['ne'] = len(L['ms'][u]['ev'])
    return d

def time_do(d):
    c = G.coach; tid = c['nt'] if d.get('t') == 'sel' else c['club']
    if not tid: raise ValueError('Você não comanda esse time no momento.')
    return G.T[tid]

def sl_de(T):
    if len(T['xi']) == 11: return slots(T['form'])
    T['xi'], sl = arrumar(T['xi'], T['form']); return sl

def tirar_do_xi(T, pid):
    if pid not in T['xi']: return
    i = T['xi'].index(pid); g = GRP[G.P[pid]['pos']]
    c = [y for y in T['pl'] if y != pid and y not in T['xi'] and disp(y, T['nac'])]
    if c: T['xi'][i] = max(c, key=lambda y: G.P[y]['ovr'] * (1.2 if GRP[G.P[y]['pos']] == g else 1))
    else: T['xi'].pop(i)

def sem_live():
    if G.live and not G.live['fim']: raise ValueError('Termine a partida em andamento primeiro.')

# ------------------------------ API ----------------------------------
API = {}
def acao(f): API[f.__name__[2:]] = f; return f

@acao
def a_meta(d):
    return dict(save=os.path.exists(SAVE),
                ligas=[dict(i=L['i'], n=L['n'], pais=PAISES[L['cc']][0], fl=bandeira(L['cc']),
                            clubs=[dict(id=t, n=G.T[t]['n'], f=G.T[t]['str'], sig=G.T[t]['sig'], cor=G.T[t]['cor']) for t in L['clubs']]) for L in G.L],
                sels=[dict(id=T['id'], n=T['n'], fl=bandeira(T['cc']), f=forca(T)) for T in sorted(selecoes(), key=lambda T: -forca(T))])

@acao
def a_novo(d):
    if G.coach: gerar_mundo()
    if d.get('clube') not in G.T: raise ValueError('Escolha um clube.')
    sel = d.get('sel') if d.get('sel') in G.T else None
    G.coach = dict(n=(d.get('nome') or 'Técnico').strip()[:30], rep=50, club=d['clube'], nt=sel, conf=60, v=0, e=0, d=0, hist=[], ofs=[])
    noticia('Bem-vindo, %s! Você é o novo técnico do %s%s.' % (G.coach['n'], G.T[d['clube']]['n'], (' e da seleção da ' + G.T[sel]['n']) if sel else ''), 'bom')
    return a_estado(d)

@acao
def a_estado(d):
    if not G or not G.coach: return dict(jogo=False)
    c = G.coach; T = G.T.get(c['club']) if c['club'] else None; pr = proximo()
    out = dict(jogo=True, live=bool(G.live and not G.live['fim']), temporada=G.season, semana=G.week + 1, total=semanas_temporada(), fase=G.phase,
               tecnico=dict(n=c['n'], rep=round(c['rep']), conf=round(c['conf']), v=c['v'], e=c['e'], d=c['d']),
               clube=jt(T) if T else None, sel=jt(G.T[c['nt']]) if c['nt'] else None, news=G.news[:14],
               prox=dict(tipo=pr['tipo'], comp=pr['comp'], h=jt(G.T[pr['h']]) if 'h' in pr else None, a=jt(G.T[pr['a']]) if 'a' in pr else None),
               ofs=[dict(i=i, t=jt(G.T[o['t']]), tipo=o['tipo'], liga=G.L[G.T[o['t']]['lg']]['n'] if o['tipo'] == 'clube' else 'Seleção nacional') for i, o in enumerate(c['ofs'])])
    if T:
        L = G.L[T['lg']]; tb = tabela_json(L); pos = [r['t']['id'] for r in tb].index(T['id'])
        for i, r in enumerate(tb): r['p'] = i + 1
        ini = max(0, min(pos - 2, len(tb) - 5))
        out.update(bud=T['bud'], folha=sum(G.P[x]['sal'] for x in T['pl']), rev=T['rev'], mor=T['mor'], liga=L['n'], lg=L['i'], pos=pos + 1, mini=tb[ini:ini + 5])
    return out

@acao
def a_elenco(d):
    T = time_do(d)
    if not (G.live and not G.live['fim']): validar_xi(T)
    sl = sl_de(T)
    return dict(t=jt(T), nac=T['nac'], form=T['form'], tac=T['tac'], xi=T['xi'], sl=sl, forms=list(FORMS), habs=HABS,
                pl=[jp(G.P[x]) for x in sorted(T['pl'], key=lambda x: (POSICOES.index(G.P[x]['pos']), -G.P[x]['ovr']))])

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

@acao
def a_tabela(d):
    lg = d.get('lg'); L = G.L[int(lg)] if lg not in (None, '') else (liga_usuario() or G.L[0])
    art = sorted([G.P[x] for t in L['clubs'] for x in G.T[t]['pl']], key=lambda p: -p['gol'])[:10]
    return dict(lg=L['i'], n=L['n'], fl=bandeira(L['cc']), rows=tabela_json(L), rod=min(G.week, len(L['fx'])), tot=len(L['fx']),
                art=[jp(p) for p in art if p['gol']], champ=[(s, G.T[t]['n']) for s, t in L['champ'][-5:]],
                ligas=[dict(i=x['i'], n=x['n'], fl=bandeira(x['cc']), pais=PAISES[x['cc']][0]) for x in G.L])

@acao
def a_mercado(d):
    c = G.coach; meu = c['club']; pos = d.get('pos') or ''; q = (d.get('q') or '').lower().strip()
    mx = int(d.get('max') or 10 ** 9); lg = d.get('lg')
    clubes = set(G.L[int(lg)]['clubs']) if lg not in (None, '') else None
    res = [p for p in G.P.values() if p['club'] != meu and p['club'] in G.T and (not pos or p['pos'] == pos)
           and int(p['val'] * 1.15) <= mx and (not q or q in p['n'].lower()) and (clubes is None or p['club'] in clubes)]
    res = sorted(res, key=lambda p: -p['ovr'])[:60]
    out = dict(lista=[dict(jp(p), preco=int(p['val'] * 1.15)) for p in res], bud=G.T[meu]['bud'] if meu else 0,
               ligas=[dict(i=x['i'], n=x['n'], fl=bandeira(x['cc'])) for x in G.L])
    if meu: out['meus'] = [dict(jp(G.P[x]), preco=int(G.P[x]['val'] * .9)) for x in sorted(G.T[meu]['pl'], key=lambda x: -G.P[x]['ovr'])]
    return out

@acao
def a_comprar(d):
    sem_live(); T = time_do({}); p = G.P[int(d['pid'])]; S = G.T[p['club']]; preco = int(p['val'] * 1.15)
    if S is T: raise ValueError('Esse jogador já é seu.')
    if len(S['pl']) <= 18: raise ValueError('O %s não quer vender: elenco curto.' % S['n'])
    if len(T['pl']) >= 35: raise ValueError('Seu elenco está cheio (máx. 35).')
    if T['bud'] < preco: raise ValueError('Dinheiro insuficiente.')
    S['pl'].remove(p['id']); tirar_do_xi(S, p['id']); T['pl'].append(p['id']); p['club'] = T['id']; p['sus'] = 0
    T['bud'] -= preco; S['bud'] += preco
    noticia('Contratação: %s (%s) chega do %s.' % (p['n'], p['pos'], S['n']), 'bom')
    return dict(a_mercado(d), msg='%s contratado!' % p['n'])

@acao
def a_vender(d):
    sem_live(); T = time_do({}); pid = int(d['pid']); p = G.P[pid]
    if pid not in T['pl']: raise ValueError('Jogador não é do seu clube.')
    if len(T['pl']) <= 16: raise ValueError('Elenco mínimo de 16 jogadores.')
    cand = [C for C in G.T.values() if not C['nac'] and C is not T and abs(C['str'] - p['ovr']) <= 6 and len(C['pl']) < 32] or \
           [C for C in G.T.values() if not C['nac'] and C is not T and len(C['pl']) < 32]
    C = R.choice(cand); preco = int(p['val'] * R.uniform(.85, 1.0))
    tirar_do_xi(T, pid); T['pl'].remove(pid); C['pl'].append(pid); p['club'] = C['id']; T['bud'] += preco
    noticia('%s foi vendido ao %s.' % (p['n'], C['n']))
    return dict(a_mercado(d), msg='%s vendido ao %s por € %s mil' % (p['n'], C['n'], format(preco, ',d').replace(',', '.')))

@acao
def a_elegiveis(d):
    T = time_do({'t': 'sel'})
    el = sorted([p for p in G.P.values() if p['nat'] == T['cc']], key=lambda p: -p['ovr'])[:90]
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
    return dict(lista=[jt(T) for T in sorted(selecoes(), key=lambda T: -forca(T))][:40])

@acao
def a_carreira(d):
    c = G.coach
    return dict(hist=c['hist'][::-1], rep=round(c['rep']), v=c['v'], e=c['e'], d=c['d'], n=c['n'], save=os.path.exists(SAVE))

@acao
def a_aceitar(d):
    sem_live(); c = G.coach; o = c['ofs'].pop(int(d['i'])); T = G.T[o['t']]
    if o['tipo'] == 'clube':
        if c['club']: noticia('Você deixou o %s.' % G.T[c['club']]['n'])
        c['club'] = T['id']; c['conf'] = 60; auto_xi(T)
        if G.week >= semanas_temporada() and G.phase == 'liga': fim_liga()
    else:
        c['nt'] = T['id']; convocar_auto(T)
    noticia('Você assinou com %s!' % T['n'], 'bom')
    return a_estado(d)

@acao
def a_demitir(d):
    sem_live(); c = G.coach
    if d.get('t') == 'sel' and c['nt']: noticia('Você deixou a seleção da %s.' % G.T[c['nt']]['n']); c['nt'] = None
    elif c['club']: noticia('Você pediu demissão do %s.' % G.T[c['club']]['n']); c['club'] = None; c['rep'] = max(1, c['rep'] - 3)
    return a_estado(d)

@acao
def a_jogar(d):
    if G.live and not G.live['fim']: return snap()
    pr = proximo(); G.live = None
    if pr['tipo'] == 'liga':
        iniciar('liga', liga_usuario()['fx'][G.week], pr['comp'])
    elif pr['tipo'] == 'sel':
        iniciar('sel', [(pr['h'], pr['a'])], pr['comp'])
    elif pr['tipo'] == 'copa':
        t = G.copa['teams']; iniciar('copa', list(zip(t[0::2], t[1::2])), pr['comp'], ko=True, neutro=True)
    elif pr['tipo'] == 'copa_sim':
        simular_copa(); return dict(live=False, msg='Copa das Nações simulada. Nova temporada começou!')
    else:
        fim_semana(); return dict(live=False, msg='Semana simulada.')
    return snap()

@acao
def a_passo(d):
    if not G.live: raise ValueError('Nenhuma partida em andamento.')
    fr = passo(int(d.get('n', 4))); L = G.live; out = dict(frames=fr, fim=L['fim'], min=L['min'])
    if L['fim']:
        out['final'] = [dict(h=jt(G.T[m['t'][0]]), a=jt(G.T[m['t'][1]]), g=m['g'], pen=m['pen'], w=m['w']) for m in L['ms']]
        if L['u'] is not None: out['res'] = resultado_usuario(L['ms'][L['u']])
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
    return dict(lado=lado_usuario())

@acao
def a_tatica(d):
    L, m, s, S = lado_live(); T = G.T[S['t']]
    if d.get('form') in FORMS and d['form'] != T['form']:
        T['form'] = d['form']; S['on'], S['sl'] = arrumar(S['on'], T['form'])
        if len(T['xi']) == 11: T['xi'] = arrumar(T['xi'], T['form'])[0]
        ev(m, L['min'], s, 'tat', 'Nova formação: ' + T['form'])
    if d.get('tac') in TATICAS and d['tac'] != T['tac']:
        T['tac'] = d['tac']; ev(m, L['min'], s, 'tat', 'Postura: ' + {'D': 'Defensiva', 'E': 'Equilibrada', 'O': 'Ofensiva'}[d['tac']])
    return dict(lado=lado_usuario())

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

# ------------------ IMPORTAR ELENCOS REAIS (CSV) ---------------------
IMPORTADOS = []
def importar_csv(caminho):
    """Substitui os elencos dos clubes citados. CSV separado por ';' com cabeçalho:
    clube;nome;posicao;idade;nacionalidade;forca;fisico;potencial;pe;habilidades
    ex.: Flamengo;Fulano da Silva;ATA;27;BR;80;75;82;E;FIN DRI
    posicao: GOL ZAG LAT VOL MEI ATA | pe: D/E/A | habilidades: códigos de HABS separados por espaço"""
    if caminho not in IMPORTADOS: IMPORTADOS.append(caminho)
    por_nome = {T['n'].lower(): T for T in G.T.values() if not T['nac']}; novos = {}
    with open(caminho, encoding='utf-8-sig') as f:
        for r in csv.reader(f, delimiter=';'):
            if len(r) < 9 or r[0].strip().lower() in ('clube', '') or r[0].startswith('#'): continue
            T = por_nome.get(r[0].strip().lower())
            if not T: print('Clube não encontrado:', r[0]); continue
            if T['id'] not in novos:
                for x in T['pl']: G.P.pop(x, None)
                T['pl'] = []; T['xi'] = []; novos[T['id']] = T
            pos = r[2].strip().upper(); nat = r[4].strip().upper()
            p = novo_jogador(pos if pos in GRP else 'MEI', int(r[5]), nat if nat in PAISES else T['cc'], T['id'], int(r[3]))
            p.update(n=r[1].strip(), fis=int(r[6]), pot=max(int(r[7]), p['ovr']), pe=(r[8].strip().upper() or 'D')[0],
                     hab=[h for h in (r[9] if len(r) > 9 else '').upper().split() if h in HABS]); valor(p)
            T['pl'].append(p['id'])
    for T in novos.values(): auto_xi(T)
    for T in selecoes(): convocar_auto(T)
    print(len(novos), 'clube(s) atualizado(s) a partir de', caminho)

# --------------------------- INTERFACE -------------------------------
HTML = r'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#ffffff">
<title>Prancheta FC</title><style>
:root{--bg:#f3f5f9;--card:#fff;--ink:#162033;--mut:#667085;--line:#e4e8ef;--pri:#0e9f6e;--pri2:#e7f7f0;--blue:#2563eb;--red:#e5484d;--yel:#f5b301;--sh:0 1px 2px rgba(16,24,40,.05),0 4px 14px rgba(16,24,40,.06)}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}
#app{display:grid;grid-template-columns:220px minmax(0,1fr);min-height:100vh}
nav{background:#fff;border-right:1px solid var(--line);padding:18px 12px;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;gap:4px}
.brand{display:flex;align-items:center;gap:10px;font-size:17px;padding:4px 10px 18px}
.logo{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#34d399,#0e9f6e);color:#fff;display:grid;place-items:center;font-weight:800;flex:none}
.logo.xl{width:64px;height:64px;font-size:30px;border-radius:18px;margin:0 auto 12px}
nav button{display:flex;align-items:center;gap:12px;border:0;background:none;padding:11px 12px;border-radius:10px;color:var(--mut);cursor:pointer;font-weight:600;text-align:left}
nav button svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}
nav button:hover{background:#f6f8fb}nav button.on{background:var(--pri2);color:var(--pri)}
.nogame nav{display:none}.nogame #app{grid-template-columns:1fr}
main{min-width:0;padding:0 24px 40px;max-width:1280px;width:100%;margin:0 auto}
header{display:flex;align-items:center;gap:14px;padding:16px 0;flex-wrap:wrap}
.who{display:flex;align-items:center;gap:12px;min-width:0}.who b{display:block;font-size:17px}.who small,small{color:var(--mut);font-size:12px}
.sp{flex:1}.kpi{background:#fff;border:1px solid var(--line);border-radius:12px;padding:7px 14px;display:flex;flex-direction:column}.kpi small{font-size:11px}.kpi b{white-space:nowrap}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(310px,1fr));align-items:start}
.two{display:grid;gap:16px;grid-template-columns:minmax(280px,420px) minmax(0,1fr);align-items:start}.two.w{grid-template-columns:minmax(0,1.4fr) minmax(0,1fr)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:var(--sh);padding:18px;margin-bottom:16px;min-width:0}
.grid>.card,.two>.card,.two>div{margin-bottom:0}
h3{font-size:12px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);margin-bottom:12px}
.btn{border:0;background:var(--pri);color:#fff;font-weight:700;padding:10px 16px;border-radius:10px;cursor:pointer;transition:filter .15s}
.btn:hover{filter:brightness(1.06)}.btn.sec{background:#eef1f6;color:var(--ink)}.btn.red{background:#fdecec;color:var(--red)}.btn.big{font-size:16px;padding:14px 22px;width:100%}
.bdg{display:inline-grid;place-items:center;width:30px;height:30px;border-radius:50%;font-size:10px;font-weight:800;flex:none;box-shadow:inset 0 0 0 1.5px rgba(0,0,0,.1);letter-spacing:-.3px}
.bdg.lg{width:58px;height:58px;font-size:16px}
.ov{display:inline-block;min-width:32px;text-align:center;padding:3px 6px;border-radius:7px;font-weight:800;font-size:12px}
.o1{background:#f1f3f6;color:#667085}.o2{background:#fff4d6;color:#a16207}.o3{background:#e0f2fe;color:#0369a1}.o4{background:#dcfce7;color:#15803d}.o5{background:#ede9fe;color:#6d28d9}
.chip{display:inline-block;padding:2px 7px;border-radius:20px;background:#f1f4f8;color:#475467;font-size:11px;font-weight:600;margin:1px 2px 1px 0;white-space:nowrap}
.pos{display:inline-block;width:36px;text-align:center;font-size:10.5px;font-weight:800;padding:3px 0;border-radius:6px;background:#eef1f6;color:#475467}
.pos.G{background:#fff4d6;color:#a16207}.pos.D{background:#e0f2fe;color:#0369a1}.pos.M{background:#dcfce7;color:#15803d}.pos.A{background:#fde8e8;color:#c0262d}
.tw{overflow-x:auto}table{width:100%;border-collapse:collapse}
th{font-size:11px;color:var(--mut);text-align:left;font-weight:700;padding:8px 6px;border-bottom:1px solid var(--line);white-space:nowrap}
td{padding:8px 6px;border-bottom:1px solid #f0f2f6;vertical-align:middle}
tr.me td{background:var(--pri2);font-weight:700}tbody tr,.click tr{cursor:pointer}
tr.tit td:first-child{box-shadow:inset 3px 0 0 var(--pri)}tr.pk td{background:#fff8e1}
.sec-t td{background:#f8fafc;font-size:11px;font-weight:800;color:var(--mut);text-transform:uppercase;letter-spacing:.06em;cursor:default}
.bar{height:6px;background:#eef1f6;border-radius:9px;overflow:hidden;min-width:40px}.bar i{display:block;height:100%;background:var(--pri);transition:width .2s}
select,input{padding:9px 11px;border:1px solid var(--line);border-radius:10px;background:#fff;max-width:100%}
.seg{display:inline-flex;background:#eef1f6;border-radius:10px;padding:3px;flex-wrap:wrap}.seg button{border:0;background:none;padding:7px 12px;border-radius:8px;font-weight:600;color:var(--mut);cursor:pointer}.seg button.on{background:#fff;color:var(--ink);box-shadow:var(--sh)}
.tools{display:flex;gap:10px;align-items:center;flex-wrap:wrap}.mut{color:var(--mut)}.red{color:var(--red)}.hint{font-size:12px}
.hero{text-align:center;padding:36px 10px 22px}.hero h1{font-size:30px}.hero p{color:var(--mut);max-width:520px;margin:8px auto 0}
.form{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}.form label{display:flex;flex-direction:column;gap:6px;font-weight:600;font-size:13px}
.clubs{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));max-height:420px;overflow:auto;padding:2px}
.club{display:flex;align-items:center;gap:10px;border:1px solid var(--line);background:#fff;border-radius:12px;padding:9px 10px;cursor:pointer;text-align:left}.club span{flex:1;font-weight:600}.club.on{border-color:var(--pri);box-shadow:0 0 0 3px var(--pri2)}
.row{display:flex;gap:10px;flex-wrap:wrap}.row>*{flex:1}
.vs{display:flex;align-items:center;justify-content:space-around;margin:14px 0 18px}.vs .x{color:var(--mut);font-size:18px}
.tm{display:flex;flex-direction:column;align-items:center;gap:7px;font-weight:700;text-align:center;min-width:0}
.comp{color:var(--pri);font-weight:700;font-size:13px}
.kv{display:grid;grid-template-columns:1fr auto;gap:8px 12px;align-items:center}.kv span{color:var(--mut)}
.nw{padding:9px 0;border-bottom:1px solid #f0f2f6;font-size:13px}.nw small{display:block}.nw.bom{color:#0b7a55}.nw.mau{color:#b42318}
.ofr{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid #f0f2f6}.ofr div{flex:1;min-width:0}.ofr small{display:block}
.pitch{position:relative;aspect-ratio:68/100;width:100%;max-width:420px;margin:auto;border-radius:16px;background:repeating-linear-gradient(0deg,#61bd7d 0 10%,#58b474 10% 20%);border:3px solid #fff;box-shadow:var(--sh);overflow:hidden}
.pitch:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px solid rgba(255,255,255,.75)}
.pitch:after{content:"";position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;border:2px solid rgba(255,255,255,.75);border-radius:50%;transform:translate(-50%,-50%)}
.area{position:absolute;left:24%;right:24%;height:14%;border:2px solid rgba(255,255,255,.75)}.area.t{top:-2px}.area.b{bottom:-2px}
.pp{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;z-index:2;width:80px}
.pp .c{width:38px;height:38px;border-radius:50%;background:#fff;display:grid;place-items:center;font-weight:800;font-size:13px;box-shadow:0 2px 6px rgba(0,0,0,.18);border:3px solid var(--kit)}
.pp .nm{font-size:10.5px;font-weight:700;color:#fff;background:rgba(8,40,24,.5);padding:1px 6px;border-radius:6px;white-space:nowrap;max-width:80px;overflow:hidden;text-overflow:ellipsis}
.pp .ps{font-size:9px;color:#fff;font-weight:800}.pp.sel .c{outline:3px solid var(--yel);outline-offset:2px}.pp.bad .c{background:#fff4d6}
.score{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;text-align:center;margin:14px 0}
.pl{font-size:46px;font-weight:800;letter-spacing:2px;font-variant-numeric:tabular-nums;line-height:1.1}
.min{display:inline-block;background:var(--pri2);color:var(--pri);font-weight:800;padding:3px 12px;border-radius:20px;margin-top:4px}
.prog{height:5px;margin:6px 0 14px}.ctl{display:flex;gap:10px}.ctl .btn{flex:1}
.feed{max-height:420px;overflow:auto}.feed div{padding:8px 2px;border-bottom:1px solid #f0f2f6;display:flex;gap:10px;align-items:center;font-size:13px}
.feed .gol{font-weight:800;color:#0b7a55}.dot{width:9px;height:9px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}
.og{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;padding:7px 0;border-bottom:1px solid #f0f2f6;font-size:12.5px}.og span:first-child{text-align:right}.og b{background:#f3f5f9;padding:2px 9px;border-radius:7px;font-variant-numeric:tabular-nums}.og.hit b{background:var(--pri);color:#fff}
.flash{animation:fl .9s}@keyframes fl{0%{transform:scale(1.3);color:var(--pri)}100%{transform:none}}
.pr{display:flex;align-items:center;gap:8px;padding:8px;border:1px solid var(--line);border-radius:10px;margin-bottom:6px;cursor:pointer;background:#fff}.pr.pk{border-color:var(--yel);background:#fff8e1}.pr b{font-size:13px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.end{text-align:center}.end h2{font-size:28px;margin-bottom:6px}.end.V h2{color:var(--pri)}.end.D h2{color:var(--red)}.end p{margin-bottom:14px;font-weight:600}
#toast{position:fixed;left:50%;bottom:24px;transform:translate(-50%,40px);opacity:0;background:#162033;color:#fff;padding:11px 18px;border-radius:12px;font-weight:600;transition:.25s;z-index:50;max-width:90vw;text-align:center;pointer-events:none}
#toast.show{opacity:1;transform:translate(-50%,0)}#toast.bad{background:var(--red)}
.mob{display:none;font-size:11.5px;color:var(--mut);margin-top:2px}
.modal{position:fixed;inset:0;background:rgba(22,32,51,.35);display:grid;place-items:center;z-index:60;padding:16px}.modal .card{max-width:380px;width:100%;margin:0}.modal p{margin-bottom:16px;font-weight:600;font-size:15px}
@media(max-width:860px){
 #app{grid-template-columns:1fr}
 nav{position:fixed;bottom:0;left:0;right:0;top:auto;height:auto;flex-direction:row;padding:5px 4px calc(5px + env(safe-area-inset-bottom));border-right:0;border-top:1px solid var(--line);z-index:20;gap:0}
 .brand{display:none}nav button{flex:1;flex-direction:column;gap:3px;font-size:10.5px;padding:6px 2px;align-items:center}
 main{padding:0 12px 92px}.two,.two.w{grid-template-columns:1fr}.hm{display:none}.mob{display:block}.grid{grid-template-columns:1fr}
 .pl{font-size:38px}.bdg.lg{width:48px;height:48px}.card{padding:14px}header{padding:12px 0}.kpi{padding:5px 10px}
}
</style></head><body class="nogame"><div id="app"><nav id="nav"></nav><main><header id="top"></header><section id="view"><div class="hero"><div class="logo xl">P</div><h1>Prancheta FC</h1><p>Carregando o mundo do futebol...</p></div></section></main></div><div id="toast"></div>
<script>
const $=s=>document.querySelector(s),V=$('#view');
const S={v:'inicio',st:null,meta:null,sel:null,t:'clube',el:null,pk:null,lg:null,mk:'comprar',mf:{pos:'',q:'',max:'',lg:''}};
const GRP={GOL:'G',ZAG:'D',LAT:'D',VOL:'M',MEI:'M',ATA:'A'},PE={D:'Destro',E:'Canhoto',A:'Ambidestro'};
const HB={FIN:'Finalização',CAB:'Cabeceio',DRI:'Drible',PAS:'Passe',VEL:'Velocidade',DES:'Desarme',MAR:'Marcação',CHL:'Chute de longe',BOL:'Bola parada',PEN:'Pênaltis',LID:'Liderança',REF:'Reflexos',SAI:'Saída do gol',RES:'Resistência',CRU:'Cruzamento'};
const FORMS=['4-4-2','4-3-3','4-2-3-1','3-5-2','5-3-2','3-4-3','4-5-1'],TAC=[['D','Defensiva'],['E','Equilibrada'],['O','Ofensiva']];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>'&#'+c.charCodeAt(0)+';');
function api(a,b){return fetch('api/'+a,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(b||{})}).then(r=>r.json()).then(j=>{if(j.erro){toast(j.erro,1);throw new Error(j.erro)}if(j.msg)toast(j.msg);return j})}
function ask(m){return new Promise(r=>{const d=document.createElement('div');d.className='modal';d.innerHTML=`<div class="card"><p>${esc(m)}</p><div class="row"><button class="btn sec">Cancelar</button><button class="btn">Confirmar</button></div></div>`;document.body.appendChild(d);d.querySelectorAll('button').forEach((x,i)=>x.onclick=()=>{d.remove();r(i==1)})})}
function toast(m,bad){const t=$('#toast');t.textContent=m;t.className='show'+(bad?' bad':'');clearTimeout(t._t);t._t=setTimeout(()=>t.className='',2800)}
const mo=k=>(k<0?'-':'')+(Math.abs(k)>=1000?'€ '+(Math.abs(k)/1000).toLocaleString('pt-BR',{maximumFractionDigits:1})+' mi':'€ '+Math.abs(k)+' mil');
const bdg=(t,c='')=>`<span class="bdg ${c}" style="background:${t.cor[0]};color:${t.cor[1]}">${t.fl||esc(t.sig)}</span>`;
const ov=v=>`<span class="ov ${v>=85?'o5':v>=78?'o4':v>=70?'o3':v>=60?'o2':'o1'}">${Math.round(v)}</span>`;
const bar=(v,c)=>`<div class="bar"><i style="width:${Math.max(0,Math.min(100,v))}%;background:${c||(v>66?'var(--pri)':v>40?'var(--yel)':'var(--red)')}"></i></div>`;
const habs=h=>h.map(x=>`<span class="chip">${HB[x]}</span>`).join('');
const tm=t=>`<div class="tm">${bdg(t,'lg')}<span>${esc(t.n)}</span>${ov(t.f)}</div>`;
const tacs=(cur,fn)=>TAC.map(([k,l])=>`<button class="${cur==k?'on':''}" onclick="${fn}({tac:'${k}'})">${l}</button>`).join('');
const fsel=(cur,fn)=>`<select onchange="${fn}({form:this.value})">${FORMS.map(f=>`<option ${f==cur?'selected':''}>${f}</option>`).join('')}</select>`;
const vazio=m=>`<div class="card"><p class="mut">${m}</p></div>`;
const IC={inicio:'<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',elenco:'<circle cx="9" cy="8" r="3.5"/><path d="M2 20c0-3.5 3-6 7-6s7 2.5 7 6M16 4.5a3.5 3.5 0 0 1 0 7M18 14c2.5.6 4 2.8 4 6"/>',tabela:'<path d="M4 6h16M4 12h16M4 18h16"/>',mercado:'<path d="M4 8h14l-3-3M20 16H6l3 3"/>',selecao:'<path d="M5 21V4h11l-2 4 2 4H5"/>',carreira:'<rect x="3" y="7" width="18" height="13" rx="2"/><path d="M9 7V5h6v2M3 13h18"/>'};
const NAV=[['inicio','Início'],['elenco','Elenco'],['tabela','Tabela'],['mercado','Mercado'],['selecao','Seleção'],['carreira','Carreira']];
function nav(){$('#nav').innerHTML='<div class="brand"><span class="logo">P</span><b>Prancheta FC</b></div>'+NAV.map(([k,l])=>`<button class="${S.v==k?'on':''}" onclick="go('${k}')"><svg viewBox="0 0 24 24">${IC[k]}</svg><span>${l}</span></button>`).join('')}
async function refresh(){S.st=await api('estado');head()}
function head(){const s=S.st,c=s.clube;$('#top').innerHTML=`<div class="who">${c?bdg(c):(s.sel?bdg(s.sel):'')}<div><b>${c?esc(c.n):'Sem clube'}</b><small>${esc(s.tecnico.n)} · ${s.temporada} · ${s.fase=='copa'?'Copa das Nações':'Semana '+Math.min(s.semana,s.total)+'/'+s.total}</small></div></div><div class="sp"></div>${c?`<div class="kpi"><small>Caixa</small><b>${mo(s.bud)}</b></div>`:''}${s.sel?`<div class="kpi"><small>Seleção</small><b>${s.sel.fl} ${esc(s.sel.n)}</b></div>`:''}`}
const R={};
async function go(v){if(LV&&!LV.done){toast('Partida em andamento!',1);return}S.v=v;nav();scrollTo(0,0);await R[v]()}
async function boot(){S.st=await api('estado');if(!S.st.jogo){S.meta=await api('meta');return novo()}document.body.classList.remove('nogame');head();if(S.st.live)return startLive(await api('snap'));go('inicio')}
/* ---------- novo jogo ---------- */
function novo(){document.body.classList.add('nogame');$('#top').innerHTML='';const m=S.meta;S.sel=null;
V.innerHTML=`<div class="hero"><div class="logo xl">P</div><h1>Prancheta FC</h1><p>Assuma um clube (e, se quiser, uma seleção), monte o time, mexa durante as partidas e construa sua carreira de técnico.</p></div>
<div class="card"><div class="form"><label>Seu nome<input id="nm" value="Professor" maxlength="30"></label>
<label>Liga<select id="lg" onchange="clubesNovo()">${m.ligas.map(l=>`<option value="${l.i}">${l.fl} ${esc(l.pais)} — ${esc(l.n)}</option>`).join('')}</select></label>
<label>Seleção (opcional)<select id="ns"><option value="">Nenhuma</option>${m.sels.map(x=>`<option value="${x.id}">${x.fl} ${esc(x.n)} (${Math.round(x.f)})</option>`).join('')}</select></label></div>
<h3 style="margin:18px 0 10px">Escolha seu clube</h3><div id="cls" class="clubs"></div>
<div class="row" style="margin-top:18px"><button class="btn big" onclick="comecar()">Começar carreira ▶</button>${m.save?'<button class="btn sec big" onclick="carregar()">Carregar jogo salvo</button>':''}</div></div>`;clubesNovo()}
function clubesNovo(){const l=S.meta.ligas[$('#lg').value];$('#cls').innerHTML=l.clubs.map(c=>`<button class="club ${S.sel==c.id?'on':''}" onclick="S.sel='${c.id}';clubesNovo()">${bdg(c)}<span>${esc(c.n)}</span>${ov(c.f)}</button>`).join('')}
async function comecar(){if(!S.sel)return toast('Escolha um clube',1);S.st=await api('novo',{nome:$('#nm').value,clube:S.sel,sel:$('#ns').value});document.body.classList.remove('nogame');head();go('inicio')}
async function carregar(){S.st=await api('carregar');document.body.classList.remove('nogame');LV=null;head();go('inicio')}
async function novoJogo(){if(!await ask('Começar um novo jogo? O progresso não salvo será perdido.'))return;S.meta=await api('meta');novo()}
/* ---------- inicio ---------- */
function mini(rows,me){return `<table>${rows.map(r=>`<tr class="${r.t.id==me?'me':''}"><td>${r.p}</td><td>${bdg(r.t)}</td><td style="width:100%">${esc(r.t.n)}</td><td>${r.d[0]}J</td><td><b>${r.d[6]}</b></td></tr>`).join('')}</table>`}
R.inicio=async()=>{await refresh();const s=S.st,p=s.prox,c=s.clube;
V.innerHTML=`<div class="grid"><div class="card"><h3>Próximo compromisso</h3><div class="comp">${esc(p.comp)}</div>
${p.h?`<div class="vs">${tm(p.h)}<b class="x">x</b>${tm(p.a)}</div>`:`<p class="mut" style="margin:14px 0">${p.tipo=='copa_sim'?'Sua seleção não disputa esta fase. Simule a Copa para iniciar a nova temporada.':'Você não tem jogo nesta semana.'}</p>`}
<button class="btn big" onclick="jogar()">${p.h?'▶ Jogar (ultra rápido)':'⏩ Avançar'}</button></div>
${c?`<div class="card"><h3>${esc(s.liga)} · ${s.pos}º lugar</h3>${mini(s.mini,c.id)}<button class="btn sec" style="margin-top:12px;width:100%" onclick="go('tabela')">Ver tabela completa</button></div>
<div class="card"><h3>Clube</h3><div class="kv"><span>Força do time</span>${ov(c.f)}<span>Caixa</span><b>${mo(s.bud)}</b><span>Receita semanal</span><b>${mo(s.rev)}</b><span>Folha semanal</span><b>${mo(s.folha)}</b><span>Moral do elenco</span>${bar(s.mor)}<span>Confiança da diretoria</span>${bar(s.tecnico.conf)}</div></div>`:''}
<div class="card"><h3>Técnico</h3><div class="kv"><span>Nome</span><b>${esc(s.tecnico.n)}</b><span>Reputação (${s.tecnico.rep})</span>${bar(s.tecnico.rep,'var(--blue)')}<span>Campanha</span><b>${s.tecnico.v}V ${s.tecnico.e}E ${s.tecnico.d}D</b></div></div>
${s.ofs.length?`<div class="card"><h3>Propostas</h3>${ofertas(s.ofs)}</div>`:''}
<div class="card"><h3>Notícias</h3>${s.news.map(n=>`<div class="nw ${n.k}"><small>${n.s} · semana ${n.w}</small>${esc(n.x)}</div>`).join('')}</div></div>`}
const ofertas=o=>o.map(o=>`<div class="ofr">${bdg(o.t)}<div><b>${esc(o.t.n)}</b><small>${esc(o.liga)} · força ${Math.round(o.t.f)}</small></div><button class="btn" onclick="aceitar(${o.i})">Aceitar</button></div>`).join('');
async function aceitar(i){if(!await ask('Aceitar esta proposta?'))return;await api('aceitar',{i});go('inicio')}
/* ---------- elenco ---------- */
R.elenco=async()=>{await refresh();const s=S.st;if(!s.clube&&!s.sel){V.innerHTML=vazio('Você está sem time. Veja as propostas em Carreira.');return}
if(S.t=='clube'&&!s.clube)S.t='sel';if(S.t=='sel'&&!s.sel)S.t='clube';S.el=await api('elenco',{t:S.t});S.pk=null;drawEl()}
function coords(sl){const r={G:[],D:[],M:[],A:[]},o=[];sl.forEach((s,i)=>r[s].push(i));
for(const g of 'GDMA'){const ids=r[g],n=ids.length;if(g=='M'&&n>=5){ids.slice(0,2).forEach((k,j)=>o[k]=[(j+1)*100/3,60]);const a=ids.slice(2);a.forEach((k,j)=>o[k]=[(j+1)*100/(a.length+1),39])}
else ids.forEach((k,j)=>o[k]=[(j+1)*100/(n+1),{G:91,D:73,M:49,A:19}[g]])}return o}
function drawEl(){const e=S.el,P={},s=S.st;e.pl.forEach(p=>P[p.id]=p);const c=coords(e.sl),res=e.pl.filter(p=>!e.xi.includes(p.id));
V.innerHTML=`<div class="card tools">${s.clube&&s.sel?`<div class="seg">${[['clube','Clube'],['sel','Seleção']].map(([k,l])=>`<button class="${S.t==k?'on':''}" onclick="S.t='${k}';R.elenco()">${l}</button>`).join('')}</div>`:''}
${fsel(e.form,'escl')}<div class="seg">${tacs(e.tac,'escl')}</div><button class="btn sec" onclick="autoEl()">Escalar automático</button><span class="mut hint">Toque em dois jogadores (campo ou lista) para trocá-los.</span></div>
<div class="two"><div><div class="pitch" style="--kit:${e.t.cor[0]}"><div class="area t"></div><div class="area b"></div>${e.xi.map((id,i)=>{const p=P[id],bad=GRP[p.pos]!=e.sl[i];return `<div class="pp ${S.pk==id?'sel':''} ${bad?'bad':''}" style="left:${c[i][0]}%;top:${c[i][1]}%" onclick="pick(${id})"><div class="c">${p.ovr}</div><div class="nm">${esc(p.n)}</div><div class="ps">${p.pos}${bad?' ⚠':''}</div></div>`}).join('')}</div>
<p class="mut hint" style="text-align:center;margin-top:8px">Força do time: <b>${Math.round(e.t.f)}</b> · ⚠ = fora de posição</p></div>
<div class="card tw"><table><tr><th>Pos</th><th>Jogador</th><th>Força</th><th class="hm">Físico</th><th class="hm">Potencial</th><th class="hm">Pé</th><th class="hm">Habilidades</th><th>Cond.</th></tr>
<tr class="sec-t"><td colspan="8">Titulares</td></tr>${e.xi.map(id=>linhaJ(P[id],1)).join('')}<tr class="sec-t"><td colspan="8">Reservas</td></tr>${res.map(p=>linhaJ(p,0)).join('')}</table></div></div>`}
function linhaJ(p,t){return `<tr class="${t?'tit':''} ${S.pk==p.id?'pk':''}" onclick="pick(${p.id})"><td><span class="pos ${GRP[p.pos]}">${p.pos}</span></td><td><b>${esc(p.n)}</b> <small>${p.fl} ${p.age} anos${p.gol?' · '+p.gol+' gols':''}${p.inj?' · <span class="red">lesão ('+p.inj+' sem.)</span>':''}${p.sus?' · <span class="red">suspenso</span>':''}</small><div class="mob">Físico ${p.fis} · Pot. ${p.pot} · ${PE[p.pe]} ${habs(p.hab)}</div></td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td class="hm">${PE[p.pe]}</td><td class="hm">${habs(p.hab)}</td><td style="min-width:56px">${bar(p.cond)}</td></tr>`}
async function pick(id){if(S.pk==null){S.pk=id;return drawEl()}if(S.pk==id){S.pk=null;return drawEl()}const a=S.pk;S.pk=null;S.el=await api('trocar',{t:S.t,a,b:id}).catch(()=>S.el);drawEl()}
async function escl(o){S.el=await api('escalar',{t:S.t,...o});drawEl()}
async function autoEl(){S.el=await api('auto',{t:S.t});drawEl();toast('Time escalado automaticamente')}
/* ---------- tabela ---------- */
R.tabela=async(lg)=>{const d=await api('tabela',{lg:lg??S.lg});S.lg=d.lg;const me=S.st.clube?.id;
V.innerHTML=`<div class="card tools"><select onchange="R.tabela(+this.value)">${d.ligas.map(l=>`<option value="${l.i}" ${l.i==d.lg?'selected':''}>${l.fl} ${esc(l.pais)} — ${esc(l.n)}</option>`).join('')}</select><span class="mut">Rodada ${d.rod} de ${d.tot}</span></div>
<div class="two w"><div class="card tw"><table><tr><th>#</th><th></th><th style="width:100%">Clube</th><th>P</th><th>J</th><th>V</th><th class="hm">E</th><th class="hm">D</th><th class="hm">GP</th><th class="hm">GC</th><th>SG</th></tr>
${d.rows.map((r,i)=>`<tr class="${r.t.id==me?'me':''}"><td>${i+1}</td><td>${bdg(r.t)}</td><td>${esc(r.t.n)}</td><td><b>${r.d[6]}</b></td><td>${r.d[0]}</td><td>${r.d[1]}</td><td class="hm">${r.d[2]}</td><td class="hm">${r.d[3]}</td><td class="hm">${r.d[4]}</td><td class="hm">${r.d[5]}</td><td>${r.d[4]-r.d[5]}</td></tr>`).join('')}</table></div>
<div><div class="card"><h3>Artilharia</h3>${d.art.length?`<table>${d.art.map((p,i)=>`<tr><td>${i+1}</td><td><b>${esc(p.n)}</b><br><small>${esc(p.cl)}</small></td><td><b>${p.gol}</b></td></tr>`).join('')}</table>`:'<p class="mut">Nenhum gol ainda.</p>'}</div>
${d.champ.length?`<div class="card"><h3>Campeões</h3>${d.champ.map(c=>`<div class="nw">${c[0]} — <b>${esc(c[1])}</b></div>`).join('')}</div>`:''}</div></div>`};
/* ---------- mercado ---------- */
R.mercado=async()=>{await refresh();if(!S.st.clube){V.innerHTML=vazio('Você precisa estar num clube para negociar jogadores.');return}
const f=S.mf,d=await api('mercado',f),cmp=S.mk=='comprar',L=cmp?d.lista:d.meus;
V.innerHTML=`<div class="card tools"><div class="seg"><button class="${cmp?'on':''}" onclick="S.mk='comprar';R.mercado()">Comprar</button><button class="${cmp?'':'on'}" onclick="S.mk='vender';R.mercado()">Vender</button></div><div class="sp"></div><div class="kpi"><small>Caixa</small><b>${mo(d.bud)}</b></div></div>
${cmp?`<div class="card tools"><select id="fp"><option value="">Todas as posições</option>${['GOL','ZAG','LAT','VOL','MEI','ATA'].map(x=>`<option ${f.pos==x?'selected':''}>${x}</option>`).join('')}</select>
<select id="fl"><option value="">Todas as ligas</option>${d.ligas.map(l=>`<option value="${l.i}" ${f.lg===String(l.i)?'selected':''}>${l.fl} ${esc(l.n)}</option>`).join('')}</select>
<select id="fm"><option value="">Qualquer preço</option>${[1000,5000,10000,25000,50000,100000].map(v=>`<option value="${v}" ${f.max==v?'selected':''}>até ${mo(v)}</option>`).join('')}</select>
<input id="fq" placeholder="Nome do jogador" value="${esc(f.q)}"><button class="btn" onclick="filtrar()">Buscar</button></div>`:''}
<div class="card tw"><table><tr><th>Pos</th><th>Jogador</th><th>Força</th><th class="hm">Físico</th><th class="hm">Pot.</th><th class="hm">Pé</th><th class="hm">Habilidades</th><th>${cmp?'Preço':'Oferta'}</th><th></th></tr>
${L.map(p=>`<tr><td><span class="pos ${GRP[p.pos]}">${p.pos}</span></td><td><b>${esc(p.n)}</b> <small>${p.fl} ${p.age} anos · ${esc(p.cl)}</small><div class="mob">Físico ${p.fis} · Pot. ${p.pot} · ${PE[p.pe]} · salário ${mo(p.sal)}/sem</div></td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td class="hm">${PE[p.pe]}</td><td class="hm">${habs(p.hab)}</td><td style="white-space:nowrap"><b>${mo(p.preco)}</b></td>
<td><button class="btn ${cmp?'':'red'}" onclick="${cmp?'comprar':'vender'}(${p.id},'${esc(p.n).replace(/&#39;/g,'')}',${p.preco})">${cmp?'Comprar':'Vender'}</button></td></tr>`).join('')}</table>${L.length?'':'<p class="mut">Nenhum jogador encontrado.</p>'}</div>`};
function filtrar(){S.mf={pos:$('#fp').value,lg:$('#fl').value,max:$('#fm').value,q:$('#fq').value};R.mercado()}
async function comprar(pid,n,v){if(await ask(`Contratar ${n} por ${mo(v)}?`)){await api('comprar',{pid});R.mercado()}}
async function vender(pid,n,v){if(await ask(`Vender ${n} por cerca de ${mo(v)}?`)){await api('vender',{pid});R.mercado()}}
/* ---------- selecao ---------- */
R.selecao=async()=>{await refresh();if(!S.st.sel){const r=await api('ranking');V.innerHTML=`<div class="card"><h3>Seleções</h3><p class="mut">Você não comanda uma seleção. Convites chegam conforme sua reputação cresce — fique de olho nas propostas.</p></div><div class="card tw"><h3>Ranking de força</h3><table>${r.lista.map((t,i)=>`<tr><td>${i+1}</td><td>${t.fl} <b>${esc(t.n)}</b></td><td>${ov(t.f)}</td></tr>`).join('')}</table></div>`;return}
const d=await api('elegiveis');S.cv=new Set(d.conv);
V.innerHTML=`<div class="card tools"><b style="font-size:16px">${d.t.fl} ${esc(d.t.n)}</b><span class="mut">Convocados: <b id="cvn">${S.cv.size}</b>/23</span><div class="sp"></div><button class="btn sec" onclick="convAuto()">Automática</button><button class="btn" onclick="convSalvar()">Salvar convocação</button><button class="btn sec" onclick="S.t='sel';go('elenco')">Escalar</button></div>
<div class="card tw"><table><tr><th></th><th>Pos</th><th>Jogador</th><th>Força</th><th class="hm">Físico</th><th class="hm">Pot.</th><th class="hm">Habilidades</th></tr>${d.lista.map(p=>`<tr class="${S.cv.has(p.id)?'tit':''}" onclick="tg(${p.id},this)"><td><input type="checkbox" ${S.cv.has(p.id)?'checked':''} style="pointer-events:none"></td><td><span class="pos ${GRP[p.pos]}">${p.pos}</span></td><td><b>${esc(p.n)}</b> <small>${p.age} anos · ${esc(p.cl)}${p.inj?' · <span class="red">lesionado</span>':''}</small></td><td>${ov(p.ovr)}</td><td class="hm">${p.fis}</td><td class="hm">${p.pot}</td><td class="hm">${habs(p.hab)}</td></tr>`).join('')}</table></div>`};
function tg(id,tr){if(S.cv.has(id))S.cv.delete(id);else{if(S.cv.size>=23)return toast('Máximo de 23 convocados',1);S.cv.add(id)}tr.classList.toggle('tit',S.cv.has(id));tr.querySelector('input').checked=S.cv.has(id);$('#cvn').textContent=S.cv.size}
async function convSalvar(){await api('convocar',{ids:[...S.cv]})}
async function convAuto(){await api('conv_auto');R.selecao();toast('Convocação automática feita')}
/* ---------- carreira ---------- */
R.carreira=async()=>{await refresh();const d=await api('carreira'),s=S.st;
V.innerHTML=`<div class="grid"><div class="card"><h3>Técnico</h3><div class="kv"><span>Nome</span><b>${esc(d.n)}</b><span>Reputação (${d.rep}/99)</span>${bar(d.rep,'var(--blue)')}<span>Campanha</span><b>${d.v}V ${d.e}E ${d.d}D</b><span>Clube</span><b>${s.clube?esc(s.clube.n):'—'}</b><span>Seleção</span><b>${s.sel?s.sel.fl+' '+esc(s.sel.n):'—'}</b></div>
<div class="row" style="margin-top:14px">${s.clube?`<button class="btn red" onclick="demitir('clube')">Sair do clube</button>`:''}${s.sel?`<button class="btn red" onclick="demitir('sel')">Sair da seleção</button>`:''}</div></div>
<div class="card"><h3>Propostas</h3>${s.ofs.length?ofertas(s.ofs):'<p class="mut">Nenhuma proposta no momento. Bons resultados aumentam sua reputação e atraem clubes e seleções maiores.</p>'}</div>
<div class="card"><h3>Jogo</h3><div class="row"><button class="btn" onclick="salvar()">Salvar</button><button class="btn sec" onclick="carregar()" ${d.save?'':'disabled'}>Carregar</button><button class="btn sec" onclick="novoJogo()">Novo jogo</button></div></div>
<div class="card tw"><h3>Histórico</h3>${d.hist.length?`<table><tr><th>Ano</th><th>Time</th><th>Competição</th><th>Pos.</th><th>Pts</th></tr>${d.hist.map(h=>`<tr><td>${h.s}</td><td>${h.tit?'🏆 ':''}<b>${esc(h.t)}</b></td><td>${esc(h.l)}</td><td>${h.pos}º</td><td>${h.pts}</td></tr>`).join('')}</table>`:'<p class="mut">Sua primeira temporada está em andamento.</p>'}</div></div>`};
async function demitir(t){if(await ask('Tem certeza?')){await api('demitir',{t});go('carreira')}}
async function salvar(){await api('salvar')}
/* ---------- partida ao vivo (ultra rapido) ---------- */
let LV=null;const ICO={gol:'⚽',am:'🟨',vm:'🟥',les:'🩹',sub:'🔁',quase:'💨',tat:'📋'};
async function jogar(){const r=await api('jogar');if(!r.live){await refresh();return R.inicio()}startLive(r)}
function startLive(r){LV={...r,q:[],busy:false,pause:false,hold:false,done:false,evs:r.ev||[],so:null};S.v='jogo';nav();drawLive();loop()}
function drawLive(){const L=LV,m=L.ms[0];
V.innerHTML=`<div class="card"><div class="comp" style="text-align:center">${esc(L.comp)}</div><div class="score"><div class="tm">${bdg(m.h,'lg')}<span>${esc(m.h.n)}</span></div><div><div class="pl" id="pl">${m.g[0]} - ${m.g[1]}</div><span class="min" id="mn">${L.min}'</span><div id="pe" class="mut hint"></div></div><div class="tm">${bdg(m.a,'lg')}<span>${esc(m.a.n)}</span></div></div>
<div class="bar prog"><i id="pg" style="width:${L.min/.9}%"></i></div><div class="ctl" id="ctl"><button class="btn" id="bp" onclick="pausar()">❚❚ Pausar</button><button class="btn sec" onclick="painel()">🔁 Substituições (<span id="sc">${L.lado.subs}</span>/5)</button></div></div>
<div id="pn"></div><div class="two w"><div class="card"><h3>Lances</h3><div class="feed" id="fd"></div></div><div class="card"><h3>Outros jogos</h3><div id="ot"></div></div></div>`;feed();outros([])}
function feed(){const L=LV,m=L.ms[0];$('#fd').innerHTML=L.evs.slice().reverse().map(e=>{const t=e.s?m.a:m.h;return `<div class="${e.k=='gol'?'gol':''}"><b style="width:30px">${e.m}'</b><span class="dot" style="background:${t.cor[0]}"></span><span>${ICO[e.k]} ${e.k=='gol'?'GOL! '+esc(e.x)+(e.y?` <small>(assist. ${esc(e.y)})</small>`:''):e.k=='sub'?`Entra <b>${esc(e.x)}</b>, sai ${esc(e.y)}`:e.k=='am'?'Amarelo: '+esc(e.x):e.k=='vm'?'EXPULSO: '+esc(e.x):e.k=='les'?'Lesão: '+esc(e.x):esc(e.x)}</span></div>`}).join('')||'<p class="mut">A bola vai rolar...</p>'}
function outros(gl){const o=LV.ms.slice(1);$('#ot').innerHTML=o.length?o.map((m,i)=>`<div class="og ${gl.includes(i+1)?'hit':''}"><span>${esc(m.h.n)}</span><b>${m.g[0]} - ${m.g[1]}${m.pen?` (${m.pen[0]}-${m.pen[1]})`:''}</b><span>${esc(m.a.n)}</span></div>`).join(''):'<p class="mut">Sem outros jogos.</p>'}
function loop(){const L=LV;if(!L||L.done)return;let w=80;
if(!L.fim&&!L.busy&&!L.hold&&!L.pause&&L.q.length<5){L.busy=true;api('passo',{n:5}).then(r=>{L.busy=false;L.q.push(...r.frames);if(r.frames.some(f=>f.pausa))L.hold=true;if(r.fim){L.fim=true;L.final=r.final;L.res=r.res}}).catch(()=>{L.busy=false})}
if(!L.pause&&L.q.length){const f=L.q.shift();aplicar(f);if(f.gols.includes(0))w=700;else if(f.min==45){w=900;toast('Intervalo')}if(f.pausa){pausar(1);toast(f.pausa=='lesão'?'Jogador lesionado! Faça a substituição.':'Jogador expulso! Reorganize o time.',1)}}
else if(L.fim&&!L.q.length&&!L.pause)return fimJogo();
L.tm=setTimeout(loop,w)}
function aplicar(f){const L=LV;L.min=f.min;f.g.forEach((g,i)=>L.ms[i].g=g);L.evs.push(...f.ev);$('#pl').textContent=`${f.g[0][0]} - ${f.g[0][1]}`;$('#mn').textContent=f.min+"'";$('#pg').style.width=(f.min/.9)+'%';
if(f.gols.includes(0)){const e=$('#pl');e.classList.remove('flash');void e.offsetWidth;e.classList.add('flash')}if(f.ev.length)feed();outros(f.gols)}
function pausar(auto){const L=LV;if(L.pause&&!auto){L.pause=false;L.hold=false;L.so=null;$('#pn').innerHTML='';$('#bp').textContent='❚❚ Pausar';return}if(L.pause)return;L.pause=true;$('#bp').textContent='▶ Continuar';painel()}
async function painel(){if(LV.fim&&!LV.q.length)return;if(!LV.pause)return pausar();const r=await api('tatica',{});LV.lado=r.lado;drawPn()}
function drawPn(){const l=LV.lado;$('#sc').textContent=l.subs;
$('#pn').innerHTML=`<div class="card"><div class="tools">${fsel(l.form,'tat')}<div class="seg">${tacs(l.tac,'tat')}</div><div class="sp"></div><button class="btn" onclick="pausar()">▶ Continuar</button></div>
<p class="mut hint" style="margin:10px 0">Toque em quem sai e depois em quem entra · ${5-l.subs} substituições restantes</p>
<div class="two w"><div><h3>Em campo</h3>${l.on.map(p=>prow(p,1)).join('')}</div><div><h3>Banco</h3>${l.bench.map(p=>prow(p,0)).join('')||'<p class="mut">Banco vazio.</p>'}</div></div></div>`}
function prow(p,on){return `<div class="pr ${LV.so==p.id?'pk':''}" onclick="${on?`LV.so=${p.id};drawPn()`:`entra(${p.id})`}"><span class="pos ${GRP[p.pos]}">${p.pos}</span><b>${esc(p.n)}</b>${p.am?'🟨':''}${p.les?'🩹':''}${on&&p.sl&&GRP[p.pos]!=p.sl?'⚠':''}<span class="sp"></span>${ov(p.ovr)}<div style="width:54px">${bar(p.en)}</div></div>`}
async function entra(id){if(!LV.so)return toast('Escolha primeiro quem sai',1);const r=await api('sub',{out:LV.so,in:id});LV.so=null;LV.lado=r.lado;drawPn()}
async function tat(o){const r=await api('tatica',o);LV.lado=r.lado;drawPn()}
function fimJogo(){const L=LV;L.done=true;const m=L.final[0];L.ms=L.final;outros([]);if(m.pen)$('#pe').textContent=`Pênaltis: ${m.pen[0]} - ${m.pen[1]}`;$('#ctl').innerHTML='';
$('#pn').innerHTML=`<div class="card end ${L.res}"><h2>${L.res=='V'?'Vitória!':L.res=='E'?'Empate':'Derrota'}</h2><p>${esc(m.h.n)} ${m.g[0]} - ${m.g[1]} ${esc(m.a.n)}${m.pen?` (pên. ${m.pen[0]}-${m.pen[1]})`:''}</p><button class="btn big" onclick="LV=null;go('inicio')">Continuar</button></div>`;scrollTo({top:0,behavior:'smooth'})}
boot().catch(e=>{V.innerHTML=vazio('Erro ao iniciar: '+esc(e.message))});
</script></body></html>'''

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

def porta_livre(p):
    import socket
    for q in range(p, p + 50):
        with socket.socket() as s:
            try: s.bind(('0.0.0.0', q)); return q
            except OSError: continue
    return p

def iniciar_servidor(porta=PORTA):
    if G is None: gerar_mundo()
    import logging; logging.getLogger('werkzeug').setLevel(logging.ERROR)
    porta = porta_livre(porta)
    th = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=porta, debug=False, use_reloader=False, threaded=True), daemon=True)
    th.start()
    print('Prancheta FC: %d ligas, %d clubes, %d jogadores, %d seleções.' % (len(G.L), sum(len(L['clubs']) for L in G.L), len(G.P), len(selecoes())))
    try:
        from google.colab import output   # Google Colab
        output.serve_kernel_port_as_window(porta, anchor_text='>>> CLIQUE AQUI para abrir o Prancheta FC em tela cheia (recomendado) <<<')
        output.serve_kernel_port_as_iframe(porta, height=820)
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
