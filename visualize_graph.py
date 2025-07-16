import pandas as pd
import networkx as nx
import plotly.graph_objects as go

def create_graph_visualization():
    try:
        # Lire les fichiers Parquet
        entities_df = pd.read_parquet("./graphrag_index/output/entities.parquet")
        relationships_df = pd.read_parquet("./graphrag_index/output/relationships.parquet")
        communities_df = pd.read_parquet("./graphrag_index/output/communities.parquet")
        print("Colonnes disponibles dans relationships_df:")
        print(relationships_df.columns.tolist())
        print(relationships_df["target"].head())
        # Créer un graphe dirigé
        G = nx.DiGraph()

        # Ajouter les nœuds (entités)
        for _, entity in entities_df.iterrows():
            G.add_node(entity['id'], 
                      title=entity['title'],
                      type=entity['type'])

        # Ajouter les arêtes (relations)
        for _, rel in relationships_df.iterrows():
            G.add_edge(rel['source'], 
                      rel['target'],
                      type=rel['type'])

        # Calculer la disposition du graphe
        pos = nx.spring_layout(G, k=1, iterations=50)

        # Préparer les données pour la visualisation
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])

        # Créer les traces pour les arêtes
        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        # Préparer les données des nœuds
        node_x = []
        node_y = []
        node_text = []
        node_color = []

        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            # Créer le texte pour le hover
            node_info = f"Title: {G.nodes[node]['title']}<br>Type: {G.nodes[node]['type']}"
            node_text.append(node_info)
            # Couleur basée sur le type
            node_color.append(hash(G.nodes[node]['type']) % 20)

        # Créer les traces pour les nœuds
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text=node_text,
            marker=dict(
                showscale=True,
                colorscale='Viridis',
                size=10,
                color=node_color,
                line_width=2))

        # Créer la figure
        fig = go.Figure(data=[edge_trace, node_trace],
                     layout=go.Layout(
                        title='Visualisation du Graphe GraphRAG',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )

        # Sauvegarder la visualisation en HTML
        fig.write_html("graph_visualization.html")
        print("Visualisation créée avec succès! Ouvrez 'graph_visualization.html' dans votre navigateur.")

    except FileNotFoundError:
        print("Erreur: Les fichiers Parquet n'ont pas été trouvés. Vérifiez les chemins d'accès.")
        print("Chemin recherché: ./graphrag_index/output/")
    except Exception as e:
        print(f"Une erreur s'est produite: {str(e)}")

if __name__ == "__main__":
    create_graph_visualization()
