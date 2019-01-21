import skfuzzy as fuzz
import skfuzzy.control as ctrl
import numpy as np


class FuzzyCarController:
    def __init__(self):
        """Init variables for previous input values"""
        self.prev_l = 0
        self.prev_c = 0
        self.prev_r = 0

        """Generate space for antecedents"""
        self.inputUniverse = np.linspace(0, 600, num=600, endpoint=True)
        self.differenceUniverse = np.linspace(-600, 600, num=600, endpoint=True)
        """Init fuzzy antecedents"""
        self.rightDistance = ctrl.Antecedent(self.inputUniverse, 'right_distance')
        self.centerDistance = ctrl.Antecedent(self.inputUniverse, 'center_distance')
        self.leftDistance = ctrl.Antecedent(self.inputUniverse, 'left_distance')
        self.centerDistDiff = ctrl.Antecedent(self.differenceUniverse, 'distance_difference')

        """Generate membership functions for inputs"""

        self.centerDistance['close'] = fuzz.trimf(self.inputUniverse, [-1, 1, 200])
        self.centerDistance['safe'] = fuzz.trimf(self.inputUniverse, [1, 220, 440])
        self.centerDistance['far'] = fuzz.trapmf(self.inputUniverse, [220, 440, 600, 600])

        self.centerDistDiff['safe'] = fuzz.trapmf(self.differenceUniverse, [-600, -600, -15, 0])
        self.centerDistDiff['sharp'] = fuzz.trapmf(self.differenceUniverse, [-15, 0, 600, 600])

        for antecedent in [self.leftDistance, self.rightDistance]:
            antecedent['close'] = fuzz.trimf(self.inputUniverse, [-1, 0, 160])
            antecedent['safe'] = fuzz.trimf(self.inputUniverse, [1, 160, 320])
            antecedent['far'] = fuzz.trapmf(self.inputUniverse, [160, 320, 600, 600])

        """Generate space for consequent; assuming binary outputs (like pressing a key)"""
        #self.outputUniverse = [-1, 0, 1]
        self.outputUniverse = np.linspace(-100, 100, num=201, endpoint=True)
        """Generate consequent set"""
        self.speedControl = ctrl.Consequent(self.outputUniverse, 'sc', 'centroid')
        self.turn = ctrl.Consequent(self.outputUniverse, 'turn', 'centroid')

        """Generate membership functions for outputs"""
        self.speedControl['hard_brake'] = fuzz.trimf(self.outputUniverse, [-101, -100, -99])
        self.speedControl['brake'] = fuzz.trimf(self.outputUniverse, [-80, -70, -60])
        self.speedControl['do_nothing'] = fuzz.trimf(self.outputUniverse, [-5, -4, -3])
        self.speedControl['accelerate'] = fuzz.trimf(self.outputUniverse, [25, 35, 45])
        self.speedControl['full_ahead'] = fuzz.trimf(self.outputUniverse, [99, 100, 101])
        self.turn['sharp_left'] = fuzz.trimf(self.outputUniverse, [-101, -100, -90])
        self.turn['turn_left'] = fuzz.trimf(self.outputUniverse, [-60, -40, -20])
        self.turn['do_nothing'] = fuzz.trimf(self.outputUniverse, [-1, 0, 1])
        self.turn['turn_right'] = fuzz.trimf(self.outputUniverse, [20, 40, 60])
        self.turn['sharp_right'] = fuzz.trimf(self.outputUniverse, [90, 100, 101])

        """Generate rules"""
        self.rule1 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['full_ahead'], self.turn['do_nothing']), label='fh, 0')

        self.rule2 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['safe']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='fh, L')

        self.rule3 = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_left']), label='0, SL')

        self.rule4 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['far']),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='0, 0')

        self.rule5 = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['safe'] & self.rightDistance['safe']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_left']), label='0, L')

        self.rule6a = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['sharp']),
            consequent=(self.speedControl['hard_brake'], self.turn['do_nothing']), label='brake, 0')

        self.rule6b = ctrl.Rule(
            antecedent=(self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='0, 0 when stopped')

        self.rule7a = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] & self.centerDistDiff['sharp']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] & self.centerDistDiff['sharp'])),
            consequent=(self.speedControl['hard_brake'], self.turn['turn_left']), label='brake, L')

        self.rule7b = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['safe'] & self.centerDistDiff['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['close'] & self.centerDistDiff['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_left']), label='0, L when stopped')

        self.rule8a = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] & self.centerDistDiff['sharp']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] & self.centerDistDiff['sharp'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_left']), label='hb, SL')

        self.rule8b = ctrl.Rule(
            antecedent=((self.leftDistance['far'] & self.centerDistance['close'] & self.rightDistance['close'] & self.centerDistDiff['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['close'] & self.centerDistDiff['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='0, SL when stopped')

        self.rule9 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['far']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='fh, right')

        self.rule10 = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['safe']) |
                        (self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['close']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['close'])),
            consequent=(self.speedControl['accelerate'], self.turn['do_nothing']), label='acc, 0')

        self.rule11 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['far'] & self.rightDistance['close']),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_left']), label='acc, SL')

        self.rule12 = ctrl.Rule(
            antecedent=(self.leftDistance['safe'] & self.centerDistance['safe'] & self.rightDistance['far']),
            consequent=(self.speedControl['do_nothing'], self.turn['turn_right']), label='0, right')

        self.rule13a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['sharp']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] & self.centerDistDiff['sharp'])),
            consequent=(self.speedControl['brake'], self.turn['turn_right']), label='brake, right')

        self.rule13b = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['safe'] & self.centerDistDiff['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['turn_right']), label='0, right when stopped')

        self.rule14a = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'])),
            consequent=(self.speedControl['hard_brake'], self.turn['do_nothing']), label='hb, 0')

        """self.rule14b = ctrl.Rule(
            antecedent=((self.leftDistance['safe'] & self.centerDistance['close'] & self.rightDistance['safe'] & self.centerDistDiff['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['close'] & self.centerDistDiff['safe'])),
            consequent=(self.speedControl['do_nothing'], self.turn['do_nothing']), label='0, 0 when close')"""

        self.rule15 = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['far']) |
                        (self.leftDistance['close'] & self.centerDistance['safe'] & self.rightDistance['far'])),
            consequent=(self.speedControl['do_nothing'], self.turn['sharp_right']), label='0, SR')

        self.rule16 = ctrl.Rule(
            antecedent=(self.leftDistance['close'] & self.centerDistance['far'] & self.rightDistance['safe']),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='acc, SR')

        self.rule17a = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['sharp']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] & self.centerDistDiff['sharp'])),
            consequent=(self.speedControl['hard_brake'], self.turn['sharp_right']), label='hb, SR')

        self.rule17b = ctrl.Rule(
            antecedent=((self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['far'] & self.centerDistDiff['safe']) |
                        (self.leftDistance['close'] & self.centerDistance['close'] & self.rightDistance['safe'] & self.centerDistDiff['safe'])),
            consequent=(self.speedControl['accelerate'], self.turn['sharp_right']), label='0, SR, when stopped')



        """Generate controller engine"""
        self.engine_cs = ctrl.ControlSystem(rules=[self.rule1, self.rule2, self.rule3, self.rule4, self.rule5,
                                                   self.rule6a, self.rule6b, self.rule7a, self.rule7b, self.rule8a,
                                                   self.rule8b, self.rule9, self.rule10, self.rule11, self.rule12,
                                                   self.rule13a, self.rule13b, self.rule14a,
                                                   self.rule15, self.rule16, self.rule17a, self.rule17b]) #deleted sule 17b
        self.engine = ctrl.ControlSystemSimulation(self.engine_cs)

    def visualise(self):
        self.leftDistance.view()
        self.centerDistance.view()
        self.rightDistance.view()
        self.centerDistDiff.view()
        self.speedControl.view()
        self.turn.view()

    def compute(self, l_dist, c_dist, r_dist):

        #if self.prev_l == l_dist and self.prev_c == c_dist and self.prev_r == r_dist:
            #self.prev_l, self.prev_c, self.prev_r = l_dist, c_dist, r_dist
            #return 20, r_dist-l_dist

        for i in l_dist, c_dist, r_dist:
            if i < 0:
                i = 0

        self.engine.input['left_distance'] = l_dist
        self.engine.input['center_distance'] = c_dist
        self.engine.input['right_distance'] = r_dist
        self.engine.input['distance_difference'] = c_dist - self.prev_c

        self.engine.compute()
        output = (round(self.engine.output['sc'], 2), round(self.engine.output['turn'], 2))

        self.prev_l, self.prev_c, self.prev_r = l_dist, c_dist, r_dist
        print (output)
        return output


if __name__ == '__main__':
    a = FuzzyCarController()
    a.visualise()
    #print(a.compute(1, 1, 1))
