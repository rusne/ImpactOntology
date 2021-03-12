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


def write_shp(filepathname, shtype, fields, objects):
    # POINT = 1; POLYLINE = 3; POLYGON = 5; MULTIPOINT = 8
    w = shapefile.Writer(shtype)
    attributes = []
    for field in fields:
        #create fields
        w.field(**field)
        attributes.append(field["name"])
    for i in range(len(objects)):
        obj = objects[i]
        rec = []
        for att in attributes:
            rec.append(obj[att])
        w.record(*rec)
        if shtype == 1:
            w.point(obj["geom"])
        elif shtype == 3:
            w.line(obj["geom"])
        elif shtype == 5:
            w.poly(obj["geom"])
    w.save(filepathname)
    print('\n {0} has been written \n'.format(filepathname))

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

def plot_patches(patches):
    fig, ax = plt.subplots()
    colors = 100*np.random.rand(len(patches))
    p = PatchCollection(patches, alpha=0.4)
    p.set_array(np.array(colors))
    ax.add_collection(p)
    fig.colorbar(p, ax=ax)

    plt.show()


def shape2patch(sh):
    # type: 'c' - circle,
    print(sh)
    t, param = eval(sh)

    if t == 'c':
        R, (x, y) = param
        ptch = Circle((x, y), R)

    return ptch
