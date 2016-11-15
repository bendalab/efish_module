import nixio as nix
import argparse
import os
from IPython import embed


def add_weight(filename, weight, overwrite=False):
    f = nix.File.open(filename, nix.FileMode.ReadWrite)
    b = f.blocks[0]
    m = b.metadata
    subject = None
    for s in m.sections:
        if "subject" in s.name.lower():
            subject = s
            break
    if subject is not None:
        v = nix.Value(weight)
        prop = None
        if "Weight" in subject.props:
            prop = subject.props["Weight"]

        if prop is None:
            prop = subject.create_property("Weight", [v])
            prop.unit = "g"
        elif prop is not None and overwrite:
            prop.values = [v]
        else:
            print("Eigenschaft Weight besteht bereits. Wenn ueberschrieben werden" +
                  " soll, muss die Option --overwrite benutzt werden!")
    f.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fuege das Tiergewicht den Metadaten hinzu.')
    parser.add_argument('datei', type=str, help="Der Pfad der Datei, die bearbeitet werden soll.")
    parser.add_argument("gewicht", type=float, help="Das Gewicht in Gramm (Dezimalpunkt beachten).")
    parser.add_argument("-o", "--overwrite", action="store_true",
                         help="Soll ein vorhandener Wert ersetzt werden? Standardwert: False")
    args = parser.parse_args()

    if not os.path.exists(args.datei):
        print('Datei %s existiert nicht!' % args.datei)
        exit()
    add_weight(args.datei, args.gewicht, args.overwrite)
