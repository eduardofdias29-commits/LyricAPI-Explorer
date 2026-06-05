import os
import customtkinter as ctk
import lyricsgenius
from dotenv import load_dotenv

load_dotenv()

class MusicLyricsExplorer(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.genius = lyricsgenius.Genius(os.getenv("GENIUS_TOKEN"))
        self.genius.verbose = False 
        self.genius.remove_section_headers = True 

        self.title("Lyric API Explorer")
        self.geometry("450x600")
        self.configure(fg_color="#121212")

        self.label_titulo = ctk.CTkLabel(
            self, 
            text="🎵 LyricAPI Explorer", 
            font=("Circular Std", 24, "bold"),
            text_color="#1DB954"
        )
        self.label_titulo.pack(pady=(30, 10))

        self.entry_artista = ctk.CTkEntry(
            self, 
            placeholder_text="Nome do Artista...", 
            width=320,
            height=40,
            fg_color="#282828",
            border_color="#1DB954"
        )
        self.entry_artista.pack(pady=5)
        self.entry_artista.bind("<Return>", lambda event: self.buscar_letra())

        self.entry_musica = ctk.CTkEntry(
            self, 
            placeholder_text="Nome da Música...", 
            width=320,
            height=40,
            fg_color="#282828",
            border_color="#1DB954"
        )
        self.entry_musica.pack(pady=10)
        self.entry_musica.bind("<Return>", lambda event: self.buscar_letra())

        self.btn_buscar = ctk.CTkButton(
            self, 
            text="PESQUISAR MÚSICA", 
            command=self.buscar_letra, 
            fg_color="#1DB954", 
            hover_color="#17a34a",
            text_color="black",
            font=("Helvetica", 14, "bold"),
            height=40
        )
        self.btn_buscar.pack(pady=10)

        self.frame_res = ctk.CTkScrollableFrame(self, fg_color="#282828", corner_radius=10)
        self.frame_res.pack(pady=20, padx=30, fill="both", expand=True)

        self.label_detalhes = ctk.CTkLabel(
            self.frame_res, 
            text="Os detalhes do música aparecerão aqui.", 
            wraplength=330, 
            justify="left",
            font=("Segoe UI", 13),
            text_color="#FFFFFF"
        )
        self.label_detalhes.pack(pady=10, padx=10, fill="x", anchor="nw")

    def buscar_letra(self):
        artista = self.entry_artista.get().strip()
        musica = self.entry_musica.get().strip()

        if not artista or not musica:
            self.label_detalhes.configure(text="Por favor, preencha o artista e a música.")
            return

        try:
            song = self.genius.search_song(musica, artista)

            if song:
                info = (
                    f"🎵 TÍTULO: {song.title}\n\n"
                    f"👤 ARTISTA: {song.artist}\n\n"
                    f"📝 LETRA:\n\n{song.lyrics}"
                )
                self.label_detalhes.configure(text=info)
            else:
                self.label_detalhes.configure(text="AVISO: Música não encontrada.")

        except Exception as e:
            self.label_detalhes.configure(text=f"Erro de conexão: Verifique sua internet.\n({e})")

if __name__ == "__main__":
    app = MusicLyricsExplorer()
    app.mainloop()