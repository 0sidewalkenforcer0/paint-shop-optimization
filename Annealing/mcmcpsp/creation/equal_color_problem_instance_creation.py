import random
import collections 

from .problem_instance_creation import ProblemInstanceCreation
from .integer_problem_instance_creation import IntegerProblemInstanceCreation
from ..problem import Problem

#Creates a problem where same configurations has equal color
class EqualColorProblemInstanceCreation(ProblemInstanceCreation[int, int]):
    
    def __init__(self, config_color_set_length, carLine_length):
        self.config_color_length = config_color_set_length
        self.carLine_length = carLine_length
        if carLine_length < config_color_set_length:
            raise ValueError("carLine_length must be greater equal than config_color_length")
        """
        Args: 
            config_color_set_length(int): Length of the set of configurations and colors (same length)
            carLine_length(int): Length of the list carLine"""

    
    def createInstance(self) -> Problem[int, int]:
        configurations, colors = self.generateConfigurationsColors()
        carLine = IntegerProblemInstanceCreation.generateCarLine(self, configurations)
        number_of_configuration_color_combinations = self.generateNumberOfCombinations(configurations, colors, carLine)
    
        return Problem(
            configurations,
            colors,
            list(carLine),
            number_of_configuration_color_combinations
        )
    
    def generateConfigurationsColors(self): 
        configuration_list = []
        configurations = set(configuration_list)
        configuration = 0
        while len(configurations) != self.config_color_length:
            configurations.add(configuration)
            configuration+=1
        colors = configurations.copy()
        return configurations, colors

    #generate Dict with Tuples ((configuration, color): number)
    def generateNumberOfCombinations(self, configurations, colors, carLine):
        
        configuration_as_list = list(configurations)
        color_as_list = [*colors]
        sequence_colors_configurations = []
        colors_and_configurations = []

        #tuples(configuration, color) that one configuration has always same color
        for configuration in configuration_as_list:
                random_color = random.choice(color_as_list)
                tup = (configuration, random_color)
                colors_and_configurations.append(tup)
                color_as_list.remove(random_color)
        
        for car in carLine:
                for tup in colors_and_configurations:
                        if car == tup[0]:
                                sequence_colors_configurations.append(tup)
                                break                
       
        sequence_colors_configurations.sort()
        number_of_configuration_color_combinations = collections.defaultdict(int)
        
        #count the combinations of configurations with the equal color
        for elem in sequence_colors_configurations:
            number_of_configuration_color_combinations[elem[0], elem[1]] += 1
        return number_of_configuration_color_combinations
