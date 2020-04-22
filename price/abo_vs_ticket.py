# Price Update April 2020
LOCKDOWN_WORKDAYS = (60 * 5) / 7
GA_HINTERLEGUNG_DAYS = 30  # there is a possibility to deposit the GA for 30 in a year (the money will be paid back for this period)
GA_LOCKDOWN_HINTERLEGUNG_DAYS = 15  # already in 2020
HOLIDAYS_PER_YEAR = 30
WORKDAYS_PER_MONTH = 22
HOLIDAYS_PER_MONTH = (HOLIDAYS_PER_YEAR + LOCKDOWN_WORKDAYS) / 12
MINDESTPRICE_IN_CHF = 4.4


def get_value_from_dict(dictionary: dict, key_value: any) -> any:
    """ searches dictionary and returns a value

    this implementation supports dictionary keys as ranges otherwise the dictionary could be accessed directly

    :param dictionary: 
    :param key_value: value to search in key of the dictionary
    """
    for key in dictionary:
        if key_value in key:
            return dictionary[key]
    return None


def calculate_price(distance_in_km: int, price_dict: dict) -> float:
    """ calculates the price based on given price table for the given number of kilometers

    :param price_dict: dict: 
    :param distance_in_km: int: 
    """
    # source --> Tarife 601 Chapter 10.1.4 on https://www.allianceswisspass.ch/de/Themen/TarifeVorschriften
    # dict --> key: 'km' ranges; value: 'km'
    steps = {range(1, 9): 4,
             range(9, 31): 2,
             range(31, 61): 3,
             range(61, 101): 4,
             range(101, 151): 5,
             range(151, 301): 10,
             range(301, 1501): 20,
             }
    price = 0
    km = 1
    while True:
        step = get_value_from_dict(steps, km)
        price_per_km = get_value_from_dict(price_dict, km)
        price += step * price_per_km
        # print(km, step, price_per_km, price)

        if km + step > distance_in_km:
            break
        else:
            km += step

    return price/100


def regular_ticket_price(distance_in_km: int) -> float:
    """ calculate the regular ticket price based on the given distance

    :int distance_in_km:
    """
    # source --> Tarife 601 Chapter 10.1.3 on https://www.allianceswisspass.ch/de/Themen/TarifeVorschriften    
    price_ticket_per_km = {range(1, 5): 44.51,
                           range(5, 15): 42.30,
                           range(15, 49): 37.24,
                           range(49, 151): 26.46,
                           range(151, 201): 25.71,
                           range(201, 251): 22.85,
                           range(251, 301): 20.63,
                           range(301, 481): 20.09,
                           range(481, 1501): 19.85,
                           }
    price = calculate_price(distance_in_km, price_ticket_per_km)
    if price < MINDESTPRICE_IN_CHF:
        price = MINDESTPRICE_IN_CHF
    return price


def abo_price_per_month(distance_in_km: int) -> float:
    """ calculate the abonament price based on the given distance

    WARNING: the abonament must be purchased for the whole year

    the price for a month is cheaper when paid for the whole year
    One will pay for 9 months one will use the whole year

    :int distance_in_km:
    """
    # source --> Tarife 650 Chapter 5.1.4 on https://www.allianceswisspass.ch/de/Themen/TarifeVorschriften
    price_abo_per_km = {range(1, 5): 1672,
                        range(5, 15): 679,
                        range(15, 17): 627,
                        range(17, 21): 627,
                        range(21, 40): 380,
                        range(40, 55): 219,
                        range(55, 251): 187,
                        }
    price_per_month_without_reduction = calculate_price(distance_in_km, price_abo_per_km)
    return (price_per_month_without_reduction * 9) / 12


def abo_price_per_year(distance_in_km: int) -> float:
    return abo_price_per_month(distance_in_km) * 12


def abo_price_per_day(distance_in_km: int) -> float:
    return abo_price_per_month(distance_in_km) / (WORKDAYS_PER_MONTH - HOLIDAYS_PER_MONTH)


def costs_calculation_ga():
    ga_hinterlegung = (365 - GA_HINTERLEGUNG_DAYS) / 365
    ga_lockdown = (365 - GA_LOCKDOWN_HINTERLEGUNG_DAYS) / 365
    ga_price_year = 3860 * ga_lockdown
    ga_price_year_with_hinterlegung = ga_price_year * ga_hinterlegung * ga_lockdown
    ga_price_month = ga_price_year / 12
    ga_price_day = ga_price_month / WORKDAYS_PER_MONTH
    ga_price_month_with_hinterlegung = ga_price_year_with_hinterlegung / 12
    ga_price_day_with_hinterlegung = ga_price_month_with_hinterlegung / WORKDAYS_PER_MONTH
    print("GA with Hinterlegung: price per year = {:.0f},  GA price per month = {:.0f},  GA price per work day = {:.2f}".format(ga_price_year_with_hinterlegung, ga_price_month_with_hinterlegung, ga_price_day_with_hinterlegung))
    print("GA without Hinterlegung: price per year = {:.0f},  GA price per month = {:.0f},  GA price per work day = {:.2f}".format(ga_price_year, ga_price_month, ga_price_day))


def costs_calculation_regular_ticket_vs_abonament():
    for distance_in_km in range(1, 130):
        print("{} km: ABO per year = {:.2f} CHF, "
              "ABO per month = {:.2f} CHF, "
              "ABO per work day = {:.2f} CHF, "
              "ticket per day = {:.2f}, "
              "regular tickets per week cheaper than ABO = {}".format(distance_in_km,
                                                                      abo_price_per_year(distance_in_km),
                                                                      abo_price_per_month(distance_in_km),
                                                                      abo_price_per_day(distance_in_km),
                                                                      regular_ticket_price(distance_in_km),
                                                                      int((abo_price_per_day(distance_in_km) * 5) / regular_ticket_price(distance_in_km))))  # round down


if __name__ == "__main__":

    costs_calculation_ga()
    costs_calculation_regular_ticket_vs_abonament()
