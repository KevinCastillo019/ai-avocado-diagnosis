from ai_service import generate_recommendation
from graph_utils import (
    GRAPH_FILE,
    get_node,
    get_start_node,
    is_diagnosis,
    load_graph,
)


def explore():
    try:
        graph = load_graph(GRAPH_FILE)
    except FileNotFoundError:
        print(f"Error: graph file '{GRAPH_FILE}' not found.")
        return

    current_node_id = get_start_node(graph)
    decision_path = []

    while True:
        node = get_node(graph, current_node_id)

        if is_diagnosis(node):
            diagnosis = node.get("diagnosis", "")
            treatments = node.get("treatment", [])

            if decision_path:
                print("\nDecision path:")
                print(" -> ".join(decision_path))

            print("\n[AI] Generating recommendation...")

            try:
                recommendation = generate_recommendation(
                    diagnosis,
                    treatments,
                    decision_path=decision_path,
                    temperature=0.4,
                )
                print("\n--- Recommendation ---")
                print(recommendation)
            except Exception as error:
                print(f"Groq API error: {error}")

            break

        print(f"\nCurrent question: {node['text']}")

        options = node.get("options", [])

        print("\nSelect an option:")

        for index, option in enumerate(options, start=1):
            print(f"{index}. {option['text']}")

        while True:
            selected = input("Option number > ")

            if selected.isdigit() and 1 <= int(selected) <= len(options):
                option = options[int(selected) - 1]
                decision_path.append(option["text"])
                current_node_id = option["destination"]
                break

            print("Invalid option.")


if __name__ == "__main__":
    explore()
