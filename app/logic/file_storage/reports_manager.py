import logging

from uuid import uuid4
from os.path import join, exists
from os import stat
from os import remove as os_remove
from shutil import move
from flask import abort

from app import cfg

_file_set = cfg.FILE_UPLOADS.FILE_SETS['REPORT']

def save(file):
    file_extension = file.filename.rsplit('.', 1)[1].lower()        
    if file_extension not in _file_set.ALLOWED_EXTENSIONS:
        abort(415, "File extension not supported")
    if file.mimetype not in _file_set.ALLOWED_MIME_TYPES:
        abort(415, "File MIME-type not supported")
    if file.content_length > _file_set.MAX_SIZE: # Не будет работать, пока Chrome и Firefox не перестанут ставить Content-Length равным 0 ¯\_(ツ)_/¯
        abort(413, "File size exceeds allowed limit")

    filename = str(uuid4())
    tmp_path = join(cfg.FILE_UPLOADS.TEMP_FOLDER, filename)
    file.save(tmp_path)
    size = stat(tmp_path).st_size
    logging.debug('File size is {}'.format(size))
    if size > _file_set.MAX_SIZE:
        remove(tmp_path)
        abort(413, "File size exceeds allowed limit")

    new_path = join(_file_set.FOLDER, filename)
    move(tmp_path, new_path)
    return filename

def get(id):
    return _file_set.FOLDER, id

def remove(filename):
    logging.debug(filename)
    path = join(_file_set.FOLDER, filename)
    logging.debug(path)
    if exists(path):
        os_remove(path)
        logging.debug(
            "Removed report [{id}] from [{path}]".format(
                id=filename,
                path=path
            )
        )
    else:
        abort(404, "Report not found")