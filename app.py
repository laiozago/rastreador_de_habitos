# %% [markdown]
# # IMPORTS

# %%
import json
import tkinter
from tkinter import ttk
import os
import unicodedata
from datetime import datetime, timedelta
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# %% [markdown]
# ## Lista de hábitos carregados do arquivo
# ### Inicializa a lista de hábitos

# %%
habitos = []    

# %% [markdown]
# ## Caminho do arquivo JSON
# ### Define o caminho do arquivo JSON onde os hábitos serão salvos

# %%
ARQUIVO_HABITOS = os.path.join(os.getcwd(), "habitos.json")

# %% [markdown]
# # Funções

# %% [markdown]
# ## Carrega os hábitos do arquivo JSON

# %%
def carregar_habitos():
    global habitos
    if os.path.exists(ARQUIVO_HABITOS):
        with open(ARQUIVO_HABITOS, "r") as arquivo:
            habitos = json.load(arquivo)
    else:
        habitos = []

# %% [markdown]
# # Mostra uma mensagem em uma janela Tkinter

# %%
def mostrar_mensagem(titulo, mensagem):
    janela = tkinter.Tk()
    janela.title(titulo)
    janela.geometry("450x200")  # Define o tamanho da janela (largura x altura)

    label = tkinter.Label(janela, text=mensagem, font=("Arial", 12), padx=10, pady=10)
    label.pack(expand=True)

    btn_ok = tkinter.Button(janela, text="OK", command=janela.destroy)
    btn_ok.pack(ipady=10, ipadx=30)
    btn_ok.configure(background="#e0e0e0", foreground="black")

    janela.mainloop()

# %% [markdown]
# # Salva os hábitos no arquivo JSON

# %%
def salvar_habitos_no_arquivo():
    with open(ARQUIVO_HABITOS, "w") as arquivo:
        json.dump(habitos, arquivo, indent=4)

# %% [markdown]
# # Atualiza a área de texto com a lista de hábitos

# %%
def atualizar_output():
    output_habitos.delete("1.0", tkinter.END)
    for h in habitos:
        output_habitos.insert(tkinter.END, f"{h['nome']}\n")

# %% [markdown]
# # Adiciona um novo hábito

# %%
def novo_habito():
    global habito, output_habitos, btn_salvar

    # Remove widgets antigos (exceto o menu)
    for widget in janela.winfo_children():
        if getattr(widget, "is_menu", False) is False:
            widget.grid_remove()

    # Campo para adicionar novo hábito
    habito = tkinter.Entry(janela)
    habito.focus_set()
    habito.grid(row=1, column=1, padx=10, pady=5)

    #Enter chama a função salvar_habito()
    habito.bind("<Return>", lambda event: salvar_habito())

    #Botão de salvar
    btn_salvar = tkinter.Button(janela, text="SALVAR", command=salvar_habito)
    btn_salvar.grid(row=1, column=2, padx=10, pady=5)

    # Área para exibir os hábitos (se ainda não existir)
    if not hasattr(novo_habito, "output_habitos") or novo_habito.output_habitos is None:
        output_habitos = tkinter.Text(janela, height=10, width=40, padx=10)
        output_habitos.grid(row=2, column=1, columnspan=2, pady=10)
    else:
        novo_habito.output_habitos = output_habitos
 
    atualizar_output()  # Mostra os hábitos cadastrados

# %% [markdown]
# # Remove acentos e converte para minúsculas

# %%
def normalizar_texto(texto):
    texto = unicodedata.normalize('NFD', texto)
    texto = texto.encode('ascii', 'ignore').decode('utf-8')
    return texto.lower().strip()

# %% [markdown]
# # Salva um novo hábito na lista e no arquivo JSON

# %%
def salvar_habito():
    global habitos, output_habitos
    
    habito_texto = habito.get()
    if habito_texto.strip():
        habito_normalizado = normalizar_texto(habito_texto)
        habitos_normalizados = [normalizar_texto(h['nome']) for h in habitos]
        if habito_normalizado in habitos_normalizados:
            mostrar_mensagem("Atenção", "Este hábito já foi cadastrado.")
        else:
            habitos.append({"nome": habito_texto, "datas":[]})
            salvar_habitos_no_arquivo()
            atualizar_output()
            habito.delete(0, tkinter.END)
    else:
        mostrar_mensagem("Atenção", "O campo está vazio. Por favor, insira um hábito válido.")

# %% [markdown]
# # Registra o progresso dos hábitos

# %%
def registrar_progresso():
    global check_vars  # Dicionário para armazenar variáveis dos Checkbuttons
    check_vars = {}

    # Remove widgets antigos (exceto o menu)
    for widget in janela.winfo_children():
        if getattr(widget, "is_menu", False) is False:
            widget.grid_remove()

    # Lista de hábitos com Checkbuttons em até 4 colunas por linha
    max_colunas = 4
    linha = 1
    coluna = 0

    for i, habito in enumerate(habitos):
        var = tkinter.IntVar()
        check = tkinter.Checkbutton(janela, text=habito['nome'], variable=var)
        check.grid(row=linha, column=coluna + 1, sticky="w", padx=10, pady=5)
        check_vars[habito['nome']] = var

        # Atualiza a posição para a próxima célula
        coluna += 1
        if coluna >= max_colunas:  # Move para a próxima linha se atingir o limite de colunas
            coluna = 0
            linha += 1
        
    # Botões para registrar e deletar alinhados ao botão SAIR
    if linha > 3:
        linha += 1  # Ajusta para ficar logo abaixo da última linha de hábitos
        btn_registrar = tkinter.Button(janela, text="REGISTRAR", command=registrar)
        btn_registrar.grid(row=linha, column=1, columnspan=2, pady=20, padx=40)

        btn_deletar = tkinter.Button(janela, text="DELETAR", command=deletar)
        btn_deletar.grid(row=linha, column=2, columnspan=2, pady=20, padx=40)
    else:
        btn_deletar = tkinter.Button(janela, text="REGISTRAR", command=registrar)
        btn_deletar.grid(row=4, column=1, columnspan=2, pady=20, padx=40)

        btn_deletar = tkinter.Button(janela, text="DELETAR", command=deletar)
        btn_deletar.grid(row=4, column=3, columnspan=2, pady=20, padx=40)
     
    # Alinha com o botão SAIR
    janela.update_idletasks()


# %% [markdown]
# # Registra o progresso dos hábitos selecionados

# %%
def registrar():
    global habitos, check_vars
    data_hoje = datetime.today().date().isoformat()  # Data atual

    # Adiciona a data ao progresso dos hábitos selecionados
    for habito in habitos:
        if check_vars[habito['nome']].get() == 1:  # Se o Checkbutton estiver marcado
            if 'datas' not in habito:
                habito['datas'] = []
            if data_hoje not in habito['datas']:
                habito['datas'].append(data_hoje)

    salvar_habitos_no_arquivo()  # Salva o progresso
    mostrar_mensagem("Progresso Registrado", "Progresso registrado com sucesso!")

    # Atualiza a interface
    registrar_progresso()
            

# %% [markdown]
# # Deleta hábitos selecionados

# %%
def deletar():
    global habitos, check_vars

    # Encontra os hábitos selecionados para deletar
    habitos_a_remover = [h for h in habitos if check_vars[h['nome']].get() == 1]

    # Remove os hábitos selecionados da lista
    habitos = [h for h in habitos if h not in habitos_a_remover]

    # Salva os hábitos atualizados no arquivo
    salvar_habitos_no_arquivo()

    # Atualiza a interface
    registrar_progresso()

# %% [markdown]
# # Ver estatísticas dos hábitos

# %%
def ver_estatisticas():
    global check_vars  # Dicionário para armazenar variáveis dos Checkbuttons
    check_vars = {}

    # Remove widgets antigos (exceto o menu)
    for widget in janela.winfo_children():
        if getattr(widget, "is_menu", False) is False:
            widget.grid_remove()

    # Lista de hábitos com Checkbuttons em até 4 colunas por linha
    max_colunas = 4
    linha = 1
    coluna = 0

    for i, habito in enumerate(habitos):
        var = tkinter.IntVar()
        check = tkinter.Checkbutton(janela, text=habito['nome'], variable=var)
        check.grid(row=linha, column=coluna + 1, sticky="w", padx=10, pady=5)
        check_vars[habito['nome']] = var

        # Atualiza a posição para a próxima célula
        coluna += 1
        if coluna >= max_colunas:  # Move para a próxima linha se atingir o limite de colunas
            coluna = 0
            linha += 1
        
    # Botao para ver estatistica
    if linha > 3:
        linha += 1  # Ajusta para ficar logo abaixo da última linha de hábitos
        btn_mostrar = tkinter.Button(janela, text="MOSTRAR", command=mostrar)
        btn_mostrar.grid(row=linha, column=1, columnspan=2, ipady=20, ipadx=40)
    else:
        btn_mostrar = tkinter.Button(janela, text="MOSTRAR", command=mostrar)
        btn_mostrar.grid(row=4, column=1, columnspan=2, ipady=20, ipadx=40)
     
    # Alinha com o botão SAIR
    janela.update_idletasks()

# %% [markdown]
# # Mostra o progresso de um hábito

# %%
def encontrar_ultima_sequencia_consecutiva(dias_praticados):
    """ Encontra a última sequência de dias consecutivos na lista. """
    if not dias_praticados:
        return [], 0

    # Converte strings de datas para objetos datetime e ordena
    dias_praticados = sorted([datetime.strptime(d, "%Y-%m-%d") for d in dias_praticados])

    ultima_seq = []
    temp_seq = [dias_praticados[0]]

    for i in range(1, len(dias_praticados)):
        if (dias_praticados[i] - dias_praticados[i - 1]).days == 1:
            temp_seq.append(dias_praticados[i])
        else:
            # Quando há uma interrupção, reinicia a sequência
            ultima_seq = temp_seq  # Armazena a última sequência encontrada
            temp_seq = [dias_praticados[i]]

    # A última sequência verificada é a mais recente
    ultima_seq = temp_seq  

    return ultima_seq, len(ultima_seq)

# %%
def mostrar_progresso(habito_nome, dias_praticados, objetivo=45):
    """
    Exibe o progresso do hábito considerando apenas a última sequência ininterrupta.
    :param habito_nome: Nome do hábito
    :param dias_praticados: Lista de dias em que o hábito foi praticado (strings no formato 'YYYY-MM-DD')
    :param objetivo: Objetivo total de dias consecutivos
    """
    # Obtém a última sequência ininterrupta de dias praticados
    ultima_sequencia, total_dias = encontrar_ultima_sequencia_consecutiva(dias_praticados)

    progresso_percentual = (total_dias / objetivo) * 100
    dias_faltantes = max(0, objetivo - total_dias)

    # Datas inicial e final da última sequência
    data_inicial = ultima_sequencia[0].strftime("%d/%m/%Y") if ultima_sequencia else "N/A"
    data_final = ultima_sequencia[-1].strftime("%d/%m/%Y") if ultima_sequencia else "N/A"

    # Cria a janela principal
    janela = tkinter.Tk()
    janela.title(habito_nome)
    janela.geometry("800x400")

    # Configura o gráfico
    fig = Figure(figsize=(8, 1.5), dpi=100)
    ax = fig.add_subplot(111)

    # Cria a barra de progresso
    ax.barh(0, total_dias, color='green', height=0.3, label=f"{progresso_percentual:.1f}%")
    ax.barh(0, objetivo, color='lightgray', height=0.3, alpha=0.5)

    # Estiliza o gráfico
    ax.set_xlim(0, objetivo)
    ax.set_yticks([])
    ax.set_title("Progresso do Hábito", fontsize=16)
    ax.set_xlabel("Dias Consecutivos", fontsize=12)
    ax.legend(loc="upper right")

    # Insere o gráfico no Tkinter
    canvas = FigureCanvasTkAgg(fig, master=janela)
    canvas.get_tk_widget().pack(fill=tkinter.BOTH, expand=True)
    canvas.draw()

    # Adiciona informações abaixo do gráfico
    info_frame = tkinter.Frame(janela)
    info_frame.pack(fill=tkinter.BOTH, expand=True, pady=10)

    # Elementos da primeira coluna
    tkinter.Label(info_frame, text="Data Inicial:", font=("Arial", 12)).grid(row=0, column=0, sticky="w", padx=10)
    tkinter.Label(info_frame, text="Data Final:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=10)

    # Elementos da segunda coluna
    tkinter.Label(info_frame, text="Total de Dias:", font=("Arial", 12)).grid(row=0, column=2, sticky="w", padx=10)
    tkinter.Label(info_frame, text="Dias Restantes:", font=("Arial", 12)).grid(row=1, column=2, sticky="w", padx=10)

    # Valores das informações
    tkinter.Label(info_frame, text=data_inicial, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="w", padx=10)
    tkinter.Label(info_frame, text=data_final, font=("Arial", 12, "bold")).grid(row=1, column=1, sticky="w", padx=10)
    tkinter.Label(info_frame, text=total_dias, font=("Arial", 12, "bold")).grid(row=0, column=3, sticky="w", padx=10)
    tkinter.Label(info_frame, text=dias_faltantes, font=("Arial", 12, "bold")).grid(row=1, column=3, sticky="w", padx=10)

    # Botão para fechar a janela
    btn_fechar = tkinter.Button(janela, text="FECHAR", command=janela.destroy)
    btn_fechar.pack(ipady=10, ipadx=30)

    # Inicia o loop da interface gráfica
    janela.mainloop()

# %% [markdown]
# # Mostra os hábitos selecionados

# %%
def mostrar():
    global habitos, check_vars

    # Encontra os hábitos selecionados para mostrar
    habitos_a_mostrar = [h for h in habitos if check_vars[h['nome']].get() == 1]

    #permitair a seleção de apenas um hábito
    if len(habitos_a_mostrar) > 1:
        mostrar_mensagem("Atenção", "Selecione apenas um hábito para visualizar as estatísticas.")
        return
    
    # Mostra os hábitos selecionados
    for habito in habitos_a_mostrar:
        mostrar_progresso(habito['nome'],habito['datas'],45)
        

# %% [markdown]
# # Sair do programa

# %%
def sair():
    resposta = True
    if resposta:
        janela.destroy()

# %% [markdown]
# # Criar janela e botoes do menu

# %%
# Cria a janela principal e os botões do menu
janela = tkinter.Tk()
janela.title("Rastreador de Hábitos")
janela.configure(bg="#f8f8f8")

style = ttk.Style()
style.configure("Menu.TButton", font=("Helvetica", 12), padding=10, background="#e0e0e0", foreground="black")

btn_novo_habito = ttk.Button(janela, text="NOVO HÁBITO", style="Menu.TButton", command=novo_habito)
btn_novo_habito.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
btn_novo_habito.is_menu = True

btn_registrar_progresso = ttk.Button(janela, text="REGISTRAR PROGRESSO", style="Menu.TButton", command=registrar_progresso)
btn_registrar_progresso.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
btn_registrar_progresso.is_menu = True

btn_ver_estatisticas = ttk.Button(janela, text="VER ESTATÍSTICAS", style="Menu.TButton", command=ver_estatisticas)
btn_ver_estatisticas.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
btn_ver_estatisticas.is_menu = True

btn_sair = ttk.Button(janela, text="SAIR", style="Menu.TButton", command=sair)
btn_sair.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
btn_sair.is_menu = True

carregar_habitos()
janela.mainloop()


