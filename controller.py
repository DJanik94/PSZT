import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


class FuzzyCarController:
    def __init__(self):
        """Init variables for previous input values"""
        self.prev_c = 0
        self.prev_prev_c = 0

        """Generate space for antecedents"""
        self.inputUniverse = np.linspace(0, 600, num=600, endpoint=True)
        self.differenceUniverse = np.linspace(-600, 600, num=600, endpoint=True)
        """Init fuzzy antecedents"""
        self.rightDistance = ctrl.Antecedent(self.inputUniverse, 'right_distance')
        self.centerDistance = ctrl.Antecedent(self.inputUniverse, 'center_distance')
        self.leftDistance = ctrl.Antecedent(self.inputUniverse, 'left_distance')
        self.speed = ctrl.Antecedent(self.differenceUniverse, 'distance_difference')

        """Generate membership functions for inputs"""

        self.centerDistance['tight'] = fuzz.trimf(self.inputUniverse, [-1, 1, 20])
        self.centerDistance['close'] = fuzz.trimf(self.inputUniverse, [-1, 1, 200])
        self.centerDistance['safe'] = fuzz.trimf(self.inputUniverse, [1, 210, 420])
        self.centerDistance['far'] = fuzz.trapmf(self.inputUniverse, [220, 420, 600, 600])

        self.speed['safe'] = fuzz.trapmf(self.differenceUniverse, [-600, -600, 9, 10])
        self.speed['fast'] = fuzz.trapmf(self.differenceUniverse, [9, 10, 600, 600])

        for antecedent in [self.leftDistance, self.rightDistance]:
            antecedent['tight'] = fuzz.trimf(self.inputUniverse, [-1, 0, 20])
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

        """Generate rules"""
        self.rule1 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['full_ahead'], self.turn['do_nothing']), label='fh, 0')

        self.rule2a = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='fh, Lff')

        self.rule2b = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='fh, L')

        self.rule3a = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_left']), label='0, SL111')

        self.rule3b = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='acc, SL')

        self.rule4a = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='0, 0a')

        self.rule4b = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='0accsd, 0')

        self.rule5a = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='0, Ldas')

        self.rule5b = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='0, L')

        self.rule6a = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='brake, 0')

        self.rule6b = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='0, 0 when stopped')

        self.rule7a = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['turn_left']), label='brake, L')

        self.rule7b = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='0, L when stopped')

        self.rule8a = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_left']), label='hb, SL')

        self.rule8b = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='0, SL when stopped')

        self.rule9a = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='fjjj, right')

        self.rule9b = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='fh, right')

        self.rule10a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                        self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                        self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'] &
                        self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                        self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['do_nothing']), label='acc, 0dfgdf')

        self.rule10b = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='acc, 0dsf')



        self.rule11 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['close']),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='acc, SsssL')

        self.rule12a = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['fast']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='0, righllt')

        self.rule12b = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                        self.speed['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='0, right')

        self.rule13a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['brake'], self.turn['turn_right']), label='brake, right')

        self.rule13b = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='0, right when stopped')

        self.rule14a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['hard_brake'], self.turn['do_nothing']), label='hb, 0')

        """self.rule14b = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='0, 0 when close')"""

        self.rule15a = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_right']), label='0, SR')

        self.rule15b = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='0, SRlll')

        self.rule16 = ctrl.Rule(
            antecedent=(self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='acc, SR')

        self.rule17a = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['fast']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_right']), label='hb, SR')

        self.rule17b = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] &
                         self.speed['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] &
                         self.speed['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='0, SR, when stopped')

        """self.rule1 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] &
                         self.speed['fast'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_left']), label='hb, SL')

        self.rule14a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['hard_brake'], self.turn['do_nothing']), label='hb, 0')"""


        """Generate controller engine"""
        self.engine_cs = ctrl.ControlSystem(rules=[self.rule1, self.rule2a, self.rule2b, self.rule3a, self.rule3b,
                                                   self.rule4a, self.rule4b, self.rule5a, self.rule5b,
                                                   self.rule6a, self.rule6b, self.rule7a, self.rule7b, self.rule8a,
                                                   self.rule8b, self.rule9a, self.rule9b, self.rule10a, self.rule10b, self.rule11, self.rule12a,
                                                   self.rule12b,
                                                   self.rule13a, self.rule13b, self.rule14a,
                                                   self.rule15a, self.rule15b, self.rule16, self.rule17a, self.rule17b])
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
        self.engine.input['distance_difference'] = speed

        self.engine.compute()
        print(speed)
        self.prev_prev_c = self.prev_c
        self.prev_c = c_dist

       #if l_dist < 1 and r_dist < 1 and c_dist < 1 and self.prev_c < 1 and self.prev_prev_c < 1:
            #output = (0, 0)
        #else:
        output = (round(self.engine.output['speed_control'], 2), round(self.engine.output['turn'], 2))

        return output


if __name__ == '__main__':
    f = FuzzyCarController()
    f.visualise()
