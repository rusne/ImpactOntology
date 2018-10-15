import shapefile


def read_shp(filepath, filename):

    sf = shapefile.Reader(filepath + filename)

    fields = sf.fields
    header = [h[0] for h in fields][1:]
    header.append('geom')
    shapes = sf.shapes()
    shapetype = sf.shapeType

    records = sf.records()
    attribute_table = []
    for i in range(len(records)):
        data = records[i]
        if shapetype == 1:
            geom = shapes[i].points
        else:
            geom = []
            points = shapes[i].points
            parts = shapes[i].parts
            parts.append(len(points))
            for i in range(len(parts) - 1):
                geom.append(points[parts[i]:parts[i + 1]])
        data.append(geom)
        attribute_table.append(data)

    return header, attribute_table


def write_shp(filepathname, shtype, objects):
    # POINT = 1; POLYLINE = 3; POLYGON = 5; MULTIPOINT = 8
    w = shapefile.Writer(shtype)
    for i in range(len(objects)):
        obj = objects[i]
        rec = []
        for key in sorted(obj.keys()):
            if i == 0:
            #create fields
                w.field(key, 'C')
            if key == 'geom':
                if shtype == 1:
                    w.point(obj[key])
                elif shtype == 3:
                    w.line(obj[key])
                elif shtype == 5:
                    w.poly(obj[key])
            rec.append(obj[key])
        w.record(*rec)
    w.save(filepathname)

def make_point(shpoint):
    # turn shapefile point into WKT point
    x, y = shpoint[0]
    stpoint = 'POINT({0} {1})'.format(x, y)
    return stpoint


def make_polygon(shpolygon):
    multi = []
    for part in shpolygon:
        poly = ['{0} {1}'.format(x, y) for x, y in part]
        # poly.append(poly[0])
        poly = ','.join(poly)
        multi.append('(' + poly + ')')
    multi = ' '.join(multi)
    polygon = 'MULTIPOLYGON(({0}))'.format(multi)
    return polygon.format(multi)


def wkt2geom(geom):
    # turn WKT geometry into shapely geometry
    from shapely.wkt import loads
    shp_geom = loads(geom)
    return shp_geom


def geom2wkt(geom):
    # turn shapely geometry into WKT geometry
    from shapely.wkt import dumps
    wkt_geom = dumps(geom)
    return wkt_geom


def wkt2list(geom):
    # turn WKT geometry into a generic list of coordinates
    ext = list(wkt2geom(geom).exterior.coords)
    int = list(wkt2geom(geom).interiors)
    if int:
        return [ext, int]
    else:
        return [ext]
