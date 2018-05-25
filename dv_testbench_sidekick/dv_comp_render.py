import os, sys
import jinja2
from argparse import ArgumentParser as AP


class dv_comp_render(object):

    def __init__(self):
        pass

    def render_from_args(self, args = sys.argv[1:]):
        parser = AP()
        parser.add_argument(
            '--template', '-t', nargs=1, metavar=('FILE'), action='append', default=[],
            dest='template', required=True, help="provide the name of the template"
        )
        parser.add_argument(
            '--output', '-o', metavar=('FILE'), action='store', default='', dest='outfile',
            help='Provide the name of the output file'
        )
        parser.add_argument(
            '--set', '-s', nargs=2, metavar=('KEY', 'VALUE'), action='append', default=[],
            dest='config', help='Override config KEY with VALUE expression'
        )

        args = parser.parse_args(args=args)

        context = {x[0]: x[1] for x in args.config}

        #
        if not args.outfile:
            args.outfile = context.get("name", "")
            # args.outfile = item.__dict__.get("name", "")
            args.outfile += ".svh" if args.outfile else ""

        if args.outfile:
            file = open(args.outfile, 'w')

        for f in args.template:
            result = self.render(f[0], context)
            if args.outfile:
                file.write(result)
                print("Using template " + f[0] + ", wrote file: " + args.outfile)
            else:
                print(result)

        if args.outfile:
            file.close()


    def render (self, tpl_path, context):
        path, filename = os.path.split(tpl_path)
        search_path = [path or './']
        search_path.append(os.path.dirname(os.path.abspath(__file__))+ "/templates")

        return jinja2.Environment(loader=jinja2.FileSystemLoader(search_path)).get_template(filename).render(context)


if __name__ == "__main__":

    dv_render = dv_comp_render()
    dv_render.render_from_args()

