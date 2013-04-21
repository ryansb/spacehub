import os

class HandlerMeta(type):
    meta_handlers = {}

    def __new__(mcs, name, bases, dct):
        if name is "FileHandlerBase":
            return type.__new__(mcs, name, bases, dct)

        if 'file_ext' not in dct:
            raise AttributeError("Need a file_ext")

        ins = type.__new__(mcs, name, bases, dct)

        mcs.register(ins, dct['file_ext'])

        return lambda: mcs.meta_handlers[dct['file_ext']]

    @classmethod
    def register(mcs, cls, ext):
        print "Handle Register: %s for extension '%s'" % (cls.__name__, ext)
        mcs.meta_handlers[ext] = cls()

    @classmethod
    def get_handler_by_filename(mcs, file_name):
        match = mcs.meta_handlers.keys()
        _proper_match = None
        _ext = None
        ext = file_name
        while ext:
            file_name, ext = os.path.splitext(file_name)
            ext = ext[1:]

            if not ext:
                break

            print "Looking at %s..." % ext
            matches = filter(lambda x: x[-len(ext):] in ext,
                    mcs.meta_handlers.keys())

            print matches
            if matches:
                print "Possible matches...", ", ".join(matches)
                _ext = ".".join([ext, _ext]) if _ext else ext
                _proper_match = matches
            else:
                break

        # At this point we should only have 1 match
        print _ext, _proper_match
        if _ext not in _proper_match:
            # we done goofed
            raise ValueError("We have no idea how to process this file")

        return mcs.meta_handlers[_ext]


class FileHandlerBase(object):
    __metaclass__ = HandlerMeta

    def handle(self, file_name, dest):
        raise AttributeError("handle() was not defined by child class")


class ZipFileHandler(FileHandlerBase):
    file_ext = "zip"

    def handle(self, file_name, dest):
        dest = os.path.abspath(dest)
        from sh import unzip
        if not os.path.exists(dest):
            os.makedirs(dest)

        # Make moves
        tar(file_name, '-d', dest)

        if len(os.listdir(dest)) is 1:
            # somewhat properly packaged tarball
            dest = os.path.join(dest, os.listdir(dest).pop())
        return dest


class TarFileHandler(FileHandlerBase):
    file_ext = "tar"

    def handle(self, file_name, dest):
        dest = os.path.abspath(dest)
        from sh import tar
        ops_flags = "xvf"
        if not os.path.exists(dest):
            os.makedirs(dest)

        # Make moves
        tar(ops_flags, file_name, "-C", dest)

        if len(os.listdir(dest)) is 1:
            # somewhat properly packaged tarball
            dest = os.path.join(dest, os.listdir(dest).pop())
        return dest


def tgz_handle(self, file_name, dest):
    dest = os.path.abspath(dest)
    from sh import tar
    ops_flags = "zxvf"
    if not os.path.exists(dest):
        os.makedirs(dest)

    # Make moves
    tar(ops_flags, file_name, "-C", dest)

    if len(os.listdir(dest)) is 1:
        # somewhat properly packaged tarball
        dest = os.path.join(dest, os.listdir(dest).pop())
    return dest


class TarGZipFileHandler(FileHandlerBase):
    file_ext = "tar.gz"
    handle = tgz_handle


class TgzFileHandler(FileHandlerBase):
    file_ext = "tgz"
    handle = tgz_handle


def handle_file(file_name, dest):
    handler = HandlerMeta.get_handler_by_filename(file_name)
    handler.handle(file_name, dest)

    return dest

__all__ = ['handle_file']
