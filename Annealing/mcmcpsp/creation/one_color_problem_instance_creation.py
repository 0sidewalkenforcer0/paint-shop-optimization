import random
import collections
from .integer_problem_instance_creation import IntegerProblemInstanceCreation
from .problem_instance_creation import ProblemInstanceCreation
from ..problem import Problem

#creates a Problem with random configurations, random carLine and just one color from colors
class OneColorProblemInstanceCreation(ProblemInstanceCreation):
    def __init__(self, configuration_set_length, colors_set_length, carLine_length):
        self.configuration_set_length = configuration_set_length
        self.colors_set_length = colors_set_length
        self.carLine_length = carLine_length
        if carLine_length < configuration_set_length:
            raise ValueError("carLine_length must be greater equal than configuration_set_length")
        """
        Args: 
            configuration_set_length(int): Length of the set of configurations
            colors_set_length(int): Length of the set of colors
            carLine_length(int): Length of the list carLine"""

    def createInstance(self) -> Problem:
        configurations = IntegerProblemInstanceCreation.generateConfigurations(self)
        colors = IntegerProblemInstanceCreation.generateColors(self)
        carLine = IntegerProblemInstanceCreation.generateCarLine(self, configurations)
        number_of_configuration_color_combinations = self.generateNumberOfCombinations(colors, carLine)
    
        return Problem(
            colors,
            configurations,
            list(carLine),
            number_of_configuration_color_combinations
        )

    #generate Dict with Tuples ((configuration, color): number)
    def generateNumberOfCombinations(self, colors, carLine):
        
        one_color_random = random.choice(list(colors))   
        sequence_colors_configurations = []       

        #tuples of configurations with same color
        for configuration in carLine:
            tup = (configuration, one_color_random)
            sequence_colors_configurations.append(tup)
       
        color_configuration_combinations = collections.defaultdict(int)
        #count the combinations of configurations with the equal color
        for elem in sequence_colors_configurations:
            color_configuration_combinations[elem[0], elem[1]] += 1
        return color_configuration_combinations
