# =====================================================================
#  PRANCHETA FC - jogo de gerenciamento de futebol (Python + HTML/JS)
#  Google Colab: cole TUDO numa celula e execute (Shift+Enter).
#  PC: pip install flask openpyxl  &&  python prancheta_fc.py
# =====================================================================
import random, math, os, sys, threading, pickle, csv, traceback, re, unicodedata, datetime as dt
try:
    from flask import Flask, request, jsonify, Response
except ImportError:
    import subprocess; subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'flask'])
    from flask import Flask, request, jsonify, Response

PORTA = 8050
SAVE = 'prancheta_save.pkl'
R = random.Random()

# ----------------------------- DADOS ---------------------------------
# pais|liga|forca do melhor|forca do pior|inicio (MM-DD)|clubes (em ordem aproximada de forca)
LIGAS = """EN|Premier League|87|72|08-16|Arsenal;Manchester City;Liverpool;Chelsea;Newcastle;Tottenham;Aston Villa;Manchester United;Nottingham Forest;Brighton;Crystal Palace;Bournemouth;Brentford;Fulham;Everton;West Ham;Sunderland;Leeds United;Wolverhampton;Burnley
ES|La Liga|87|68|08-16|Real Madrid;Barcelona;Atlético de Madrid;Athletic Bilbao;Villarreal;Real Betis;Real Sociedad;Sevilla;Celta de Vigo;Girona;Valencia;Osasuna;Rayo Vallecano;Mallorca;Getafe;Espanyol;Alavés;Elche;Levante;Real Oviedo
IT|Serie A|84|67|08-23|Inter de Milão;Napoli;Juventus;Milan;Atalanta;Roma;Como;Lazio;Bologna;Fiorentina;Torino;Udinese;Genoa;Sassuolo;Cagliari;Parma;Lecce;Verona;Cremonese;Pisa
DE|Bundesliga|87|67|08-23|Bayern de Munique;Bayer Leverkusen;Borussia Dortmund;RB Leipzig;Eintracht Frankfurt;VfB Stuttgart;SC Freiburg;Hoffenheim;Mainz 05;Wolfsburg;Werder Bremen;Borussia Mönchengladbach;Union Berlin;Augsburg;Colônia;Hamburgo;St. Pauli;Heidenheim
FR|Ligue 1|86|64|08-16|Paris Saint-Germain;Olympique de Marseille;Monaco;Lille;Lyon;Nice;Lens;Strasbourg;Rennes;Toulouse;Brest;Nantes;Auxerre;Le Havre;Angers;Paris FC;Lorient;Metz
BR|Brasileirão Série A|80|68|04-12|Flamengo;Palmeiras;Botafogo;Cruzeiro;Fluminense;São Paulo;Atlético Mineiro;Internacional;Corinthians;Bahia;Grêmio;Red Bull Bragantino;Vasco da Gama;Santos;Mirassol;Vitória;Athletico Paranaense;Coritiba;Chapecoense;Remo
PT|Liga Portugal|81|60|08-09|Benfica;Porto;Sporting;Braga;Vitória de Guimarães;Famalicão;Santa Clara;Gil Vicente;Moreirense;Rio Ave;Estoril;Casa Pia;Arouca;Nacional;Estrela da Amadora;Tondela;AVS;Alverca
NL|Eredivisie|79|60|08-09|PSV;Feyenoord;Ajax;AZ Alkmaar;Twente;Utrecht;NEC Nijmegen;Go Ahead Eagles;Heerenveen;Sparta Rotterdam;Groningen;Fortuna Sittard;PEC Zwolle;Heracles;NAC Breda;Excelsior;Telstar;Volendam
AR|Liga Profesional|77|63|02-01|River Plate;Boca Juniors;Racing Club;Vélez Sarsfield;Estudiantes;Talleres;Independiente;San Lorenzo;Rosario Central;Argentinos Juniors;Lanús;Huracán;Defensa y Justicia;Belgrano;Newell's Old Boys;Unión de Santa Fe;Platense;Tigre;Instituto;Godoy Cruz;Banfield;Gimnasia La Plata;Barracas Central;Independiente Rivadavia;Sarmiento;Central Córdoba;Atlético Tucumán;Aldosivi;Deportivo Riestra;Gimnasia de Mendoza
TR|Süper Lig|78|62|08-09|Galatasaray;Fenerbahçe;Beşiktaş;Trabzonspor;Başakşehir;Samsunspor;Göztepe;Eyüpspor;Kasımpaşa;Antalyaspor;Konyaspor;Alanyaspor;Kayserispor;Gaziantep;Rizespor;Kocaelispor;Gençlerbirliği;Fatih Karagümrük
BE|Pro League|77|61|07-26|Club Brugge;Union Saint-Gilloise;Anderlecht;Genk;Gent;Antwerp;Standard Liège;Mechelen;Westerlo;Charleroi;Sint-Truiden;OH Leuven;Cercle Brugge;Dender;Zulte Waregem;La Louvière
SC|Scottish Premiership|75|59|08-02|Celtic;Rangers;Hearts;Aberdeen;Hibernian;Motherwell;Dundee United;St Mirren;Kilmarnock;Falkirk;Dundee;Livingston
SA|Saudi Pro League|80|60|08-23|Al-Hilal;Al-Nassr;Al-Ittihad;Al-Ahli;Al-Qadsiah;Al-Ettifaq;Al-Shabab;Al-Taawoun;Al-Fateh;Al-Khaleej;Al-Fayha;Al-Kholood;Al-Riyadh;Damac;Al-Hazem;Al-Okhdood;Al-Najma;NEOM
US|MLS|74|62|02-22|Inter Miami;LAFC;Columbus Crew;FC Cincinnati;Seattle Sounders;LA Galaxy;Philadelphia Union;Vancouver Whitecaps;Orlando City;Atlanta United;New York City FC;New York Red Bulls;Minnesota United;Nashville SC;San Diego FC;Charlotte FC;Austin FC;Portland Timbers;Real Salt Lake;Houston Dynamo;Sporting Kansas City;FC Dallas;Chicago Fire;New England Revolution;Colorado Rapids;St. Louis City;San Jose Earthquakes;D.C. United;CF Montréal;Toronto FC
MX|Liga MX|75|62|07-12|América;Toluca;Tigres UANL;Monterrey;Cruz Azul;Guadalajara;Pumas UNAM;Pachuca;León;Atlas;Santos Laguna;Tijuana;Juárez;Necaxa;Puebla;Querétaro;Mazatlán;Atlético San Luis
JP|J1 League|70|60|02-14|Kashima Antlers;Vissel Kobe;Sanfrecce Hiroshima;Kashiwa Reysol;Kyoto Sanga;Machida Zelvia;Urawa Reds;Kawasaki Frontale;Gamba Osaka;Cerezo Osaka;FC Tokyo;Yokohama F. Marinos;Nagoya Grampus;Avispa Fukuoka;Shimizu S-Pulse;Tokyo Verdy;Fagiano Okayama;V-Varen Nagasaki;Mito HollyHock;JEF United Chiba
KR|K League 1|68|59|03-01|Jeonbuk Hyundai;Ulsan HD;Pohang Steelers;FC Seoul;Gangwon FC;Daejeon Hana Citizen;Gimcheon Sangmu;Gwangju FC;Jeju SK;FC Anyang;Suwon FC;Incheon United
CN|Super League|67|56|03-01|Shanghai Port;Shanghai Shenhua;Chengdu Rongcheng;Beijing Guoan;Shandong Taishan;Tianjin Jinmen Tiger;Zhejiang FC;Henan FC;Qingdao West Coast;Yunnan Yukun;Dalian Yingbo;Wuhan Three Towns;Shenzhen Peng City;Qingdao Hainiu;Chongqing Tonglianglong;Liaoning Tieren
RU|Premier Liga|75|61|07-19|Zenit;Krasnodar;Spartak Moscou;CSKA Moscou;Lokomotiv Moscou;Dínamo Moscou;Rubin Kazan;Rostov;Akhmat Grozny;Krylia Sovetov;Baltika;Dinamo Makhachkala;Akron Tolyatti;Pari NN;Orenburg;Sochi
UA|Premier Liga|71|57|08-02|Shakhtar Donetsk;Dínamo de Kiev;Polissya Zhytomyr;Kryvbas;LNZ Cherkasy;Oleksandriya;Karpaty Lviv;Zorya Luhansk;Kolos Kovalivka;Veres Rivne;Rukh Lviv;Obolon Kyiv;Metalist 1925;Kudrivka;Epitsentr;Poltava
GR|Super League|75|60|08-23|Olympiacos;PAOK;AEK Atenas;Panathinaikos;Aris;OFI Creta;Asteras Tripolis;Atromitos;Volos;Levadiakos;Panetolikos;Kifisia;Panserraikos;AEL Larissa
CH|Super League|73|61|07-19|Basel;Young Boys;Servette;Lugano;Luzern;St. Gallen;Lausanne-Sport;Zürich;Sion;Thun;Grasshoppers;Winterthur
AT|Bundesliga|74|60|07-26|Red Bull Salzburg;Sturm Graz;Rapid Viena;Austria Viena;LASK;Wolfsberger AC;Hartberg;Rheindorf Altach;Blau-Weiß Linz;WSG Tirol;Grazer AK;Ried
DK|Superliga|73|60|07-19|Copenhague;Midtjylland;Brøndby;AGF Aarhus;Nordsjælland;Randers;Silkeborg;Viborg;OB Odense;Sønderjyske;Vejle;Fredericia
NO|Eliteserien|72|58|03-29|Bodø/Glimt;Molde;Brann;Rosenborg;Viking;Vålerenga;Sarpsborg 08;Fredrikstad;Tromsø;Lillestrøm;Sandefjord;HamKam;Kristiansund;KFUM Oslo;Start;Aalesund
SE|Allsvenskan|70|58|03-29|Malmö FF;Mjällby;Hammarby;AIK;Djurgården;IFK Göteborg;Häcken;Elfsborg;GAIS;Sirius;Brommapojkarna;Halmstad;Degerfors;Västerås SK;Kalmar FF;Örgryte
PL|Ekstraklasa|70|58|07-19|Lech Poznań;Raków Częstochowa;Jagiellonia;Legia Varsóvia;Pogoń Szczecin;Górnik Zabrze;Cracovia;Widzew Łódź;Motor Lublin;GKS Katowice;Piast Gliwice;Zagłębie Lubin;Korona Kielce;Radomiak;Lechia Gdańsk;Wisła Płock;Arka Gdynia;Bruk-Bet Termalica
CZ|Chance Liga|74|58|07-19|Slavia Praga;Sparta Praga;Viktoria Plzeň;Baník Ostrava;Jablonec;Sigma Olomouc;Hradec Králové;Slovan Liberec;Bohemians 1905;Mladá Boleslav;Teplice;Karviná;Pardubice;Dukla Praga;Zlín;Slovácko
HR|HNL|73|57|07-26|Dinamo Zagreb;Hajduk Split;Rijeka;Osijek;Varaždin;Lokomotiva Zagreb;Slaven Belupo;Istra 1961;Gorica;Vukovar 1991
RS|SuperLiga|73|55|07-19|Estrela Vermelha;Partizan;Vojvodina;Čukarički;TSC Bačka Topola;Novi Pazar;Radnički 1923;OFK Beograd;Železničar Pančevo;Spartak Subotica;IMT Belgrado;Mladost Lučani;Radnički Niš;Napredak;Javor;Radnik Surdulica
CO|Liga BetPlay|71|58|01-25|Atlético Nacional;Millonarios;América de Cali;Junior Barranquilla;Independiente Santa Fe;Deportes Tolima;Independiente Medellín;Deportivo Cali;Once Caldas;Atlético Bucaramanga;Deportivo Pereira;Águilas Doradas;Alianza FC;Fortaleza CEIF;Llaneros;Boyacá Chicó;Internacional de Bogotá;Cúcuta Deportivo;Jaguares de Córdoba;Envigado
CL|Primera División|69|57|02-14|Colo-Colo;Universidad de Chile;Universidad Católica;Coquimbo Unido;O'Higgins;Palestino;Audax Italiano;Huachipato;Everton de Viña;Cobresal;Unión La Calera;Ñublense;Deportes Iquique;Deportes La Serena;Deportes Limache;Deportes Concepción
UY|Primera División|69|56|02-07|Peñarol;Nacional;Defensor Sporting;Liverpool;Danubio;Racing Montevideo;Cerro Largo;Boston River;Montevideo Wanderers;Progreso;Plaza Colonia;Juventud;Cerro;River Plate Montevideo;Central Español;Montevideo City Torque
PY|División de Honor|68|56|02-07|Olimpia;Cerro Porteño;Libertad;Guaraní;Nacional Asunción;Sportivo Luqueño;Sportivo Trinidense;2 de Mayo;Sportivo Ameliano;Tacuary;Recoleta;General Caballero JLM
EC|LigaPro|71|56|02-21|Independiente del Valle;LDU Quito;Barcelona SC;Emelec;Universidad Católica;Aucas;Deportivo Cuenca;Orense;Macará;Técnico Universitario;Mushuc Runa;Delfín;El Nacional;Libertad FC;Manta;Vinotinto
PE|Liga 1|67|55|02-07|Universitario;Alianza Lima;Sporting Cristal;Cusco FC;Melgar;Cienciano;ADT;Sport Huancayo;Alianza Atlético;Deportivo Garcilaso;Atlético Grau;Juan Pablo II;Los Chankas;Sport Boys;Comerciantes Unidos;UTC;Ayacucho FC;Binacional
AU|A-League|66|56|10-17|Melbourne City;Auckland FC;Western Sydney Wanderers;Sydney FC;Melbourne Victory;Adelaide United;Central Coast Mariners;Macarthur FC;Brisbane Roar;Wellington Phoenix;Newcastle Jets;Perth Glory
EG|Premier League|70|55|08-16|Al Ahly;Pyramids;Zamalek;Al Masry;Ceramica Cleopatra;Modern Sport;ZED;Smouha;ENPPI;Ismaily;Al Ittihad;Talaea El Gaish;El Gouna;Ghazl El Mahalla;Petrojet;National Bank;Haras El Hodoud;Pharco
MA|Botola Pro|69|55|09-06|RS Berkane;Wydad Casablanca;Raja Casablanca;FAR Rabat;FUS Rabat;MAS Fès;Hassania Agadir;Olympic Safi;Difaâ El Jadida;Union Touarga;IR Tanger;Renaissance Zemamra;CODM Meknès;Kawkab Marrakech;Olympique Dcheira;Yacoub El Mansour
ZA|Premiership|68|55|08-09|Mamelodi Sundowns;Orlando Pirates;Kaizer Chiefs;Stellenbosch;Sekhukhune United;TS Galaxy;AmaZulu;Polokwane City;Golden Arrows;Chippa United;Richards Bay;Durban City;Siwelele;Magesi;Marumo Gallants;Orbit College"""

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
'it':"Marco Luca Andrea Matteo Lorenzo Alessandro Davide Federico Simone Nicolò Riccardo Giacomo Stefano Daniele Francesco Gianluca Tommaso Filippo|Rossi Russo Ferrari Esposito Bianchi Romano Colombo Ricci Marino Greco Bruno Gallo Conti De_Luca Costa Mancini Giordano Rizzo Lombardi Moretti Barbieri Fontana",
'de':"Lukas Leon Jonas Felix Maximilian Niklas Tim Jan Paul Florian Julian Kevin Marcel Tobias Moritz Fabian Luca David|Müller Schmidt Schneider Fischer Weber Meyer Wagner Becker Schulz Hoffmann Koch Richter Klein Wolf Schröder Neumann Braun Zimmermann Krüger Hartmann Lange Werner",
'fr':"Lucas Hugo Théo Nathan Mathis Enzo Louis Raphaël Antoine Maxime Kylian Clément Adrien Yanis Baptiste Jules Mathéo Noah|Martin Bernard Dubois Thomas Robert Richard Petit Durand Leroy Moreau Simon Laurent Lefebvre Michel Garcia David Bertrand Roux Vincent Fournier Morel Girard",
'pt':"João Diogo Rúben Tiago Rafael Gonçalo Bruno André Nuno Pedro Ricardo Miguel Francisco Rodrigo Vítor Hugo Fábio Duarte|Silva Santos Ferreira Pereira Oliveira Costa Rodrigues Martins Sousa Fernandes Gonçalves Gomes Lopes Marques Alves Almeida Ribeiro Pinto Carvalho Teixeira Moreira",
'nl':"Daan Sem Thijs Lars Jesse Bram Luuk Milan Stijn Ruben Tim Joey Kevin Sven Jordy Wout Jens Niels|de_Jong de_Vries van_Dijk Bakker Janssen Visser Smit Meijer de_Boer Mulder de_Groot Bos Vos Peters Hendriks van_Leeuwen Dekker Brouwer de_Wit Dijkstra Maes Peeters",
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

DADOS_XLSX = 'prancheta_dados.xlsx'      # planilha opcional com ligas/clubes/jogadores reais
ANO_BASE = 2026
DATAS_FIFA = ('09-08', '10-13', '11-17', '03-24')          # amistosos de seleções
DATAS_CN = ('06-20', '06-27', '07-04', '07-11')            # Copa das Nações (oitavas -> final)
FASES_CN = ['Oitavas de final', 'Quartas de final', 'Semifinal', 'Final']
COPAS = {'EN':'FA Cup','ES':'Copa del Rey','IT':'Coppa Italia','DE':'DFB-Pokal','FR':'Coupe de France','BR':'Copa do Brasil',
         'PT':'Taça de Portugal','NL':'KNVB Beker','AR':'Copa Argentina','TR':'Copa da Turquia','BE':'Copa da Bélgica',
         'SC':'Scottish Cup','SA':"King's Cup",'US':'U.S. Open Cup','MX':'Copa MX','JP':"Emperor's Cup",'KR':'Korea Cup',
         'CN':'Copa da China','RU':'Copa da Rússia','UA':'Copa da Ucrânia','GR':'Copa da Grécia','CH':'Copa da Suíça',
         'AT':'ÖFB-Cup','DK':'Copa da Dinamarca','NO':'Copa da Noruega','SE':'Svenska Cupen','PL':'Puchar Polski',
         'CZ':'Copa da Tchéquia','HR':'Copa da Croácia','RS':'Copa da Sérvia','CO':'Copa Colombia','CL':'Copa Chile',
         'UY':'Copa AUF Uruguay','PY':'Copa Paraguay','EC':'Copa Ecuador','PE':'Copa do Peru','AU':'Australia Cup',
         'EG':'Copa do Egito','MA':'Copa do Trono','ZA':'Nedbank Cup'}
ABREV = {'FIN':'Fin','CAB':'Cab','DRI':'Dri','PAS':'Pas','VEL':'Vel','DES':'Des','MAR':'Mar','CHL':'Chu','BOL':'Bpa',
         'PEN':'Pen','LID':'Lid','REF':'Ref','SAI':'Sgo','RES':'Res','CRU':'Cru'}
# nomes de países (pt/en) -> (código, pool de nomes) para o importador de planilhas
PAISES_EXTRA = {'QA':('Catar','ar'),'AE':('Emirados Árabes','ar'),'IR':('Irã','ar'),'IL':('Israel','en'),'RO':('Romênia','sl'),
    'HU':('Hungria','sl'),'BG':('Bulgária','sl'),'SK':('Eslováquia','sl'),'SI':('Eslovênia','sl'),'BA':('Bósnia','sl'),
    'AL':('Albânia','sl'),'MK':('Macedônia do Norte','sl'),'ME':('Montenegro','sl'),'FI':('Finlândia','nd'),'IS':('Islândia','nd'),
    'IE':('Irlanda','en'),'WA':('País de Gales','en'),'NI':('Irlanda do Norte','en'),'CY':('Chipre','gr'),'VE':('Venezuela','es'),
    'BO':('Bolívia','es'),'CR':('Costa Rica','es'),'HN':('Honduras','es'),'GT':('Guatemala','es'),'PA':('Panamá','es'),
    'SV':('El Salvador','es'),'CA':('Canadá','en'),'JM':('Jamaica','en'),'TN':('Tunísia','ar'),'NZ':('Nova Zelândia','en'),
    'IN':('Índia','en'),'TH':('Tailândia','cn'),'VN':('Vietnã','cn'),'ID':('Indonésia','cn'),'MY':('Malásia','cn'),
    'UZ':('Uzbequistão','ru'),'KZ':('Cazaquistão','ru'),'GE':('Geórgia','ru'),'AM':('Armênia','ru'),'AZ':('Azerbaijão','ru'),
    'BY':('Belarus','ru'),'LT':('Lituânia','ru'),'LV':('Letônia','ru'),'EE':('Estônia','ru'),'AO':('Angola','pt'),
    'MZ':('Moçambique','pt'),'CV':('Cabo Verde','pt'),'GN':('Guiné','af'),'BF':('Burkina Faso','af'),'CD':('RD Congo','af'),
    'CG':('Congo','af'),'GA':('Gabão','af'),'TG':('Togo','af'),'BJ':('Benin','af'),'KE':('Quênia','af'),'ZM':('Zâmbia','af'),
    'ZW':('Zimbábue','af'),'TZ':('Tanzânia','af'),'UG':('Uganda','af'),'LU':('Luxemburgo','fr'),'IQ':('Iraque','ar'),
    'JO':('Jordânia','ar'),'SY':('Síria','ar'),'LB':('Líbano','ar'),'KW':('Kuwait','ar'),'BH':('Bahrein','ar'),'OM':('Omã','ar'),
    'LY':('Líbia','ar')}
for _k, _v in PAISES_EXTRA.items(): PAISES.setdefault(_k, _v)
NOMES_PAIS_EN = {'brazil':'BR','argentina':'AR','uruguay':'UY','chile':'CL','colombia':'CO','paraguay':'PY','peru':'PE',
    'ecuador':'EC','mexico':'MX','spain':'ES','united states':'US','usa':'US','england':'EN','scotland':'SC','australia':'AU',
    'italy':'IT','germany':'DE','austria':'AT','switzerland':'CH','france':'FR','belgium':'BE','netherlands':'NL',
    'holland':'NL','portugal':'PT','turkey':'TR','turkiye':'TR','japan':'JP','south korea':'KR','korea republic':'KR',
    'china':'CN','china pr':'CN','saudi arabia':'SA','egypt':'EG','morocco':'MA','algeria':'DZ','russia':'RU','ukraine':'UA',
    'denmark':'DK','norway':'NO','sweden':'SE','poland':'PL','czech republic':'CZ','czechia':'CZ','croatia':'HR',
    'serbia':'RS','greece':'GR','south africa':'ZA','senegal':'SN','nigeria':'NG','ghana':'GH','ivory coast':'CI',
    "cote d'ivoire":'CI','cameroon':'CM','mali':'ML','qatar':'QA','united arab emirates':'AE','uae':'AE','iran':'IR',
    'israel':'IL','romania':'RO','hungary':'HU','bulgaria':'BG','slovakia':'SK','slovenia':'SI','bosnia and herzegovina':'BA',
    'albania':'AL','north macedonia':'MK','montenegro':'ME','finland':'FI','iceland':'IS','ireland':'IE','republic of ireland':'IE',
    'wales':'WA','northern ireland':'NI','cyprus':'CY','venezuela':'VE','bolivia':'BO','costa rica':'CR','honduras':'HN',
    'guatemala':'GT','panama':'PA','el salvador':'SV','canada':'CA','jamaica':'JM','tunisia':'TN','new zealand':'NZ',
    'india':'IN','thailand':'TH','vietnam':'VN','indonesia':'ID','malaysia':'MY','uzbekistan':'UZ','kazakhstan':'KZ',
    'georgia':'GE','armenia':'AM','azerbaijan':'AZ','belarus':'BY','lithuania':'LT','latvia':'LV','estonia':'EE',
    'angola':'AO','mozambique':'MZ','cape verde':'CV','guinea':'GN','burkina faso':'BF','dr congo':'CD','congo':'CG',
    'gabon':'GA','togo':'TG','benin':'BJ','kenya':'KE','zambia':'ZM','zimbabwe':'ZW','tanzania':'TZ','uganda':'UG',
    'luxembourg':'LU','iraq':'IQ','jordan':'JO','syria':'SY','lebanon':'LB','kuwait':'KW','bahrain':'BH','oman':'OM','libya':'LY'}
# cores reais (fundo/texto) dos clubes mais conhecidos; os demais recebem cores automáticas
CORES_CLUBES = dict(x.split('=') for x in (
 'Arsenal=ef0107/fff;Manchester City=6cabdd/fff;Liverpool=c8102e/fff;Chelsea=034694/fff;Newcastle=241f20/fff;Tottenham=132257/fff;'
 'Aston Villa=670e36/fff;Manchester United=da291c/fff;Nottingham Forest=dd0000/fff;Brighton=0057b8/fff;Crystal Palace=1b458f/fff;'
 'Bournemouth=b50e12/fff;Brentford=e30613/fff;Fulham=f8fafc/111;Everton=003399/fff;West Ham=7a263a/fff;Sunderland=eb172b/fff;'
 'Leeds United=f8fafc/1d428a;Wolverhampton=fdb913/231f20;Burnley=6c1d45/fff;Real Madrid=f8fafc/00529f;Barcelona=a50044/fff;'
 'Atlético de Madrid=cb3524/fff;Athletic Bilbao=ee2523/fff;Villarreal=ffe667/005187;Real Betis=0bb363/fff;Real Sociedad=0067b1/fff;'
 'Sevilla=f8fafc/d80027;Celta de Vigo=8ac3ee/111;Valencia=f8fafc/111;Girona=cd2534/fff;Osasuna=d91a21/fff;Rayo Vallecano=f8fafc/e53027;'
 'Mallorca=e20613/fff;Getafe=005999/fff;Espanyol=007fc8/fff;Alavés=0761af/fff;Elche=05642c/fff;Levante=004d98/fff;Real Oviedo=0055a5/fff;'
 'Inter de Milão=0068a8/fff;Napoli=12a0d7/fff;Juventus=111111/fff;Milan=fb090b/111;Atalanta=1e71b8/fff;Roma=8e1f2f/f0bc42;Como=0047bb/fff;'
 'Lazio=87d8f7/111;Bologna=1a2f48/fff;Fiorentina=482e92/fff;Torino=8a1e03/fff;Udinese=111111/fff;Genoa=a71930/fff;Sassuolo=00a752/fff;'
 'Cagliari=002350/fff;Parma=ffd200/0b3a8f;Bayern de Munique=dc052d/fff;Borussia Dortmund=fde100/111;Bayer Leverkusen=e32221/111;'
 'RB Leipzig=f8fafc/dd0741;Eintracht Frankfurt=e1000f/111;VfB Stuttgart=f8fafc/e32219;SC Freiburg=111111/fff;Werder Bremen=1d9053/fff;'
 'Wolfsburg=65b32e/fff;Borussia Mönchengladbach=f8fafc/111;Union Berlin=eb1923/fff;Hamburgo=f8fafc/0a3f86;Colônia=f8fafc/ed1c24;'
 'St. Pauli=624839/fff;Mainz 05=c3141e/fff;Hoffenheim=1961b5/fff;Augsburg=ba3733/fff;Heidenheim=e2001a/fff;Paris Saint-Germain=004170/fff;'
 'Olympique de Marseille=2faee0/fff;Monaco=e51b22/fff;Lille=e01e13/fff;Lyon=f8fafc/1e3a8a;Nice=c8102e/111;Lens=ffd700/c8102e;'
 'Rennes=e13327/111;Strasbourg=009fe3/fff;Nantes=fcd405/0a5a2a;Toulouse=6a2c91/fff;Flamengo=c8102e/fff;Palmeiras=006437/fff;'
 'Botafogo=111111/fff;Cruzeiro=1e3a8a/fff;Fluminense=7a1f3d/fff;São Paulo=f8fafc/d6001c;Atlético Mineiro=111111/fff;Internacional=d6001c/fff;'
 'Corinthians=f8fafc/111;Bahia=0055a4/fff;Grêmio=0d80bf/111;Red Bull Bragantino=f8fafc/d6001c;Vasco da Gama=111111/fff;Santos=f8fafc/111;'
 'Mirassol=ffd100/006b3f;Vitória=d6001c/111;Athletico Paranaense=c8102e/111;Coritiba=00543c/fff;Chapecoense=00843d/fff;Remo=0b2a6b/fff;'
 'Benfica=e1001a/fff;Porto=003d9e/fff;Sporting=008057/fff;Braga=d7001c/fff;Vitória de Guimarães=f8fafc/111;PSV=ed1c24/fff;Feyenoord=e10e0e/fff;'
 'Ajax=f8fafc/c8102e;AZ Alkmaar=d6001c/fff;Twente=e30613/fff;River Plate=f8fafc/d6001c;Boca Juniors=0f3d91/ffd100;Racing Club=6cace4/fff;'
 'Independiente=d6001c/fff;San Lorenzo=0b2a6b/fff;Estudiantes=d6001c/fff;Vélez Sarsfield=f8fafc/0b3a8f;Rosario Central=0b3a8f/ffd100;'
 "Newell's Old Boys=d6001c/111;Talleres=0b2a6b/fff;Lanús=7a1f3d/fff;Galatasaray=a90432/fdb912;Fenerbahçe=1a2a6c/ffed00;Beşiktaş=111111/fff;"
 'Trabzonspor=7b1c2b/6ec6f0;Club Brugge=0067ce/111;Anderlecht=4f2d7f/fff;Union Saint-Gilloise=ffd200/0b3a8f;Genk=0047ab/fff;Gent=0b3a8f/fff;'
 'Standard Liège=e30613/fff;Celtic=018749/fff;Rangers=1b458f/fff;Hearts=8e1b30/fff;Aberdeen=d6001c/fff;Hibernian=007a3d/fff;'
 'Al-Hilal=0055a5/fff;Al-Nassr=ffd100/0b2a6b;Al-Ittihad=ffd100/111;Al-Ahli=007a3d/fff;Inter Miami=f7b5cd/111;LAFC=111111/c39e6d;'
 'LA Galaxy=00245d/fff;Seattle Sounders=5d9741/fff;Columbus Crew=fedd00/111;América=ffd100/0b2a6b;Guadalajara=d6001c/fff;Cruz Azul=0047ab/fff;'
 'Monterrey=0b2a6b/fff;Tigres UANL=fdb913/0b2a6b;Toluca=d6001c/fff;Pumas UNAM=0b2a6b/c39e6d;Kashima Antlers=b5002d/fff;Urawa Reds=e60012/111;'
 'Vissel Kobe=8a0021/fff;Zenit=0091d5/fff;Spartak Moscou=d6001c/fff;CSKA Moscou=0b2a6b/fff;Shakhtar Donetsk=f36c21/111;Dínamo de Kiev=f8fafc/0b3a8f;'
 'Olympiacos=d6001c/fff;PAOK=111111/fff;AEK Atenas=ffd100/111;Panathinaikos=007a3d/fff;Dinamo Zagreb=0047ab/fff;Hajduk Split=f8fafc/0b3a8f;'
 'Estrela Vermelha=d6001c/fff;Partizan=111111/fff;Colo-Colo=f8fafc/111;Universidad de Chile=0b3a8f/fff;Universidad Católica=f8fafc/0b3a8f;'
 'Atlético Nacional=00843d/fff;Millonarios=0b3a8f/fff;América de Cali=d6001c/fff;Peñarol=ffd100/111;Nacional=f8fafc/0b3a8f;Olimpia=f8fafc/111;'
 'Cerro Porteño=0b3a8f/fff;LDU Quito=f8fafc/0b3a8f;Barcelona SC=ffd100/111;Emelec=0b3a8f/fff;Independiente del Valle=111111/fff;'
 'Universitario=f5e6c8/7a1f3d;Alianza Lima=0b2a6b/fff;Sporting Cristal=6cace4/fff;Al Ahly=d6001c/fff;Zamalek=f8fafc/d6001c;'
 'Wydad Casablanca=d6001c/fff;Raja Casablanca=00843d/fff;Mamelodi Sundowns=ffd100/0b6e3a;Orlando Pirates=111111/fff;Kaizer Chiefs=ffd100/111;'
 'Copenhague=f8fafc/0b3a8f;Brøndby=ffd100/0b3a8f;Bodø/Glimt=ffd100/111;Rosenborg=f8fafc/111;Molde=0b3a8f/fff;Malmö FF=6cace4/fff;AIK=111111/ffd100;'
 'Djurgården=0b3a8f/fff;Hammarby=00843d/fff;Red Bull Salzburg=f8fafc/d6001c;Rapid Viena=00843d/fff;Sturm Graz=111111/fff;Austria Viena=5b2a86/fff;'
 'Basel=d6001c/fff;Young Boys=ffd100/111;Legia Varsóvia=f8fafc/00843d;Lech Poznań=0b3a8f/fff;Slavia Praga=d6001c/fff;Sparta Praga=7a1f3d/fff;'
 'Viktoria Plzeň=0b3a8f/fff').split(';'))
CORES_CLUBES = {k: tuple('#' + c for c in v.split('/')) for k, v in CORES_CLUBES.items()}
CORES_PAIS = {'BR': ('#ffd100', '#0b6e3a'), 'AR': ('#6cace4', '#fff'), 'FR': ('#1e3a8a', '#fff'), 'ES': ('#c8102e', '#ffd100'), 'EN': ('#f8fafc', '#1e3a8a'),
              'DE': ('#f8fafc', '#111'), 'IT': ('#0b4ea2', '#fff'), 'PT': ('#c8102e', '#fff'), 'NL': ('#f36c21', '#fff'), 'BE': ('#c8102e', '#fff'),
              'UY': ('#6cace4', '#fff'), 'CO': ('#ffd100', '#0b3a8f'), 'MX': ('#006847', '#fff'), 'US': ('#f8fafc', '#0b2a6b'), 'JP': ('#0b2a6b', '#fff'),
              'HR': ('#f8fafc', '#c8102e'), 'MA': ('#c8102e', '#fff'), 'SN': ('#f8fafc', '#00853f'), 'KR': ('#c8102e', '#fff'), 'CL': ('#c8102e', '#fff')}

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


# --------------------------- INTERFACE -------------------------------
HTML = r'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><meta name="theme-color" content="#ffffff">
<title>Prancheta FC</title><style>:root{--bg:#f3f5f9;--card:#fff;--ink:#162033;--mut:#667085;--line:#e4e8ef;--pri:#0e9f6e;--pri2:#e7f7f0;--blue:#2563eb;--red:#e5484d;--yel:#f5b301;
--sh:0 1px 2px rgba(16,24,40,.05),0 4px 14px rgba(16,24,40,.06);--pc:#0e9f6e;--pt:#fff}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--ink);font-size:14px;-webkit-font-smoothing:antialiased}
button,input,select{font:inherit;color:inherit}button{cursor:pointer}
/* ---------- topo ---------- */
#topo{position:sticky;top:0;z-index:30;background:#fff;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:10px;padding:6px 14px;min-height:62px}
.marca{display:flex;align-items:center;gap:9px;font-size:16px;white-space:nowrap}
.logo{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#34d399,#0e9f6e);color:#fff;display:grid;place-items:center;font-weight:800;flex:none}
.logo.xl{width:64px;height:64px;font-size:30px;border-radius:18px;margin:0 auto 12px}
#menu{display:flex;gap:2px;flex:1;overflow-x:auto;scrollbar-width:none;padding:0 4px}#menu::-webkit-scrollbar{display:none}
#menu button{border:0;background:none;display:flex;flex-direction:column;align-items:center;gap:3px;padding:6px 8px;border-radius:10px;color:var(--mut);font-size:11.5px;font-weight:600;min-width:62px;position:relative}
#menu button svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
#menu button:hover{background:#f4f6f9}#menu button.on{background:var(--pri2);color:var(--pri)}
.badge{position:absolute;top:2px;right:10px;background:var(--red);color:#fff;border-radius:9px;font-size:10px;padding:0 5px;line-height:15px}
.hoje{font-weight:700;white-space:nowrap;text-align:right;font-size:13px}.hoje small{display:block;color:var(--mut);font-weight:500}
.nogame #topo #menu,.nogame .hoje,.nogame #bjogar,.nogame #painel{display:none}.nogame #corpo{grid-template-columns:1fr}
/* ---------- estrutura ---------- */
#corpo{display:grid;grid-template-columns:300px minmax(0,1fr);min-height:calc(100vh - 62px)}
main{min-width:0;padding:16px 18px 40px}
#painel{background:var(--pc);color:var(--pt);padding:14px;position:sticky;top:62px;height:calc(100vh - 62px);overflow:auto}
#painel small{color:inherit;opacity:.8}
.pn-top{display:flex;align-items:center;gap:10px}.pn-nome{font-size:17px;display:block;line-height:1.2}.pn-seta{display:none;margin-left:auto}
.pn-corpo{display:flex;flex-direction:column;gap:10px;margin-top:12px}
.pn-box{background:rgba(255,255,255,.13);border-radius:12px;padding:10px}#painel.claro .pn-box{background:rgba(0,0,0,.05)}
.pn-linha{display:flex;justify-content:space-between;align-items:center;gap:8px}
.pn-msg{border:0;background:rgba(255,255,255,.2);color:inherit;border-radius:8px;padding:4px 9px;font-weight:700}#painel.claro .pn-msg{background:rgba(0,0,0,.07)}
.pn-conf{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pn-conf small{display:block;margin-bottom:4px;font-weight:600}
.cbar{height:16px;border-radius:5px;background:rgba(255,255,255,.25);overflow:hidden;position:relative;font-size:10.5px;font-weight:800;text-align:center;line-height:16px;color:#fff}
#painel.claro .cbar{background:rgba(0,0,0,.08);color:var(--ink)}.cbar i{position:absolute;left:0;top:0;bottom:0}.cbar span{position:relative}
.pn-prox-t{font-weight:800;font-size:12px;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}
.pn-adv{display:flex;align-items:center;gap:10px}.pn-adv small{display:block}
.pn-bts{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.btn.sec2{background:rgba(255,255,255,.92);color:var(--ink)}
.cardj{background:#fff;color:var(--ink);border-radius:12px;padding:12px;display:flex;flex-direction:column;gap:6px;box-shadow:var(--sh)}
.cardj small{color:var(--mut)!important;opacity:1!important}.cardj.vazio{text-align:center;padding:16px}
.cj-h{display:flex;align-items:center;gap:6px;font-size:15px}.cj-f{margin-left:auto;font-weight:800;color:var(--pri)}
.cj-acoes{display:flex;gap:6px;flex-wrap:wrap}.cj-acoes button{border:1px solid var(--line);background:#f7f9fc;border-radius:8px;padding:5px 9px;font-size:12px;font-weight:700}
.cj-acoes button:hover{background:var(--pri2);border-color:var(--pri)}.cj-acoes button.red{color:var(--red)}
.cj-v{display:flex;justify-content:space-between;gap:8px;font-size:12.5px;flex-wrap:wrap}
.cj-st{font-size:12px}.cj-st td,.cj-st th{padding:3px 4px;text-align:center}.cj-st td:first-child{text-align:left;font-weight:600}
.pn-rod{display:flex;justify-content:space-between;font-weight:700;font-size:12.5px;opacity:.9}
/* ---------- componentes ---------- */
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);padding:16px;margin-bottom:14px;min-width:0}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));align-items:start}.grid>.card{margin-bottom:0}
.two{display:grid;gap:14px;grid-template-columns:minmax(280px,400px) minmax(0,1fr);align-items:start}.two.w{grid-template-columns:minmax(0,1.5fr) minmax(0,1fr)}
.two>.card,.two>div{margin-bottom:0}
h2{font-size:18px}h2 small{font-size:12.5px;color:var(--mut);font-weight:500;margin-left:6px}
h3{font-size:12px;text-transform:uppercase;letter-spacing:.07em;color:var(--mut);margin-bottom:10px}h3.sub{margin:18px 0 8px}
.barra-v{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:12px}
.btn{border:0;background:var(--pri);color:#fff;font-weight:700;padding:9px 14px;border-radius:10px;transition:filter .15s;white-space:nowrap}
.btn:hover{filter:brightness(1.06)}.btn.sec{background:#eef1f6;color:var(--ink)}.btn.red{background:#fdecec;color:var(--red)}.btn.big{font-size:16px;padding:13px 20px;width:100%}
.btn.jogar{background:#ff6b2c}.btn:disabled{opacity:.5;cursor:default}
.bdg{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;font-size:10px;font-weight:800;flex:none;box-shadow:inset 0 0 0 1.5px rgba(0,0,0,.12);letter-spacing:-.3px;vertical-align:middle}
.bdg.sm{width:20px;height:20px;font-size:7.5px}.bdg.lg{width:52px;height:52px;font-size:15px}
.ov{display:inline-block;min-width:28px;text-align:center;padding:2px 5px;border-radius:6px;font-weight:800;font-size:12px}
.o1{background:#f1f3f6;color:#667085}.o2{background:#fff4d6;color:#a16207}.o3{background:#e0f2fe;color:#0369a1}.o4{background:#dcfce7;color:#15803d}.o5{background:#ede9fe;color:#6d28d9}
.chip{display:inline-block;padding:1px 6px;border-radius:20px;background:#f1f4f8;color:#475467;font-size:11px;font-weight:600;margin:1px 2px 1px 0;white-space:nowrap}
.pos{display:inline-block;width:34px;text-align:center;font-size:10.5px;font-weight:800;padding:2px 0;border-radius:5px;background:#eef1f6;color:#475467}
.pos.G{background:#fff4d6;color:#a16207}.pos.D{background:#e0f2fe;color:#0369a1}.pos.M{background:#dcfce7;color:#15803d}.pos.A{background:#fde8e8;color:#c0262d}
.tw,.tabela-wrap{overflow-x:auto}.tabela-wrap{background:#fff;border:1px solid var(--line);border-radius:12px;box-shadow:var(--sh)}
table{width:100%;border-collapse:collapse}
th{font-size:11px;color:var(--mut);text-align:left;font-weight:700;padding:7px 6px;border-bottom:1px solid var(--line);white-space:nowrap;background:#fafbfd;position:sticky;top:0}
td{padding:6px;border-bottom:1px solid #eef1f5;vertical-align:middle}
table.dens td{padding:4px 6px;font-size:13px;white-space:nowrap}table.dens th{cursor:pointer;user-select:none}table.dens tbody tr{cursor:pointer}
tr.p-GOL td{background:#f2f3f5}tr.p-LAT td{background:#fffbe0}tr.p-ZAG td{background:#eef0ff}tr.p-VOL td,tr.p-MEI td{background:#eafaee}tr.p-ATA td{background:#fff0f0}
table.dens tbody tr:hover td{filter:brightness(.97)}tr.selj td{box-shadow:inset 0 2px 0 var(--pri),inset 0 -2px 0 var(--pri)}
tr.tit td:first-child{box-shadow:inset 4px 0 0 var(--pri)}.estrela{color:#e5484d}
.en{display:inline-block;width:56px;height:15px;border-radius:4px;background:#e9ecf1;position:relative;overflow:hidden;vertical-align:middle;font-size:10px;font-weight:800;text-align:center;line-height:15px}
.en i{position:absolute;left:0;top:0;bottom:0}.en span{position:relative}
tr.me td{background:var(--pri2);font-weight:700}
.bar{height:6px;background:#eef1f6;border-radius:9px;overflow:hidden;min-width:40px}.bar i{display:block;height:100%;background:var(--pri)}
select,input{padding:8px 10px;border:1px solid var(--line);border-radius:9px;background:#fff;max-width:100%}
.seg{display:inline-flex;background:#eef1f6;border-radius:10px;padding:3px;flex-wrap:wrap}.seg button{border:0;background:none;padding:6px 11px;border-radius:8px;font-weight:600;color:var(--mut)}.seg button.on{background:#fff;color:var(--ink);box-shadow:var(--sh)}
.tools{display:flex;gap:8px;align-items:center;flex-wrap:wrap}.mut{color:var(--mut)}.red{color:var(--red)}.verde{color:var(--pri)}.hint{font-size:12px}.sp{flex:1}
.kv{display:grid;grid-template-columns:1fr auto;gap:7px 12px;align-items:center}.kv span{color:var(--mut)}
.nw{padding:9px 0;border-bottom:1px solid #f0f2f6;font-size:13px;display:flex;gap:10px;align-items:flex-start}.nw small{color:var(--mut);white-space:nowrap}
.nw.bom{color:#0b7a55}.nw.mau{color:#b42318}.nw.nova{font-weight:700}
.hero{text-align:center;padding:30px 10px 18px}.hero h1{font-size:30px}.hero p{color:var(--mut);max-width:560px;margin:8px auto 0}
.form{display:grid;gap:12px;grid-template-columns:repeat(auto-fit,minmax(210px,1fr))}.form label{display:flex;flex-direction:column;gap:6px;font-weight:600;font-size:13px}
.clubs{display:grid;gap:8px;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));max-height:400px;overflow:auto;padding:2px}
.club{display:flex;align-items:center;gap:10px;border:1px solid var(--line);background:#fff;border-radius:12px;padding:8px 10px;text-align:left}.club span{flex:1;font-weight:600}.club.on{border-color:var(--pri);box-shadow:0 0 0 3px var(--pri2)}
.row{display:flex;gap:10px;flex-wrap:wrap}.row>*{flex:1}
/* ---------- janela / agenda ---------- */
.janela{background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:var(--sh);overflow:hidden}
.jan-h{display:flex;align-items:center;gap:10px;padding:12px 14px;border-bottom:1px solid var(--line);flex-wrap:wrap}.jan-h h2{flex:1}
.x{border:1px solid var(--line);background:#fff;border-radius:9px;width:38px;height:36px;font-weight:800}
table.ag td{white-space:nowrap}table.ag td.r{text-align:right}table.ag tr.prox td{background:#fff4e8;font-weight:700}table.ag tr.click{cursor:pointer}
.res{display:inline-block;min-width:52px;text-align:center;border-radius:6px;padding:2px 6px;font-weight:800;background:#eef1f6}
.res.V{background:#dcfce7;color:#15803d}.res.E{background:#f1f3f6}.res.D{background:#fde8e8;color:#c0262d}
/* ---------- escalação ---------- */
.pitch{position:relative;aspect-ratio:68/100;width:100%;max-width:400px;margin:auto;border-radius:14px;background:repeating-linear-gradient(0deg,#61bd7d 0 10%,#58b474 10% 20%);border:3px solid #fff;box-shadow:var(--sh);overflow:hidden}
.pitch:before{content:"";position:absolute;left:0;right:0;top:50%;border-top:2px solid rgba(255,255,255,.75)}
.pitch:after{content:"";position:absolute;left:50%;top:50%;width:26%;aspect-ratio:1;border:2px solid rgba(255,255,255,.75);border-radius:50%;transform:translate(-50%,-50%)}
.area{position:absolute;left:24%;right:24%;height:14%;border:2px solid rgba(255,255,255,.75)}.area.t{top:-2px}.area.b{bottom:-2px}
.pp{position:absolute;transform:translate(-50%,-50%);display:flex;flex-direction:column;align-items:center;gap:2px;cursor:pointer;z-index:2;width:80px}
.pp .c{width:36px;height:36px;border-radius:50%;background:#fff;display:grid;place-items:center;font-weight:800;font-size:13px;box-shadow:0 2px 6px rgba(0,0,0,.18);border:3px solid var(--kit)}
.pp .nm{font-size:10.5px;font-weight:700;color:#fff;background:rgba(8,40,24,.5);padding:1px 6px;border-radius:6px;white-space:nowrap;max-width:80px;overflow:hidden;text-overflow:ellipsis}
.pp .ps{font-size:9px;color:#fff;font-weight:800}.pp.sel .c{outline:3px solid var(--yel);outline-offset:2px}.pp.bad .c{background:#fff4d6}
/* ---------- partida ao vivo ---------- */
.placar{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:10px;text-align:center}
.tm{display:flex;flex-direction:column;align-items:center;gap:6px;font-weight:700;min-width:0}
.pl{font-size:42px;font-weight:800;letter-spacing:2px;font-variant-numeric:tabular-nums;line-height:1.1}
.min{display:inline-block;background:var(--pri2);color:var(--pri);font-weight:800;padding:2px 12px;border-radius:20px}
.prog{height:5px;margin:10px 0}.ctl{display:flex;gap:8px;flex-wrap:wrap;align-items:center}.ctl .btn{flex:1}
.comp{color:var(--pri);font-weight:700;font-size:13px}
.aovivo{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(300px,1fr);gap:14px;align-items:start}
.campo{position:relative;width:100%;aspect-ratio:105/68;border-radius:14px;overflow:hidden;background:#4f9a3a}
.campo svg{position:absolute;inset:0;width:100%;height:100%}
.sombra{position:absolute;top:0;bottom:0;background:linear-gradient(90deg,rgba(0,0,0,.28),rgba(0,0,0,.12));transition:all .3s;pointer-events:none}
.v .sombra{left:0!important;right:0!important;width:auto!important}
.jd{position:absolute;width:22px;height:22px;margin:-11px 0 0 -11px;border-radius:50%;display:grid;place-items:center;font-size:9.5px;font-weight:800;box-shadow:0 1px 3px rgba(0,0,0,.35);border:2px solid rgba(255,255,255,.9);transition-property:left,top;transition-timing-function:linear;z-index:2}
.jd.cans{outline:2px solid #ffb020}.bola{position:absolute;width:13px;height:13px;margin:-6.5px 0 0 -6.5px;border-radius:50%;background:#fff;box-shadow:0 0 0 2px #222,0 2px 4px rgba(0,0,0,.4);z-index:3;transition-property:left,top;transition-timing-function:ease-out}
.status{position:absolute;left:50%;top:10px;transform:translateX(-50%);background:rgba(255,255,255,.94);border-radius:10px;padding:5px 12px;font-weight:800;font-size:13px;z-index:4;white-space:nowrap;box-shadow:var(--sh);max-width:94%;overflow:hidden;text-overflow:ellipsis}
.status small{font-weight:600;color:var(--mut)}.status.gol{background:#ff6b2c;color:#fff}.status.gol small{color:#fff}
.abas{display:flex;gap:4px;border-bottom:1px solid var(--line);margin:-4px 0 10px;overflow-x:auto}.abas button{border:0;background:none;padding:8px 10px;font-weight:700;color:var(--mut);border-bottom:2px solid transparent;white-space:nowrap}
.abas button.on{color:var(--pri);border-color:var(--pri)}
.feed{max-height:430px;overflow:auto}.feed div{padding:7px 2px;border-bottom:1px solid #f0f2f6;display:flex;gap:8px;align-items:center;font-size:13px}
.feed .gol{font-weight:800;color:#0b7a55}.dot{width:9px;height:9px;border-radius:50%;flex:none;box-shadow:inset 0 0 0 1px rgba(0,0,0,.15)}
.og{display:grid;grid-template-columns:1fr auto 1fr;gap:8px;align-items:center;padding:6px 0;border-bottom:1px solid #f0f2f6;font-size:12.5px}.og span:first-child{text-align:right}
.og b{background:#f3f5f9;padding:2px 8px;border-radius:7px;font-variant-numeric:tabular-nums}.og.hit b{background:var(--pri);color:#fff}
.flash{animation:fl .9s}@keyframes fl{0%{transform:scale(1.3);color:var(--pri)}100%{transform:none}}
.pr{display:flex;align-items:center;gap:7px;padding:7px;border:1px solid var(--line);border-radius:9px;margin-bottom:5px;cursor:pointer;background:#fff;font-size:13px}
.pr.pk{border-color:var(--yel);background:#fff8e1}.pr b{overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.fim{text-align:center}.fim h2{font-size:26px;margin-bottom:6px}.fim.V h2{color:var(--pri)}.fim.D h2{color:var(--red)}.fim p{margin-bottom:12px;font-weight:600}
/* estatística comparativa */
.cmp{padding:7px 0}.cmp .l{display:flex;justify-content:space-between;font-size:13px;gap:8px}.cmp .l span{color:var(--ink);font-weight:600}.cmp .l b{font-weight:800}
.cmp .bb{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:4px}.cmp .bb div{height:6px;border-radius:4px;background:#eef1f6;overflow:hidden;display:flex}
.cmp .bb div:first-child{justify-content:flex-end}.cmp .bb i{display:block;height:100%}
.secao{background:#f6f8fb;border-radius:8px;text-align:center;font-weight:800;font-size:11px;letter-spacing:.07em;color:var(--mut);padding:6px;margin:10px 0 4px;text-transform:uppercase}
.garg .lane{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin:6px 0 12px}.garg .lane div{border-radius:9px;padding:8px;text-align:center;background:#f6f8fb}
.garg .lane b{display:block;font-size:18px}.garg li{margin:4px 0 4px 18px;font-size:13px}.garg .sug{background:#fff8e1;border-radius:10px;padding:10px;margin-top:8px}
.nota{display:inline-block;min-width:30px;text-align:center;border-radius:6px;font-weight:800;font-size:12px;padding:1px 4px;color:#fff;background:#94a3b8}
.n1{background:#e5484d}.n2{background:#f59e0b}.n3{background:#22c55e}.n4{background:#0e9f6e}.n5{background:#2563eb}
/* ---------- modal / toast ---------- */
#modal:empty{display:none}#modal{position:fixed;inset:0;background:rgba(22,32,51,.4);z-index:60;display:grid;place-items:center;padding:14px}
.mbox{background:#fff;border-radius:16px;box-shadow:0 20px 50px rgba(0,0,0,.25);width:min(860px,100%);max-height:92vh;overflow:auto;padding:16px}
.mbox.peq{width:min(420px,100%)}.mbox p{margin-bottom:14px;font-weight:600;font-size:15px}
.mhead{display:flex;align-items:center;gap:10px;margin-bottom:8px}.mhead h2{flex:1;font-size:16px}
#toast{position:fixed;left:50%;bottom:22px;transform:translate(-50%,40px);opacity:0;background:#162033;color:#fff;padding:10px 18px;border-radius:12px;font-weight:600;transition:.25s;z-index:80;max-width:90vw;text-align:center;pointer-events:none}
#toast.show{opacity:1;transform:translate(-50%,0)}#toast.bad{background:var(--red)}
.mob{display:none}
/* ---------- celular ---------- */
@media(max-width:900px){
 #topo{flex-wrap:wrap;padding:6px 10px 0;gap:6px}.marca b{display:none}.hoje{margin-left:auto}#menu{order:5;flex-basis:100%;padding-bottom:4px}
 #menu button{min-width:58px;font-size:10.5px;padding:5px 4px}
 #corpo{grid-template-columns:1fr}#painel{position:static;height:auto;padding:10px 12px}
 .pn-seta{display:inline}#painel:not(.aberto) .pn-corpo>*:not(.pn-sempre){display:none}#painel:not(.aberto) .pn-corpo{margin-top:8px}
 #painel #card{display:none}
 main{padding:12px 10px 40px}.two,.two.w,.aovivo{grid-template-columns:1fr}.hm{display:none}.mob{display:block}.grid{grid-template-columns:1fr}
 .pl{font-size:34px}.bdg.lg{width:44px;height:44px}.card{padding:12px}
 .campo{aspect-ratio:68/105;max-width:420px;margin:0 auto}
}
</style></head>
<body class="nogame">
<header id="topo"><div class="marca"><span class="logo">P</span><b>Prancheta FC</b></div><nav id="menu"></nav>
<div class="hoje" id="hoje"></div><button id="bjogar" class="btn jogar" onclick="jogar()">▶ Continuar</button></header>
<div id="corpo"><aside id="painel"></aside><main id="view"><div class="hero"><div class="logo xl">P</div><h1>Prancheta FC</h1><p>Carregando o mundo do futebol...</p></div></main></div>
<div id="modal"></div><div id="toast"></div>
<script>const $=s=>document.querySelector(s),V=()=>$('#view');
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
</script></body></html>
'''

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

