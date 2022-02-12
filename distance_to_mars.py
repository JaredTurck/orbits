# distance between mars and earth changes daily due to planets orbiting the sun
# speed of light also changes depenting on medium
#speed of light = 299,792,458 m/s in vaccum

from numpy import exp, pi, absolute, linspace
import matplotlib.pyplot as plt
import datetime, numpy, math

class orbits():
    AU_units = {
        "Mercury" : 0.39,
        "Venus" : 0.72,
        "Earth" : 1.00,
        "Mars" : 1.524,
        "Jupiter" : 5.2,
        "Saturn" : 9.5,
        "Uranus" : 19.2,
        "Neptune" : 30.1,
    }

    au2km = 149_597_870.7
    refrence_point = datetime.datetime(2003, 8, 28) # t=0
    speed_of_light = 299_792_458 # m/s
    display_date = datetime.datetime.now()

    def planet(t, r):
        return r * exp(2 * pi * 1j * (r ** -1.5 * t))

    def graph():
        x = linspace(0, 4, 1000)
        plt.plot(x, distance(x, "Earth", "Mars"))
        plt.xlabel("Time in years")
        plt.ylabel("Distance in AU")
        plt.ylim(0, 3)
        plt.show()

    def distance(date, planet_1, planet_2):
        ''' calculates distance between two planets at any given date '''
        
        future_date = datetime.datetime.strptime(date, "%d-%m-%Y")
        delta = (future_date - orbits.refrence_point) # time delta
        delta_seconds = (delta.days * 60 * 60) + delta.seconds + (delta.microseconds / 1000000)
        delta_years = delta_seconds / 60 / 60 / 365

        au_planet_1 = orbits.planet(delta_years, orbits.AU_units[planet_1])
        au_planet_2 = orbits.planet(delta_years, orbits.AU_units[planet_2])
        au_distance = absolute(au_planet_1 - au_planet_2)
        distance_in_km = orbits.au2km * au_distance

        return distance_in_km, au_distance

    def light_seconds(distance):
        ''' calculates the time in seconds it takes light to travel distance k/m '''
        return distance / (orbits.speed_of_light / 1000)

    def next_day():
        orbits.display_date = orbits.display_date + datetime.timedelta(days=1)
        a,b = orbits.distance(orbits.display_date, "Earth", "Mars")
        return b

#orbits.distance("12-02-2022", "Earth", "Mars")
