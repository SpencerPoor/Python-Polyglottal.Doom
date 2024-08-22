from settings import *
from data_types import *

# Manages models for walls in map segments
class Models:
    def __init__(self, engine):
        self.engine = engine
        # Takes raw_segments for loaded map from level_data
            # Reason for rendering to all RAW segments instead of BSP partitioned segments:
                ## During Binary Space Partitioning, one segment can be partitioned into several segments
                ## To improve overhead performance, instead of rendering to all split segments, rendering once to all raw segments-
                ## -means less rendering as multiple split segments can share the same single wall render that was rendered for one raw segment
                ### Please see wall_render_logic.png file in VisualAidImages folder for a visual aid on why this provides less overhead
        self.raw_segments = engine.level_data.raw_segments
        # Generates an empty list to store models
        self.wall_models: list[ray.Model] = []
        #
        self.wall_id = 0
        # Executes build process for wall models
        self.build_wall_models()

    # Builds wall models for each segment in raw_segments
    def build_wall_models(self):
        for seg in self.raw_segments:
            # Invokes WallModel class defined below to generate the model
            wall_model = WallModel(self.engine, seg).model
            self.add_wall_model(wall_model, seg)

    # Adds wall models to wall_models list in __init__
    def add_wall_model(self, wall_model, segment):
        self.wall_models.append(wall_model)
        # Adds wall model ID to segment it will be associated with, linking the segment and wall model together inside the wall_models list
        segment.wall_model_id.add(self.wall_id)
        self.wall_id += 1

# Creates wall models for the provided segment (Acts as a "helper function" for build_wall_models in Models class)
class WallModel:
    def __init__(self, engine, segment):
        self.engine = engine
        self.segment = segment
        #
        self.model: ray.Model = self.get_model()

    # Generates model from a generated quad mesh
    def get_model(self):
        # get_quad_mesh method creates quad mesh
        mesh = self.get_quad_mesh()
        model = ray.load_model_from_mesh(mesh)
        model.materials[0].maps[ray.MATERIAL_MAP_DIFFUSE].texture = self.get_texture()
        #
        return model
    
    # Helper function that generates quad mesh based on segment math data from __init__ parameter
    def get_quad_mesh(self) -> ray.Mesh:
        triangle_count = 2
        vertex_count = 4

        # get segment coords
        (x0, z0), (x1, z1) = self.segment.pos

        # get normals
        delta = vec3(x1, 0, z1) - vec3(x0, 0, z0)
        normal = glm.normalize(vec3(-delta.z, delta.y, delta.x))
        normals = glm.array([normal] * vertex_count)

        # get tex coords
        width = glm.length(delta)
        bottom, top = 0.0, 1.0
        #
        uv0, uv1, uv2, uv3 = (0, bottom), (width, bottom), (width, top), (0, top)
        tex_coords = glm.array([glm.vec2(v) for v in [uv0, uv1, uv2, uv3]])

        # get vertices
        v0, v1, v2, v3 = (x0, bottom, z0), (x1, bottom, z1), (x1, top, z1), (x0, top, z0)
        vertices = glm.array([vec3(v) for v in [v0, v1, v2, v3]])

        # get indices
        indices = [0, 1, 2, 0, 2, 3]
        indices = glm.array.from_numbers(glm.uint16, *indices)

        # get mesh
        mesh = ray.Mesh()
        #
        mesh.triangleCount = triangle_count
        mesh.vertexCount = vertex_count
        #
        mesh.vertices = ray.ffi.from_buffer("float []", vertices)
        mesh.indices = ray.ffi.from_buffer("unsigned short []", indices)
        mesh.texcoords = ray.ffi.from_buffer("float []", tex_coords)
        mesh.normals = ray.ffi.from_buffer("float []", normals)

        ray.upload_mesh(mesh, False)
        return mesh
    
    # Random color is generated for use with generating textures in get_texture
    def get_rnd_col(self):
        col = *glm.ivec3(glm.abs(glm.ballRand(1.0) * 255)), 255
        return col
    
    # Generates texture for model
    def get_texture(self):
        # Image initialized for texture
        image = ray.gen_image_checked(10, 10, 1, 1, self.get_rnd_col(), WHITE_COLOR)
        # Texture is loaded from initialized image
        texture = ray.load_texture_from_image(image)
        # Image is then unloaded
        ray.unload_image(image)
        # Texture is returned
        return texture