"""
    Backup Directories, Handle Files...
"""

import os, logging, zipfile

def make_zipfile(output_filename, source_dir):
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)
                    
def backup_log_directory(log_directory, backup_directory, compress=True,
                         ommit_level=2, verbose=False):
    # @todo: raw copy
    # ommit_level 0: overwrite.
    # ommit_level 1: write if selected compression method not backuped yet
    # ommit_level 2: write only if neither method contains directory.
    nothing_found = True
    # get all directory names in log_directory.
    # zip them into backup_directory
    for directory in os.listdir(log_directory):
        full_dir = os.path.join(log_directory, directory)
        nothing_found = False
        if os.path.isdir(full_dir):
            if  os.path.exists(os.path.join(full_dir, 'combat.log'))\
            and os.path.exists(os.path.join(full_dir, 'game.log'))\
            and os.path.exists(os.path.join(full_dir, 'chat.log'))\
            and os.path.exists(os.path.join(full_dir, 'game.net.log')):
                output_filename = '%s.zip' % directory
                if os.path.exists(os.path.join(backup_directory, output_filename))\
                    and ((ommit_level >= 1 and compress) or (ommit_level==2 and not compress)):
                    logging.warning('Log %s exists as zip backup, ommited.' % output_filename)
                elif os.path.exists(os.path.join(backup_directory, directory))\
                    and ((ommit_level == 2 and compress) or (ommit_level>=1 and not compress)):
                    logging.warning('Log %s exists as directory backup, ommited.' % directory)
                else:
                    # do the backup
                    if compress:
                        make_zipfile(os.path.join(backup_directory, output_filename),
                                 full_dir)
                        logging.info('Backed up %s' % directory)
                        if verbose:
                            print "Backed up %s" % directory
                    else:
                        if verbose:
                            print "Directory Raw Backup not implemented yet."
                        raise NotImplementedError
        else:
            if verbose:
                print "%s is not a directory." % full_dir
    if verbose and nothing_found:
        print "Nothing to backup found in %s" % log_directory


if __name__ == '__main__':
    print "Performing Log Backup (Dev)"
    log_source = os.path.join(os.path.expanduser('~'),
                              'Documents', 'My Games', 'StarConflict', 'logs')
    log_dest = os.path.join(os.path.expanduser('~'),
                              'Documents', 'My Games', 'sc')
    backup_log_directory(log_source, log_dest, verbose=True, compress=True)
    
