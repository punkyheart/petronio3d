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
