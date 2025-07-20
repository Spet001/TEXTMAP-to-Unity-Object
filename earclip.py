def ear_clipping_triangulate(polygon):
    def is_convex(a, b, c):
        return ((b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])) < 0

    def point_in_triangle(pt, a, b, c):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        b1 = sign(pt, a, b) < 0.0
        b2 = sign(pt, b, c) < 0.0
        b3 = sign(pt, c, a) < 0.0
        return b1 == b2 == b3

    verts = polygon[:]
    triangles = []
    while len(verts) >= 3:
        ear_found = False
        for i in range(len(verts)):
            prev = verts[i - 1]
            curr = verts[i]
            next = verts[(i + 1) % len(verts)]
            if is_convex(prev, curr, next):
                if not any(point_in_triangle(p, prev, curr, next) for j, p in enumerate(verts) if j not in [i-1, i, (i+1)%len(verts)]):
                    triangles.append((polygon.index(prev), polygon.index(curr), polygon.index(next)))
                    verts.pop(i)
                    ear_found = True
                    break
        if not ear_found:
            break  # não conseguiu triangulação
    return triangles
