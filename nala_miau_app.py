import streamlit as st
import pandas as pd
from datetime import datetime, time
from pathlib import Path

st.set_page_config(page_title="Nala Translator", page_icon="🐱", layout="wide")

DATA_FILE = Path("nala_miados.csv")

# -----------------------------
# Base de conhecimento inicial
# -----------------------------
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
    "reclamacao_frustracao",
    "caixa_areia_coco",
    "indefinido",
]


def ensure_data_file() -> None:
    if not DATA_FILE.exists():
        demo_data = pd.DataFrame(
            [
                {
                    "data": "2026-04-16",
                    "hora": "06:00",
                    "local": "quarto",
                    "tipo_miado": "resmungo",
                    "intensidade": "baixa",
                    "duracao": "curta",
                    "repeticao": "repetido",
                    "perto_porta": "nao",
                    "perto_caixa": "nao",
                    "perto_comida": "nao",
                    "humanos_na_cama": "sim",
                    "situacao_antes": "humanos ainda dormindo",
                    "classe_real": "pedido_atencao",
                    "acao_tomada": "levantar",
                    "resultado": "parou de miar",
                },
                {
                    "data": "2026-04-16",
                    "hora": "20:10",
                    "local": "porta banheiro",
                    "tipo_miado": "longo_crescente",
                    "intensidade": "media",
                    "duracao": "longa",
                    "repeticao": "insistente",
                    "perto_porta": "sim",
                    "perto_caixa": "nao",
                    "perto_comida": "nao",
                    "humanos_na_cama": "nao",
                    "situacao_antes": "porta fechada",
                    "classe_real": "pedido_porta",
                    "acao_tomada": "abrir porta",
                    "resultado": "entrou e parou",
                },
                {
                    "data": "2026-04-16",
                    "hora": "07:25",
                    "local": "caixa",
                    "tipo_miado": "chamado",
                    "intensidade": "baixa",
                    "duracao": "curta",
                    "repeticao": "unico",
                    "perto_porta": "nao",
                    "perto_caixa": "sim",
                    "perto_comida": "nao",
                    "humanos_na_cama": "nao",
                    "situacao_antes": "entrou na caixa",
                    "classe_real": "caixa_areia_coco",
                    "acao_tomada": "observar",
                    "resultado": "terminou e saiu",
                },
                {
                    "data": "2026-04-16",
                    "hora": "22:05",
                    "local": "quarto",
                    "tipo_miado": "resmungo",
                    "intensidade": "baixa",
                    "duracao": "media",
                    "repeticao": "repetido",
                    "perto_porta": "nao",
                    "perto_caixa": "nao",
                    "perto_comida": "nao",
                    "humanos_na_cama": "nao",
                    "situacao_antes": "horario de dormir",
                    "classe_real": "pedido_atencao",
                    "acao_tomada": "ir para cama",
                    "resultado": "se acalmou",
                },
                {
                    "data": "2026-04-16",
                    "hora": "18:40",
                    "local": "quintal",
                    "tipo_miado": "resmungo",
                    "intensidade": "baixa",
                    "duracao": "curta",
                    "repeticao": "repetido",
                    "perto_porta": "nao",
                    "perto_caixa": "nao",
                    "perto_comida": "nao",
                    "humanos_na_cama": "nao",
                    "situacao_antes": "cacando e frustrada",
                    "classe_real": "reclamacao_frustracao",
                    "acao_tomada": "observar",
                    "resultado": "continuou agitada",
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


# -----------------------------
# Funções auxiliares
# -----------------------------
def to_minutes(t: time) -> int:
    return t.hour * 60 + t.minute


def now_minutes(t: time) -> int:
    return to_minutes(t)


def within_range(current: time, start: time, end: time) -> bool:
    cm = now_minutes(current)
    sm = to_minutes(start)
    em = to_minutes(end)
    return sm <= cm <= em


def nearest_meal_distance_minutes(current: time) -> int:
    cm = now_minutes(current)
    return min(abs(cm - to_minutes(meal)) for meal in ROTINA["comidas"])


def classify_miau(event: dict) -> tuple[str, str, list[tuple[str, int]]]:
    scores = {label: 0 for label in CLASSES}
    hora_evento = datetime.strptime(event["hora"], "%H:%M").time()

    # Regra 1: porta
    if event["perto_porta"] == "sim":
        scores["pedido_porta"] += 5
    if event["tipo_miado"] in ["longo_crescente", "longo"]:
        scores["pedido_porta"] += 3
    if event["repeticao"] in ["insistente", "repetido"]:
        scores["pedido_porta"] += 2

    # Regra 2: caixa de areia
    if event["perto_caixa"] == "sim":
        scores["caixa_areia_coco"] += 5
    if within_range(hora_evento, ROTINA["coco_manha_inicio"], ROTINA["coco_manha_fim"]):
        scores["caixa_areia_coco"] += 2
    if within_range(hora_evento, ROTINA["coco_noite_inicio"], ROTINA["coco_noite_fim"]):
        scores["caixa_areia_coco"] += 2

    # Regra 3: atenção ao acordar / dormir
    if event["humanos_na_cama"] == "sim":
        scores["pedido_atencao"] += 4
    if within_range(hora_evento, ROTINA["acorda_inicio"], ROTINA["acorda_fim"]):
        scores["pedido_atencao"] += 2
    if within_range(hora_evento, ROTINA["dorme_inicio"], ROTINA["dorme_fim"]):
        scores["pedido_atencao"] += 3
    if event["tipo_miado"] == "resmungo":
        scores["pedido_atencao"] += 1

    # Regra 4: reclamação / frustração
    if event["tipo_miado"] == "resmungo":
        scores["reclamacao_frustracao"] += 4
    if "cacando" in event["situacao_antes"].lower() or "caçando" in event["situacao_antes"].lower():
        scores["reclamacao_frustracao"] += 3
    if "mandou descer" in event["situacao_antes"].lower() or "contrariada" in event["situacao_antes"].lower():
        scores["reclamacao_frustracao"] += 3

    # Fome não é prioridade para Nala, então apenas observação contextual
    if nearest_meal_distance_minutes(hora_evento) <= 20:
        scores["indefinido"] += 1

    best_label = max(scores, key=scores.get)
    ranking = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    explanations = {
        "pedido_porta": "Miado compatível com pedido de acesso, principalmente por estar perto da porta e apresentar padrão longo/crescente.",
        "pedido_atencao": "Miado compatível com busca por atenção, especialmente por ocorrer em horário sensível da rotina dela.",
        "reclamacao_frustracao": "Miado compatível com reclamação ou frustração, principalmente pelo padrão de resmungo e contexto descrito.",
        "caixa_areia_coco": "Miado compatível com o comportamento já observado durante o uso da caixa de areia para cocô.",
        "indefinido": "Não há sinais suficientes para uma hipótese forte; o ideal é observar contexto e reação após sua ação.",
    }

    return best_label, explanations[best_label], ranking


# -----------------------------
# Interface
# -----------------------------
st.title("🐱 Nala Translator")
st.caption("Protótipo de interpretação de miados com base em contexto e regras comportamentais.")

with st.sidebar:
    st.header("Sobre a Nala")
    st.write("**Idade:** 5 meses")
    st.write("**Perfil:** carente ao acordar/dormir e quando vocês chegam em casa")
    st.write("**Rotina ativa:** 19h às 22h")
    st.write("**Dorme:** 22h às 23h")
    st.write("**Cocô:** 7h–8h e 19h–21h")
    st.info("Neste MVP, a previsão é feita por regras. Depois você pode evoluir para modelo com áudio real.")

aba1, aba2, aba3 = st.tabs(["Interpretar miado", "Registrar evento", "Base de dados"])

with aba1:
    st.subheader("Fazer previsão rápida")
    col1, col2 = st.columns(2)

    with col1:
        data_evento = st.date_input("Data", value=datetime.today().date())
        hora_evento = st.time_input("Hora", value=datetime.now().time().replace(second=0, microsecond=0))
        local = st.selectbox("Local", ["quarto", "banheiro", "porta banheiro", "porta quarto", "caixa", "sala", "quintal", "outro"])
        tipo_miado = st.selectbox("Tipo de miado", ["resmungo", "curto", "longo", "longo_crescente", "chamado", "outro"])
        intensidade = st.selectbox("Intensidade", ["baixa", "media", "alta"])

    with col2:
        duracao = st.selectbox("Duração", ["curta", "media", "longa"])
        repeticao = st.selectbox("Repetição", ["unico", "repetido", "insistente"])
        perto_porta = st.radio("Perto da porta?", ["sim", "nao"], horizontal=True)
        perto_caixa = st.radio("Perto da caixa?", ["sim", "nao"], horizontal=True)
        humanos_na_cama = st.radio("Humanos ainda na cama?", ["sim", "nao"], horizontal=True)

    situacao_antes = st.text_input(
        "Situação anterior",
        placeholder="Ex.: porta fechada, caçando, horário de dormir, vocês ainda estavam dormindo..."
    )

    if st.button("Interpretar agora", type="primary"):
        event = {
            "data": str(data_evento),
            "hora": hora_evento.strftime("%H:%M"),
            "local": local,
            "tipo_miado": tipo_miado,
            "intensidade": intensidade,
            "duracao": duracao,
            "repeticao": repeticao,
            "perto_porta": perto_porta,
            "perto_caixa": perto_caixa,
            "perto_comida": "nao",
            "humanos_na_cama": humanos_na_cama,
            "situacao_antes": situacao_antes or "sem contexto informado",
        }
        classe, explicacao, ranking = classify_miau(event)

        st.success(f"Hipótese principal: **{classe}**")
        st.write(explicacao)
        st.write("### Ranking de hipóteses")
        ranking_df = pd.DataFrame(ranking, columns=["hipotese", "pontuacao"])
        st.dataframe(ranking_df, use_container_width=True)

with aba2:
    st.subheader("Registrar evento observado")
    with st.form("registro_form"):
        c1, c2 = st.columns(2)
        with c1:
            data_reg = st.date_input("Data do evento", value=datetime.today().date(), key="reg_data")
            hora_reg = st.time_input("Hora do evento", value=datetime.now().time().replace(second=0, microsecond=0), key="reg_hora")
            local_reg = st.selectbox("Local", ["quarto", "banheiro", "porta banheiro", "porta quarto", "caixa", "sala", "quintal", "outro"], key="reg_local")
            tipo_reg = st.selectbox("Tipo de miado", ["resmungo", "curto", "longo", "longo_crescente", "chamado", "outro"], key="reg_tipo")
            intensidade_reg = st.selectbox("Intensidade", ["baixa", "media", "alta"], key="reg_intensidade")
        with c2:
            duracao_reg = st.selectbox("Duração", ["curta", "media", "longa"], key="reg_duracao")
            repeticao_reg = st.selectbox("Repetição", ["unico", "repetido", "insistente"], key="reg_repeticao")
            perto_porta_reg = st.radio("Perto da porta?", ["sim", "nao"], horizontal=True, key="reg_porta")
            perto_caixa_reg = st.radio("Perto da caixa?", ["sim", "nao"], horizontal=True, key="reg_caixa")
            humanos_cama_reg = st.radio("Humanos na cama?", ["sim", "nao"], horizontal=True, key="reg_cama")

        situacao_reg = st.text_input("Situação anterior", key="reg_situacao")
        classe_real_reg = st.selectbox("Classe real observada", CLASSES, key="reg_classe")
        acao_reg = st.text_input("Ação tomada", placeholder="Ex.: abrir porta, levantar, observar", key="reg_acao")
        resultado_reg = st.text_input("Resultado", placeholder="Ex.: parou de miar, entrou no quarto", key="reg_resultado")

        enviado = st.form_submit_button("Salvar evento")
        if enviado:
            row = {
                "data": str(data_reg),
                "hora": hora_reg.strftime("%H:%M"),
                "local": local_reg,
                "tipo_miado": tipo_reg,
                "intensidade": intensidade_reg,
                "duracao": duracao_reg,
                "repeticao": repeticao_reg,
                "perto_porta": perto_porta_reg,
                "perto_caixa": perto_caixa_reg,
                "perto_comida": "nao",
                "humanos_na_cama": humanos_cama_reg,
                "situacao_antes": situacao_reg or "sem contexto informado",
                "classe_real": classe_real_reg,
                "acao_tomada": acao_reg,
                "resultado": resultado_reg,
            }
            save_event(row)
            st.success("Evento salvo com sucesso no CSV do projeto.")

with aba3:
    st.subheader("Base atual")
    df = load_data()
    st.dataframe(df, use_container_width=True)

    st.write("### Resumo por classe")
    if not df.empty:
        resumo = df["classe_real"].value_counts().reset_index()
        resumo.columns = ["classe", "quantidade"]
        st.dataframe(resumo, use_container_width=True)
    else:
        st.info("Sem dados ainda.")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar base CSV",
        data=csv,
        file_name="nala_miados.csv",
        mime="text/csv",
    )
