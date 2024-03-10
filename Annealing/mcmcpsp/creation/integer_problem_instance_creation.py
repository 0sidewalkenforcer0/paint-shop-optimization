import random
import logging
import collections 

from .problem_instance_creation import ProblemInstanceCreation
from ..problem import Problem

class IntegerProblemInstanceCreation(ProblemInstanceCreation[int, int]):
    """
    Args:
        configuration_set_length(int): Length of the set of configurations
        colors_set_length(int): Length of the set of colors
        carLine_length(int): Length of the list carLine

    """
    
    def __init__(self, configuration_set_length, colors_set_length, carLine_length):
        self.configuration_set_length = configuration_set_length
        self.colors_set_length = colors_set_length
        self.carLine_length = carLine_length
        if carLine_length < colors_set_length or carLine_length < configuration_set_length:
            raise ValueError("carLine_length must be greater equal than color_set_length and configuration_set_length")

    
    def createInstance(self) -> Problem[int, int]:
        configurations = self.generateConfigurations()
        colors = self.generateColors()
        carLine = self.generateCarLine(configurations)
        number_of_configuration_color_combinations = self.generateNumberOfCombinations(colors, carLine)
        logging.debug('creation of problem instance')
    
        return Problem(
            colors,
            configurations,
            list(carLine),
            number_of_configuration_color_combinations
        )
    
    def generateConfigurations(self): 
        configuration_list = []
        configurations = set(configuration_list)
        configuration = 0
        logging.debug('generation of configurations set')
        while len(configurations) != self.configuration_set_length:
            configurations.add(configuration)
            configuration+=1
        return configurations

    def generateColors(self):
        color_list = []
        colors = set(color_list)
        color = 0
        logging.debug('generation of colors set')
        while len(colors) != self.colors_set_length:
            colors.add(color)
            color+=1
        return colors

    def generateCarLine(self, configurations):
        #carLine as a list
        configuration_as_list = list(configurations)
        carLine =[]
        logging.debug('building of carLine')
        # All configurations needs to contain in carLine at lest ones
        for configuration in configuration_as_list:
            carLine.append(configuration)

        while len(carLine) != self.carLine_length:
            item = random.choice(configuration_as_list)
            carLine.append(item)
    
        random.shuffle(carLine)
        return carLine

    #generate Dict with Tuples ((configuration, color): number)
    def generateNumberOfCombinations(self, colors, carLine):
        sequence_colors_configurations = []       
        carLine_contains = carLine.copy()
        color_as_list = list(colors)
        logging.debug('building of number_of_configuration_color_combinations dictionary')
        #examines that all colors contains at least ones
        for color in color_as_list:
            random_carLine = random.choice(carLine_contains)
            carLine_contains.remove(random_carLine)
            tup = (random_carLine, color)
            sequence_colors_configurations.append(tup)

        #rest configuration with random colors
        for configuration in carLine_contains:
            random_color = random.choices(color_as_list)
            color_int = random_color[0]
            tup = (configuration, color_int)
            sequence_colors_configurations.append(tup)
       
        sequence_colors_configurations.sort()
        number_of_configuration_color_combinations = collections.defaultdict(int)
        #count the combinations of configurations with the equal color
        for elem in sequence_colors_configurations:
            number_of_configuration_color_combinations[elem[0], elem[1]] += 1
        return number_of_configuration_color_combinations
