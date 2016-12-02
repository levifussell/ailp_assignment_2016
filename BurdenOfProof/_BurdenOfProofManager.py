from _LoggerManager import _Log, _LoggerState

import carneades.src.carneades.caes as cs

from enum import Enum

class _BurdenState(Enum):
    TICKET = 1
    NO_TICKET = 2
    BROKE = 3

class _BurdenOfProofManager:

    def __init__(self, allPropositions, allArgumentsSet, allAudience, allProofOfStandards, argumentProp):

        self.allPropositions = allPropositions
        self.allArgumentsSet = allArgumentsSet
        self.allAudience = allAudience
        self.allProofOfStandards = allProofOfStandards

        self.argumentTargetProp = argumentProp
        self.currentWeakProps = [argumentProp]
        self.currentArgSet = []
        self.temporaryAssumptions = []

        self.state = _BurdenState.TICKET

    def step(self):

        # wait for input to continue step
        continueSim = input('------------------(continue?)------------------')

        _Log('\n\nstart state: {}'.format(self.state), _LoggerState.WARNING)

        # print('all props: {}'.format(self.allArgumentsSet.propset()))
        # print('target prop: {}'.format(self.currentWeakProps))
        # because the proposition that both parties are arguing for is already
        #  included in the currentWeakProps, we begin by finding applicablt arguments
        nextArg = self.getNextArgument()
        if nextArg != None:
            self.currentArgSet.append(nextArg)

        print('!!chosen arg: {}'.format(nextArg))

        argsetStep = cs.ArgumentSet()
        for arg in self.currentArgSet:
            argsetStep.add_argument(arg, arg_id=arg.arg_id)


        self.temporaryAssumptions = []

        for prop in argsetStep.propset():
            # check if acceptable
            try:
                # if not(caesStep.acceptable(prop)):
                if prop != None and not(prop in self.currentWeakProps) and not(prop in self.allAudience.assumptions):
                    self.currentWeakProps.append(prop)
                    # print('arg numm1111:{}, {}'.format(prop, argsetStep.get_arguments(prop)))
                    negateAllowed = True
                    try:
                        if len(argsetStep.get_arguments(prop.negate())) == 0:
                            negateAllowed = False
                        else:
                            negateAllowed = True
                    except:
                        negateAllowed = True

                    if len(argsetStep.get_arguments(prop)) == 0 and negateAllowed:
                        self.temporaryAssumptions.append(prop.negate())
                    # _Log('weak prop found: {}'.format(prop), _LoggerState.WARNING)
            except:pass

        # print('propsNEW: {}'.format(argsetStep.propset()))

        # build a CAES to simulate this argument
        assumpStep = []
        assumpStep.extend(self.allAudience.assumptions)
        assumpStep.extend(self.temporaryAssumptions)
        audStep = cs.Audience(assumpStep, self.allAudience.weight)

        print('asasasasa:{}'.format(audStep.assumptions))

        caesStep = cs.CAES(argsetStep, audStep, self.allProofOfStandards)

        # check if the target prop is now acceptable
        # try:
        if caesStep.acceptable(self.argumentTargetProp):
            if self.state == _BurdenState.TICKET:
                self.state = _BurdenState.NO_TICKET
                self.currentWeakProps = [self.argumentTargetProp]

        elif not caesStep.acceptable(self.argumentTargetProp) and self.state == _BurdenState.NO_TICKET:
            self.state = _BurdenState.TICKET
            self.currentWeakProps = [self.argumentTargetProp]
        # except:
        #     try:
        #         # if fails, the argument isn't acceptable
        #         # if caesStep.acceptable(self.argumentTargetProp.negate()):
        #         #     self.state = _BurdenState.TICKET
        #         # else:
        #         #     self.state = _BurdenState.NO_TICKET
        #         self.state = _BurdenState.BROKE
        #     except:
        #         self.state = _BurdenState.BROKE


        # itterate through the propositions in the argumentSet and check for applicability
        # print('prooopssps: {}'.format(argsetStep.propset()))

        # self.temporaryAssumptions = []
        #
        # for prop in argsetStep.propset():
        #     # check if acceptable
        #     try:
        #         # if not(caesStep.acceptable(prop)):
        #         if prop != None and not(prop in self.currentWeakProps) and not(prop in self.allAudience.assumptions):
        #             self.currentWeakProps.append(prop)
        #
        #             if self.allArgumentsSet.get_arguments(prop) == 0:
        #                 self.temporaryAssumptions.append(prop.negate())
        #             # _Log('weak prop found: {}'.format(prop), _LoggerState.WARNING)
        #     except:pass
                # if the applicability fails, it is a weak prop
                # if prop != None and not(prop in self.currentWeakProps):
                #     self.currentWeakProps.append(prop)
                # _Log('weak prop found: {}'.format(prop), _LoggerState.WARNING)

        # document weak props
        propsData = ""
        for i in range(0, len(self.currentWeakProps)):
            propsData += "{}. weak prop: {}\n".format(i, self.currentWeakProps[i])

        _Log(propsData, _LoggerState.WARNING)

        _Log('\n\nend state: {}'.format(self.state), _LoggerState.WARNING)

    def getNextArgument(self):

        # find argument that targets the weaknesses (ordered in order of best to worst)
        weakPropArgs = []
        # an argument that targets a higher prop is more significant
        weakPropArgStrengths = []
        # for arg in self.allArguments:
        #     depthOfProp = 0
        #     for i in range(0, len(self.currentWeakProps)):
        #         if arg.conclusion == self.currentWeakProps[i]:
        #             weakPropArgs.append(arg)
        #             weakPropArgStrengths.append(i)
        for i in range(0, len(self.currentWeakProps)):
            attackProp = self.currentWeakProps[i]
            if self.state == _BurdenState.NO_TICKET:
                attackProp = attackProp.negate()

            try:
                propArgs = self.allArgumentsSet.get_arguments(attackProp)
                # weakPropArgs.extend(propArgs)
                for j in range(0, len(propArgs)):
                    # if not(propArgs[j] in self.currentArgSet):
                        weakPropArgs.append(propArgs[j])
                        weakPropArgStrengths.append(i)
            except: pass

        # now we have the possible arguments for the weak props, list them
        # argsData = ""
        # for i in range(0, len(weakPropArgs)):
        #     argsData += "{}. Arg: {},        strength={}\n".format(i, weakPropArgs[i], weakPropArgStrengths[i])

        # _Log(argsData, _LoggerState.WARNING)

        # for now, return the highest strength argument
        try:
            return weakPropArgs[-1]
        except:
            return None

    def determineCurrentArgumentWeaknesses(self): pass
