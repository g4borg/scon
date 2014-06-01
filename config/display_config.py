"""
    Simple brainstorm to display a config file.
"""
import os, logging
from settings import settings
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

class ConfigFile(object):
    def __init__(self, config_file=None):
        self.cvars = []
        if config_file:
            self.config_file = config_file
        elif settings:
            # settings based loading.
            self.config_file = os.path.join(settings.get_path(), 'user_config.xml')
    
    def open(self, filename = None):
        # reads a config file.
        filename = filename or self.config_file
        self.tree = ET.parse(filename)
        doc = self.tree.getroot()
        if doc.tag == 'UserConfig' \
            and len(doc) == 1\
            and doc[0].tag == 'CVars'\
            and doc[0].attrib['version'] == '4':
            logging.info( "Found valid config file." )
            # save my cvars
            self.cvars = doc[0]
        else:
            logging.info( "Config File not supported." )
        return self
    
    def pprint(self):
        # print out my cvars
        for child in self.cvars:
            print '%s = %s' % (child.tag, child.attrib['val'])
    
    def write(self, filename):
        output = '<?xml version="1.0"?>\n'
        doc = self.tree.getroot()
        # we manually serialize it to keep it exactly the same 
        # like original SC to avoid problems with their software.
        def append_node(node, depth=0):
            # xml serializing helper function...
            s = ['%s<%s' % (' '*depth*2, node.tag),]
            for key, val in node.attrib.items():
                s.append(' %s="%s"' % (key, val))
            if len(node):
                s.append('>\n')
                # append children
                for child in node:
                    s.extend(append_node(child, depth+1))
                s.append('%s</%s>\n' % (' '*depth*2, node.tag))
            else:
                s.append(' />\n')
            return s
        l = append_node(doc)
        output = output + ''.join( l )
        if filename is None:
            # dev.
            assert output[-1], '\n'
        else:
            try:
                f = open(filename, 'w')
                f.write(output)
            finally:
                f.close()
        return output
    
    def debug_serializing(self):
        # detects if output would result in the same data as input
        input, output = None, None
        try:
            f = open(self.config_file, 'r')
            input = f.read()
        finally:
            f.close()
        output = self.write(None)
        return output == input
            
    
def read_config(config_file):
    tree = ET.parse(config_file)
    # doc = tree.getroot()
    return tree

if __name__ == '__main__':
    # Read the config
    settings.autodetect()
    c = ConfigFile().open()
    print '#' * 80
    print "Output File would be:"
    print c.write(None)
    print '#' * 80
    print "Detected Settings:"
    c.pprint()
    print '#' * 80
    print 'Serializing Test successful: %s' % c.debug_serializing()
    