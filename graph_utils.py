import json
from pathlib import Path


GRAPH_FILE = "data.json"


def load_graph(file_path=GRAPH_FILE):
    """Load the graph file and normalize it to a single internal schema."""

    path = Path(file_path)

    with path.open(encoding="utf-8") as file:
        raw_graph = json.load(file)

    return {
        "start": raw_graph.get("inicio", raw_graph.get("start")),
        "nodes": {
            node_id: _normalize_node(node)
            for node_id, node in raw_graph.get("nodos", raw_graph.get("nodes", {})).items()
        },
    }


def get_node(graph, node_id):
    return graph["nodes"][node_id]


def get_start_node(graph):
    return graph["start"]


def is_diagnosis(node):
    return node.get("type") == "diagnosis"


def _normalize_node(node):
    normalized_node = {
        "id": node.get("id"),
        "type": _normalize_type(node.get("tipo", node.get("type"))),
    }

    if "texto" in node or "text" in node:
        normalized_node["text"] = node.get("texto", node.get("text", ""))

    if "opciones" in node or "options" in node:
        normalized_node["options"] = [
            {
                "text": option.get("texto", option.get("text", "")),
                "destination": option.get(
                    "destino",
                    option.get("destination"),
                ),
            }
            for option in node.get("opciones", node.get("options", []))
        ]

    if "diagnostico" in node or "diagnosis" in node:
        normalized_node["diagnosis"] = node.get(
            "diagnostico",
            node.get("diagnosis", ""),
        )

    if "tratamiento" in node or "treatment" in node:
        normalized_node["treatment"] = node.get(
            "tratamiento",
            node.get("treatment", []),
        )

    return normalized_node


def _normalize_type(node_type):
    if node_type == "diagnostico":
        return "diagnosis"

    if node_type == "pregunta":
        return "question"

    return node_type


def cargar_grafo(ruta_archivo=GRAPH_FILE):
    return load_graph(ruta_archivo)


def obtener_nodo(grafo, nodo_id):
    return get_node(grafo, nodo_id)


def obtener_inicio(grafo):
    return get_start_node(grafo)


def es_diagnostico(nodo):
    return is_diagnosis(nodo)
