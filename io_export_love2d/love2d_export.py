import bpy

def write_some_data(context, filepath, use_some_setting):
    print("running write_some_data...")
    f = open(filepath, 'w', encoding='utf-8')
    f.write("print(\"Hello Blender %s Löve\")\n" % use_some_setting)

    imageSet = set()
    drawables = []

    for o in context.collection.objects:
        if o.empty_display_type == 'IMAGE':
            o.data
            p = str.removeprefix(bpy.path.relpath(o.data.filepath),"//")
            p = str.replace(p, "\\", "/")
            print(p)
            imageSet.add(p)
            # todo: use empty size to calculate scale. empty size is width of image.
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
            }
            drawables.append(drawable)

    f.write("local images = {}\n")
    for image in imageSet:
        f.write("images[\"%s\"] = love.graphics.newImage(\"%s\")\n" % (image,image))

    drawables.reverse()
    for drawable in drawables:
        f.write("love.graphics.draw(images[\"%s\"], %s, %s, %s, %s, %s, %s, %s)\n" %(drawable["image"], drawable["x"], drawable["y"], drawable["r"], drawable["sx"], drawable["sy"], drawable["ox"], drawable["oy"]))
        
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
