import os
import sys
import datetime
import shutil
from pathlib import Path
import flet as ft
from PIL import Image
import ffmpeg
from docx2pdf import convert as docx_convert
from pypdf import PdfReader

# ==============================================================================
# 1. ARQUITETURA DE DADOS
# ==============================================================================

CONVERSION_MAP = {
    "Imagens": {
        "png": ["jpg", "webp", "bmp", "ico", "tiff"],
        "jpg": ["png", "webp", "bmp", "tiff"],
        "webp": ["png", "jpg", "ico"],
        "bmp": ["png", "jpg", "webp"],
        "ico": ["png", "bmp"]
    },
    "Vídeo": {
        "mp4": ["mkv", "avi", "mov", "mp3 (Extrair Áudio)", "gif"],
        "mkv": ["mp4", "avi", "mp3 (Extrair Áudio)"],
        "avi": ["mp4", "mkv"],
        "mov": ["mp4", "avi"],
        "webm": ["mp4", "mp3 (Extrair Áudio)"]
    },
    "Áudio": {
        "mp3": ["wav", "ogg", "flac"],
        "wav": ["mp3", "ogg", "flac"],
        "ogg": ["mp3", "wav"],
        "flac": ["mp3", "wav"]
    },
    "Documentos": {
        "docx": ["pdf"],     
        "pdf": ["txt"]       
    }
}

# ==============================================================================
# 2. ENGINE DE CONVERSÃO (Backend Atualizado com Output Path)
# ==============================================================================

class ConversionEngine:
    @staticmethod
    def _resolve_output_path(source_path, target_ext, output_folder=None):
        """Helper para calcular o caminho final."""
        source_path = Path(source_path)
        new_filename = source_path.with_suffix(target_ext).name
        
        if output_folder:
            # Salva na pasta escolhida pelo usuário
            return str(Path(output_folder) / new_filename)
        else:
            # Salva na mesma pasta do arquivo original
            return str(source_path.with_suffix(target_ext))

    @staticmethod
    def get_ffmpeg_path():
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
            ffmpeg_binary = os.path.join(base_path, 'ffmpeg.exe' if os.name == 'nt' else 'ffmpeg')
        else:
            ffmpeg_binary = 'ffmpeg' 
        return ffmpeg_binary

    @staticmethod
    def convert_image(source, target_ext, output_folder=None):
        try:
            output_path = ConversionEngine._resolve_output_path(source, target_ext, output_folder)
            
            img = Image.open(source)
            if img.mode in ("RGBA", "P") and target_ext in [".jpg", ".bmp"]:
                img = img.convert("RGB")
            
            img.save(output_path)
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro imagem: {e}")

    @staticmethod
    def convert_media(source, target_ext, output_folder=None):
        try:
            output_path = ConversionEngine._resolve_output_path(source, target_ext, output_folder)
            
            if target_ext == ".mp3" and source.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                (
                    ffmpeg
                    .input(source)
                    .output(output_path, acodec='libmp3lame', qscale=2)
                    .overwrite_output()
                    .run(quiet=True)
                )
            else:
                (
                    ffmpeg
                    .input(source)
                    .output(output_path)
                    .overwrite_output()
                    .run(quiet=True)
                )
            return output_path
        except ffmpeg.Error as e:
            raise RuntimeError(f"Erro FFmpeg: {e}")

    @staticmethod
    def convert_document(source, target_ext, output_folder=None):
        output_path = ConversionEngine._resolve_output_path(source, target_ext, output_folder)
        try:
            if source.endswith(".docx") and target_ext == ".pdf":
                docx_convert(source, output_path)
            elif source.endswith(".pdf") and target_ext == ".txt":
                reader = PdfReader(source)
                with open(output_path, "w", encoding="utf-8") as f:
                    for page in reader.pages:
                        text = page.extract_text()
                        if text:
                            f.write(text)
                            f.write("\n")
            else:
                raise NotImplementedError("Formato não suportado.")
            return output_path
        except Exception as e:
            raise RuntimeError(f"Erro Docs: {e}")

# ==============================================================================
# 3. INTERFACE DO USUÁRIO (Frontend - Flet)
# ==============================================================================

def main(page: ft.Page):
    # Configurações da Janela
    page.title = "UniConverter Pro - Batch Edition"
    page.window_width = 550
    page.window_height = 800  # Aumentei um pouco a altura
    page.window_resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    
    # --- Componentes de Estado ---
    selected_category = ft.Ref[ft.Dropdown]()
    selected_source = ft.Ref[ft.Dropdown]()
    selected_target = ft.Ref[ft.Dropdown]()
    selected_output_dir = ft.Ref[ft.Text]() # Guarda o caminho visualmente
    output_dir_path = ft.Ref[ft.Text]()     # Guarda o caminho tecnicamente (hidden ou var)
    
    btn_upload = ft.Ref[ft.ElevatedButton]()
    btn_select_dir = ft.Ref[ft.ElevatedButton]()
    
    # Feedback
    progress_bar = ft.Ref[ft.ProgressBar]()
    status_text = ft.Ref[ft.Text]()
    detail_text = ft.Ref[ft.Text]()
    
    # Modal Logs
    log_field = ft.Ref[ft.TextField]()
    log_dialog = ft.AlertDialog(
        title=ft.Text("Relatório da Conversão"),
        content=ft.Container(
            content=ft.TextField(
                ref=log_field,
                multiline=True,
                read_only=True,
                text_size=12,
                min_lines=10,
                max_lines=15,
                width=450
            ),
            width=500,
        ),
        actions=[ft.TextButton("Fechar", on_click=lambda e: page.close_dialog())],
    )

    # --- Pickers ---
    # Picker de Arquivos
    file_picker = ft.FilePicker()
    
    # Picker de Diretório (NOVO)
    dir_picker = ft.FilePicker()
    
    page.overlay.extend([file_picker, dir_picker])

    # --- Lógica de Reset ---
    def reset_ui():
        progress_bar.current.visible = False
        progress_bar.current.value = 0
        status_text.current.value = ""
        detail_text.current.value = ""
        page.update()

    # --- Handlers de Dropdown ---
    def on_category_change(e):
        cat = selected_category.current.value
        
        selected_source.current.options = []
        selected_source.current.value = None
        selected_source.current.disabled = False
        
        selected_target.current.options = []
        selected_target.current.value = None
        selected_target.current.disabled = True
        
        btn_upload.current.disabled = True
        
        if cat in CONVERSION_MAP:
            formats = list(CONVERSION_MAP[cat].keys())
            selected_source.current.options = [ft.dropdown.Option(f) for f in formats]
        
        reset_ui()
        page.update()

    def on_source_change(e):
        cat = selected_category.current.value
        src = selected_source.current.value
        
        selected_target.current.options = []
        selected_target.current.value = None
        selected_target.current.disabled = False
        
        btn_upload.current.disabled = True
        
        if cat and src:
            targets = CONVERSION_MAP[cat].get(src, [])
            selected_target.current.options = [ft.dropdown.Option(t) for t in targets]
        
        reset_ui()
        page.update()

    def on_target_change(e):
        # Habilita botões finais
        can_proceed = True if selected_target.current.value else False
        btn_upload.current.disabled = not can_proceed
        btn_select_dir.current.disabled = not can_proceed
        reset_ui()
        page.update()

    # --- Handler de Diretório (NOVO) ---
    def on_dir_click(e):
        dir_picker.get_directory_path(dialog_title="Selecione onde salvar os arquivos")

    def on_dir_result(e: ft.FilePickerResultEvent):
        if e.path:
            # Atualiza visualmente e guarda o path
            output_dir_path.current.value = e.path
            selected_output_dir.current.value = f"Salvar em: ...{e.path[-30:]}" if len(e.path) > 30 else f"Salvar em: {e.path}"
            selected_output_dir.current.color = ft.colors.GREEN_400
        else:
            # Se cancelou, mantém o anterior ou volta pro padrão
            if not output_dir_path.current.value:
                selected_output_dir.current.value = "Padrão: Mesma pasta da origem"
                selected_output_dir.current.color = ft.colors.GREY_500
        page.update()

    # --- Handler de Upload/Processamento ---
    def on_upload_click(e):
        src_ext = selected_source.current.value
        if not src_ext:
            return
        
        file_picker.pick_files(
            allow_multiple=True,
            allowed_extensions=[src_ext],
            dialog_title=f"Selecione arquivos {src_ext.upper()}"
        )

    def on_file_picked(e: ft.FilePickerResultEvent):
        if not e.files:
            return

        total_files = len(e.files)
        cat = selected_category.current.value
        raw_target = selected_target.current.value
        target_ext = "." + raw_target.split(" ")[0].lower()
        
        # Recupera o diretório de saída (se houver, senão passa None)
        out_dir = output_dir_path.current.value if output_dir_path.current.value else None
        
        # UI Prep
        progress_bar.current.visible = True
        progress_bar.current.value = 0
        btn_upload.current.disabled = True
        btn_select_dir.current.disabled = True
        
        log_buffer = [f"Início: {datetime.datetime.now().strftime('%H:%M:%S')}", "="*40]
        if out_dir:
            log_buffer.append(f"Destino Global: {out_dir}")
        
        success_count = 0
        error_count = 0

        # LOOP
        for idx, file_obj in enumerate(e.files, start=1):
            current_file_name = file_obj.name
            
            # Update UI
            status_text.current.value = f"Processando: {idx}/{total_files}"
            status_text.current.color = ft.colors.BLUE
            detail_text.current.value = f"Arquivo: {current_file_name}"
            progress_bar.current.value = (idx - 1) / total_files
            page.update()

            try:
                output_file = ""
                # Passamos o out_dir para a engine
                if cat == "Imagens":
                    output_file = ConversionEngine.convert_image(file_obj.path, target_ext, out_dir)
                elif cat in ["Vídeo", "Áudio"]:
                    output_file = ConversionEngine.convert_media(file_obj.path, target_ext, out_dir)
                elif cat == "Documentos":
                    output_file = ConversionEngine.convert_document(file_obj.path, target_ext, out_dir)
                
                log_buffer.append(f"[OK] {current_file_name}")
                success_count += 1
                
            except Exception as err:
                log_buffer.append(f"[ERRO] {current_file_name}: {str(err)}")
                error_count += 1
        
        # Finalização
        progress_bar.current.value = 1.0
        status_text.current.value = "Concluído"
        status_text.current.color = ft.colors.WHITE
        detail_text.current.value = f"Sucesso: {success_count} | Erros: {error_count}"
        
        btn_upload.current.disabled = False
        btn_select_dir.current.disabled = False
        
        log_buffer.append("="*40)
        log_buffer.append(f"Resumo: {success_count} convertidos, {error_count} falhas.")
        log_field.current.value = "\n".join(log_buffer)
        
        page.dialog = log_dialog
        log_dialog.open = True
        page.update()

    # Binds
    file_picker.on_result = on_file_picked
    dir_picker.on_result = on_dir_result

    # --- Layout ---
    
    header = ft.Container(
        content=ft.Column([
            ft.Text("UniConverter", size=30, weight=ft.FontWeight.BOLD, color=ft.colors.CYAN_400),
            ft.Text("Batch Edition + Custom Path", size=12, color=ft.colors.GREY_400),
        ]),
        padding=ft.padding.only(bottom=10)
    )

    controls_card = ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Column([
                # 1. Categoria
                ft.Text("1. Categoria", weight="bold"),
                ft.Dropdown(
                    ref=selected_category,
                    label="Selecione o tipo de mídia",
                    options=[ft.dropdown.Option(k) for k in CONVERSION_MAP.keys()],
                    on_change=on_category_change,
                ),
                
                # 2. Origem
                ft.Text("2. Formato de Origem", weight="bold"),
                ft.Dropdown(
                    ref=selected_source,
                    label="Entrada",
                    disabled=True,
                    on_change=on_source_change,
                ),
                
                # 3. Destino
                ft.Text("3. Formato de Destino", weight="bold"),
                ft.Dropdown(
                    ref=selected_target,
                    label="Saída",
                    disabled=True,
                    on_change=on_target_change,
                ),
                
                ft.Divider(height=10),
                
                # 4. Seleção de Pasta (Opcional)
                ft.Row([
                    ft.Icon(ft.icons.FOLDER_OPEN, color=ft.colors.GREY_400),
                    ft.Column([
                        ft.Text("Local de Salvamento (Opcional)", size=12, weight="bold"),
                        ft.Text(ref=selected_output_dir, value="Padrão: Mesma pasta da origem", size=11, color=ft.colors.GREY_500)
                    ], spacing=2, expand=True),
                    ft.OutlinedButton(
                        ref=btn_select_dir,
                        text="Alterar",
                        icon=ft.icons.EDIT_LOCATION_ALT,
                        disabled=True, # Habilita junto com upload
                        on_click=on_dir_click,
                        style=ft.ButtonStyle(padding=10)
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

                # Campo oculto para guardar o path real
                ft.Text(ref=output_dir_path, visible=False, value=""), 
                
                ft.Divider(height=10),
                
                # 5. Ação Final
                ft.ElevatedButton(
                    ref=btn_upload,
                    text="Selecionar Arquivos e Converter",
                    icon=ft.icons.PLAY_ARROW_ROUNDED,
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=20,
                        bgcolor={ft.MaterialState.HOVERED: ft.colors.CYAN_900}
                    ),
                    disabled=True,
                    on_click=on_upload_click,
                    width=500
                )
            ], spacing=12)
        )
    )

    status_area = ft.Container(
        content=ft.Column([
            ft.ProgressBar(ref=progress_bar, visible=False, color=ft.colors.CYAN_400, bgcolor=ft.colors.GREY_800),
            ft.Text(ref=status_text, size=16, weight="bold"),
            ft.Text(ref=detail_text, size=12, color=ft.colors.GREY_500, no_wrap=True)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
        padding=ft.padding.only(top=15),
        bgcolor=ft.colors.with_opacity(0.05, ft.colors.WHITE),
        border_radius=10,
        alignment=ft.alignment.center
    )

    page.add(header, controls_card, status_area)

if __name__ == "__main__":
    ft.app(target=main)