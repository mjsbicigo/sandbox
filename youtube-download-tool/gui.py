import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from threading import Thread
from backend import baixar_playlist

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Music Downloader")
        self.root.geometry("600x400")
        self.url = tk.StringVar()
        self.download_dir = tk.StringVar()
        self.cancelar_download = False  # Variável de controle para cancelar o download

        self.setup_gui()

    def setup_gui(self):
        tk.Label(self.root, text="Link do YouTube (vídeo ou playlist):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.url, width=80).pack(pady=5)

        dir_frame = tk.Frame(self.root)
        dir_frame.pack(pady=5)
        tk.Entry(dir_frame, textvariable=self.download_dir, width=60).pack(side=tk.LEFT)
        tk.Button(dir_frame, text="Escolher pasta", command=self.selecionar_pasta).pack(side=tk.LEFT, padx=5)

        self.progress_label = tk.Label(self.root, text="Progresso: 0 de 0")
        self.progress_label.pack(pady=5)
        self.progressbar = ttk.Progressbar(self.root, length=400)
        self.progressbar.pack(pady=5)

        self.logbox = tk.Text(self.root, height=10, width=80, state=tk.DISABLED)
        self.logbox.pack(pady=5)

        # Frame para os botões
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, anchor="e")  # Alinha no canto direito (east)

        tk.Button(button_frame, text="Cancelar", command=self.cancelar).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Iniciar Download", command=self.iniciar_download).pack(side=tk.RIGHT,)

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory()
        if pasta:
            self.download_dir.set(pasta)

    def iniciar_download(self):
        if not self.url.get() or not self.download_dir.get():
            messagebox.showwarning("Campos obrigatórios", "Preencha o link e escolha a pasta de download.")
            return
        Thread(target=self.executar_download, daemon=True).start()
    
    def cancelar(self):
        if not self.url.get() or not self.download_dir.get():
            messagebox.showwarning("Cancelar", "Nenhum download em andamento para cancelar.")
            return
        self.cancelar_download = True  # Sinaliza para cancelar o download
        self.atualizar_log("⛔ Download cancelado pelo usuário.")

    # def executar_download(self):
    #     self.cancelar_download = False  # Reseta o estado de cancelamento
    #     self.progressbar["value"] = 0
    #     self.atualizar_log("🔄 Iniciando processo...")

    #     video_ids = baixar_playlist(
    #         url=self.url.get(),
    #         pasta_destino=self.download_dir.get(),
    #         callback_progresso=self.atualizar_progresso,
    #         callback_log=self.atualizar_log,
    #         cancelar_callback=self.verificar_cancelamento  # Passa o callback de cancelamento
    #     )

    #     if not self.cancelar_download:
    #         self.atualizar_log("🏁 Processo finalizado!")
    #     else:
    #         self.atualizar_log("⚠️ Processo interrompido.")

    def limpar_log(self):
        self.logbox.config(state=tk.NORMAL)
        self.logbox.delete("1.0", tk.END)
        self.logbox.config(state=tk.DISABLED)

    def executar_download(self):
        self.cancelar_download = False  # Reseta o estado de cancelamento
        self.progressbar["value"] = 0
        self.atualizar_log("🔄 Iniciando processo...")

        baixar_playlist(
            url=self.url.get(),
            pasta_destino=self.download_dir.get(),
            callback_progresso=self.atualizar_progresso,
            callback_log=self.atualizar_log,
            cancelar_callback=self.verificar_cancelamento
        )
        
        if self.cancelar_download:
            self.progressbar["value"] = 0
            self.progress_label.config(text="Progresso: 0 de 0")
            self.limpar_log()
            self.atualizar_log("⚠️ Processo cancelado.")
        else:
            self.atualizar_log("🏁 Processo finalizado!")

    def verificar_cancelamento(self):
        return self.cancelar_download

    def atualizar_log(self, texto):
        self.logbox.config(state=tk.NORMAL)
        self.logbox.insert(tk.END, texto + "\n")
        self.logbox.yview(tk.END)
        self.logbox.config(state=tk.DISABLED)

    def atualizar_progresso(self, atual, total):
        self.progress_label.config(text=f"Progresso: {atual} de {total}")
        self.progressbar["maximum"] = total
        self.progressbar["value"] = atual

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()