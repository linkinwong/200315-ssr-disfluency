#!/usr/bin/env python

"""
A feature extractor for chunking.
__author__ = linlin
"""

# Separator of field values.
separator = ' '

# Field names of the input data.
fields = 'y w pos token sem part pp p n nn'

# Attribute templates.
templates = (
    (('w', -2), ),
    (('w', -1), ),
    (('w',  0), ),
    (('w',  1), ),
    (('w',  2), ),
    (('w', -1), ('w',  0)),
    (('w',  0), ('w',  1)),
    (('pos', -2), ),
    (('pos', -1), ),
    (('pos',  0), ),
    (('pos',  1), ),
    (('pos',  2), ),
    (('pos', -2), ('pos', -1)),
    (('pos', -1), ('pos',  0)),
    (('pos',  0), ('pos',  1)),
    (('pos',  1), ('pos',  2)),
    (('pos', -2), ('pos', -1), ('pos',  0)),
    (('pos', -1), ('pos',  0), ('pos',  1)),
    (('pos',  0), ('pos',  1), ('pos',  2)),
    (('sem', -2),),
    (('sem', -1),),
    (('sem',  0),),
    (('sem',  1),),
    (('sem',  2),),
    (('sem', -2), ('sem', -1)),
    (('sem', -1), ('sem', 0)),
    (('sem', 0), ('sem', 1)),
    (('sem', 1), ('sem', 2)),
    (('part', 0),),
    (('pp', 0),),
    (('p', 0),),
    (('n', 0),),
    (('nn', 0),),
    )


import crfutils

def feature_extractor(X):
    # Apply attribute templates to obtain features (in fact, attributes)
    crfutils.apply_templates(X, templates)
    if X:
	# Append BOS and EOS features manually
        X[0]['F'].append('__BOS__')     # BOS feature
        X[-1]['F'].append('__EOS__')    # EOS feature

if __name__ == '__main__':
    crfutils.main(feature_extractor, fields=fields, sep=separator)
