from flask import Flask
from configparser import ConfigParser
import threading
import time
from obsws_python import ReqClient
import os


rodando = False

status = "PARADO"
cena_atual = "-"

modo_sucata = False

SUCATA = "SUCATA"


PASTA_MOLDURAS = r"S:\KAUAN\BACKUP CENAS\MOLDURAS"

moldura_atual = "Financeiras"




app = Flask(__name__)

# ==========================================
# CONFIGURAÇÃO
# ==========================================

config = ConfigParser()
config.read("config.ini")

OBS_HOST = config["OBS"]["host"]
OBS_PORT = int(config["OBS"]["port"])
OBS_PASSWORD = config["OBS"]["password"]

PRINCIPAL = "F4 - LOTES SEM PIP"

ANUNCIOS = [
    "MÊS",
    "F9 - CENTRAL ATENDIMENTO",
    "F7 - ALERTA - MULTA 20%",
    "F8 - NÃO EMPRESTE SEU LOGIN",
    "F6 - ALERTA - RESPONSÁVEL"
]

tempo_principal = 5
tempo_anuncio = 6

rodando = False


# ==========================================
# CONEXÃO OBS
# ==========================================

def conectar_obs():
    return ReqClient(
        host=xxxx,
        port=xxxx,
        password=xxx
    )


# ==========================================
# TROCA DE CENA
# ==========================================

def trocar_cena(nome_cena):
    global cena_atual

    try:
        obs = conectar_obs()
        obs.set_current_program_scene(nome_cena)

        cena_atual = nome_cena

        print(
            f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] "
            f"Cena alterada para: {nome_cena}"
        )

        return True

    except Exception as erro:
        print(
            f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] "
            f"ERRO OBS: {erro}"
        )

        return False

# ==========================================
# MOLDURAS
# ==========================================

MOLDURAS = {
    "Financeiras": r"C:\Users\kauan.santos\Desktop\Automação_OBS\MOLDURAS\Financeiras.png",
    "Seguradoras": r"C:\Users\kauan.santos\Desktop\Automação_OBS\MOLDURAS\Seguradoras.png",
    "Judicial": r"C:\Users\kauan.santos\Desktop\Automação_OBS\MOLDURAS\Judicial.png",
    "BancosSeguradoras": r"C:\Users\kauan.santos\Desktop\Automação_OBS\MOLDURAS\BancosSeguradoras.png",
    "Equipamentos": r"C:\Users\kauan.santos\Desktop\Automação_OBS\MOLDURAS\Equipamentos.png"
}

def trocar_moldura_obs(nome):

    try:

        caminho = MOLDURAS[nome]

        obs = conectar_obs()

        obs.set_input_settings(
            "Tela de Apresentação",
            {
                "file": caminho
            },
            True
        )

        print(f"Moldura alterada para {nome}")

    except Exception as erro:

        print("ERRO AO TROCAR MOLDURA:", erro)




# ==========================================
# LOOP PRINCIPAL
# ==========================================

def loop_cenas():
    global rodando, modo_sucata

    while True:

        if not rodando:
            time.sleep(1)
            continue

        for anuncio in ANUNCIOS:

            if not rodando:
                break

            # FOTO PRINCIPAL
            trocar_cena(PRINCIPAL)

            for _ in range(tempo_principal):
                if not rodando:
                    break
                time.sleep(1)

            if not rodando:
                break

            # SUCATA (se ativada)
            if modo_sucata:

                trocar_cena(SUCATA)

                for _ in range(tempo_anuncio):
                    if not rodando:
                        break
                    time.sleep(1)

                if not rodando:
                    break

                trocar_cena(PRINCIPAL)

                for _ in range(tempo_principal):
                    if not rodando:
                        break
                    time.sleep(1)

                if not rodando:
                    break

            # ANÚNCIO
            trocar_cena(anuncio)

            for _ in range(tempo_anuncio):
                if not rodando:
                    break
                time.sleep(1)

# ==========================================
# THREAD
# ==========================================

threading.Thread(
    target=loop_cenas,
    daemon=True
).start()


# ==========================================
# WEB
# ==========================================
@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="pt-br">
<head>

<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">

<title>Controle OBS</title>

<style>

:root{
    --bg:#050816;
    --card:#0F172A;
    --card2:#111C38;

    --cyan:#00E5FF;
    --blue:#2563EB;
    --purple:#7C3AED;
    --pink:#DB2777;

    --white:#FFFFFF;
    --gray:#94A3B8;
}

body{
    font-family:'Segoe UI',sans-serif;

    background:
        radial-gradient(circle at top,
        #172554 0%,
        #0B1020 40%,
        #050816 100%);

    color:var(--white);

    margin:0;
    padding:20px;
    text-align:center;
}

h1{
    font-size:32px;
    font-weight:700;
    margin-bottom:25px;

  
}

.status-box{
    width:95%;
    max-width:600px;
    margin:auto;
    margin-bottom:25px;

    background:rgba(15,23,42,.95);
    border:1px solid rgba(148,163,184,.25);

    border-radius:18px;
    padding:20px;
    box-sizing:border-box;

    box-shadow: 0 6px 18px rgba(0,0,0,.35);
}

.status-titulo{
    font-size:30px;
    font-weight:800;
    color:#E5E7EB; /* cinza claro suave */

    text-shadow:none;

    background-color:#1F2937; /* cinza escuro sólido */
    padding:10px 15px;
    border-radius:12px;

    border:1px solid #374151; /* borda discreta */

    box-shadow:none;
}

.status-info{
    margin-top:10px;
    color:var(--gray);
    font-size:17px;
}

button,
#sucataStatus{

    width:100%;
    max-width:320px;

    height:60px;

    margin:10px auto;

    display:block;

    border:none;
    border-radius:14px;

    font-size:17px;
    font-weight:700;

    cursor:pointer;

    transition:.25s;
}

button:hover,
#sucataStatus:hover{

    transform:translateY(-2px);

    box-shadow:
        0 0 20px rgba(255,255,255,.15);
}

/* INICIAR */

.start{
    background: linear-gradient(
        135deg,
        #0B3D2E,
        #146C43
    );

    color: white;

    box-shadow:
        0 0 20px rgba(20,108,67,.35);
}

/* PAUSAR */

.pause{
    background: linear-gradient(
        135deg,
        #FACC15,
        #EAB308
    );

    color: #1F1F1F;

    box-shadow:
        0 0 20px rgba(234,179,8,.45);
}
/* PARAR */

.stop{
    background: linear-gradient(
        135deg,
        #7F1D1D,
        #B91C1C
    );

    color: white;

    border: 1px solid #991B1B;

    box-shadow: 0 0 10px rgba(185,28,28,.25);
}
/* SUCATA ON */

.sucata-on{
    background: linear-gradient(
        135deg,
        #7F1D1D,
        #B91C1C
    );

    color: white;

    border: 1px solid #991B1B;

    box-shadow: 0 0 12px rgba(185,28,28,.25);
}

/* SUCATA OFF */

.sucata-off{
    background:#1E293B;
    color:#CBD5E1;
}

/* ALERTA */

.sucata{
    background:linear-gradient(
        135deg,
        #DB2777,
        #EC4899
    );

    color:white;

    box-shadow:
        0 0 20px rgba(219,39,119,.45);
}
#moldura{
    width:100%;
    max-width:320px;
    height:60px;

    margin:10px auto;
    display:block;

    border-radius:14px;

    background:#1F2937;
    color:#FFFFFF;

    border:1px solid #374151;

    font-size:16px;
    font-weight:600;

    text-align-last:center;

    outline:none;
    cursor:pointer;

    appearance:none;
    -webkit-appearance:none;
    -moz-appearance:none;

    padding-left:20px;
    padding-right:50px;

    box-shadow:none;

    background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='14' height='14' viewBox='0 0 24 24' fill='none' stroke='%23FFFFFF' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'/%3E%3C/svg%3E");

    background-repeat:no-repeat;
    background-position:right 18px center;
    background-size:14px;

    transition:.2s;
}

/* quando clica */
#moldura:focus{
    border:1px solid #00E5FF;

    box-shadow:
        0 0 20px rgba(0,229,255,.35),
        0 0 40px rgba(124,58,237,.15);

    transform:translateY(-2px);
}

/* opções dentro do select */
#moldura option{
    background:#0B1020;
    color:#FFFFFF;
}
.status-label{
    color:#FFFFFF;
}

.status-value{
    color:var(--cyan);
        text-shadow:none;
}

</style>

</head>

<body>

<h1>Controle Automático OBS</h1>

<div class="status-box">

  <div class="status-titulo" id="status">
    <span class="status-label">STATUS:</span>
    <span class="status-value">PARADO</span>
</div>

    <div class="status-info" id="cena">
        Cena Atual: -
    </div>

</div>

<select id="moldura"
        onchange="trocarMoldura(this.value)"
        style="
    
        ">

    <option value="Financeiras"> Financeiras</option>
    <option value="Seguradoras"> Seguradoras</option>
    <option value="Judicial">Judicial</option>
    <option value="BancosSeguradoras">Bancos e Seguradoras</option>
    <option value="Equipamentos">Equipamentos</option>
</select>

<button class="start" onclick="fetch('/start')">
    INICIAR
</button>

<button class="pause" onclick="fetch('/pause')">
    PAUSAR
</button>

<button class="stop" onclick="fetch('/stop')">
    PARAR
</button>

<button id="sucataStatus"
        class="sucata-off"
        onclick="fetch('/sucata').then(() => atualizarStatus())">
    MODO SUCATA: OFF
</button>



<script>

async function trocarMoldura(nome){

    await fetch("/moldura/" + nome);

}

async function atualizarStatus(){

    const resposta = await fetch('/status');
    const dados = await resposta.json();

   document.getElementById("status").innerHTML =
    '<span class="status-label">STATUS:</span> ' +
    '<span class="status-value">' + dados.status + '</span>';

    document.getElementById("cena").innerHTML =
        "Cena Atual: " + dados.cena;

    const box = document.querySelector(".status-box");

    if(dados.status === "RODANDO"){
    box.style.borderColor = "#22C55E";
}
else if(dados.status === "PAUSADO"){
    box.style.borderColor = "#FACC15";
}
else{
    box.style.borderColor = "#DB2777";
}
    const sucata =
    document.getElementById("sucataStatus");

if(dados.modo_sucata){

    sucata.innerHTML = "MODO SUCATA: ON";

    sucata.classList.remove("sucata-off");
    sucata.classList.add("sucata-on");

}
else{

    sucata.innerHTML = "MODO SUCATA: OFF";

    sucata.classList.remove("sucata-on");
    sucata.classList.add("sucata-off");

}
    
}

setInterval(atualizarStatus, 1000);

atualizarStatus();

</script>

</body>
</html>
"""


@app.route("/start")
def start():
    global rodando, status

    rodando = True
    status = "RODANDO"

    print(
        f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] "
        f"Automação iniciada"
    )

    return "OK"


@app.route("/pause")
def pause():
    global rodando, status

    rodando = False
    status = "PAUSADO"

    print(
        f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] "
        f"Automação pausada"
    )

    return "OK"


@app.route("/stop")
def stop():
    global rodando, status

    rodando = False
    status = "PARADO"

    trocar_cena(PRINCIPAL)

    print(
        f"[{time.strftime('%d/%m/%Y %H:%M:%S')}] "
        f"Automação encerrada"
    )

    return "OK"


@app.route("/status")
def status_api():

    return {
        "status": status,
        "cena": cena_atual,
        "modo_sucata": modo_sucata
    }
    
@app.route("/sucata")
def sucata():

    global modo_sucata

    modo_sucata = not modo_sucata

    return {
        "modo_sucata": modo_sucata
    }
    
    # ROTA MOLDURA

@app.route("/moldura/<nome>")
def mudar_moldura(nome):

    global moldura_atual

    moldura_atual = nome

    trocar_moldura_obs(nome)

    return {"ok": True}
    
    


# ==========================================
# EXECUÇÃO
# ==========================================

if __name__ == "__main__":

    print("=" * 50)
    print("CONTROLE OBS INICIADO")
    print(f"HOST: {OBS_HOST}")
    print(f"PORTA: {OBS_PORT}")
    print("=" * 50)

    app.run(
        host="127.0.0.1",
        port=5000
    )
