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
        mcs.meta_handlers[ext] = cls()

    @classmethod
    def get_handler_by_filename(mcs, file_name):
        match = mcs.meta_handlers.keys()
        _proper_match = None
        _ext = None
        while match is not None:
            file_name, ext = os.path.splitext(file_name)
            matches = filter(lambda x: x[:0-len(ext)] is ext,
                    mcs.meta_handlers.keys())
            if matches:
                _ext = "%s.%s" % (ext, _ext)
                _proper_match = matches

        # At this point we should only have 1 match
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
        from sh import unzip


class GZipFileHandler(FileHandlerBase):
    file_ext = "gz"

    def handle(self, file_name, dest):
        from sh import gunzip



def tgz_handle(self, file_name, dest):
    from sh import tar


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
