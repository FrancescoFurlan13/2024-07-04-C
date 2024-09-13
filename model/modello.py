from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        self._list_sightings = []
        self._directed_graph = nx.DiGraph()  # Grafo orientato

    def load_sightings(self):
        self._list_sightings = DAO.get_all_sightings()

    def get_years(self):
        # Estrai gli anni dagli avvistamenti e rimuovi duplicati
        years = set(sighting.datetime.year for sighting in self._list_sightings)

        # Ordina gli anni in ordine decrescente
        return sorted(years, reverse=True)

    def get_shapes_by_year(self, year: int):
        # Filtra le forme per l'anno selezionato, escludendo quelle vuote e ordinando alfabeticamente
        shapes = set(
            sighting.shape
            for sighting in self._list_sightings
            if sighting.datetime.year == year and sighting.shape and sighting.shape.strip()
        )
        return sorted(shapes)

    def build_weighted_graph(self, shape: str, year: int):
        # Filtra gli avvistamenti per anno e forma
        filtered_sightings = [s for s in self._list_sightings if s.datetime.year == year and s.shape == shape]

        # Aggiungi tutti gli avvistamenti come nodi, anche se non creano archi
        self._directed_graph.clear()
        for sighting in filtered_sightings:
            self._directed_graph.add_node(sighting)

        # Aggiungi gli archi tra avvistamenti nello stesso stato e con longitudine minore -> maggiore
        for sighting1 in filtered_sightings:
            for sighting2 in filtered_sightings:
                if sighting1.state == sighting2.state:
                    if sighting1.longitude < sighting2.longitude:
                        weight = abs(sighting2.longitude - sighting1.longitude)
                        self._directed_graph.add_edge(sighting1, sighting2, weight=weight)

    def get_num_of_nodes(self):
        # Restituisce il numero di vertici nel grafo
        return self._directed_graph.number_of_nodes()

    def get_num_of_edges(self):
        # Restituisce il numero di archi nel grafo
        return self._directed_graph.number_of_edges()

    def get_top_5_heaviest_edges(self):
        # Ordina gli archi per peso in ordine decrescente e restituisci i primi 5
        sorted_edges = sorted(self._directed_graph.edges(data=True), key=lambda e: e[2]['weight'], reverse=True)
        return sorted_edges[:5]