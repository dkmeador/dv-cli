#! /usr/bin/env python3
import sys
import json
import os
import atexit
from argparse import ArgumentParser as AP

class dv_project:

    def __init__(self, path="./"):
        self.project_filename = ".dv_cli_project.json"
        self.fullpath = path + self.project_filename
        self.data = {}
        atexit.register(self.write_on_exit)

    def init_project(self, args):
        if ( os.path.isfile(self.fullpath) ):
            sys.exit("Project file already exists:" + self.fullpath)
        else:
            self.data = {'about'      : {'project' : "my_project"},
                    'agents'     : {},
                    'interfaces' : {},
                    'envs'       : {},
                    'tests'      : {}
                    }
            # Write JSON file
            self.write_project()


    def write_project(self):
        # Write JSON file
        with open(self.fullpath, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(self.data,
                indent=4, sort_keys=True,
                separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)


    def read_project(self):
        if ( not os.path.isfile(self.fullpath) ):
            sys.exit("Project file does not exist:" + self.fullpath)
        else:
            fp = open(self.fullpath, 'r', encoding='utf8')
            return json.load(fp)

    def add_interface(self):
        if (not any(self.data)):
            self.data = self.read_project()
        self.data['interfaces']['interface1'] = { }

    def add_agent(self, args):
        parser = AP()
        parser.add_argument(
            '--name', '-n', metavar=('NAME'), action='store',
            dest='name', required=True, help="provide the name of the template"
        )
#        parser.add_argument(
#            '--template', '-t', metavar=('FILE'), action='store_const',
#            dest='template', required=False, help="provide the name of the template"
#        )
        parser.add_argument(
            '--package', '-p', metavar=('PKG'), action='store',
            dest='package', required=False, help="provide the name of the template else defaults to <name>_pkg"
        )
        parser.add_argument(
            '--set', '-s', nargs=2, metavar=('KEY', 'VALUE'), action='append', default=[],
            dest='config', help='Override config KEY with VALUE expression'
        )

        pargs = parser.parse_args(args=args)

        context = {x[0]: x[1] for x in pargs.config}

        if (not any(self.data)):
            self.data = self.read_project()

        self.data['agents'][pargs.name] = { 'package': pargs.name + '_pkg' if (pargs.package is None) else pargs.package,
                                           'children' : [],
                                                  }

    def add_env(self,args):
        parser = AP()
        parser.add_argument(
            '--name', '-n', metavar=('NAME'), action='store',
            dest='name', required=True, help="provide the name of the template"
        )
        parser.add_argument(
            '--package', '-p', metavar=('PKG'), action='store',
            dest='package', required=False, help="provide the name of the template else defaults to <name>_pkg"
        )
        parser.add_argument(
            '--set', '-s', nargs=2, metavar=('KEY', 'VALUE'), action='append', default=[],
            dest='config', help='Override config KEY with VALUE expression'
        )

        pargs = parser.parse_args(args=args)

        if (not any(self.data)):
            self.data = self.read_project()

        self.data['agents'][pargs.name] = {'package': pargs.name + '_pkg' if (pargs.package is None) else pargs.package,
                                           'children' : [],
                                         }

    def add_test(self):
        if (not any(self.data)):
            self.self.data = self.read_project()
        self.data['tests']['test1'] = { 'package': 'test1_pkg',
                                     'parent' : "uvm_test"
                                    }
    def write_on_exit(self):
        if (any(self.data)):
            self.write_project();
