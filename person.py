"""
1. Define a class Person
2. instantiate Person's for every member of The Blues
3. instantiate Person's for every member of the tech crew
4. instantiate Person's for every member of the transportation team
"""
class Person:
    def __init__(self, first_name, last_name, rank, job, gender):
        self.first_name = first_name
        self.last_name = last_name
        self.rank = rank
        self.job = job
        self.gender = gender