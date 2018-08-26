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
                    'interfaces' : {},
                    'components' : {},
                    'basetests'  : {},
                    'tests'      : {},
                    'objects'    : {}
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


    def command_new(self,args):
        '''
            Add a new object or component to the project
        '''
        parser = self.create_commom_argparse()

        pargs = parser.parse_args(args=args)

        if (not any(self.data)):
            self.data = self.read_project()

        self.add_to_project(pargs)


    def add_to_project(self,pargs):
        # Convert list of list pairs to a dict
        config_dict = {x[0] : x[1] for x in pargs.config}

        # defaults
        data_ref    = self.data
        parent_name = "uvm_object"
        package_name = pargs.name + '_pkg' if (pargs.package is None) else pargs.package

        if (pargs.kind == "basetest"):
            parent_name = "uvm_test" if (not  pargs.parent) else pargs.parent;
            data_ref = self.data['basetests']
        elif (pargs.kind == "test"):
            parent_name = "uvm_test" if (not  pargs.parent) else pargs.parent;  # fixme: default to the pkg of parent
            data_ref = self.data['tests']
        elif (pargs.kind == "agent"):
            parent_name = "uvm_agent" if (not  pargs.parent) else pargs.parent;
            data_ref = self.data['components']
        elif (pargs.kind == "env"):
            parent_name = "uvm_env" if (not  pargs.parent) else pargs.parent;
            data_ref = self.data['components']
        elif (pargs.kind == "interface"):
            parent_name = None #interfaces do not support inheritance and can't have a parent
            package_name = None
            data_ref = self.data['interfaces']
        else:
            data_ref = self.data['objects']

        data_ref[pargs.name] = { 'name' : pargs.name,
                                  'kind' : pargs.kind,
                                  'package': package_name,
                                  'children' : [],
                                  'parent' : parent_name,
                                  'config'   : config_dict,
                                  'exists' : False
                                }
        return data_ref[pargs.name]



    def command_add(self,args):
        '''
            Add an existing object or component to the project
        '''
        parser = self.create_commom_argparse()

        pargs = parser.parse_args(args=args)

        if (not any(self.data)):
            self.data = self.read_project()

        obj_ref = self.add_to_project(pargs)

        obj_ref['exists'] = True





    def create_commom_argparse(self):
        parser = AP()
        parser.add_argument(
            '--name', '-n', metavar=('NAME'), action='store',
            dest='name', required=True, help="provide the name of the verification component"
        )
        parser.add_argument(
            '--kind', '-k', metavar=('KIND'), action='store',
            dest='kind', required=True, help="provide the kind of the verification component"
        )
        parser.add_argument(
            '--package', '-p', metavar=('PKG'), action='store',
            dest='package', required=False, help="provide the name of the template else defaults to <name>_pkg"
        )
        parser.add_argument(
            '--parent', '-r', metavar=('PARENT'), action='store',
            dest='parent', required=False, help="provide the name of the parent class"
        )
        parser.add_argument(
            '--set', '-s', nargs=2, metavar=('KEY', 'VALUE'), action='append', default=[],
            dest='config', help='Override config KEY with VALUE expression'
        )
        return parser

    def print_project(self):
        if (not any(self.data)):
            self.data = self.read_project()
        pass

    def write_on_exit(self):
        if (any(self.data)):
            self.write_project();
