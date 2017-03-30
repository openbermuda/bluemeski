"""
See how the Oasis runs.

Watch the stream go by


"""

from karmapi import pigfarm, base

class Magic(pigfarm.MagicCarpet):
    pass
    
def main():

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--path', default=None)

    args = parser.parse_args()

    farm = pigfarm.PigFarm()

    if args.path:

        data = base.load_folder(args.path)

        farm.data.put(data)
    

    from karmapi.mclock2 import GuidoClock

    farm.add(Magic)
    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
