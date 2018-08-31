import dv_project
import dv_comp_render

class dv_build():

    def __init__(self):
        self.dv_proj = dv_project.dv_project()
        self.dv_proj.read_project()

    def command_build(self,name):
        dv_render = dv_comp_render.dv_comp_render()
        data = self.dv_proj.read_project()

        tpl_dir = data['about']['template_dir']
        context = data['objects'][name]
        #for chld in data['objects'][]
        #context['children'].update()

        if (data['objects'][name]['kind'] == 'agent'):
            output = dv_render.render(tpl_dir + '/agent/uvm_agent_driver.svh' , context)
            print (output)
        else:
            output = dv_render.render(tpl_dir + '/uvm_object.svh' , context)
            print (output)
