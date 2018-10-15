import bpy, math
from bpy import context
from bpy.types import Panel, Operator
from math import radians, degrees

bl_info = {  
 "name": "CreatePlanets",  
 "author": "Irina Marčeta, Boris Stajić",  
 "version": (0, 7),  
 "blender": (2, 7, 9),  
 "location": "3D VIEW > TOOLS > Tools Tab Label > objectmode > Irina/Boris",  
 "description": "Use it to create planets as spheres, parent them to selection and animate rotation and revolution",  
 "warning": "",  
 "wiki_url": "",  
 "tracker_url": "",  
 "category": "Animation"} 
#---------------------------------------------------------------------------------------
# Klasa koja pravi planete
#---------------------------------------------------------------------------------------
class Planet():
    radius = 1.0
    orbit = 0.0
    rotation_speed = 0.0
    orbit_speed = 0.0
    def Create(self, radius, orbit, rotation_speed, orbit_speed):
        orbit /= 10
        orbit_speed /= 10
        rotation_speed/= 10
        #---ANIMACIJA ROTACIJE--------------------------
        def AnimateRotation(rotation_speed):            
            ctx = bpy.context
            ctx.scene.frame_start = 0
            ctx.scene.frame_end = 719
            ctx.scene.frame_current = 0
            bpy.ops.anim.keyframe_insert_menu(type='Rotation')
            for i in range(1440):  
                ctx.scene.frame_current = 1439;                
                bpy.ops.transform.rotate(value = (3.14159 * rotation_speed / 180) * 0.1, axis=(0,0,1))
                bpy.ops.anim.keyframe_insert_menu(type = 'Rotation')                
            # Promena krivih da se dobije LINEARNA animacija
            ctx.area.type = 'GRAPH_EDITOR'
            ctx.object.animation_data.action.fcurves[0].select=True
            bpy.ops.graph.handle_type(type='VECTOR')
            ctx.area.type = 'TEXT_EDITOR'
            bpy.context.area.type = 'VIEW_3D'
            bpy.ops.screen.frame_jump(0)
        # Kraj animacije rotacije
        #------------------------------
        def AnimateRevolution(orbit_speed):
            ctx = bpy.context
            ctx.scene.frame_start = 0
            ctx.scene.frame_end = 1440
            fstart = bpy.context.scene.frame_start 
            fend = bpy.context.scene.frame_end     
            helper.rotation_euler = (0, 0, 0)
            helper.keyframe_insert(data_path="rotation_euler", frame = fstart)                
            helper.rotation_euler = (0, 0, 6.28319 * orbit_speed) #360
            helper.keyframe_insert(data_path="rotation_euler", frame = fend)
            # Promena krivih da se dobije LINEARNA animacija
            ctx.area.type = 'GRAPH_EDITOR'
            ctx.object.animation_data.action.fcurves[0].select=True
            bpy.ops.graph.handle_type(type='VECTOR')
            ctx.area.type = 'TEXT_EDITOR'
            bpy.context.area.type = 'VIEW_3D' 
            bpy.ops.screen.frame_jump(0)       
        # Kraj animacije revolucije
        #------------------------------            
        selectedObjects = bpy.context.selected_objects
        #--------------------------
        # Proveri da li je selektovan tačno jedan objekat
        # ako jeste kreiraj sferu u odnosu na njega
        #--------------------------
        if len(selectedObjects) == 1:
            print("Success!")
            print(bpy.context.object.location)
            selectedObjects = bpy.context.object
            location = bpy.context.object.location
            cursor = context.scene.cursor_location
            bpy.ops.object.empty_add(type='PLAIN_AXES',view_align=False)
            helper = bpy.context.object
            #----------- Pozicioniraj HELPER
            bpy.ops.transform.translate(value=(-cursor[0],-cursor[1],-cursor[2]))
            bpy.ops.transform.translate(value=(location[0],location[1],location[2]))
            # Linkuj novi HELPER za SELEKTOVARNI OBJEKAT
            bpy.ops.object.select_all(action='DESELECT') # Deselektuj sve
            helper.select = True
            selectedObjects.select = True
            bpy.context.scene.objects.active = selectedObjects
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            #----------- Napravi Sferu 
            bpy.ops.mesh.primitive_uv_sphere_add()
            bpy.ops.transform.resize(value = (radius/10, radius/10, radius/10)) # Veličina sfere
            sphere = bpy.context.object
            #----------- Pozicioniraj Sferu 
            bpy.ops.transform.translate(value=(-cursor[0],-cursor[1],-cursor[2]))
            bpy.ops.transform.translate(value=(location[0],location[1],location[2]))
            bpy.ops.transform.translate(value =(0,-orbit,0))
            AnimateRotation(rotation_speed) # Animiraj rotaciju
            
            # Linkuj SFERU za HELPER            
            bpy.ops.object.select_all(action='DESELECT') # Deselektuj sve
            helper.select = True
            sphere.select = True
            bpy.context.scene.objects.active = helper
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            AnimateRevolution(orbit_speed) # Animiraj revoluciju
        else:
            print("No selection, creating from (0,0,0)")
            # Napravi HELPER
            bpy.ops.object.empty_add(type='PLAIN_AXES',view_align=False)
            # Postavi HELPER na 0,0,0
            cursor = context.scene.cursor_location
            bpy.ops.transform.translate(value=(-cursor[0],-cursor[1],-cursor[2]))
            helper = bpy.context.object
            #----------- Napravi Sferu 
            bpy.ops.mesh.primitive_uv_sphere_add()
            bpy.ops.transform.resize(value = (radius/10, radius/10, radius/10)) # Veličina sfere
            sphere = bpy.context.object
            #----------- Pozicioniraj Sferu 
            bpy.ops.transform.translate(value=(-cursor[0],-cursor[1],-cursor[2]))
            bpy.ops.transform.translate(value =(0,-orbit,0))
            AnimateRotation(rotation_speed) # Animiraj rotaciju
            
            # Linkuj SFERU za HELPER            
            bpy.ops.object.select_all(action='DESELECT') # Deselektuj sve
            helper.select = True
            sphere.select = True
            bpy.context.scene.objects.active = helper
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=False)
            AnimateRevolution(orbit_speed) # Animiraj revoluciju
# Kraj klase Planet
#--------------------------
 
#---------------------------------------------------------------------------------------
# Ovde je glavni deo koda
#---------------------------------------------------------------------------------------
def main(context):
# Napravi objekat Planeta u odnosu na ulazne parametre
    radius = context.scene.planet_size
    orbit = context.scene.planet_orbit
    rotation_speed  = context.scene.planet_rotation_speed
    orbit_speed = context.scene.planet_orbit_speed
    myPlanet = Planet()
    myPlanet.Create(radius, orbit, rotation_speed, orbit_speed)
    #bpy.ops.screen.animation_play()
   
#---------------------------------------------------------------------------------------
# Napravi operator koji će posle koristiti dugme CREATE
#---------------------------------------------------------------------------------------
class CreateSolSystem(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.create_solsystem"
    bl_label = "Creates a Solar System"

    def execute(self, context):
        main(context)
        return {'FINISHED'}
#---------------------------------------------------------------------------------------
# Napravi operator za zaustavljanje i premotavanje animacije
#---------------------------------------------------------------------------------------
class StopAnimation(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "action.stop_animation"
    bl_label = "Stops animation"

    def execute(self, context):
        bpy.ops.screen.animation_cancel()
        bpy.ops.screen.frame_jump(0)
        return {'FINISHED'}
#---------------------------------------------------------------------------------------
# Napravi operator za čišćenje scene
#---------------------------------------------------------------------------------------
class ClearScene(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "action.clear_scene"
    bl_label = "Deletes all the meshes in the scene"

    def execute(self, context):
            class ClearScene():
                # Selektuj sve objekte u sceni
                for o in bpy.data.objects:
                        o.select = True              
                # obriši
                bpy.ops.object.delete()
            return {'FINISHED'}
#---------------------------------------------------------------------------------------
# Napravi operator za resetovanje parametara
#---------------------------------------------------------------------------------------
class ResetParameters(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "action.reset_parameters"
    bl_label = "Resets parameters"

    def execute(self, context):
            class ResetParameters():
                bpy.context.scene.planet_size = 1
                bpy.context.scene.planet_orbit = 0
                bpy.context.scene.planet_rotation_speed= 0
                bpy.context.scene.planet_orbit_speed = 0
            return {'FINISHED'}
#---------------------------------------------------------------------------------------
# UI
#---------------------------------------------------------------------------------------
class OurToolPanel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = 'Tools Tab Label'
    bl_context = 'objectmode'
    bl_category = 'Irina/Boris'
#--------------------------------------------------------------------------------------- 
# Napravi slidere za input value
#---------------------------------------------------------------------------------------     
    bpy.types.Scene.planet_size = bpy.props.IntProperty(
        name = "Size", # Tekst na slajderu
        default = 1, # Default vrednost
        description = "Change planet size"
        )
    bpy.types.Scene.planet_orbit = bpy.props.IntProperty(
        name = "Orbit", # Tekst na slajderu
        default = 0, # Default vrednost
        description = "Change planet orbit"
        )
    bpy.types.Scene.planet_rotation_speed  = bpy.props.IntProperty(
        name = "Rotation Speed", # Tekst na slajderu
        default = 0, # Default vrednost
        description = "Change planet rotation speed"
        )
    bpy.types.Scene.planet_orbit_speed  = bpy.props.IntProperty(
        name = "Orbital Speed", # Tekst na slajderu
        default = 0, # Default vrednost
        description = "Change planet orbital speed"
        )        
#---------------------------------------------------------------------------------------     
    # Ovde se dodaju UI elementi
    def draw(self, context):
        layout = self.layout
        layout.operator('object.create_solsystem', text='CREATE', icon='WORLD_DATA') # Dugme poziva operator
        row = layout.row()
        row.prop(context.scene, "planet_size")
        #row = layout.row()
        row.prop(context.scene, "planet_orbit")
        row = layout.row()
        row.prop(context.scene, "planet_rotation_speed")
        row = layout.row()
        row.prop(context.scene, "planet_orbit_speed")
        row = layout.row()
        row.operator("screen.animation_play", text="Play/Pause", icon='PLAY')
        row = layout.row()
        row.operator("action.stop_animation", text="Stop", icon='REW')
        layout = self.layout
        layout.operator('action.clear_scene', text='Clear Scene', icon='X')
        layout = self.layout
        layout.operator('action.reset_parameters', text='Reset Parameters', icon='LOAD_FACTORY')
        row = layout.row()
        row.label(text="Use regular undo CTRL+Z")
        row = layout.row()
        row.label(text="to edit the last object")
#---------------------------------------------------------------------------------------   
# UTILITY
#---------------------------------------------------------------------------------------
# Registruj klase
def register():
    bpy.utils.register_class(CreateSolSystem)
    bpy.utils.register_class(StopAnimation)
    bpy.utils.register_class(ClearScene)
    bpy.utils.register_class(ResetParameters)
    bpy.utils.register_class(OurToolPanel)
# Odregistruj klase
def unregister():
    bpy.utils.unregister_class(CreateSolSystem)
    bpy.utils.unregister_class(StopAnimation)
    bpy.utils.unregister_class(ClearScene)
    bpy.utils.unregister_class(ResetParameters)
    bpy.utils.unregister_class(OurToolPanel)    
# Ovo je potrebno da bi skripta radila iz tekst editora, to su neke globalne promenljive
if __name__=='__main__':
    register()
    
    

