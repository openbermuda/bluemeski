"""
See how the Oasis runs.

Watch the stream go by


"""

from karmapi import pigfarm


def main():

    farm = pigfarm.PigFarm()

    from karmapi.mclock2 import GuidoClock

    farm.add(GuidoClock)

    pigfarm.run(farm)
    
if __name__ == '__main__':

    main()
