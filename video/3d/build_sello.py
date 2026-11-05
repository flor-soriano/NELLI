"""Sello Nelli 3D: escudo tinta, filete oro, N papel, garita ambar. Giro 360."""
import bpy, math, os, sys, tempfile
from mathutils import Vector

argv = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
MODO = argv[0] if argv else "still"   # still | anim
# Sin ruta de salida, se escribe en una carpeta temporal propia (no en una ruta fija compartida).
SALIDA = argv[1] if len(argv) > 1 else os.path.join(tempfile.mkdtemp(prefix="nelli-sello-"), "sello.png")

bpy.ops.wm.read_factory_settings(use_empty=True)
esc = bpy.context.scene

def mat(nombre, color, rough=0.35, metal=0.0):
    m = bpy.data.materials.new(nombre); m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    bsdf.inputs["Metallic"].default_value = metal
    return m

TINTA = mat("tinta", (0.035, 0.028, 0.022), 0.32, 0.25)
ORO = mat("oro", (0.62, 0.36, 0.06), 0.24, 0.9)
PAPEL = mat("papel", (0.92, 0.90, 0.84), 0.42, 0.0)
AMBAR = mat("ambar", (0.85, 0.52, 0.05), 0.3, 0.55)

PUNTOS = [(-1.0, 1.05), (0.0, 1.30), (1.0, 1.05), (1.0, 0.10), (0.0, -1.18), (-1.0, 0.10)]

def escudo(nombre, escala, grosor, material, y):
    verts = [(x*escala, y, z*escala) for x, z in PUNTOS]
    mesh = bpy.data.meshes.new(nombre)
    mesh.from_pydata(verts, [], [list(range(len(verts)))])
    obj = bpy.data.objects.new(nombre, mesh); bpy.context.collection.objects.link(obj)
    sol = obj.modifiers.new("grosor", "SOLIDIFY"); sol.thickness = grosor
    bev = obj.modifiers.new("borde", "BEVEL"); bev.width = 0.045; bev.segments = 3
    obj.data.materials.append(material)
    return obj

def tubo(nombre, puntos, radio, material, y):
    cur = bpy.data.curves.new(nombre, "CURVE"); cur.dimensions = "3D"
    cur.bevel_depth = radio; cur.bevel_resolution = 4
    spl = cur.splines.new("POLY"); spl.points.add(len(puntos)-1)
    for p, (x, z) in zip(spl.points, puntos): p.co = (x, y, z, 1)
    obj = bpy.data.objects.new(nombre, cur); bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj

grupo = bpy.data.objects.new("Sello", None); bpy.context.collection.objects.link(grupo)
piezas = [escudo("escudo", 1.0, 0.16, TINTA, 0.0),
          tubo("filete", PUNTOS + [PUNTOS[0]], 0.028, ORO, 0.105)]
# filete interior escalado
filete2 = tubo("filete2", [(x*0.86, z*0.86) for x, z in PUNTOS] + [ (PUNTOS[0][0]*0.86, PUNTOS[0][1]*0.86) ], 0.016, ORO, 0.105)
piezas.append(filete2)
# N en texto extruido
bpy.ops.object.text_add(location=(0, 0.10, -0.08))
n = bpy.context.object; n.name = "N"; n.data.body = "N"; n.data.size = 1.55
n.data.extrude = 0.055; n.data.bevel_depth = 0.012; n.data.align_x = "CENTER"; n.data.align_y = "CENTER"
n.rotation_euler = (math.radians(90), 0, 0); n.data.materials.append(PAPEL); piezas.append(n)
# garita ambar sobre la N
piezas.append(tubo("garita", [(-0.34, -0.18), (-0.10, -0.42), (0.42, 0.20)], 0.045, AMBAR, 0.17))
for p in piezas: p.parent = grupo

# camara y luces de estudio
bpy.ops.object.camera_add(location=(0, 6.2, 0.55))
cam = bpy.context.object; esc.camera = cam
_dir = Vector((0, 0, 0.05)) - cam.location
cam.rotation_euler = _dir.to_track_quat("-Z", "Y").to_euler()
def luz(nombre, loc, energia, tam):
    d = bpy.data.lights.new(nombre, "AREA"); d.energy = energia; d.shape = "DISK"; d.size = tam
    o = bpy.data.objects.new(nombre, d); bpy.context.collection.objects.link(o); o.location = loc
    o.rotation_euler = (math.radians(55), 0, math.radians(18)); return o
luz("clave", (-3.2, -3.5, 3.2), 900, 3.0); luz("relleno", (3.4, -2.5, 0.6), 320, 2.2); luz("borde", (0.5, 2.5, 3.4), 520, 2.0)
mundo = bpy.data.worlds.new("mundo"); esc.world = mundo; mundo.use_nodes = True
mundo.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.010, 0.008, 1)
mundo.node_tree.nodes["Background"].inputs[1].default_value = 0.55

esc.render.engine = "BLENDER_EEVEE"
esc.render.resolution_x = 900; esc.render.resolution_y = 900
esc.render.film_transparent = False
if MODO == "anim":
    esc.frame_start = 1; esc.frame_end = 72; esc.render.fps = 30
    grupo.rotation_euler = (0, 0, 0); grupo.keyframe_insert("rotation_euler", frame=1)
    grupo.rotation_euler = (0, 0, math.radians(360)); grupo.keyframe_insert("rotation_euler", frame=73)
    # giro sobre el eje vertical de la escena (Y del objeto = profundidad): usar Z mundo via rotacion en Y local del grupo
    esc.render.filepath = SALIDA
    bpy.ops.render.render(animation=True)
else:
    esc.render.filepath = SALIDA
    bpy.ops.render.render(write_still=True)
print("SELLO_OK", MODO, SALIDA)
