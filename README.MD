# Conversor de TEXTMAP para OBJ

 📜 Ferramenta para converter mapas do **Doom (formato TEXTMAP/UDMF)** - Abra um .WAD com a ferramenta **SLADE** e extraia o **TEXTMAP.txt** desejado do mapa - em arquivos **.OBJ 3D**, preservando geometria de paredes, pisos e tetos. Ideal para usar como base em engines modernas (Unity, Blender, etc).

### Pré-requisitos
- Python 3.8+

### Passo a Passo
**Execute a interface gráfica**:
  
   python interface_tkinter.py


 Selecione seu arquivo TEXTMAP.txt (gerado pelo Obsidian ou editores de mapa Doom).

 Salve o .OBJ no local desejado

⚙️ Funcionalidades
✅ Extrai vértices, linedefs, setores do TEXTMAP

✅ Converte para malha 3D com triangulação automática (Ear Clipping)

✅ Interface gráfica simples (Tkinter)


👥 Créditos
Algoritmo earclip.py adaptado de Geometric Tools.