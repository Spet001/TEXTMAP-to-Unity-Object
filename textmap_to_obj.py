import json
import os
from earclip import ear_clipping_triangulate

def load_map_data(path="parsed_map.json"):
    if not os.path.exists(path):
        print(f"ERRO: Arquivo '{path}' não encontrado.")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_point(idx, vertices):
    v = vertices[idx]
    return (v["x"], v["y"])

def write_obj(map_data, out_path="map.obj"):
    if not map_data:
        print("ERRO: Nenhum dado de mapa carregado.")
        return

    vertices = map_data["vertices"]
    sectors = map_data["sectors"]
    sidedefs = map_data["sidedefs"]
    linedefs = map_data["linedefs"]

    if not vertices or not sectors or not linedefs or not sidedefs:
        print("ERRO: Dados incompletos no mapa.")
        return

    print("Iniciando exportação para OBJ...")
    obj_lines = ["# Doom map OBJ"]
    face_list = []
    vert_idx = 1

    for sector in sectors:
        sid = sector["id"]
        edges = []

        for linedef in linedefs:
            for side in ["sidefront", "sideback"]:
                side_index = linedef.get(side)
                if side_index is not None and 0 <= side_index < len(sidedefs):
                    sd = sidedefs[side_index]
                    if sd["sector"] == sid:
                        v1 = get_point(linedef["v1"], vertices)
                        v2 = get_point(linedef["v2"], vertices)
                        edges.append((v1, v2))

        if not edges:
            continue

        # montar cadeia contínua de pontos
        ordered = [edges[0][0], edges[0][1]]
        edges = edges[1:]
        while edges:
            for i, (a, b) in enumerate(edges):
                if ordered[-1] == a:
                    ordered.append(b)
                    edges.pop(i)
                    break
                elif ordered[-1] == b:
                    ordered.append(a)
                    edges.pop(i)
                    break
            else:
                break

        if len(ordered) < 3:
            continue

        floor = sector.get("heightfloor", 0)
        ceil = sector.get("heightceiling", 256)

        base = vert_idx
        for x, y in ordered:
            obj_lines.append(f"v {x} {floor} {y}")
        tris = ear_clipping_triangulate(ordered)
        for a, b, c in tris:
            face_list.append(f"f {base+a} {base+b} {base+c}")
        vert_idx += len(ordered)

        base = vert_idx
        for x, y in ordered:
            obj_lines.append(f"v {x} {ceil} {y}")
        for a, b, c in tris:
            face_list.append(f"f {base+c} {base+b} {base+a}")
        vert_idx += len(ordered)

    for linedef in linedefs:
        for side_key in ["sidefront", "sideback"]:
            side_index = linedef.get(side_key)
            if side_index is None or side_index < 0:
                continue
            sd = sidedefs[side_index]
            sector = sectors[sd["sector"]]
            floor = sector.get("heightfloor", 0)
            ceil = sector.get("heightceiling", 256)

            v1 = vertices[linedef["v1"]]
            v2 = vertices[linedef["v2"]]

            obj_lines += [
                f"v {v1['x']} {floor} {v1['y']}",
                f"v {v2['x']} {floor} {v2['y']}",
                f"v {v2['x']} {ceil} {v2['y']}",
                f"v {v1['x']} {ceil} {v1['y']}",
            ]
            face_list.append(f"f {vert_idx} {vert_idx+1} {vert_idx+2} {vert_idx+3}")
            vert_idx += 4

    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(obj_lines))
        f.write("\n")
        f.write("\n".join(face_list))
        f.write("\n")
    print(f"OBJ exportado com sucesso: {out_path}")
