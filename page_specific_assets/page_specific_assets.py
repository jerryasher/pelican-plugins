"""Add JavaScript and CSS files for Pelican
============================================

This plugin allows you to embed page specific JS and CSS in individual posts

+ create page specific css in a file within the pelican directory
  structure and have it linked to a page and served when the page is
  served.

  stylesheet: A.css, B.css, C.css
  style: css-fragment

+ reference external css from a url and have it linked to a page and
  served when the page is served. (Useful for using Google Fonts)

  stylesheet: https://

+ reference a google font selector
  google-font: font-selector

+ create page specific JavaScript in a file within the pelican
  directory structure and have it linked to a page and served when the
  page is served.

  javascript: D, E, F
  script: javascript-fragment

+ reference standard JavaScript libraries (jQuery, Three.js, D3.js,
  etc) by tags and have the correct links for those added to the HEAD

  libs jQuery, ThreeJs, D3JS

+ reference external JavaScript libraries by URL

  libs https://...

+ reference google font families

"""
import os
import logging

from pelican import signals, utils

logger = logging.getLogger(__name__)


def process_page_tags(generator, metadata):
    logger.info("psa: process_page_tags: generator %s" % generator)
    logger.info("psa: process_page_tags: metadata type(metadata) %s" %
                type(metadata))

    for k in metadata:
        v = metadata[k]
        logger.info("psa: process_page_tags: metadata k %s => type(v) %s v %s" %
                    (k, type(v), v))

    process_tags(generator, metadata)


def process_tags(generator, metadata):
    """Process keys in the meta data and insert javascript or link to
    javascript, and insert style or link to external stylesheets in
    the article header.
    """

    print("psa: pt")

    logger.info("psa: process_tags: generator %s" % generator)
    logger.info("psa: process_tags: metadata type(metadata) %s" %
                type(metadata))

    # for k in metadata:
    #     v = metadata[k]
    #     logger.info("psa: process_tags: metadata k %s => type(v) %s v %s" %
    #                 (k, type(v), v))

    googleapi = "https://ajax.googleapis.com/ajax/libs/"
    cloudflare = "https://cdnjs.cloudflare.com/ajax/libs/"
    external_page_libs = {
        'jquery': googleapi + 'jquery/3.1.1/jquery.min.js',
        'jquery3': googleapi + 'jquery/3.1.1/jquery.min.js',
        'jquery2': googleapi + 'jquery/2.2.4/jquery.min.js',
        'three.js': googleapi + 'threejs/r76/three.min.js',
        'threejs': googleapi + 'threejs/r76/three.min.js',
        'vue': cloudflare + "vue/2.0.3/vue.js"
    }

    font_keys = ['google-font']
    block_keys = ['style', 'script']
    reference_keys = ['stylesheet', 'lib']

    equivalent_keys = {
        'stylesheet': 'stylesheet',
        'lib': 'lib',
        'google-font': 'google-font',
        'font': 'google-font',
        'style': 'style',
        'css': 'style',
        'script': 'script',
        'javascript': 'script',
    }

    location = {
        'stylesheet': 'header_assets',
        'google-font': 'header_assets',
        'font': 'header_assets',
        'style': 'header_assets',
        'lib': 'footer_assets',
        'script': 'footer_assets'
    }

    reference_fmts = {
        'stylesheet': '<link rel="stylesheet" href="{0}" type="text/css" />',
        'lib': '<script src="{0}"></script>',
        'google-font':
        '<link rel="stylesheet"'
            'href="http://fonts.googleapis.com/css?family={0}" />'
    }

    dirs = {'stylesheet': 'css',
            'lib': 'js'}

    site_url = generator.settings['SITEURL']
    if 'EXTERNAL_PAGE_LIBS' in generator.settings:
        external_page_libs += generator.settings['EXTERNAL_PAGE_LIBS']

    sections = location.values()
    frags = {}

    for key in metadata:
        lkey = key.lower()

        if lkey in equivalent_keys:
            lkey = equivalent_keys[lkey]
        else:
            lkey = key[0:-1]  # strip off last char ("s" or any)
            if lkey in equivalent_keys:
                lkey = equivalent_keys[lkey]

        html_frags = []
        entities = metadata[key]
        if isinstance(entities, type(u"u")):
            entities = [entities]

        if lkey in block_keys:
            # style and script
            logger.info("psa: block_keys: key->%s lkey->%s type->%s "
                        "entities %s" % (key, lkey, type(entities), entities))

            for block in entities:
                html_frags.append(block)
        elif lkey in font_keys:
            logger.info("psa: font_keys: lkey %s type(entities) %s entities %s"
                        % (lkey, type(entities), entities))

            for font in entities:
                html = reference_fmts[lkey].format(font)
                html_frags.append(html)
        elif lkey in reference_keys:
            logger.info("psa: reference_keys: lkey %s type(entities) %s "
                        "entities %s" % (lkey, type(entities), entities))

            for line in entities:
                refs = line.replace(" ", "").split(",")
                for ref in refs:
                    if ref in external_page_libs:
                        link = external_page_libs[ref]
                    elif ref.startswith('http://') or \
                            ref.startswith('https://'):
                        link = ref
                    else:
                        if generator.settings['RELATIVE_URLS']:
                            link = "%s/%s" % (dirs[key], ref)
                        else:
                            link = "%s/%s/%s" % (site_url, dirs[key], ref)
                    html = reference_fmts[lkey].format(link)
                    html_frags.append(html)

        if html_frags:
            section = location[lkey]
            if section in frags:
                current = frags[section]
            else:
                current = []
            html_frags = current + html_frags
            frags[section] = html_frags
            logger.info("psa: frags[%s] = %s" % (section, html_frags))

    for s in sections:
        if s in frags:
            metadata[s] = frags[s]
            logger.info("psa: metadata[%s] = (%s) %s" %
                        (s, type(metadata[s]), metadata[s]))


def copy_assets(content, output, file_list):
    """
    Copy assets from content folders to output folders

    Parameters
    ----------
    content: a string, the file path of the content directoy
    output: a string, the file path of the output directory

    file_list: list
        List of files to be transferred

    Output
    ------
    Copies files from content to output
    """

    if not os.path.exists(output):
        os.makedirs(output)
    for file_ in file_list:
        file_content = os.path.join(content, file_)
        logger.info("psa: copy_assets %s to %s" % (file_content, output))
        utils.copy(file_content, output)


def move_assets(generator):
    """
    Move files from js/css folders to output folder
    """

    js_files = generator.get_files('js', extensions='js')
    css_files = generator.get_files('css', extensions='css')

    js_dest = os.path.join(generator.output_path, 'js')
    copy_assets(generator.path, js_dest, js_files)

    css_dest = os.path.join(generator.output_path, 'css')
    copy_assets(generator.path, css_dest, css_files)


def register():
    """
    Plugin registration
    """
    signals.article_generator_context.connect(process_tags)
    signals.page_generator_context.connect(process_page_tags)
    signals.article_generator_finalized.connect(move_assets)
    logger.info("psa: page_specific_assets plugin registered")
