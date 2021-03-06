""" Generate a gallery of Bokeh plots from a configuration file.

"""
from __future__ import absolute_import

import json
from os.path import abspath, dirname, join

from sphinx.errors import SphinxError
from sphinx.util import console, copyfile, ensuredir

from .bokeh_directive import BokehDirective
from .templates import GALLERY_PAGE

class BokehGalleryDirective(BokehDirective):

    has_content = False
    required_arguments = 1

    def run(self):
        env = self.state.document.settings.env
        app = env.app

        docdir = dirname(env.doc2path(env.docname))

        dest_dir = join(docdir, "gallery")
        ensuredir(dest_dir)

        specpath = join(docdir, self.arguments[0])
        env.note_dependency(specpath)
        spec = json.load(open(specpath))
        details = spec['details']

        details_iter = app.status_iterator(details,
                                           'copying gallery files... ',
                                           console.brown,
                                           len(details),
                                           lambda x: x['name'] + ".py")

        env.gallery_updated = []
        for detail in details_iter:
            src_path = abspath(join("..", detail['path']))
            dest_path = join(dest_dir, detail['name'] + ".py")
            docname = join("docs", "gallery", detail['name'])

            try:
                copyfile(src_path, dest_path)
            except OSError as e:
                raise SphinxError('cannot copy gallery file %r, reason: %s' % (src_path, e))

            try:
                env.clear_doc(docname)
                env.read_doc(docname, app=app)
                env.gallery_updated.append(docname)
            except Exception as e:
                raise SphinxError('failed to read gallery doc %r, reason: %s' % (docname, e))

        names = [detail['name']for detail in details]
        rst_text = GALLERY_PAGE.render(names=names)

        return self._parse(rst_text, "<bokeh-gallery>")

def env_updated_handler(app, env):
    # this is to make sure the files that were copied and read by hand
    # in by the directive get marked updated and written out appropriately
    return getattr(env, 'gallery_updated', [])

def setup(app):
    app.connect('env-updated', env_updated_handler)
    app.add_directive('bokeh-gallery', BokehGalleryDirective)
