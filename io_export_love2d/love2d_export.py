import bpy

def correctPath(bPath):
    p = str.removeprefix(bpy.path.relpath(bPath),"//")
    p = str.replace(p, "\\", "/")
    return p

def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("print(\"Hello Blender %s Löve\")\n" % use_some_setting)

    imageSet = set()
    fontSet = set()
    drawables = []

    for o in context.collection.objects:
        if o.type == 'GPENCIL':
            print("todo: gpencil export")
            # get gpencil bounding box
            # render gpencil to image. probably use clipping region set to bounds of the gpencil object.
            # https://docs.blender.org/manual/en/latest/editors/3dview/navigate/regions.html
        elif o.type == 'FONT':
            print("todo: font export")
            print(o.data.body) # print the text
            # o.data.font is the font. find path...
            p = correctPath(o.data.font.filepath)
            
            # todo (1st prio): figur out font size. how to get love font size from blender font size.
            
            # todo: also store the size of the font. currently hardcoded to 140.
            # the set needs to hold the same font twice if it exists with different sizes!
            # o.data.size
            fontSet.add(p) 
            
            s = 1.0 
            
            drawable = {
                "name": o.name,
                "text": o.data.body,
                "font": p,
                "x": o.location.x,
                "y": -o.location.y,
                "r": -o.rotation_euler.z,
                "sx": o.scale.x,
                "sy": o.scale.y,
                "ox": o.data.offset_x,
                "oy": o.data.size + o.data.offset_y, #todo: font height instead of o.data.size
                "kx": -o.data.shear,
                "ky": 0,
            }
            drawables.append(drawable)
            
        elif o.type == 'EMPTY' and o.empty_display_type == 'IMAGE':
            o.data
            p = correctPath(o.data.filepath)
            print(p)
            imageSet.add(p)
            
            # use empty size to calculate scale. empty display size is width its width in blender units.
            s = o.empty_display_size / o.data.size[0]
            drawable = {
                "name": o.name,
                "image": p,
                "x": o.location.x,
                "y": -o.location.y,
                "r": -o.rotation_euler.z,
                "sx": s * o.scale.x,
                "sy": s * o.scale.y,
                "ox": o.data.size[0] * -o.empty_image_offset[0],
                "oy": o.data.size[1] * (1.0+o.empty_image_offset[1]),
                "kx": 0,
                "ky": 0,
            }
            drawables.append(drawable)

    f.write("local images = {}\n")
    for image in imageSet:
        f.write("images[\"%s\"] = love.graphics.newImage(\"%s\")\n" % (image,image))
    
    f.write("local fonts = {}\n")
    for font in fontSet:
        # todo: dont use a constant size of 140. Instead get the size from the blender font object
        f.write("fonts[\"%s\"] = love.graphics.newFont(\"%s\", 140)\n" % (font,font))

    drawables.reverse()
    for drawable in drawables:
        x = drawable["x"]
        y = drawable["y"]
        r = drawable["r"]
        sx= drawable["sx"]
        sy= drawable["sy"]
        ox= drawable["ox"]
        oy= drawable["oy"]
        kx= drawable["kx"]
        ky= drawable["ky"]
        if "image" in drawable:
            f.write("love.graphics.setColor(1,1,1,1)")
            f.write("love.graphics.draw(images[\"%s\"], %s, %s, %s, %s, %s, %s, %s)\n" %(drawable["image"], x, y, r, sx, sy, ox, oy))
        elif "text" in drawable:
            f.write("love.graphics.setColor(0,0,0,1)")
            f.write("love.graphics.print(\"%s\", fonts[\"%s\"], %s, %s, %s, %s, %s, %s, %s, %s, %s)\n" %(drawable["text"], drawable["font"], x, y, r, sx, sy, ox, oy, kx, ky))
    f.close()

    return {'FINISHED'}

# test call
# print("running write_some_data...")
# write_some_data(bpy.context, "//test.lua", True)



# ExportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ExportLove2D(Operator, ExportHelper):
    """This appears in the tooltip of the operator and in the generated docs"""
    bl_idname = "export_test.some_data"  # important since its how bpy.ops.import_test.some_data is constructed
    bl_label = "Export Some Data"

    # ExportHelper mix-in class uses this.
    filename_ext = ".lua"

    filter_glob: StringProperty(
        default="*.lua",
        options={'HIDDEN'},
        maxlen=255,  # Max internal buffer length, longer would be clamped.
    )

    # List of operator properties, the attributes will be assigned
    # to the class instance from the operator settings before calling.
    use_setting: BoolProperty(
        name="Example Boolean",
        description="Example Tooltip",
        default=True,
    )

    type: EnumProperty(
        name="Example Enum",
        description="Choose between two items",
        items=(
            ('OPT_A', "First Option", "Description one"),
            ('OPT_B', "Second Option", "Description two"),
        ),
        default='OPT_A',
    )

    def execute(self, context):
        return write_some_data(context, self.filepath, self.use_setting)


# Only needed if you want to add into a dynamic menu
def menu_func_export(self, context):
    self.layout.operator(ExportLove2D.bl_idname, text="Text Export Operator")


# Register and add to the "file selector" menu (required to use F3 search "Text Export Operator" for quick access).
def register():
    bpy.utils.register_class(ExportLove2D)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportLove2D)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
