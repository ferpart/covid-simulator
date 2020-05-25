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

    def __str__(self):
        """
        Print the current state from every person in the node.
        """
        res = ""
        for _, person in enumerate(self.persons):
            res += person.state + '\n'
        return res

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
    def __init__(self):
        self.nodes = {}
        # 0 : House, 1 : Supermarket, 2 : Hospital, 3 : Transportation
        self.places = { 0 : "House", 1 : "Supermarket", 2 : "Hospital", 3 : "Transportation" }
        self.matrix = { "House"          : [0.75, 0.1, 0.05, 0.1],
                        "Supermarket"    : [0.5, 0.4, 0.0, 0.1],
                        "Hospital"       : [0.5, 0.0, 0.4, 0.0],
                        "Transportation" : [0.6, 0.15, 0.05, 0.2] }

    def __str__(self):
        res = ""
        for key in self.nodes:
            res += self.nodes[key].place + " : "
            for _, person in enumerate(self.nodes[key].persons):
                res += person.state + "\t"
            res += "\n"
        return res

    def update_node_states(self):
        for key in self.nodes:
            self.nodes[key].update_matrix()
            self.nodes[key].update_states()

    def move(self):
        for key in self.nodes:
            for _, person in enumerate(self.nodes[key].persons):
                rand = random()
                transitions = self.matrix[person.place]
                total = 0
                for idx, trans in enumerate(transitions):
                    total += trans
                    if total <= rand:
                        if person in self.nodes[person.node].persons:
                            self.nodes[person.node].persons.remove(person)
                            if self.places[idx] == "House":
                                self.nodes[person.node].persons.append(person)
                            elif self.places[idx] == "Supermarket":
                                self.nodes[4].persons.append(person)
                            elif self.places[idx] == "Hospital":
                                self.nodes[5].persons.append(person)
                            elif self.places[idx] == "Transportation":
                                self.nodes[6].persons.append(person)
                        break

def main():
    city = City()
    house1 = Node("House", 1)
    house1.generate_persons(10, 0)
    house2 = Node("House", 2)
    house2.generate_persons(10, 1)
    house3 = Node("House", 3)
    house3.generate_persons(8, 2)
    supermarket = Node("Supermarket", 4)
    hospital = Node("Hospital", 5)
    transportation = Node("Transportation", 6)
    city.nodes = {1 : house1, 2 : house2, 3 : house3, 4 : supermarket, 5 : hospital, 6 : transportation}

    print(city)
    time.sleep(2)
    while 1:
        os.system('cls' if os.name == 'nt' else 'clear')
        city.update_node_states()
        city.move()
        """ for key in city.nodes:
            print(len(city.nodes[key].persons)) """
        print(city)
        time.sleep(2)
    

if __name__ == "__main__":
    main()