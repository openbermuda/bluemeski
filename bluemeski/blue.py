"""
See how the Oasis runs.

Watch the stream go by


"""
from datetime import datetime, timedelta
from pathlib import Path

from karmapi import pigfarm, base

class Magic(pigfarm.MagicCarpet):
    pass

def data_diff(aa, bb):
    """ Return something useful to compare whatever aa is to bb """

    keys = set(aa.keys())
    keys.update(set(bb.keys()))

    data = {}

    for key in keys:
        if key in aa and key in bb:
            data[key] = aa[key] - bb[key]
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

    compare = args.compare
    if compare:
        compare = args.path / compare 
    
    if args.today:
        now = datetime.now()
        yesterday = now - timedelta(days=1)

        day = now

        path = path / f'{day.year}/{day.month}/{day.day}' 

        # compare to yesterday?
        if not compare:
            day = yesterday
            compare = Path(args.path) / args.name
            compare = compare / f'{day.year}/{day.month}/{day.day}'
        

    if path.exists():
        data = base.load_folder(path)
        data = pigfarm.make_timestamp_index(data)
        farm.data.put(data)

        farm.add(Magic, dict(data=data))
    else:
        print(path, 'AWOL')
        farm.add(Magic)

    print('COMPARE', compare)
    if compare and compare.exists():
        print('compare exists')
        b_data = base.load_folder(compare)
        b_data = pigfarm.make_timestamp_index(b_data)

        delta = data_diff(data, b_data)

        farm.add(Magic, dict(data=b_data))
        farm.add(Magic, dict(data=delta))
        
    from karmapi.mclock2 import GuidoClock
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
