import streamlit as st

from ai_service import generate_recommendation
from graph_utils import (
    GRAPH_FILE,
    get_node,
    get_start_node,
    is_diagnosis,
    load_graph,
)


st.set_page_config(
    page_title="Cauca Avocado Assistant",
    page_icon="🥑",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 4em;
        background-color: #2e7d32;
        color: white;
        font-weight: bold;
        border: 2px solid #1b5e20;
    }

    .stButton>button:hover {
        background-color: #1b5e20;
        border: 2px solid #ffffff;
    }

    .stInfo {
        border-left: 6px solid #2e7d32;
        background-color: #f1f8e9;
        color: #1b5e20;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialize_state():
    """Initialize graph and session variables."""

    if "current_node_id" in st.session_state:
        return

    st.session_state.graph = load_graph(GRAPH_FILE)
    st.session_state.current_node_id = get_start_node(st.session_state.graph)
    st.session_state.history = []


def advance(option):
    """Move to the next node in the graph."""

    st.session_state.history.append(option["text"])
    st.session_state.current_node_id = option["destination"]


def restart_diagnosis():
    """Restart graph traversal."""

    st.session_state.current_node_id = get_start_node(st.session_state.graph)
    st.session_state.history = []


try:
    initialize_state()
except FileNotFoundError:
    st.error(f"Error: '{GRAPH_FILE}' file not found.")
    st.stop()


st.title("🥑 Avocado Disease Diagnosis System")
st.write("---")

node = get_node(
    st.session_state.graph,
    st.session_state.current_node_id,
)

options = node.get("options", [])

if st.session_state.history:
    st.caption("Decision path: " + " → ".join(st.session_state.history))

if not is_diagnosis(node):
    st.info(f"**Current question:** {node['text']}")
    st.write("### Select an option:")

    columns = st.columns(len(options))

    for index, option in enumerate(options):
        with columns[index]:
            if st.button(
                option["text"],
                key=f"btn_{index}_{st.session_state.current_node_id}",
            ):
                advance(option)
                st.rerun()
else:
    diagnosis = node.get("diagnosis", "Problem identified")
    treatments = node.get("treatment", [])

    st.success(f"Diagnosis result: {diagnosis}")

    with st.spinner("Generating management recommendations..."):
        try:
            recommendation = generate_recommendation(
                diagnosis,
                treatments,
                decision_path=st.session_state.history,
            )
            st.subheader("🌱 Management Plan")
            st.markdown(recommendation)
        except Exception as error:
            st.error(f"AI generation error: {error}")

st.divider()

if st.button("Restart Diagnosis", type="secondary"):
    restart_diagnosis()
    st.rerun()
