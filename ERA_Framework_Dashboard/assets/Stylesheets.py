# ------- Module: Stylesheets ----------------------
# ------- Stylesheets define the Style of ----------
# ------- Dash components --------------------------
# -*----- coding: utf-8 --------------------------*-


def get_stylesheet_cyto() -> list:
    stylesheet = [
        # Group selectors
        # Define the node and edge styles
        {
            'selector': 'node',
            'style': {
                'label': 'data(label)'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'line-color': 'grey',
                'target-arrow-color': 'grey',
                'target-arrow-shape': 'triangle',
                'label': 'data(impact_score)'
            }
        },


        # Class selectors
        # Design the shapes for each asset type
        {
            'selector': '[class ^= "Process"]',
            'style': {
                'shape': 'rectangle'
            }
        },
        {
            'selector': '[class ^= "Application"]',
            'style': {
                'shape': 'triangle'
            }
        },
        {
            'selector': '[class ^= "Technology"]',
            'style': {
                'shape': 'circle'
            }
        },
        {
            'selector': '[class ^= "Vulnerability"]',
            'style': {
                'shape': 'vee'
            }
        },
        # Design the color of assets according to era score
        {
            'selector': '[era_score < 7.0]',
            'style': {
                'background-color': 'orange'
            }
        },
        {
            'selector': '[era_score < 4.0]',
            'style': {
                'background-color': 'green'
            }
        },
        {
            'selector': '[era_score >= 7.0]',
            'style': {
                'background-color': 'red'
            }
        }
    ]
    return stylesheet


def get_style_pre():
    style = {
        'pre': {
            'border': 'thin lightgrey solid',
            'overflowX': 'scroll'
        }
    }
    return style


def get_style_upload():
    style = {
        'width': '95%',
        'height': '60px',
        'lineHeight': '60px',
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin-top': '10px',
        'margin-left': '20px',
        'margin-right': '20px',
        'margin-bottom': '50px',
        'color': '#bdc8c9',
        'border-color': '#bdc8c9'
    }
    return style

