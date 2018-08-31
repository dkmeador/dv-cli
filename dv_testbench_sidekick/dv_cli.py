#! /usr/bin/env python3
import dv_comp_render
import dv_project
import dv_build
import sys
from argparse import ArgumentParser as AP
'''
Steps
Dv_cli init <tbname>
Dv_cli agent <agentname> [options] [-item item_name]
Dv_cli env <envname>
Dv_cli add <agent/uvc> <env/uvc> [-inst instance_name]
Dv_cli build [-dest target_dir] // <- build specified tb
Dv_cli print
Dv_cli rm <agent/uvc> <env/uvc>
Dv_cli connect path path
Ex: dv_cli connect myenv::agnt1 myenv:agent2
Ex: dv_cli connect myenv::agnt1 myenv:env1.agent3
'''

class dv_cli:

    def __init__(self):
        self.project = dv_project.dv_project()
        parser = AP(description="Top level command for building Verification Environments",
                    usage = sys.argv[0] +
        ''' <command> [<args>]
        build_agent  - Build a drive uvm component
        build_test   - Build a test component''')
        parser.add_argument(
            'command', help="sub-command to run"
        )
        args = parser.parse_args(sys.argv[1:2])
        self.subcmd_args = sys.argv[2:]

        if not hasattr(self, 'command_' + args.command):
            print ("Unknown command")
            parser.print_help()
            exit(1)

        # dispatch to the sub-command
        getattr(self, 'command_' + args.command)()

    def command_build_component(self):
        dv_render = dv_comp_render.dv_comp_render()
        dv_render.render_from_args(['-t', 'uvm_object.svh']+self.subcmd_args)

    def command_build_agent(self):
        dv_render = dv_comp_render.dv_comp_render()
        dv_render.render_from_args(['-t', 'uvm_agent_driver.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_monitor.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_config.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_sequencer.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_pkg.svh']+self.subcmd_args)


    def command_init(self):
        ''' The initialize subcommand creates an initial a project configuration file
        if the
        '''
        self.project.init_project(self.subcmd_args)


    def command_new(self):
        ''' Dv_cli add <agent/uvc> <env/uvc> [-inst instance_name]
        '''
        self.project.command_new(self.subcmd_args)

    def command_add(self):
        ''' Dv_cli add <agent/uvc> <env/uvc> [-inst instance_name]
        '''
        self.project.command_add(self.subcmd_args)

    def command_inst(self):
        self.project.command_inst(self.subcmd_args)

    def command_build(self):
        '''
        Dv_cli build [-dest target_dir] // <- build specified tb
        '''

        parser = AP()
        parser.add_argument('name', metavar='NAME', #nargs='+',
                             help='a name of the object type to instance')
        pargs = parser.parse_args(args=self.subcmd_args)

        dvbuild = dv_build.dv_build();
        dvbuild.command_build(pargs.name)

    def command_print(self):
        ''' Dv_cli print '''
        self.project.print_project()


    def command_rm(self):
        ''' Dv_cli rm <agent/uvc> <env/uvc> '''
        pass


if __name__ == "__main__":

    dv = dv_cli()
