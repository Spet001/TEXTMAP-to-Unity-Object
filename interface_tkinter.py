import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess
from textmap_to_obj import load_map_data, write_obj

def exportar_completo():
    textmap_path = filedialog.askopenfilename(
        title="Selecione o arquivo TEXTMAP (.txt)",
        filetypes=[("Arquivos TEXTMAP", "*.txt")]
    )
    if not textmap_path:
        return

    # Gerar parsed_map.json
    print(f"Executando parser em: {textmap_path}")
    resultado = subprocess.run(["python", "textmap_parser.py", textmap_path], capture_output=True, text=True)

    if resultado.returncode != 0 or not os.path.exists("parsed_map.json"):
        print(resultado.stderr)
        messagebox.showerror("Erro", "Falha ao gerar o JSON a partir do TEXTMAP.")
        return

    out_path = filedialog.asksaveasfilename(
        title="Salvar como OBJ",
        defaultextension=".obj",
        filetypes=[("Arquivos OBJ", "*.obj")]
    )
    if not out_path:
        return

    map_data = load_map_data("parsed_map.json")
    if not map_data:
        messagebox.showerror("Erro", "Falha ao carregar o parsed_map.json.")
        return

    write_obj(map_data, out_path)
    messagebox.showinfo("Sucesso", f"Mapa exportado para: {out_path}")

root = tk.Tk()
root.title("Exportador TEXTMAP → OBJ")
root.geometry("430x170")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack(expand=True)

label = tk.Label(frame, text="1) Selecione TEXTMAP.txt   →   2) Gera .OBJ via JSON")
label.pack(pady=(0, 10))

btn_exportar = tk.Button(frame, text="Exportar TEXTMAP → OBJ", command=exportar_completo)
btn_exportar.pack()

root.mainloop()
