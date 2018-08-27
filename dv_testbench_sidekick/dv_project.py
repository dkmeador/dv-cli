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
            self.data = {'about'      : {'project' : "my_project",
                                         'template_dir' : os.path.dirname(os.path.realpath(__file__)) + '/templates',
                                         'subdir_per_pkg' : True
                                        },
                    'interfaces' : {},
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


    def command_add(self,args):
        '''
            Add an existing object or component to the project
        '''
        parser = self.create_commom_argparse()
        parser.add_argument(
            'file', metavar='FILE',
             help="provide the file name of the verification component"
        )
        pargs = parser.parse_args(args=args)

        if (not any(self.data)):
            self.data = self.read_project()

        obj_ref = self.add_to_project(pargs)

        obj_ref['exists'] = True

    def command_inst(self,args):
        parser = self.create_connect_argparse()

        pargs = parser.parse_args(args=args)

        if (not any(self.data)):
            self.data = self.read_project()

        self.data['objects'][pargs.inst_loc]['children'][pargs.inst_name] = {'name' : pargs.name, 'num_insts' :pargs.inst_num}


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
            data_ref = self.data['objects']
        elif (pargs.kind == "env"):
            parent_name = "uvm_env" if (not  pargs.parent) else pargs.parent;
            data_ref = self.data['objects']
        elif (pargs.kind == "interface"):
            parent_name = None #interfaces do not support inheritance and can't have a parent
            package_name = None
            data_ref = self.data['interfaces']
        else:
            data_ref = self.data['objects']

        data_ref[pargs.name] = { 'name' : pargs.name,
                                  'kind' : pargs.kind,
                                  'package': package_name,
                                  'children' : {},
                                  'parent' : parent_name,
                                  'config'   : config_dict,
                                  'exists' : False
                                }
        return data_ref[pargs.name]



    def create_commom_argparse(self, parser = None):
        if (parser == None):
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

    def create_connect_argparse(self,parser = None):
        '''
            inst foo --in bar [-as foo_inst] [-parameter myparm myparmvalue]
        '''
        if (parser == None):
            parser = AP()

        parser.add_argument('name', metavar='NAME', #nargs='+',
                             help='a name of the object type to instance')

        parser.add_argument(
            '--in', '-i', metavar=('INST_LOCATION'), action='store',
            dest='inst_loc', required=True, help="provide the name of the class to place the instance"
        )
        parser.add_argument(
            '--as', '-a', metavar=('INST_NAME'), action='store',
            dest='inst_name', required=True, help="provide the name of the instance"
        )
        parser.add_argument(
            '--num', '-n', metavar=('NUM'), action='store',
            dest='inst_num', required=False,
            help="provide the number of instance as an integer 'q' for a queue or 'd' for dynamic array"
        )

        return parser

    def print_project(self):
        if (not any(self.data)):
            self.data = self.read_project()
        print ("Objects:")
        for id,desc in self.data['objects'].items():
            print (desc['package'] + "::" + id + " of type " + desc['kind'] + ", extended from " + desc['parent'])

        print ("Interfaces:")
        for id,desc in self.data['interfaces'].items():
            print (id)

        print ("Tests:")
        for id,desc in self.data['tests'].items():
            print (desc['package'] + "::" + id + " of type " + desc['kind'] + ", extended from " + desc['parent'])


    def write_on_exit(self):
        if (any(self.data)):
            self.write_project();
