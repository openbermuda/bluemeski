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
    parser.add_argument('--now', action='store_true')
    parser.add_argument('--hours', type=float, default=1)

    parser.add_argument('name', nargs='?', default='sensehat')

    parser.add_argument('compare', nargs='?')
    
    args = parser.parse_args()

    farm = pigfarm.PigFarm()

    path = Path(args.path)

    path = path / args.name

    compare = args.compare
    if compare:
        compare = args.path / compare

    today = args.today
    now = datetime.utcnow()
    start = None
    end = None
    cstart = None
    cend = None

    hours = args.hours
    if args.now:
        today = True
        start = now - timedelta(seconds=3600 * hours)
        end = now
        cstart = start
        
    if today:
        yesterday = now - timedelta(days=1)

        day = now

        path = path / f'{day.year}/{day.month}/{day.day}' 

        # compare to yesterday?
        if not compare:
            day = yesterday

            if args.now:
                cstart = yesterday - timedelta(seconds=3600 * hours)
                cend =  yesterday
                
            compare = Path(args.path) / args.name
            compare = compare / f'{day.year}/{day.month}/{day.day}'
            print('compare:', cstart, cend)        

    if path.exists():
        data = base.load_folder(path)
        
        farm.add(Magic, dict(data=data, begin=start, end=end, title=path))
    else:
        print(path, 'AWOL')
        farm.add(Magic)
        compare = None

    print('COMPARE', compare)
    if compare and compare.exists():
        print('compare exists')
        b_data = base.load_folder(compare)

        delta = data_diff(data, b_data)

        farm.add(Magic, dict(data=b_data, begin=cstart, end=cend, title=compare))
        farm.add(Magic, dict(data=delta, title=f'{path} - {compare}'))
        
    from karmapi.mclock2 import GuidoClock
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
