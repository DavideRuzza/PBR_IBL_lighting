import moderngl_window as mglw
import moderngl as mgl
import numpy as np
from camera import OrbitCamera
from moderngl_window.geometry import sphere
from pyrr import Matrix44 as m44

class MainWin(OrbitCamera):
    title = "PBR"
    window_size = (1024, 512)
    gl_version = (4, 6, 0)
    aspect_ratio = window_size[0]/window_size[1]
    resource_dir='resources/'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.N_inst = 40
        self.simple3d = self.load_program("shader/simple3d.glsl")

        self.proj_mat = m44.perspective_projection(40, self.aspect_ratio, 0.1, 100)

        x_pos = (np.arange(self.N_inst)-(self.N_inst-1)/2)*0.2
        y_pos = (np.arange(self.N_inst)-(self.N_inst-1)/2)*0.2

        x, y = np.meshgrid(x_pos, y_pos)
        z = np.sin(x)*np.sin(y)
        pos =  np.stack([x, y, z], axis=2)
        self.pos = pos.reshape((pos.shape[0]*pos.shape[1], pos.shape[2]))


        self.sph = sphere(0.1, 20, 32, True, True)

        self.inst_data = self.ctx.buffer(reserve=4*3*self.N_inst*self.N_inst)
        self.sph.buffer(self.inst_data, "3f4/i", "in_offset")
        
        
        # print(x_pos)
    

        self.ctx.enable(mgl.DEPTH_TEST)
    
    def render(self, t, dt):
        self.ctx.clear()
        
        self.inst_data.write((self.pos*[1, 1, np.sin(2*t)]).astype('f4'))
        mvp = self.proj_mat*self.view_mat
        self.simple3d["mvp"].write(mvp.astype('f4'))
        self.sph.render(self.simple3d, instances=self.N_inst*self.N_inst)
        # self.vao_inst.render(instances=self.N_inst)

MainWin.run()
