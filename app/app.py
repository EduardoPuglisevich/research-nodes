from flask import Flask, render_template,request
import pandas as pd
import networkx as nx
import json
from networkx.readwrite import json_graph
import numpy as np

app = Flask(__name__)

df = pd.read_csv('data/data_clean.csv')
titles = df['Title'].values
ids = df['ID'].values
titles = list(zip(ids,titles))
titles_top5_pr= df.sort_values(by='pagerank', ascending=False).head(5)['Title'].values
ids_top5_pr = df.sort_values(by='pagerank', ascending=False).head(5)['ID'].values
titles_top5_pr = list(zip(ids_top5_pr,titles_top5_pr))

with open('data/graph.json', 'r') as f:
    data = json.load(f)
G = json_graph.node_link_graph(data)
print(G)

def create_weighted_subgraph(G, node, depth, visited=None,threshold=0):
    if visited is None:
        visited = set()
    subgraph = nx.Graph()
    subgraph.add_node(node)
    visited.add(node)
    if depth == 0:
        return subgraph
    neighbors = list(G.neighbors(node))
    for neighbor in neighbors:
        if neighbor not in visited:
            weight = G[node][neighbor]['weight']
            if weight > threshold:
                subgraph.add_node(neighbor)
                subgraph.add_edge(node, neighbor, weight=weight)
                subgraph = nx.compose(subgraph, create_weighted_subgraph(G, neighbor, depth-1, visited,threshold))
    return subgraph


@app.route('/')
def index():
    
    nodes = [
        {"id": "A", "group": 2},
        {"id": "B", "group": 2},
        {"id": "C", "group": 1},
        {"id": "D", "group": 1},
        {"id": "E", "group": 1},
        {"id": "F", "group": 2},
    ]
    links = [
        {"source": "A", "target": "B"},
        {"source": "A", "target": "C"},
        {"source": "C", "target": "E"},
        {"source": "C", "target": "D"},
        {"source": "D", "target": "E"},
        {"source": "A", "target": "F"},
        {"source": "F", "target": "B"},
    ]
    
    return render_template('index.html', nodes=nodes, links=links,titles =titles_top5_pr)

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/graph', methods=['POST', 'GET'])
def graph():
    recomended_titles = []
    recomended_titles_community = []
    node = 0
    nodes = []
    links = []
    if request.method == 'POST':
        node = int(request.form['node'])
        community = df.loc[df['ID'] == node, 'community'].values[0]
        depth = 1
        threshold = float(request.form['threshold'])
        subgraph = create_weighted_subgraph(G, node, depth,threshold=threshold)
        data = json_graph.node_link_data(subgraph)
        edges = subgraph.edges(data=True)
        sorted_edges = sorted(edges, key=lambda x: x[2]['weight'], reverse=True)
        top_nodes = set()
        for edge in sorted_edges:
            if len(top_nodes) >= 5:
                break
            if edge[0] == node:
                top_nodes.add(edge[1])
            else:
                top_nodes.add(edge[0])
        recomended_titles = df[df['ID'].isin(top_nodes)]['Title'].values
        ids_recomended_titles = df[df['ID'].isin(top_nodes)]['ID'].values
        recomended_titles = list(zip(ids_recomended_titles,recomended_titles))
        
        recomended_titles_community = df[df['community'] == community].sort_values(by='closeness_by_community', ascending=False).head(5)['Title'].values
        ids_recomended_titles_community = df[df['community'] == community].sort_values(by='closeness_by_community', ascending=False).head(5)['ID'].values
        recomended_titles_community = list(zip(ids_recomended_titles_community,recomended_titles_community))
       
        nodes = [{"id": node, "group": str(df.loc[df['ID'] == node, 'community'].values[0])} for node in subgraph.nodes]
        links = data['links']
        print(len(nodes))
    if node != 0:
        node = df.loc[df['ID'] == node, 'Title'].values[0]
    else:
        node = None
    return render_template('graph.html', node=node,articles=titles, titles =recomended_titles, nodes=nodes, links=links, titles_community = recomended_titles_community)

