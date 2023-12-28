import tkinter as tk
from tkinter import ttk

import networkx as nx
import osmnx as ox

import algoritmos as alg
from enchaminhamento import sort_encomendas, sort_estafetas, create_sections, route
from encomenda import Encomenda
from estafeta import Estafeta
import time

ENCOMENDAS = []
ESTAFETAS = []
GRAPH = nx.read_gml('./dados/grafo.gml')

class Application:
    def __init__(self, root):
        self.root = root
        self.root.title("Health Planet")
        self.root.geometry("500x500")
        self.current_frame = self.root

        # Adicionando a tela de boas-vindas com o logo
        self.logo_label = tk.Label(
            root, text="Health Planet", font=("Helvetica", 24))
        self.logo_label.pack(pady=50)

        # Adicionando um botão para continuar após o clique do usuário
        self.continuar_btn = ttk.Button(
            root, text="Clique para Continuar", command=self.mostrar_menu)
        self.continuar_btn.pack(pady=20)

        self.frame_menu_inicial = ttk.Frame(root)
        self.frame_menu_inicial.pack_forget()

        self.btn_criar_estafeta = ttk.Button(
            self.frame_menu_inicial, text='Criar estafeta', command=self.mostrar_estafeta)
        self.btn_criar_estafeta.pack(pady=10)

        self.btn_criar_encomenda = ttk.Button(
            self.frame_menu_inicial, text='Criar encomenda', command=self.mostrar_encomenda)
        self.btn_criar_encomenda.pack(pady=20)

        self.btn_algoritmos = ttk.Button(
            self.frame_menu_inicial, text="Executar algoritmos", command=self.mostrar_algoritmos)
        self.btn_algoritmos.pack(pady=30)

        # Inicialmente, ocultar o menu de escolha do algoritmo
        self.frame_algoritmos = ttk.Frame(root)
        self.frame_algoritmos.pack_forget()

        # Configurando o menu
        self.label = ttk.Label(self.frame_algoritmos, text="Escolha o algoritmo:")
        self.label.pack(pady=10)

        self.algoritmo_var = tk.StringVar()

        self.radio_dfs = ttk.Radiobutton(
            self.frame_algoritmos, text="DFS", variable=self.algoritmo_var, value="dfs")
        self.radio_dfs.pack()

        self.radio_bfs = ttk.Radiobutton(
            self.frame_algoritmos, text="BFS", variable=self.algoritmo_var, value="bfs")
        self.radio_bfs.pack()

        self.radio_dijkstra = ttk.Radiobutton(
            self.frame_algoritmos, text="Dijkstra", variable=self.algoritmo_var, value="dijkstra")
        self.radio_dijkstra.pack()

        self.radio_iddfs = ttk.Radiobutton(
            self.frame_algoritmos, text="IDDFS", variable=self.algoritmo_var, value="iddfs")
        self.radio_iddfs.pack()

        self.radio_bidirectional = ttk.Radiobutton(
            self.frame_algoritmos, text="Bidirectional", variable=self.algoritmo_var, value="bidirectional")
        self.radio_bidirectional.pack()

        self.radio_greedy = ttk.Radiobutton(self.frame_algoritmos, text="Greedy",
                                                   variable=self.algoritmo_var, value="greedy_search")
        self.radio_greedy.pack()

        self.radio_astar = ttk.Radiobutton(self.frame_algoritmos, text="A*",
                                                   variable=self.algoritmo_var, value="astar_search")
        self.radio_astar.pack()

        self.btn_executar = ttk.Button(
            self.frame_algoritmos, text="Executar", command=self.executar_algoritmo)
        self.btn_executar.pack(pady=10)

        self.btn_sair_algoritmos = ttk.Button(
            self.frame_algoritmos, text="Sair", command=self.mostrar_menu)
        self.btn_sair_algoritmos.pack(pady=10)

        self.frame_estafeta = ttk.Frame(root)
        self.frame_estafeta.pack_forget()

        self.enc_label = ttk.Label(self.frame_estafeta, text="Estafeta:")
        self.enc_label.pack(pady=10)

        self.var_estafeta = tk.StringVar()

        self.text_estafeta = tk.Text(self.frame_estafeta, height=1, width=20)
        self.text_estafeta.pack(pady=10)

        self.frame_encomenda = ttk.Frame(root)
        self.frame_encomenda.pack_forget()

        self.enco_label = ttk.Label(self.frame_encomenda, text="Encomenda:")
        self.enco_label.pack(pady=10)

        self.var_encomenda = tk.StringVar()

        self.text_encomenda1 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda1.pack(pady=10)

        self.text_encomenda2 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda2.pack(pady=10)

        self.text_encomenda3 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda3.pack(pady=10)

        self.text_encomenda4 = tk.Text(self.frame_encomenda, height=1, width=20)
        self.text_encomenda4.pack(pady=10)

        self.var_vehiculo = tk.IntVar()

        self.radio_bicycle = ttk.Radiobutton(
            self.frame_estafeta, text="Bicicleta", variable=self.var_vehiculo, value=1)
        self.radio_bicycle.pack()

        self.radio_bike = ttk.Radiobutton(
            self.frame_estafeta, text="Mota", variable=self.var_vehiculo, value=2)
        self.radio_bike.pack()

        self.radio_car = ttk.Radiobutton(
            self.frame_estafeta, text="Carro", variable=self.var_vehiculo, value=3)
        self.radio_car.pack()

        self.btn_criar_estafeta = ttk.Button(
            self.frame_estafeta, text="Criar", command=self.save_estafeta)
        self.btn_criar_estafeta.pack()

        self.btn_sair_estafeta = ttk.Button(
            self.frame_estafeta, text="Sair", command=self.mostrar_menu)
        self.btn_sair_estafeta.pack(pady=10)

        self.btn_criar_encomenda = ttk.Button(
            self.frame_encomenda, text="Criar encomenda", command=self.save_encomenda)
        self.btn_criar_encomenda.pack()

        self.btn_sair_encomenda = ttk.Button(
            self.frame_encomenda, text="Sair", command=self.mostrar_menu)
        self.btn_sair_encomenda.pack(pady=10)

    def mostrar_menu(self):
        # Esconder a tela de boas-vindas
        self.logo_label.pack_forget()
        self.continuar_btn.pack_forget()
        if self.current_frame != self.root:
            self.current_frame.pack_forget()

        self.current_frame = self.frame_menu_inicial
        # Mostrar o menu de escolha do algoritmo
        self.frame_menu_inicial.pack(pady=50)

    def mostrar_algoritmos(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_algoritmos
        self.frame_algoritmos.pack(pady=50)

    @staticmethod
    def seconds_to_hours_minutes(seconds):
        # Calculate hours and minutes
        hours, remainder = divmod(seconds, 3600)
        minutes, _ = divmod(remainder, 60)

        # Create a formatted string
        time_str = "{:02}:{:02}".format(int(hours), int(minutes))

        return time_str

    def executar_algoritmo(self):
        escolha = self.algoritmo_var.get()

        if escolha == "dfs":
            algorithm = alg.dfs
        elif escolha == "bfs":
            algorithm = alg.bfs
        elif escolha == "dijkstra":
            algorithm = alg.dijkstra
        elif escolha == "iddfs":
            algorithm = alg.iddfs
        elif escolha == "bidirectional":
            algorithm = alg.bidirectional
        elif escolha == "greedy_search":
            algorithm = alg.greedy_search
        elif escolha == "astar_search":
            algorithm = alg.astar_search    
        else:
            print("Escolha inválida.")
            return

        encomendas = sort_encomendas(GRAPH, ENCOMENDAS)
        estafetas = sort_estafetas(ESTAFETAS)
        start_time = time.time()
        s = create_sections(encomendas, estafetas)

        r, late = route(estafetas, s, algorithm, GRAPH)
        total_time = time.time() - start_time
        print("Realizou route")

        for section, rota in r.items():
            if len(rota) == 1:
                ox.plot_graph_route(GRAPH, rota[0], route_color='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                                    show=False, save=True, filepath=f"./routes/section_{section}.png")
            else:
                ox.plot_graph_routes(GRAPH, rota, route_colors='yellow', route_linewidth=6, node_size=0, route_alpha=1,
                                     show=False, save=True, filepath=f"./routes/section_{section}.png")

        for estafeta, (t_rating, late_encomendas, n_encomendas) in late.items():
            with open(f"./routes/{estafeta}_relatorio.txt", 'w') as f:
                lines = [f"Estafeta: {estafeta}\n", f"Numero de encomendas: {n_encomendas}\n"
                    , f"Rating: {format(t_rating / n_encomendas, '.2f')}\n", 'Encomendas atrasadas:\n']
                for enc, (delay, rating) in late_encomendas.items():
                    lines.append(f"Encomenda {enc}: {self.seconds_to_hours_minutes(delay)} (rating: {rating})\n")
                f.writelines(lines)

        with open(f"./routes/informacao.txt", 'w') as f:
            f.writelines([f"Algoritmo utilizado: {escolha}\n",
                          f"Tempo de processamento: {format(total_time, '.2f')} s"])

    def mostrar_estafeta(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_estafeta
        self.clean_estafeta_vars()
        self.frame_estafeta.pack(pady=50)

    def save_estafeta(self):
        vehiculo = self.var_vehiculo.get()
        nome = self.text_estafeta.get(1.0, "end-1c")
        if vehiculo != 0 and nome != '':
            ESTAFETAS.append(Estafeta(nome, vehiculo))
            self.clean_estafeta_vars()

    def clean_estafeta_vars(self):
        self.text_estafeta.delete("1.0", "end")
        self.var_vehiculo.set(0)

    def mostrar_encomenda(self):
        self.current_frame.pack_forget()
        self.current_frame = self.frame_encomenda
        self.clean_encomenda_vars()
        self.frame_encomenda.pack(pady=50)

    def save_encomenda(self):
        #self.text_encomenda
        Idnt = self.text_encomenda1.get(1.0, "end-1c")
        Client = self.text_encomenda2.get(1.0, "end-2c")
        Origem = self.text_encomenda3.get(1.0, "end-3c")
        Destino = self.text_encomenda4.get(1.0, "end-4c")
        if Client != '' and Origem != '' and Destino != '':
            ENCOMENDAS.append(Encomenda(Idnt, Client, Origem, Destino))
            self.clean_encomenda_vars()

    def clean_encomenda_vars(self):
        self.text_encomenda1.delete("1.0", "end")
        self.text_encomenda2.delete("1.0", "end")
        self.text_encomenda3.delete("1.0", "end")
        self.text_encomenda4.delete("1.0", "end")


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
