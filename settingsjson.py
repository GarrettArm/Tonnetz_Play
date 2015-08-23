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
     'desc': 'Easy mode is "Off".  Options below only apply to "Complex On"',
     'section': 'General',
     'key': 'complex'},

    {'type': 'title',
     'title': 'Left Side'},

    {'type': 'options',
     'title': 'Octaves Up',
     'desc': 'Major Scale is 1 Octave up, 1 Octave down, 2 Fifths up, 1 Fifth down, and 1 Third up.\nMinor Scale is 1 Octave up, 1 Octave down, 1 Fifth up, 2 Fifths down, and 1 Third down ',
     'section': 'Fundamental',
     'key': 'octaves_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'octaves_down',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'fifths_down',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Fundamental',
     'key': 'thirds_down',
     'options': ['0', '1', '2', '3', '4', '5']},


    {'type': 'title',
     'title': 'Right Side'},


    {'type': 'options',
     'title': 'Octaves Up',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Octaves Down',
     'desc': '',
     'section': 'Melody',
     'key': 'octaves_down',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Fifths Up',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Fifths Down',
     'desc': '',
     'section': 'Melody',
     'key': 'fifths_down',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Thirds Up',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_up',
     'options': ['0', '1', '2', '3', '4', '5']},

    {'type': 'options',
     'title': 'Thirds Down',
     'desc': '',
     'section': 'Melody',
     'key': 'thirds_down',
     'options': ['0', '1', '2', '3', '4', '5']}])
