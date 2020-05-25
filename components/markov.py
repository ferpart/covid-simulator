import os
import time
from random import random

class Person:
    """
    A class used to represent a person.

    Attributes
    ----------
    state : str
        The current state of this persons at any moment of time. The person
        can be 'Susceptible', 'Infected', 'Recovered' or 'Death'.
    node : str
        Indicates to which nodes does this person belongs.
    """
    def __init__(self, state, node, place):
        self.state = state
        self.node = node
        self.place = place


class Node:
    """
    Class used to represent places such as houses, hospitals, and supermarkets.

    Attributes
    ----------
    id : str
        Id of the node.
    place : str
        The type of place it is.
    persons : [Person]
        An array conformed from the people that are currently in this place.
    states : {int : str}
        Helper variable to assign a new state to a given person.
    matrix : [[float]]
        It is the transition matrix, gives the probability of P(new state | current state).

    Methods
    -------
    __str__()
        Prints the states of the persons in this place.
    generate_persons(total, infected)
        Generate persons in the current place, where total is the total number
        of persons in the place and infected is the number of infected persons.
    update_states()
        Updates the state of every person in this place.
    """
    def __init__(self, place, id):
        self.id = id
        self.place = place
        self.persons = []
        # 0: Susceptible, 1: Sick, 2: Recovered, 3: Death
        self.states = { 0 : "Susceptible", 1 : "Infected", 2 : "Recovered", 3 : "Death"}
        self.matrix = { "Susceptible" : [0.8, 0.2, 0.0, 0.0],
                        "Infected"    : [0.0, 0.8, 0.15, 0.05],
                        "Recovered"   : [0.0, 0.0, 1.0, 0.0],
                        "Death"       : [0.0, 0.0, 0.0, 1.0] }
        self.total = len(self.persons)
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.death = 0

    def __str__(self):
        """
        Print the current state from every person in the node.
        """
        res = ""
        for _, person in enumerate(self.persons):
            res += person.state + '\n'
        return res

    def update_stats(self):
        self.total = len(self.persons)
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.death = 0
        for _, person in enumerate(self.persons):
            self.total += 1
            if person.state == "Susceptible":
                self.susceptible += 1
            elif person.state == "Infected":
                self.death += 1
            elif person.state == "Recovered":
                self.recovered += 1
            elif person.state == "Death":
                self.death += 1

    def generate_persons(self, total, infected):
        """
        Creates the persons that will belong to this place.

        Parameters
        ----------
        total : int
            The total number of persons to create.
        infected: int
            The number of infected persons in the total amount.
        """
        for i in range(total):
            if i < infected:
                p = Person("Infected", self.id, self.place)
            else:
                p = Person("Susceptible", self.id, self.place)
            self.persons.append(p)

    def update_matrix(self):
        infected = 0
        for _, person in enumerate(self.persons):
            if person.state == 'Infected':
                infected += 1
        if infected > 0:
            self.matrix["Susceptible"][0] = 0.9
            self.matrix["Susceptible"][1] = 0.1
        else:
            self.matrix["Susceptible"][0] = 1.0
            self.matrix["Susceptible"][1] = 0.0

    def update_states(self):
        """
        Updates every person's state in the persons array.
        It generates a random value between 0 and 1, and
        with the help of the matrix, the person's state
        will be updated or it will remain the same.
        """
        for _, person in enumerate(self.persons):
            person_state = person.state
            rand = random()
            transitions = self.matrix[person_state]
            total = 0
            for idx, trans in enumerate(transitions):
                total += trans
                if (rand <= total):
                    person.state = self.states[idx]
                    break

class City:
    """
    Class used to represent a city with nodes and persons.

    Attributes
    ----------
    node : {int : Node}
        A dictionary of nodes, this conform the city.
    """
    def __init__(self, house1, house2, house3, house4, house5, supermarket, hospital, transportation):
        self.house1 = house1
        self.house2 = house2
        self.house3 = house3
        self.house4 = house4
        self.house5 = house5
        self.supermarket = supermarket
        self.hospital = hospital
        self.transportation = transportation
        self.nodes = [self.house1, self.house2, self.house3, self.house4, self.house5, self.supermarket, self.hospital, self.transportation]
        self.matrix = { "House"          : [0.75, 0.1, 0.05, 0.1],
                        "Supermarket"    : [0.5, 0.4, 0.0, 0.1],
                        "Hospital"       : [0.5, 0.0, 0.4, 0.1],
                        "Transportation" : [0.6, 0.15, 0.05, 0.2] }
        self.total = len(house1.persons) + len(house2.persons) + len(house3.persons) + len(house4.persons) + len(house5.persons)
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.death = 0

    def __str__(self):
        res = ""
        for _, node in enumerate(self.nodes):
            res += node.place + " : "
            for _, person in enumerate(node.persons):
                res += person.state + "\t"
            res += "\n"
        return res

    def update_node_states(self):
        for _, node in enumerate(self.nodes):
            node.update_matrix()
            node.update_states()

    def update_stats(self):
        self.susceptible = 0
        self.infected = 0
        self.recovered = 0
        self.death = 0
        for _, node in enumerate(self.nodes):
            for _, person in enumerate(node.persons):
                if person.state == "Susceptible":
                    self.susceptible += 1
                elif person.state == "Infected":
                    self.infected += 1
                elif person.state == "Recovered":
                    self.recovered += 1
                elif person.state == "Death":
                    self.death += 1
            node.update_stats()

    def move(self):
        for _, node in enumerate(self.nodes):
            curr_pos = node.place
            transition = self.matrix[curr_pos]
            for _, person in enumerate(node.persons):
                rand = random()
                total = 0
                for idx, trans in enumerate(transition):
                    total += trans
                    if (rand <= total):
                        node.persons.remove(person)
                        if idx == 0:
                            if person.node == 1:
                                self.house1.persons.append(person)
                            elif person.node == 2:
                                self.house2.persons.append(person)
                            elif person.node == 3:
                                self.house3.persons.append(person)
                            elif person.node == 4:
                                self.house4.persons.append(person)
                            else:
                                self.house5.persons.append(person)
                        elif idx == 1:
                            self.supermarket.persons.append(person)
                        elif idx == 2:
                            self.hospital.persons.append(person)
                        else:
                            self.transportation.persons.append(person)
                        break



def main():
    house1 = Node("House", 1)
    house1.generate_persons(10, 0)
    house2 = Node("House", 2)
    house2.generate_persons(10, 1)
    house3 = Node("House", 3)
    house3.generate_persons(10, 2)
    house4 = Node("House", 4)
    house4.generate_persons(10, 1)
    house5 = Node("House", 5)
    house5.generate_persons(10, 0)
    supermarket = Node("Supermarket", 6)
    hospital = Node("Hospital", 7)
    transportation = Node("Transportation", 8)
    city = City(house1, house2, house3, house4, house5, supermarket, hospital, transportation)

    print(city)
    time.sleep(2)
    while 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        city.update_node_states()
        city.move()
        city.update_stats()
        print(city)
        print(city.total)
        print(city.susceptible)
        print(city.infected)
        print(city.recovered)
        print(city.death)
        time.sleep(2)
    

if __name__ == "__main__":
    main()