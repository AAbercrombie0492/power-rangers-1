from werkzeug.routing import BaseConverter
import shapely
from shapely.geometry import shape, JOIN_STYLE
from shapely.ops import cascaded_union

def join_polygons(polygons):
    eps = 0.001
    buffered_polys = [poly.buffer(eps, 1, join_style=JOIN_STYLE.mitre) for poly in polygons]
    super_poly = cascaded_union(buffered_polys)
    super_poly = super_poly.buffer(-eps, 1, join_style=JOIN_STYLE.mitre)
    return super_poly

class ListConverter(BaseConverter):

    def to_python(self, value):
        return value.split('+')

    def to_url(self, values):
        return '+'.join(BaseConverter.to_url(value)
                        for value in values)
