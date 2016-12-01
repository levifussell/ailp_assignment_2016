import caes as cs

"""PROPOSITIONS"""

give_citizenship = cs.PropLiteral('give_citizenship')
give_citizenship_not = give_citizenship.negate()

parents_have_citizenship = cs.PropLiteral('parents_have_citizenship')

meet_eligibility_requirements = cs.PropLiteral('meet_eligibility_requirements')
meet_age_minimum = cs.PropLiteral('eligible_age')
meet_permanent_residence_minimum = cs.PropLiteral('eligible_age')
meet_physically_present_minimum = cs.PropLiteral('meet_physically_present_minimum')

pass_language_test = cs.PropLiteral('pass_language_test')
read_language = cs.PropLiteral('read_english')
write_language = cs.PropLiteral('write_language')
speak_language = cs.PropLiteral('speak_language')
pass_knowledge_test = cs.PropLiteral('pass_knowledge_test')
know_history = cs.PropLiteral('know_history')
know_government = cs.PropLiteral('know_government')

demonstrate_moral_character = cs.PropLiteral('demonstrate_moral_character')
demonstrate_moral_character_not = demonstrate_moral_character.negate()
working_minimum = cs.PropLiteral('working_minimum')
commit_serious_crime = cs.PropLiteral('commit_serious_crime')

take_oath_of_allegiance = cs.PropLiteral('take_oath_of_allegiance')

"""ARGUMENTS"""

# citizenship
arg_for_citizenship_1 = cs.Argument(give_citizenship,
    premises={parents_have_citizenship})

arg_for_citizenship_2 = cs.Argument(give_citizenship,
    premises={meet_eligibility_requirements, pass_language_test,
        pass_knowledge_test,
        take_oath_of_allegiance})

arg_for_citizenship_3 = cs.Argument(give_citizenship_not,
    premises={demonstrate_moral_character_not})

# eligibility requirements
arg_for_meet_eligibility_requirements = cs.Argument(meet_eligibility_requirements,
    premises={meet_age_minimum, meet_permanent_residence_minimum,
        meet_physically_present_minimum})

# language test
arg_for_pass_language_test = cs.Argument(pass_language_test,
    premises={read_language, write_language,
        speak_language})

# knowledge test
arg_for_pass_knowledge_test = cs.Argument(pass_knowledge_test,
    premises={know_history, know_government})

# demonstrate_moral_character
arg_for_not_demonstrate_moral_character = cs.Argument(demonstrate_moral_character_not,
    premises={commit_serious_crime})

arg_for_demonstrate_moral_character = cs.Argument(demonstrate_moral_character,
    premises={working_minimum})


argset = cs.ArgumentSet()
argset.add_argument(arg_for_citizenship_1, arg_id='arg_for_citizenship_1')
argset.add_argument(arg_for_citizenship_2, arg_id='arg_for_citizenship_2')
argset.add_argument(arg_for_citizenship_3, arg_id='arg_for_citizenship_3')
argset.add_argument(arg_for_meet_eligibility_requirements, arg_id='arg_for_meet_eligibility_requirements')
argset.add_argument(arg_for_pass_language_test, arg_id='arg_for_pass_language_test')
argset.add_argument(arg_for_pass_knowledge_test, arg_id='arg_for_pass_knowledge_test')
argset.add_argument(arg_for_not_demonstrate_moral_character, arg_id='arg_for_not_demonstrate_moral_character')
argset.add_argument(arg_for_demonstrate_moral_character, arg_id='arg_for_demonstrate_moral_character')

argset.draw()

"""PROOF OF STANDARDS
Possible values for proof standards: `"scintilla"`, `"preponderance"`,
`"clear_and_convincing"`, `"beyond_reasonable_doubt"`, and
`"dialectical_validity"`.
"""

ps = cs.ProofStandard(
    [(give_citizenship, "preponderance"),
    (demonstrate_moral_character_not, "preponderance")])


"""CAES"""

assumptions = {parents_have_citizenship,
commit_serious_crime}
# assumptions = {meet_age_minimum,
#     meet_permanent_residence_minimum,
#     meet_physically_present_minimum,
#     read_language,
#     write_language,
#     speak_language,
#     know_history,
#     know_government,
#     take_oath_of_allegiance,
#     commit_serious_crime,
#     working_minimum}

weights = {'arg_for_citizenship_1':1.0,
    'arg_for_citizenship_2':0.5,
    'arg_for_citizenship_3':0.6,
    'arg_for_meet_eligibility_requirements':0.8,
    'arg_for_pass_language_test':0.8,
    'arg_for_pass_knowledge_test':0.8,
    'arg_for_not_demonstrate_moral_character':0.3,
    'arg_for_demonstrate_moral_character':0.5}

audience = cs.Audience(assumptions, weights)

caes = cs.CAES(argset, audience, ps)
print(caes.get_all_arguments())

print(caes.acceptable(give_citizenship))

print(caes.get_all_arguments_set())














""""""
