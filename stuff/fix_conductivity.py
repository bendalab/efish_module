import nixio as nix
import argparse
import os
from IPython import embed


def set_conductivity(filename, conductivity, overwrite):
    f = nix.File.open(filename, nix.FileMode.ReadWrite)
    b = f.blocks[0]
    m = b.metadata
    rec = None
    for s in m.sections:
        if "recording" in s.name.lower():
            rec = s
            break
    if rec is not None:
        cv = nix.Value(float(conductivity))

        prop = None
        if "x-pos" in rec.props:
            prop = rec.props["WaterConductivity"]
            if prop is None:
                prop = rec.create_Property("WaterConductivity", [cv])
                prop.unit = "uS/cm"
            elif prop is not None and overwrite:
                del rec["x-pos"]
                prop = rec.create_Property("WaterConductivity", [cv])
                prop.unit = "uS/cm"
            else:
                print("Eigenschaft WaterConductivity besteht bereits. Wenn ueberschrieben werden" +
                      " soll, muss die Option -o (--overwrite) benutzt werden!")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Aendere die Leitfaehigkeit der Messung.')
    parser.add_argument('datei', type=str, help="Der Pfad der Datei, die bearbeitet werden soll.")
    parser.add_argument("conductivity", type=float, help="Die Leitfaehigkeit.")
    parser.add_argument("-o", "--overwrite", action="store_true",
                        help="Soll ein vorhandener Wert ersetzt werden? Standardwert: False")
    args = parser.parse_args()

    if not os.path.exists(args.datei):
        print('Datei %s existiert nicht!' % args.datei)
        exit()
    set_conductivity(args.datei, args.x, args.y, args.overwrite)
