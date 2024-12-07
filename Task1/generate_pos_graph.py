import string
import networkx as nx
import re
import matplotlib.pyplot as plt
import spacy

class GeneratePosGraph:
    def __init__(self):
        self.extractor = spacy.load("en_core_web_sm")
        self.graph = nx.Graph()
    
    
    def clean_text(self, text):
        punctuation = string.punctuation
        text = text.lower()
        text = text.translate(str.maketrans("", "", punctuation))
        text = re.sub(r'\s+', ' ', text).strip()

        return text
    
    def pos_extractor(self, text):
        text = self.clean_text(text)
        doc = self.extractor(text)

        return doc
    
    def add_node2graph(self, text):
        doc = self.pos_extractor(text)
        all_pos = set([token.pos_ for token in doc])
        for pos in all_pos:
            self.graph.add_node(pos, color="pink")
        for token in doc:
            self.graph.add_node(token.text, color='cyan')
            self.graph.add_edge(token.text, token.pos_, relation="IS")
        
    def generate_graph(self, text:str):
        plt.figure(figsize=(12,12))
        self.add_node2graph(text)
        pos = nx.spring_layout(self.graph, k=.35)
        node_colors = [self.graph.nodes[node]["color"] for node in graph.nodes]

        nx.draw(self.graph,pos,
            with_labels=True,node_color=node_colors,
            node_size=800,font_size=10,font_color="black")

        edge_labels = nx.get_edge_attributes(self.graph, "relation")
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        plt.savefig("graph_image.png", format="PNG")
