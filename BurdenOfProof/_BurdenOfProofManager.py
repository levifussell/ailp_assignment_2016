from _LoggerManager import _Log, _LoggerState

import carneades.src.carneades.caes as cs

from enum import Enum

class _BurdenState(Enum):
    TICKET = 1
    NO_TICKET = 2
    BROKE = 3

class WeightedPropEdge:

    def __init__(self, prop, weight):
        self.prop = prop
        self.weight = weight

    def __str__(self):
        return "({})-> {}".format(self.weight, self.prop)

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

        self.searchGraph = {}
        self.searchGraph[argumentProp] = []
        self.latestProp = None
        self.trialedAssumptionProps = []
        self.effectiveProps = []

        self.temporaryAudience = self.allAudience

        self.state = _BurdenState.TICKET

    def step(self):

        # wait for input to continue step
        input('------------------(continue?)------------------')

        _Log('\n\nstart state: {}'.format(self.state), _LoggerState.WARNING)

        # print('all props: {}'.format(self.allArgumentsSet.propset()))
        # print('target prop: {}'.format(self.currentWeakProps))
        # because the proposition that both parties are arguing for is already
        #  included in the currentWeakProps, we begin by finding applicablt arguments
        stateAgainst = _BurdenState.TICKET
        if self.state == _BurdenState.TICKET:
            stateAgainst = _BurdenState.NO_TICKET

        nextArg = self.getNextArgument()
        if nextArg != None:
            self.currentArgSet.append(nextArg)

        # print('!!chosen arg: {}'.format(nextArg))

            print("{}:  {} because {} and not {}".format(stateAgainst, nextArg.conclusion, nextArg.premises, nextArg.exceptions))
        else:
            print("{}: DAMN I have no arguments. You win.".format(stateAgainst))

        argsetStep = cs.ArgumentSet()
        for arg in self.currentArgSet:
            argsetStep.add_argument(arg, arg_id=arg.arg_id)


        self.temporaryAssumptions = []
        # self.currentWeakProps = [self.argumentTargetProp]

        for prop in argsetStep.propset():
            # check if acceptable
            try:
                hasNoArgumentsFor = False
                try:
                    if len(argsetStep.get_arguments(prop)) == 0 and len(argsetStep.get_arguments(prop.negate())) == 0:
                        hasNoArgumentsFor = True
                except:
                    hasNoArgumentsFor = True

                # if not(caesStep.acceptable(prop)):
                if prop != None and not(prop in self.currentWeakProps) and hasNoArgumentsFor:

                    if not(prop in self.allAudience.assumptions):
                        self.currentWeakProps.append(prop)

                    # check which argument this prop was a part of and link it to that argument's conclusion
                    for arg in self.currentArgSet:
                        if prop in arg.premises:
                            if not(prop in self.searchGraph.keys()):
                                self.searchGraph[prop] = []

                            weight = len(arg.premises) + len(arg.exceptions) #self.allAudience.weight[arg.arg_id]
                            weightedLink = WeightedPropEdge(arg.conclusion, weight)
                            self.searchGraph[prop].append(weightedLink)
                            # remember the latest prop, so that when we are successful we can trace up the graph
                            # TODO: later replace this with a list of all successful props and choose the prop that
                            #  is the shortest distance to the argumentTargetProp
                            self.latestProp = prop
                            if prop in self.allAudience.assumptions and not(prop in self.effectiveProps) and not(prop in self.trialedAssumptionProps):
                                self.trialedAssumptionProps.append(prop)
                                self.effectiveProps.append(prop)

                    # print('arg numm1111:{}, {}'.format(prop, argsetStep.get_arguments(prop)))
                    # negateAllowed = True
                    # try:
                    #     if len(argsetStep.get_arguments(prop.negate())) == 0:
                    #         negateAllowed = False
                    #     else:
                    #         negateAllowed = True
                    # except:
                    #     negateAllowed = True


                    # if the proposition contains no arguments for the negative or positive case (or both
                    #  cases don't exist),
                    #  then add it as an assumption to the audience temporarily. If either the positive
                    #  or negative have arguments for them, then no assumptions are added
                if prop != None and not(prop in self.temporaryAudience.assumptions):
                    try:
                        if len(argsetStep.get_arguments(prop)) == 0 and len(argsetStep.get_arguments(prop.negate())) == 0:
                            self.temporaryAssumptions.append(prop.negate())
                            # self.currentWeakProps.remove(prop)
                    except:
                        self.temporaryAssumptions.append(prop.negate())
                        # self.currentWeakProps.remove(prop)
                    # _Log('weak prop found: {}'.format(prop), _LoggerState.WARNING)
            except:pass

        # print('propsNEW: {}'.format(argsetStep.propset()))

        # build a CAES to simulate this argument
        assumpStep = []
        assumpStep.extend(self.allAudience.assumptions)
        assumpStep.extend(self.temporaryAssumptions)
        self.temporaryAudience = cs.Audience(assumpStep, self.allAudience.weight)

        print('\nCURRENT ASSUMPTIONS:{}\n'.format(self.temporaryAudience.assumptions))

        caesStep = cs.CAES(argsetStep, self.temporaryAudience, self.allProofOfStandards)

        # check if the target prop is now acceptable
        # try:
        if caesStep.acceptable(self.argumentTargetProp) and self.state == _BurdenState.TICKET:
            # if self.state == _BurdenState.TICKET:
            self.state = _BurdenState.NO_TICKET
            # self.currentWeakProps = [self.argumentTargetProp]
            invertWeakProps = []
            for prop in self.currentWeakProps:
                invertWeakProps.append(prop.negate())
            self.currentWeakProps = invertWeakProps;

            # trace the argument found back to the target argument prop and write it out
            finalArg = self.traceShortestArgument()
            finalArgStr = "FINAL ARG: "
            for arg in finalArg:
                finalArgStr += "\nPath: "
                for prop in arg:
                    finalArgStr += "->{}".format(prop)

            _Log(finalArgStr, _LoggerState.WARNING)
            self.effectiveProps = []
            # self.searchGraph = {}
            # self.searchGraph[self.argumentTargetProp] = []

        elif not caesStep.acceptable(self.argumentTargetProp) and self.state == _BurdenState.NO_TICKET:
            self.state = _BurdenState.TICKET
            # self.currentWeakProps = [self.argumentTargetProp]
            invertWeakProps = []
            for prop in self.currentWeakProps:
                invertWeakProps.append(prop.negate())
            self.currentWeakProps = invertWeakProps;

            # trace the argument found back to the target argument prop and write it out
            finalArg = self.traceShortestArgument()
            finalArgStr = "FINAL ARG: "
            for arg in finalArg:
                finalArgStr += "\nPath: "
                for prop in arg:
                    finalArgStr += "->{}".format(prop)

            _Log(finalArgStr, _LoggerState.WARNING)
            self.effectiveProps = []
            # self.searchGraph = {}
            # self.searchGraph[self.argumentTargetProp] = []

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


        # draw out graph
        searchGraphStr = ""
        for node in self.searchGraph.keys():
            searchGraphStr += "\n{} -> ".format(node)
            for link in self.searchGraph[node]:
                searchGraphStr += "{}, ".format(link)

        _Log(searchGraphStr, _LoggerState.WARNING)

    def getNextArgument(self):

        # find argument that targets the weaknesses (ordered in order of best to worst)
        weakPropArgs = []
        # an argument that targets a higher prop is more significant
        weakPropArgWeights = []
        weakPropArgWeightsCum = []
        # for arg in self.allArguments:
        #     depthOfProp = 0
        #     for i in range(0, len(self.currentWeakProps)):
        #         if arg.conclusion == self.currentWeakProps[i]:
        #             weakPropArgs.append(arg)
        #             weakPropArgStrengths.append(i)
        for i in range(0, len(self.currentWeakProps)):
            attackProp = self.currentWeakProps[i]
            # if self.state == _BurdenState.NO_TICKET:
            #     attackProp = attackProp.negate()

            try:
                propArgs = self.allArgumentsSet.get_arguments(attackProp)
                # weakPropArgs.extend(propArgs)
                for j in range(0, len(propArgs)):
                    if not(propArgs[j] in self.currentArgSet):
                        weakPropArgs.append(propArgs[j])
                        argWeight = propArgs[i].premises + propArgs[i].exceptions
                        weakPropArgWeights.append(argWeight)
                        weakPropArgWeightsCum.append(self.calculateCulmWeight(propArgs[j], argWeight))
            except: pass

        # now we have the possible arguments for the weak props, list them
        # argsData = ""
        # for i in range(0, len(weakPropArgs)):
        #     argsData += "{}. Arg: {},        strength={}\n".format(i, weakPropArgs[i], weakPropArgStrengths[i])
        #
        # _Log(argsData, _LoggerState.WARNING)

        # for now, return the last argument in the list (depth first search)
        try:
            return weakPropArgs[-1]
        except:
            return None

    def determineCurrentArgumentWeaknesses(self): pass

    def calculateCulmWeight(self, propStart, startWeight):

        currentPropNode = WeightedPropEdge(propStart, 0)
        cumWeight = startWeight

        if currentPropNode.prop == self.argumentTargetProp or currentPropNode.prop == self.argumentTargetProp.negate():
            return cumWeight
        else:
            # for now, get the first value the node points to
            firstProp = self.searchGraph[currentPropNode.prop][0]
            self.calculateCulmWeight(firstProp.prop, cumWeight + firstProp.weight)

    def graphHeuristic_depthFirstSearch(self, argumentList):
        return argumentList[-1]

    def graphHeuristic_breadthFirstSearch(self, argumentList):
        return argumentList[0]

    def graphHeuristic_weightFirstSearch(self, argumentList, argumentWeightList):
        minProp = argumentList[0]
        minPropWeight = 1000

        for i in range(0, len(argumentList)):
            if argumentWeightList[i] < minPropWeight:
                minPropWeight = argumentWeightList[i]
                minProp = argumentList[i]

        return minProp

    def graphHeuristic_djikstra(self, argumentList, argumentWeightCumList):
        return self.graphHeuristic_weightFirstSearch(argumentList, argumentWeightCumList)

    def traceShortestArgument(self):

        # find the shortest argument from the successful props. For now there is only one successful prop
        shortestArgumentProps = []

        # argueForProp = self.argumentTargetProp
        # if self.state = _BurdenState.TICKET:
        #     argueForProp = argueForProp.negate()

        for eProp in self.effectiveProps:

            currentPropNode = WeightedPropEdge(eProp, 0)
            shortestArgumentEProp = [currentPropNode]

            while currentPropNode.prop != self.argumentTargetProp and currentPropNode.prop != self.argumentTargetProp.negate():
                # for now, get the first value the node points to
                currentPropNode = self.searchGraph[currentPropNode.prop][0]
                shortestArgumentEProp.append(currentPropNode)

            shortestArgumentProps.append(shortestArgumentEProp)

        return shortestArgumentProps
