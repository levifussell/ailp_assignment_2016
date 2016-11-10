import caes as cs

"""PROPOSITIONS"""

ticket_revoked = cs.PropLiteral('ticket_revoked')
ticket_revoked_not = ticket_revoked.negate()

own_car = cs.PropLiteral('own_car')
own_car_not = own_car.negate()
car_hired_out = cs.PropLiteral('car_hired_out')
car_stolen = cs.PropLiteral('car_stolen')
car_documents = cs.PropLiteral('car_documents')

parking_legal = cs.PropLiteral('parking_legal')
parking_legal_not = parking_legal.negate()
visible_parking_signs = cs.PropLiteral('visible_parking_signs')
visible_parking_signs_not = visible_parking_signs.negate()
photo_of_parking_signs = cs.PropLiteral('photo_of_parking_signs')
photo_of_parking_signs_not = cs.PropLiteral('photo_of_parking_signs_not')
permit_valid = cs.PropLiteral('permit_valid')
permit_valid_not = permit_valid.negate()
permit_displayed = cs.PropLiteral('permit_displayed')
permit_displayed_not = permit_displayed.negate()
# permit_scratched = cs.PropLiteral('permit_scratched')

parking_exception = cs.PropLiteral('parking_exception')
parking_exception_not = parking_exception.negate()
is_diplomat = cs.PropLiteral('is_diplomat')
is_emergency = cs.PropLiteral('is_emergency')

"""ARGUMENTS"""

# ticket
arg_for_revoking_ticket_1 = cs.Argument(ticket_revoked,
    premises={parking_legal})

arg_for_revoking_ticket_2 = cs.Argument(ticket_revoked,
    premises={own_car_not})

arg_for_revoking_ticket_3 = cs.Argument(ticket_revoked,
    premises={parking_exception})

# car
arg_for_owning_a_car = cs.Argument(own_car,
    premises={car_documents},
    exceptions={car_hired_out, car_stolen})

arg_for_not_owning_a_car_1 = cs.Argument(own_car_not,
    premises={car_hired_out})

arg_for_not_owning_a_car_2 = cs.Argument(own_car_not,
    premises={car_stolen})

# parking
arg_for_not_legal_parking = cs.Argument(parking_legal_not,
    premises={visible_parking_signs, permit_valid_not})

arg_for_legal_parking_1 = cs.Argument(parking_legal,
    premises={visible_parking_signs_not},
    exceptions={photo_of_parking_signs_not})

arg_for_legal_parking_2 = cs.Argument(parking_legal,
    premises={permit_valid})

# permit
arg_for_permit_valid = cs.Argument(permit_valid,
    premises={permit_displayed})

# parking exceptions
arg_for_parking_exception_1 = cs.Argument(parking_exception,
    premises={is_diplomat})

arg_for_parking_exception_2 = cs.Argument(parking_exception,
    premises={is_emergency})

argset = cs.ArgumentSet()
argset.add_argument(arg_for_revoking_ticket_1, arg_id='arg_for_revoking_ticket_1')
argset.add_argument(arg_for_revoking_ticket_2, arg_id='arg_for_revoking_ticket_2')
argset.add_argument(arg_for_revoking_ticket_3, arg_id='arg_for_revoking_ticket_3')
argset.add_argument(arg_for_owning_a_car, arg_id='arg_for_owning_a_car')
argset.add_argument(arg_for_not_owning_a_car_1, arg_id='arg_for_not_owning_a_car_1')
argset.add_argument(arg_for_not_owning_a_car_2, arg_id='arg_for_not_owning_a_car_2')
argset.add_argument(arg_for_not_legal_parking, arg_id='arg_for_not_legal_parking')
argset.add_argument(arg_for_legal_parking_1, arg_id='arg_for_legal_parking_1')
argset.add_argument(arg_for_legal_parking_2, arg_id='arg_for_legal_parking_2')
argset.add_argument(arg_for_permit_valid, arg_id='arg_for_permit_valid')
argset.add_argument(arg_for_parking_exception_1, arg_id='arg_for_parking_exception_1')
argset.add_argument(arg_for_parking_exception_2, arg_id='arg_for_parking_exception_2')

argset.draw()

"""PROOF OF STANDARDS
Possible values for proof standards: `"scintilla"`, `"preponderance"`,
`"clear_and_convincing"`, `"beyond_reasonable_doubt"`, and
`"dialectical_validity"`.
"""

ps = cs.ProofStandard(
    [(ticket_revoked, "scintilla"),
    (own_car, "dialectical_validity"),
    (parking_exception, "preponderance"),
    (parking_legal, "scintilla")])


"""CAES"""

assumptions = {car_documents,
    photo_of_parking_signs,
    visible_parking_signs,
    permit_valid_not
    }
weights = {'arg_for_revoking_ticket_1':0.8,
    'arg_for_revoking_ticket_2':0.8,
    'arg_for_revoking_ticket_3':0.6,
    'arg_for_owning_a_car':0.8,
    'arg_for_not_owning_a_car_1':0.8,
    'arg_for_not_owning_a_car_2':0.8,
    'arg_for_not_legal_parking':0.8,
    'arg_for_legal_parking_1':0.8,
    'arg_for_legal_parking_2':0.8,
    'arg_for_not_visible_signs':0.4,
    'arg_for_permit_valid':0.8,
    'arg_for_parking_exception_1':0.8,
    'arg_for_parking_exception_2':0.8}

audience = cs.Audience(assumptions, weights)

caes = cs.CAES(argset, audience, ps)
print(caes.get_all_arguments())

print(caes.acceptable(ticket_revoked))














""""""
