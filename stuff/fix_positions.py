import nixio as nix
import argparse
import os
from IPython import embed


def set_positions(filename, x, y, overwrite):
    f = nix.File.open(filename, nix.FileMode.ReadWrite)
    b = f.blocks[0]
    m = b.metadata
    rec = None
    for s in m.sections:
        if "recording" in s.name.lower():
            rec = s
            break
    if rec is not None:
        xv = nix.Value(float(x))
        yv = nix.Value(float(y))

        prop = None
        if "x-pos" in rec.props:
            prop = rec.props["x-pos"]
            if prop is None:
                prop = rec.create_Property("x-pos", [xv])
                prop.unit = "cm"
            elif prop is not None and overwrite:
                del rec["x-pos"]
                prop = rec.create_Property("x-pos", [xv])
                prop.unit = "cm"
            else:
                print("Eigenschaft x-pos besteht bereits. Wenn ueberschrieben werden" +
                      " soll, muss die Option --overwrite benutzt werden!")

        if "y-pos" in rec.props:
            prop = rec.props["y-pos"]
            if prop is None:
                prop = rec.create_property("y-pos", [yv])
                prop.unit = "cm"
            elif prop is not None and overwrite:
                del rec["x-pos"]
                prop = rec.create_Property("x-pos", [yv])
                prop.unit = "cm"
            else:
                print("Eigenschaft y-pos  besteht bereits. Wenn ueberschrieben werden" +
                      " soll, muss die Option --overwrite benutzt werden!")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aendere die Position der Messelektroden.')
    parser.add_argument('datei', type=str, help="Der Pfad der Datei, die bearbeitet werden soll.")
    parser.add_argument("x", type=float, help="Die x-Position der Elektrode.")
    parser.add_argument("y", type=float, help="Die y-Position der Elektrode.")
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help="Soll ein vorhandener Wert ersetzt werden? Standardwert: False")
    args = parser.parse_args()

    if not os.path.exists(args.datei):
        print('Datei %s existiert nicht!' % args.datei)
        exit()
    set_positions(args.datei, args.x, args.y, args.overwrite)
