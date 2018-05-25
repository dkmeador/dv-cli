#! /usr/bin/env python3
import dv_comp_render
import sys
from argparse import ArgumentParser as AP

class dv_cli:

    def __init__(self):
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

        if not hasattr(self, args.command):
            print ("Unknown command")
            parser.print_help()
            exit(1)

        # dispatch to the sub-command
        getattr(self, args.command)()

    def build_agent(self):
        dv_render = dv_comp_render.dv_comp_render()
        dv_render.render_from_args(['-t', 'uvm_agent_driver.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_monitor.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_config.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_sequencer.svh']+self.subcmd_args)
        #dv_render.render_from_args(['-t', 'uvm_agent_pkg.svh']+self.subcmd_args)

    def build_test(self):
        dv_render = dv_comp_render.dv_comp_render()
        dv_render.render_from_args(['-t', 'uvm_test.svh']+self.subcmd_args)


if __name__ == "__main__":

    dv = dv_cli()