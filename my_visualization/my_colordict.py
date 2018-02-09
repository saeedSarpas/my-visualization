"""
main.py
Main class of my_visualization package
"""


def get(cscheme):
    """Return colorscheme

    Parameter
    ---------
    cscheme : str
        Color scheme name
    """
    return CDICT[str(cscheme) if cscheme in CDICT.keys() else 'RAINBOW']



CDICT = {
    'RAINBOW': {
        'dict': {
            'red': [
                (0.00, 0.00000, 0.28125),
                (0.33, 0.46484, 0.46484),
                (0.66, 0.67967, 0.67967),
                (1.00, 0.90625, 0.90625)
            ],
            'green': [
                (0.00, 0.00000, 0.26562),
                (0.33, 0.54297, 0.54297),
                (0.66, 0.73828, 0.73828),
                (1.00, 0.83984, 0.83984)
            ],
            'blue': [
                (0.00, 0.00000, 0.29687),
                (0.33, 0.58594, 0.58594),
                (0.66, 0.75000, 0.75000),
                (1.00, 0.73828, 0.73828)
            ]
        },
        'primary_colors': ['#ff4843', '#328bdc', '#5fae5b', '#fbac47'],
        'primary_shadows': ['#d97b78', '#84a8ca', '#88af85', '#d9b876'],
        'helper_colors': ['#e68570', '#688eb5', '#91ab59', '#e1ca61'],
        'background': '#ffffff',
        'gridcolor': '#ffffff',
        'axiscolor': '#000000'
    },
    'ICE': {
        'dict': {
            'red': [
                (0.00, 0.00000, 0.94531),
                (0.05, 0.73047, 0.73047),
                (0.21, 0.62890, 0.62890),
                (1.00, 0.09765, 0.09765)
            ],
            'green': [
                (0.00, 0.00000, 0.94531),
                (0.05, 0.72656, 0.72656),
                (0.21, 0.83203, 0.83203),
                (1.00, 0.58203, 0.58203)
            ],
            'blue': [
                (0.00, 0.00000, 0.94531),
                (0.05, 0.74219, 0.74219),
                (0.21, 0.88281, 0.88281),
                (1.00, 0.67578, 0.67578)
            ]
        },
        'primary_colors': ['#ff4843', '#328bdc', '#fbac47', '#5fae5b'],
        'primary_shadows': ['#d97b78', '#84a8ca', '#d9b876', '#88af85'],
        'helper_colors': ['#e68570', '#688eb5', '#e1ca61', '#91ab59'],
        'background': '#f0f0f0',
        'gridcolor': '#ffffff',
        'axiscolor': '#666666'
    },
}
