from jinja2 import Template

template = Template(open('maps/map_template.html').read())


def render_map_with_dicts(dicts, map_name):
    """
    Every dict in dicts must have the following keys:
            Latitude
            Longitude
            description
            color
            scale
    """
    with open('maps/%s' % map_name, 'w+') as f:
        f.write(template.render(points=dicts))


def render_map_with_dataframe(df, map_name):
    if 'color' not in df.columns:
        df['color'] = 'red'
    if 'description' not in df.columns:
        df['description'] = ""
    if 'scale' not in df.columns:
        df['scale'] = 5.0
    dicts = df.T.to_dict().values()
    render_map_with_dicts(dicts, map_name)
