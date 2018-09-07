import numpy as np
import random
from copy import copy, deepcopy

"""To do this we will require the setup of the
TransientSurvey object to take in ranges for the different
variables. This will allow the construction of the
characterized genome"""

class TransientGenetic:
    """Class that optimizes survey score with genetic algorithm"""

    def __init__(self, survey, scoringFunc, surveyTime):
        """
        Args:
            survey:
                The TransientSurvey object to run and reset
                in order to optimize
            scoringFunc:
                Function that takes as its only argument
                    the survey object, and returns a float:
                    the score of the survey. Higher => better
            surveyTime:
                Iterations to run survey before scoring it
        
        """

        self.vChar = deepcopy(survey.profile.vChar)
        self.oChar = deepcopy(survey.profile.oChar)
        self.hChar = deepcopy(survey.profile.hChar)
        self.sChar = deepcopy(survey.profile.sChar)
        self.score = scoringFunc
        self.runTime = surveyTime
        self.surv = survey
        return
