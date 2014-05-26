"""
    Simple brainstorm to display a config file.
"""
import os, logging
logging.basicConfig(level=logging.INFO)
# import ET:
try:
    ET = None
    import lxml.etree as ET
    logging.info('Using LXML.')
except ImportError:
    try:
        import cElementTree as ET
        logging.info('Using cElementTree')
    except ImportError:
        try:
            import elementtree.ElementTree as ET
            logging.info('Using ElementTree')
        except ImportError:
            import xml.etree.ElementTree as ET # python 2.5
            logging.info('Using xml.ElementTree')
finally:
    if not ET:
        raise NotImplementedError, "XML Parser not found in your Python."
##################################################################################################


CONFIG_FILE = os.path.join(os.path.expanduser('~'),
                                     'Documents',
                                     'My Games',
                                     'StarConflict',
                                     'user_config.xml')

def read_config(config_file):
    tree = ET.parse(config_file)
    # doc = tree.getroot()
    return tree

if __name__ == '__main__':
    # Read the config
    tree = read_config(CONFIG_FILE)
    doc = tree.getroot()
    if doc.tag == 'UserConfig' \
    and len(doc) == 1\
    and doc[0].tag == 'CVars'\
    and doc[0].attrib['version'] == '4':
        print "Found valid config file."
        cvars = doc[0]
        for child in cvars:
            print '%s = %s' % (child.tag, child.attrib['val'])
    else:
        print "Not found valid config file."