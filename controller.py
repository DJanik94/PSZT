import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


class FuzzyCarController:
    def __init__(self):

        """Generate space for antecedents"""
        self.inputUniverse = np.linspace(0, 600, num=600, endpoint=True)
        self.differenceUniverse = np.linspace(-15, 15, num=300, endpoint=True)

        """Init fuzzy antecedents"""
        self.rightDistance = ctrl.Antecedent(self.inputUniverse, 'right_distance')
        self.centerDistance = ctrl.Antecedent(self.inputUniverse, 'center_distance')
        self.leftDistance = ctrl.Antecedent(self.inputUniverse, 'left_distance')
        self.speed = ctrl.Antecedent(self.differenceUniverse, 'speed')

        """Generate membership functions for inputs"""
        self.centerDistance['close'] = fuzz.trimf(self.inputUniverse, [-1, 0, 200])
        self.centerDistance['safe'] = fuzz.trimf(self.inputUniverse, [1, 210, 420])
        self.centerDistance['far'] = fuzz.trapmf(self.inputUniverse, [220, 420, 600, 600])

        self.speed['safe'] = fuzz.trapmf(self.differenceUniverse, [-15, -15, 9, 10])
        self.speed['fast'] = fuzz.trapmf(self.differenceUniverse, [9, 10, 15, 15])

        for antecedent in [self.leftDistance, self.rightDistance]:
            antecedent['close'] = fuzz.trimf(self.inputUniverse, [-1, 0, 160])
            antecedent['safe'] = fuzz.trimf(self.inputUniverse, [1, 160, 320])
            antecedent['far'] = fuzz.trapmf(self.inputUniverse, [160, 320, 600, 600])

        """Generate space for consequent; assuming binary outputs (like pressing a key)"""
        self.outputUniverse = np.linspace(-100, 100, num=201, endpoint=True)
        """Generate consequent set"""
        self.speedControl = ctrl.Consequent(self.outputUniverse, 'speed_control', 'centroid')
        self.turn = ctrl.Consequent(self.outputUniverse, 'turn', 'centroid')

        """Generate membership functions for outputs"""
        self.speedControl['hard_brake'] = fuzz.trimf(self.outputUniverse, [-101, -100, -99])
        self.speedControl['brake'] = fuzz.trimf(self.outputUniverse, [-80, -70, -60])
        self.speedControl['do_nothing'] = fuzz.trimf(self.outputUniverse, [-1, 0, 1])
        self.speedControl['accelerate'] = fuzz.trimf(self.outputUniverse, [25, 35, 45])
        self.speedControl['full_ahead'] = fuzz.trimf(self.outputUniverse, [99, 100, 101])
        self.turn['sharp_left'] = fuzz.trimf(self.outputUniverse, [-101, -100, -90])
        self.turn['turn_left'] = fuzz.trimf(self.outputUniverse, [-60, -40, -20])
        self.turn['do_nothing'] = fuzz.trimf(self.outputUniverse, [-5, 0, 5])
        self.turn['turn_right'] = fuzz.trimf(self.outputUniverse, [20, 40, 60])
        self.turn['sharp_right'] = fuzz.trimf(self.outputUniverse, [90, 100, 101])

        """Define rules"""
        self.rule1 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_left']), label='hb, SL')

        self.rule2 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['hard_brake'], self.turn['do_nothing']), label='hb, do nothing')

        self.rule3 = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_right']), label='hb, SR')

        self.rule4 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['turn_left']), label='brake, turn_left')

        self.rule5 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] &
                        self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['do_nothing']), label='brake, do_nothing')

        self.rule6 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['turn_right']), label='brake, turn_right')

        self.rule7 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_left']), label='do_nothing, sharp_left')

        self.rule8 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                        self.speed['fast']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                        self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='do_nothing, turn_left')

        self.rule9 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='0, 0a')

        self.rule10 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far'] &
                        self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='do_nothing, turn_right')

        self.rule11 = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_right']), label='do_nothing, sharp_right')

        self.rule12 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['close'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='accelerate, sharp_left')

        self.rule13 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                        self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                        self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='accelerate, turn_left')

        self.rule14 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] &
                        self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='accelerate, do_nothing')

        self.rule15 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far'] &
                        self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='accelerate, turn_right')

        self.rule16 = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='accelerate, sharp_right')

        self.rule17 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['full_ahead'], self.turn['do_nothing']), label='fh, 0')

        """Initialize computing engine"""
        self.engine_cs = ctrl.ControlSystem(rules=[self.rule1, self.rule2, self.rule3, self.rule4, self.rule5,
                                                   self.rule6, self.rule7, self.rule8, self.rule9, self.rule10,
                                                   self.rule11, self.rule12, self.rule13, self.rule14, self.rule15,
                                                   self.rule16, self.rule17])
        self.engine = ctrl.ControlSystemSimulation(self.engine_cs)

    def visualise(self):
        self.leftDistance.view()
        self.centerDistance.view()
        self.rightDistance.view()
        self.speed.view()
        self.speedControl.view()
        self.turn.view()

    def compute(self, l_dist, c_dist, r_dist, speed):
        self.engine.input['left_distance'] = l_dist
        self.engine.input['center_distance'] = c_dist
        self.engine.input['right_distance'] = r_dist
        self.engine.input['speed'] = speed
        self.engine.compute()
        output = (round(self.engine.output['speed_control'], 2), round(self.engine.output['turn'], 2))
        return output


if __name__ == '__main__':
    f = FuzzyCarController()
    f.visualise()
