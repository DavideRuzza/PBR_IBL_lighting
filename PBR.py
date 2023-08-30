import moderngl_window as mglw
import moderngl as mgl
import numpy as np
from camera import OrbitCamera
from moderngl_window.geometry import sphere, cube
from pyrr import Matrix44 as m44

class MainWin(OrbitCamera):
    title = "PBR"
    window_size = (1024, 512)
    gl_version = (4, 6, 0)
    aspect_ratio = window_size[0]/window_size[1]
    resource_dir='resources/'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.N_inst = 400
        self.simple3d = self.load_program("shader/simple3d.glsl")
        self.pbr_prog = self.load_program("shader/PBR.glsl")

        self.proj_mat = m44.perspective_projection(40, self.aspect_ratio, 0.1, 100)
        self.sph = sphere(0.4)
        
        self.pos = np.array([
            [0, 0, 0],
            [1, 0, 0],
            [2, 0, 0]
        ], dtype='f4')

        self.sph_col = np.array([
            [0.00, 0.33, 1.00],
            [0.68, 0.92, 0.16],
            [0.73, 0.25, 0.86]
        ], dtype='f4')


        self.materials = np.array([
            #albedo              metallic   rough   ao
            [0.00, 0.33, 1.00,    0.0      , 0.1   , 0.01 ],
            [0.68, 0.92, 0.16,    0.2      , 0.3   , 1.0 ],
            [0.73, 0.25, 0.86,    0.8      , 0.1   , 0.02 ]
        ], dtype='f4')

        self.N_inst = 3

        self.sph.buffer(self.pos, "3f/i", "in_offset")
        # self.sph.buffer(self.sph_col, "3f/i", "in_albedo")
        self.sph.buffer(self.materials, "3f f f f/i", ["in_albedo", "in_metallness", "in_roughness", "in_ao"])

        
        self.light_pos = np.array([
            [2, 2, 2],
            [-2, 2, 2],
            [2, -2, 2],
            [2, 2, -2],
        ], dtype='f4')
        
        self.light_col = np.array([
            [1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.],
            [1., 1., 1.]
        ], dtype='f4')

        self.ctx.enable(mgl.DEPTH_TEST)
    
    def render(self, t, dt):
        self.ctx.clear()
        
        mvp = self.proj_mat*self.view_mat
        self.pbr_prog["mvp"].write(mvp.astype('f4'))
        self.pbr_prog["lightPositions"].write(self.light_pos*2)
        self.pbr_prog["camPos"].write(self.eye)
        self.pbr_prog["lightColors"].write(self.light_col)
        self.sph.render(self.pbr_prog, instances=self.N_inst)
        # self.vao_inst.render(instances=self.N_inst)

MainWin.run()
