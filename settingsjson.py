import json

general_settings_json = json.dumps([

    {'type': 'title',
     'title': 'General Options'},

    {'type': 'options',
     'title': 'Scale',
     'desc': '',
     'section': 'General',
     'key': 'scale',
     'options': ['Major', 'Minor', 'Freehand']},

    {'type': 'options',
     'title': 'Key',
     'desc': '',
     'section': 'General',
     'key': 'key',
     'options': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']},

    {'type': 'string',
     'title': 'A string setting',
     'desc': 'String description text',
     'section': 'General',
     'key': 'stringexample'},

    {'type': 'path',
     'title': 'A path setting',
     'desc': 'Path description text',
     'section': 'General',
     'key': 'pathexample'},

    {'type': 'bool',
     'title': 'boolean example',
     'desc': 'Boolean description text',
     'section': 'General',
     'key': 'boolexample'}])

fund_settings_json = json.dumps([

    {'type': 'numeric',
     'title': 'Octaves Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'octaves_up'},

    {'type': 'numeric',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'octaves_down'},

    {'type': 'numeric',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_up'},

    {'type': 'numeric',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_down'},

    {'type': 'numeric',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_up'},

    {'type': 'numeric',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_down'}])

melody_settings_json = json.dumps([

    {'type': 'numeric',
     'title': 'Octaves Up',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_up'},

    {'type': 'numeric',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_down'},

    {'type': 'numeric',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_up'},

    {'type': 'numeric',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_down'},

    {'type': 'numeric',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_up'},

    {'type': 'numeric',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_down'}])