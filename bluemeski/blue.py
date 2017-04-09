"""
See how the Oasis runs.

Watch the stream go by


"""
from datetime import datetime
from pathlib import Path

from karmapi import pigfarm, base

class Magic(pigfarm.MagicCarpet):
    pass

def data_diff(aa, bb):
    """ Return something useful to compare what is aa to bb """

    keys = set(aa.keys())
    keys += set(bb.keys())

    data = {}

    for key in keys:
        if key in aa and key in bb:
            data[key] = aa - bb
        else:
            if key in aa:
                data[key] = aa[key]
            else:
                data[key] = bb[key]

    return data
    
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default='.')
    parser.add_argument('--today', action='store_true')

    parser.add_argument('name', nargs='?', default='sensehat')

    parser.add_argument('compare', nargs='?')
    
    args = parser.parse_args()

    farm = pigfarm.PigFarm()

    path = Path(args.path)

    path = path / args.name

    if args.today:
        now = datetime.now()
        path = path / f'{now.year}/{now.month}/{now.day}'

    if path.exists():
        data = base.load_folder(path)

        farm.data.put(data)

    compare = args.compare
    print('COMPARE', compare)
    if compare:
        compare = path / compare

    if compare.exists():
        print('compare exists')
        b_data = base.load_folder(path)

        delta = data_diff(data, b_data)

    from karmapi.mclock2 import GuidoClock

    farm.add(Magic, dict(data=data))

    if compare.exists():
        farm.add(Magic, dict(data=b_data))
        farm.add(Magic, dict(data=delta))
        
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
