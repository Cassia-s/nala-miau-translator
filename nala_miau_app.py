import streamlit as st
import pandas as pd
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

st.set_page_config(page_title="Nala Translator", page_icon="🐱", layout="wide")

DATA_FILE = Path("nala_miados.csv")
TIMEZONE = ZoneInfo("America/Sao_Paulo")

ROTINA = {
    "acorda_inicio": time(5, 0),
    "acorda_fim": time(6, 0),
    "comidas": [time(7, 0), time(9, 0), time(12, 0), time(15, 0), time(18, 0)],
    "dorme_inicio": time(22, 0),
    "dorme_fim": time(23, 0),
    "ativo_inicio": time(19, 0),
    "ativo_fim": time(22, 0),
    "coco_manha_inicio": time(7, 0),
    "coco_manha_fim": time(8, 0),
    "coco_noite_inicio": time(19, 0),
    "coco_noite_fim": time(21, 0),
}

CLASSES = [
    "pedido_porta",
    "pedido_atencao",
    "miado_atencao",
    "miado_carinho",
    "reclamacao_frustracao",
    "caixa_areia_coco",
    "indefinido",
]

DEMO_MIAUS = {
    "Miado de porta": {
        "tipo_miado": "longo_crescente",
        "intensidade": "media",
        "duracao": "longa",
        "repeticao": "insistente",
        "perto_porta": "sim",
        "perto_caixa": "nao",
        "humanos_na_cama": "nao",
        "ronronando": "nao",
        "local": "porta quarto",
        "situacao_antes": "porta fechada",
    },
    "Miado ao acordar": {
        "tipo_miado": "resmungo",
        "intensidade": "baixa",
        "duracao": "curta",
        "repeticao": "repetido",
        "perto_porta": "nao",
        "perto_caixa": "nao",
        "humanos_na_cama": "sim",
        "ronronando": "nao",
        "local": "quarto",
        "situacao_antes": "voces ainda estavam dormindo",
    },
    "Miado na caixa": {
        "tipo_miado": "chamado",
        "intensidade": "baixa",
        "duracao": "curta",
        "repeticao": "unico",
        "perto_porta": "nao",
        "perto_caixa": "sim",
        "humanos_na_cama": "nao",
        "ronronando": "nao",
        "local": "caixa",
        "situacao_antes": "entrou na caixa",
    },
    "Miado de reclamacao": {
        "tipo_miado": "resmungo",
        "intensidade": "baixa",
        "duracao": "media",
        "repeticao": "repetido",
        "perto_porta": "nao",
        "perto_caixa": "nao",
        "humanos_na_cama": "nao",
        "ronronando": "nao",
        "local": "quintal",
        "situacao_antes": "cacando e frustrada",
    },
    "Miado de atencao": {
        "tipo_miado": "curto",
        "intensidade": "baixa",
        "duracao": "curta",
        "repeticao": "varios_miadinhos",
        "perto_porta": "nao",
        "perto_caixa": "nao",
        "humanos_na_cama": "nao",
        "ronronando": "nao",
        "local": "quarto",
        "situacao_antes": "quer interacao",
    },
    "Miado de carinho": {
        "tipo_miado": "curto",
        "intensidade": "baixa",
        "duracao": "media",
        "repeticao": "repetido",
        "perto_porta": "nao",
        "perto_caixa": "nao",
        "humanos_na_cama": "nao",
        "ronronando": "sim",
        "local": "quarto",
        "situacao_antes": "procurando colo e contato",
    },
}


def now_sp() -> datetime:
    return datetime.now(TIMEZONE)



def ensure_data_file() -> None:
    if not DATA_FILE.exists():
        demo_data = pd.DataFrame(
            [
                {
                    "data": "2026-04-16",
                    "hora": "06:00",
                    "fonte": "demo",
                    "local": "quarto",
                    "tipo_miado": "resmungo",
                    "intensidade": "baixa",
                    "duracao": "curta",
                    "repeticao": "repetido",
                    "perto_porta": "nao",
                    "perto_caixa": "nao",
                    "humanos_na_cama": "sim",
                    "ronronando": "nao",
                    "situacao_antes": "humanos ainda dormindo",
                    "classe_real": "pedido_atencao",
                },
                {
                    "data": "2026-04-16",
                    "hora": "20:10",
                    "fonte": "demo",
                    "local": "porta banheiro",
                    "tipo_miado": "longo_crescente",
                    "intensidade": "media",
                    "duracao": "longa",
                    "repeticao": "insistente",
                    "perto_porta": "sim",
                    "perto_caixa": "nao",
                    "humanos_na_cama": "nao",
                    "ronronando": "nao",
                    "situacao_antes": "porta fechada",
                    "classe_real": "pedido_porta",
                },
                {
                    "data": "2026-04-16",
                    "hora": "07:25",
                    "fonte": "demo",
                    "local": "caixa",
                    "tipo_miado": "chamado",
                    "intensidade": "baixa",
                    "duracao": "curta",
                    "repeticao": "unico",
                    "perto_porta": "nao",
                    "perto_caixa": "sim",
                    "humanos_na_cama": "nao",
                    "ronronando": "nao",
                    "situacao_antes": "entrou na caixa",
                    "classe_real": "caixa_areia_coco",
                },
                {
                    "data": "2026-04-16",
                    "hora": "21:00",
                    "fonte": "demo",
                    "local": "quarto",
                    "tipo_miado": "curto",
                    "intensidade": "baixa",
                    "duracao": "media",
                    "repeticao": "repetido",
                    "perto_porta": "nao",
                    "perto_caixa": "nao",
                    "humanos_na_cama": "nao",
                    "ronronando": "sim",
                    "situacao_antes": "procurando colo e contato",
                    "classe_real": "miado_carinho",
                },
            ]
        )
        demo_data.to_csv(DATA_FILE, index=False)



def load_data() -> pd.DataFrame:
    ensure_data_file()
    return pd.read_csv(DATA_FILE)



def save_event(row: dict) -> None:
    df = load_data()
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)



def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute



def within_range(current: time, start: time, end: time) -> bool:
    cm = to_minutes(current)
    sm = to_minutes(start)
    em = to_minutes(end)
    return sm <= cm <= em



def nearest_meal_distance_minutes(current: time) -> int:
    cm = to_minutes(current)
    return min(abs(cm - to_minutes(meal)) for meal in ROTINA["comidas"])



def classify_miau(event: dict) -> tuple[str, str, list[tuple[str, int]]]:
    scores = {label: 0 for label in CLASSES}
    hora_evento = datetime.strptime(event["hora"], "%H:%M").time()
    situacao = event["situacao_antes"].lower()

    if event["perto_porta"] == "sim":
        scores["pedido_porta"] += 5
    if event["tipo_miado"] in ["longo_crescente", "longo"]:
        scores["pedido_porta"] += 3
    if event["repeticao"] in ["insistente", "repetido"]:
        scores["pedido_porta"] += 2

    if event["perto_caixa"] == "sim":
        scores["caixa_areia_coco"] += 5
    if within_range(hora_evento, ROTINA["coco_manha_inicio"], ROTINA["coco_manha_fim"]):
        scores["caixa_areia_coco"] += 2
    if within_range(hora_evento, ROTINA["coco_noite_inicio"], ROTINA["coco_noite_fim"]):
        scores["caixa_areia_coco"] += 2

    if event["humanos_na_cama"] == "sim":
        scores["pedido_atencao"] += 4
    if within_range(hora_evento, ROTINA["acorda_inicio"], ROTINA["acorda_fim"]):
        scores["pedido_atencao"] += 2
    if within_range(hora_evento, ROTINA["dorme_inicio"], ROTINA["dorme_fim"]):
        scores["pedido_atencao"] += 3
    if event["tipo_miado"] == "resmungo":
        scores["pedido_atencao"] += 1

    if event["tipo_miado"] == "curto":
        scores["miado_atencao"] += 2
    if event["intensidade"] == "baixa":
        scores["miado_atencao"] += 2
    if event["repeticao"] in ["varios_miadinhos", "repetido"]:
        scores["miado_atencao"] += 3
    if "interacao" in situacao or "interação" in situacao:
        scores["miado_atencao"] += 2

    if event["ronronando"] == "sim":
        scores["miado_carinho"] += 5
    if event["tipo_miado"] in ["curto", "chamado"]:
        scores["miado_carinho"] += 1
    if "colo" in situacao or "contato" in situacao or "carinho" in situacao:
        scores["miado_carinho"] += 3

    if event["tipo_miado"] == "resmungo":
        scores["reclamacao_frustracao"] += 4
    if "cacando" in situacao or "caçando" in situacao:
        scores["reclamacao_frustracao"] += 3
    if "mandou descer" in situacao or "contrariada" in situacao:
        scores["reclamacao_frustracao"] += 3

    if nearest_meal_distance_minutes(hora_evento) <= 20:
        scores["indefinido"] += 1

    best_label = max(scores, key=scores.get)
    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    explanations = {
        "pedido_porta": "Hipótese principal: ela quer acesso a um ambiente. O padrão combina com miado de porta, mais longo e insistente.",
        "pedido_atencao": "Hipótese principal: ela quer atenção ou quer iniciar a rotina com vocês.",
        "miado_atencao": "Hipótese principal: ela quer atenção. Esse padrão combina com miado baixo em vários miadinhos curtos.",
        "miado_carinho": "Hipótese principal: ela está buscando carinho ou proximidade. O ronronado junto com o miado reforça essa hipótese.",
        "reclamacao_frustracao": "Hipótese principal: ela está reclamando ou frustrada com alguma interrupção ou tentativa de caçar.",
        "caixa_areia_coco": "Hipótese principal: miado associado ao uso da caixa, especialmente no horário em que isso costuma acontecer.",
        "indefinido": "Não há contexto suficiente para uma conclusão forte. Vale observar local e o que acontece logo depois.",
    }
    return best_label, explanations[best_label], ranking



def build_event_from_demo(sample_name: str, hora_str: str) -> dict:
    sample = DEMO_MIAUS[sample_name]
    agora = now_sp()
    return {
        "data": agora.strftime("%Y-%m-%d"),
        "hora": hora_str,
        "fonte": "demo",
        "local": sample["local"],
        "tipo_miado": sample["tipo_miado"],
        "intensidade": sample["intensidade"],
        "duracao": sample["duracao"],
        "repeticao": sample["repeticao"],
        "perto_porta": sample["perto_porta"],
        "perto_caixa": sample["perto_caixa"],
        "humanos_na_cama": sample["humanos_na_cama"],
        "ronronando": sample["ronronando"],
        "situacao_antes": sample["situacao_antes"],
    }



def suggest_sample_from_audio(audio) -> str:
    if not audio:
        return "Miado ao acordar"

    tamanho = getattr(audio, "size", 0)
    nome = getattr(audio, "name", "").lower()

    if "ogg" in nome or tamanho <= 25000:
        return "Miado de atencao"
    if 25001 <= tamanho <= 45000:
        return "Miado de reclamacao"
    if 45001 <= tamanho <= 70000:
        return "Miado de carinho"
    return "Miado de porta"


st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #0f172a 0%, #111827 100%);
    }
    .hero {
        padding: 1.2rem 1.4rem;
        border-radius: 22px;
        background: linear-gradient(135deg, rgba(168,85,247,.22), rgba(59,130,246,.16));
        border: 1px solid rgba(255,255,255,.08);
        margin-bottom: 1rem;
    }
    .card {
        padding: 1rem 1.1rem;
        border-radius: 18px;
        background: rgba(255,255,255,.04);
        border: 1px solid rgba(255,255,255,.06);
        margin-bottom: .8rem;
    }
    .small {
        font-size: 0.92rem;
        opacity: .9;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class='hero'>
        <h1>🐱 Nala Translator</h1>
        <p class='small'>Protótipo para interpretar miados com base em contexto, rotina e padrões provisórios. Nesta versão, o app já sugere automaticamente um tipo provável de miado ao receber um áudio.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

colA, colB = st.columns([1.4, 1])

with colA:
    st.markdown("### Teste rápido")
    modo = st.radio(
        "Como deseja testar?",
        ["Escolher um miado provisório", "Enviar um áudio"],
        horizontal=True,
    )

    agora = now_sp()
    hora_str = agora.strftime("%H:%M")
    st.caption(f"🕒 Horário automático: {hora_str}")

    if modo == "Escolher um miado provisório":
        sample_name = st.selectbox("Escolha o tipo de miado", list(DEMO_MIAUS.keys()))
        st.info("Use isso na apresentação de hoje. Depois você pode substituir por gravações reais da Nala.")
        event = build_event_from_demo(sample_name, hora_str)
    else:
        audio = st.file_uploader("Envie um áudio de miado", type=["wav", "mp3", "m4a", "ogg"])
        st.caption("Modelo simplificado de análise de áudio (heurístico). Em evolução para classificação real com features acústicas.")

        sample_name = "Miado ao acordar"  # valor padrão seguro

        if audio: sample_name = suggest_sample_from_audio(audio)
        st.success(f"🔍 Áudio analisado automaticamente → {sample_name}")

        usar_ajuste_manual = st.toggle("Ajustar previsão manualmente", value=False)

        if usar_ajuste_manual:
            sample_name = st.selectbox(
                "Tipo de miado",
                list(DEMO_MIAUS.keys()),
                index=list(DEMO_MIAUS.keys()).index(sample_name) if sample_name else 0,
            )

        event = build_event_from_demo(sample_name, hora_str)
        event["fonte"] = "audio_upload" if audio else "demo"

    if st.button("Interpretar miado", type="primary", use_container_width=True):
        classe, explicacao, ranking = classify_miau(event)

        st.markdown(
            f"""
            <div class='card'>
                <h3>Hipótese principal</h3>
                <h2>{classe}</h2>
                <p>{explicacao}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Ranking de hipóteses")
        ranking_df = pd.DataFrame(ranking, columns=["hipotese", "pontuacao"])
        st.dataframe(ranking_df, use_container_width=True, hide_index=True)

        save_event(
            {
                "data": agora.strftime("%Y-%m-%d"),
                "hora": hora_str,
                "fonte": event.get("fonte", "demo"),
                "local": event["local"],
                "tipo_miado": event["tipo_miado"],
                "intensidade": event["intensidade"],
                "duracao": event["duracao"],
                "repeticao": event["repeticao"],
                "perto_porta": event["perto_porta"],
                "perto_caixa": event["perto_caixa"],
                "humanos_na_cama": event["humanos_na_cama"],
                "ronronando": event["ronronando"],
                "situacao_antes": event["situacao_antes"],
                "classe_real": classe,
            }
        )

with colB:
    st.markdown("### Como o MVP funciona")
    st.markdown(
        """
        <div class='card'>
            <b>Hoje</b><br>
            O app usa contexto comportamental, rotina e amostras provisórias de miado.
        </div>
        <div class='card'>
            <b>Áudio</b><br>
            Quando você envia um áudio, o sistema sugere automaticamente um padrão inicial para acelerar a interpretação.
        </div>
        <div class='card'>
            <b>Próxima etapa</b><br>
            Trocar as amostras provisórias por gravações reais e extrair características do áudio.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Tipos já mapeados")
    st.write("- Miado de porta")
    st.write("- Miado ao acordar")
    st.write("- Miado na caixa")
    st.write("- Miado de reclamação")
    st.write("- Miado de atenção")
    st.write("- Miado de carinho")

st.markdown("---")

aba1, aba2 = st.tabs(["Eventos salvos", "Resumo"])

with aba1:
    df = load_data()
    st.dataframe(df, use_container_width=True, hide_index=True)

with aba2:
    df = load_data()
    resumo = df["classe_real"].value_counts().reset_index()
    resumo.columns = ["classe", "quantidade"]
    st.dataframe(resumo, use_container_width=True, hide_index=True)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("Baixar CSV", data=csv, file_name="nala_miados.csv", mime="text/csv")
