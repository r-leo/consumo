from folium import Element
from folium.plugins import DualMap
from folium.utilities import deep_copy
from IPython.display import HTML


def custom_dual_map(location, tiles, zoom_start, submap_size, title_left, title_right,
                    geojson_left=None, geojson_right=None, scrollWheelZoom=True):
    
    # Create DualMap object and add GeoJSON layers
    m = DualMap(location=location, tiles=tiles, zoom_start=zoom_start, scrollWheelZoom=scrollWheelZoom)
    if geojson_left:
        deep_copy(geojson_left).add_to(m.m1)
    if geojson_right:
        deep_copy(geojson_right).add_to(m.m2)

    # Unpack submap dimensions
    w, h = submap_size

    # Function to generate the HTML code for each subplot's title
    def map_title(side, title):
        return f"""
        <div id="title_{side}" style="
            position: absolute;
            top: 10px;
            right: {w + 20 + 10 if side == 'left' else 10}px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 5px 10px;
            z-index: 9999;
            font-weight: bold;
            border-radius: 5px;
            font-size: 14px;">
            {title}
        </div>
        """

    # CSS to inject into the map classes
    new_css = f"""
    <style>
    #{m.m1.get_name()}, #{m.m2.get_name()} {{
        height: {h}px;
        width: {w}px;
    }}
    #{m.m2.get_name()} {{
        left: {w + 20}px;
    }}
    .leaflet-bottom {{
        display: none;
    }}
    path.leaflet-interactive {{
        outline: none;
    }}
    </style>
    """

    # Inject CSS and HTMl
    m.get_root().html.add_child(Element(new_css))
    m.get_root().html.add_child(Element(map_title('left', title_left)))
    m.get_root().html.add_child(Element(map_title('right', title_right)))

    return m, w, h


def plot_dual_map(m, w, h):
    new_html = m._repr_html_().replace(
        'position:relative;width:100%;height:0;padding-bottom:60%;',
        f'position:relative;width:{2 * w + 20}px;height:{h}px;padding-bottom:0;')
    return HTML(new_html)