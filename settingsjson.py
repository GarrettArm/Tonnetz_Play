import json

general_settings_json = json.dumps([

    {'type': 'options',
     'title': 'Key',
     'desc': '',
     'section': 'General',
     'key': 'key',
     'options': ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']},

    {'type': 'options',
     'title': 'Scale',
     'desc': '',
     'section': 'General',
     'key': 'scale',
     'options': ['Major', 'Minor', 'Freehand']},

    {'type': 'bool',
     'title': 'Complex',
     'desc': '',
     'section': 'General',
     'key': 'complex'},

    {'type': 'title',
     'title': 'Left Side'},

    {'type': 'options',
     'title': 'Octaves Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'octaves_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'octaves_down',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_down',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_down',
     'options': ['0','1','2','3','4','5']},


    {'type': 'title',
     'title': 'Right Side'},


    {'type': 'options',
     'title': 'Octaves Up',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_down',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_down',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_up',
     'options': ['0','1','2','3','4','5']},

    {'type': 'options',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_down',
     'options': ['0','1','2','3','4','5']}])