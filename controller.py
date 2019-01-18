import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


class FuzzyCarController:
    def __init__(self):
        """Generate space for antecedents"""
        self.inputUniverse = np.linspace(0, 600, num=600, endpoint=True)

        """Init fuzzy antecedents"""
        self.rightDistance = ctrl.Antecedent(self.inputUniverse, 'right_distance')
        self.centerDistance = ctrl.Antecedent(self.inputUniverse, 'center_distance')
        self.leftDistance = ctrl.Antecedent(self.inputUniverse, 'left_distance')

        """Generate membership functions for inputs"""

        self.centerDistance['close'] = fuzz.trapmf(self.inputUniverse, [0, 0, 75, 150])
        self.centerDistance['safe'] = fuzz.trimf(self.inputUniverse, [75, 150, 225])
        self.centerDistance['far'] = fuzz.trapmf(self.inputUniverse, [150, 225, 600, 600])

        for antecedent in [self.leftDistance, self.rightDistance]:
            antecedent['close'] = fuzz.trapmf(self.inputUniverse, [0, 0, 50, 100])
            antecedent['safe'] = fuzz.trimf(self.inputUniverse, [50, 100, 200])
            antecedent['far'] = fuzz.trapmf(self.inputUniverse, [100, 200, 600, 600])

        """Generate space for consequent; assuming binary outputs (like pressing a key)"""
        #self.outputUniverse = [-1, 0, 1]
        self.outputUniverse = np.linspace(-100, 100, num=201, endpoint=True)
        """Generate consequent set"""
        self.speedControl = ctrl.Consequent(self.outputUniverse, 'sc', 'centroid')
        self.turn = ctrl.Consequent(self.outputUniverse, 'turn', 'mom')

        """Generate membership functions for outputs"""
        self.speedControl['brake'] = fuzz.trimf(self.outputUniverse, [-101, -100, -60])
        self.speedControl['do_nothing'] = fuzz.trimf(self.outputUniverse, [-60, 1, 25])
        self.speedControl['accelerate'] = fuzz.trimf(self.outputUniverse, [5, 100, 101])
        self.turn['turn_left'] = fuzz.trimf(self.outputUniverse, [-101, -100, -40])
        self.turn['do_nothing'] = fuzz.trimf(self.outputUniverse, [-50, 0, 50])
        self.turn['turn_right'] = fuzz.trimf(self.outputUniverse, [40, 100, 101])

        """Generate rules"""
        self.rule1 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'])),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='acc, 0')

        self.rule2 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='acc, L')

        self.rule3 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='0, L')

        self.rule4 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='0, 0')

        self.rule5 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['brake'], self.turn['do_nothing']), label='brake, 0')

        self.rule6 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['brake'], self.turn['turn_left']), label='brake, L')

        self.rule7 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='acc, R')

        self.rule8 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'])),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='0, R')

        self.rule9 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'])),
            consequent=(self.speedControl['brake'], self.turn['turn_right']), label='brake, R')

        """Generate controller engine"""
        self.engine_cs = ctrl.ControlSystem(rules=[self.rule1, self.rule2, self.rule3, self.rule3, self.rule4,
                                                   self.rule5, self.rule6, self.rule7, self.rule8, self.rule9])
        self.engine = ctrl.ControlSystemSimulation(self.engine_cs)

        self.dupa=5

    def visualise(self):
        self.leftDistance.view()
        self.centerDistance.view()
        self.rightDistance.view()
        self.speedControl.view()
        self.turn.view()

    def compute(self, l_dist, c_dist, r_dist):

        for i in l_dist, c_dist, r_dist:
            if i < 0:
                i = -i
        self.engine.input['left_distance'] = l_dist
        self.engine.input['center_distance'] = c_dist
        self.engine.input['right_distance'] = r_dist

        self.engine.compute()
        output = (round(self.engine.output['sc'], 2), round(self.engine.output['turn'], 2))
        return output



if __name__ == '__main__':
    a = FuzzyCarController()
    a.visualise()
    #print(a.compute(1, 1, 1))
