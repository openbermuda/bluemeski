"""
See how the Oasis runs.

Watch the stream go by


"""
from datetime import datetime
from pathlib import Path

from karmapi import pigfarm, base

class Magic(pigfarm.MagicCarpet):
    pass
    
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default='.')
    parser.add_argument('--today', action='store_true')
    parser.add_argument('name', nargs='?', default='sensehat')

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
    

    from karmapi.mclock2 import GuidoClock

    farm.add(Magic)
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
