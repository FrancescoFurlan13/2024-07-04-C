import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fill_year_dropdown(self):
        # Carica gli avvistamenti nel model
        self._model.load_sightings()

        # Ottieni gli anni ordinati dal model
        years = self._model.get_years()

        # Popola il menù a tendina con gli anni
        self._view.ddyear.options.clear()
        for year in years:
            self._view.ddyear.options.append(ft.dropdown.Option(str(year)))

        # Aggiorna la vista
        self._view.update_page()

    def fill_shape_dropdown(self, e=None):
        # Ottieni l'anno selezionato dal menù a tendina degli anni
        selected_year = int(self._view.ddyear.value)

        # Recupera le forme per l'anno selezionato
        shapes = self._model.get_shapes_by_year(selected_year)

        # Popola il menù a tendina con le forme
        self._view.ddshape.options.clear()
        for shape in shapes:
            self._view.ddshape.options.append(ft.dropdown.Option(shape))

        # Aggiorna la vista
        self._view.update_page()

    def handle_graph(self, e):
        #pulisco il risultato precedente
        self._view.txt_result1.controls.clear()
        # Ottieni l'anno e la forma selezionati
        selected_year = int(self._view.ddyear.value)
        selected_shape = self._view.ddshape.value

        # Costruisci il grafo pesato e orientato
        self._model.build_weighted_graph(selected_shape, selected_year)

        # Ottieni il numero di vertici e archi
        num_vertices = self._model.get_num_of_nodes()
        num_edges = self._model.get_num_of_edges()

        # Stampa numero di vertici e archi
        self._view.txt_result1.controls.append(ft.Text(f"Numero di vertici: {num_vertices}"))
        self._view.txt_result1.controls.append(ft.Text(f"Numero di archi: {num_edges}"))

        # Ottieni e stampa i 5 archi di peso maggiore
        top_5_edges = self._model.get_top_5_heaviest_edges()
        self._view.txt_result1.controls.append(ft.Text("I 5 archi di peso maggiore sono:"))

        for edge in top_5_edges:
            source = edge[0].id
            target = edge[1].id
            weight = edge[2]['weight']
            self._view.txt_result1.controls.append(ft.Text(f"{source} -> {target} | weight = {weight}"))

        # Aggiorna la vista
        self._view.update_page()

    def handle_path(self, e):
        pass
