import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


class FuzzyCarController:
    def __init__(self):
        """Generate space for antecedents"""
        self.inputUniverse = np.linspace(0, 200, num=201, endpoint=True)

        """Init fuzzy antecedents"""
        self.rightDistance = ctrl.Antecedent(self.inputUniverse, 'right_distance')
        self.centerDistance = ctrl.Antecedent(self.inputUniverse, 'center_distance')
        self.leftDistance = ctrl.Antecedent(self.inputUniverse, 'left_distance')

        """Generate membership functions for inputs"""
        for antecedent in [self.leftDistance, self.centerDistance, self.rightDistance]:
            antecedent['close'] = fuzz.trapmf(self.inputUniverse, [0, 0, 20, 60])
            antecedent['safe'] = fuzz.trimf(self.inputUniverse, [20, 60, 100])
            antecedent['far'] = fuzz.trapmf(self.inputUniverse, [60, 100, 200, 200])

        """Generate space for consequent; assuming binary outputs (like pressing a key)"""
        self.outputUniverse = [-1, 0, 1]

        """Generate consequent set"""
        self.speedControl = ctrl.Consequent(self.outputUniverse, 'sc', 'mom')
        self.turn = ctrl.Consequent(self.outputUniverse, 'turn', 'mom')

        """Generate membership functions for outputs"""
        self.speedControl['brake'] = fuzz.trimf(self.outputUniverse, [-1, -1, -1])
        self.speedControl['do_nothing'] = fuzz.trimf(self.outputUniverse, [0, 0, 0])
        self.speedControl['accelerate'] = fuzz.trimf(self.outputUniverse, [1, 1, 1])
        self.turn['turn_left'] = fuzz.trimf(self.outputUniverse, [-1, -1, -1])
        self.turn['do_nothing'] = fuzz.trimf(self.outputUniverse, [0, 0, 0])
        self.turn['turn_right'] = fuzz.trimf(self.outputUniverse, [1, 1, 1])

        """Generate rules"""
        self.rule1 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'])),
            consequent=(self.speedControl['accelerate'] and self.turn['do_nothing']), label='acc, 0')

        self.rule2 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe']),
            consequent=(self.speedControl['accelerate'] and self.turn['turn_left']), label='acc, L')

        self.rule3 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'] and self.turn['turn_left']), label='0, L')

        self.rule4 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'] and self.turn['do_nothing']), label='0, 0')

        self.rule5 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['brake'] and self.turn['do_nothing']), label='brake, 0')

        self.rule6 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['brake'] and self.turn['turn_left']), label='brake, L')

        self.rule7 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['accelerate'] and self.turn['turn_right']), label='acc, R')

        self.rule8 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'])),
            consequent=(self.speedControl['do_nothing'] and self.turn['turn_right']), label='0, R')

        self.rule9 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'])),
            consequent=(self.speedControl['brake'] and self.turn['turn_right']), label='brake, R')

        """Generate controller engine"""
        self.engine_cs = ctrl.ControlSystem(rules=[self.rule1, self.rule2, self.rule3, self.rule3, self.rule4,
                                                   self.rule5, self.rule6, self.rule7, self.rule8, self.rule9])
        self.engine = ctrl.ControlSystemSimulation(self.engine_cs)

    def visualise(self):
        self.leftDistance.view()
        self.centerDistance.view()
        self.rightDistance.view()
        self.speedControl.view()
        self.turn.view()

    def compute(self, l_dist, c_dist, r_dist):
        self.engine.input['left_distance'] = l_dist
        self.engine.input['center_distance'] = c_dist
        self.engine.input['right_distance'] = r_dist

        self.engine.compute()
        output = (self.engine.output['sc'], self.engine.output['turn'])
        return output


a = FuzzyCarController()

a.visualise()

print(a.compute(190, 1, 1))
