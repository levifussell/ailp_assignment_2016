<!> Propositions <!>

<Proposition>
    <name>own_car</name>
    <proof>dialectical_validity</proof>
</Proposition>

<Proposition>
    <name>parking_exception</name>
    <proof>preponderance</proof>
</Proposition>

<!> ARGUMENTS <!>

    <!> ticket <!>
<Argument>
    <name>arg_for_revoking_ticket_1</name>
    <conclusion>ticket_revoked</conclusion>
    <premises>[parking_legal]</premises>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_revoking_ticket_2</name>
    <conclusion>ticket_revoked</conclusion>
    <premises>[neg_own_car]</premises>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_revoking_ticket_3</name>
    <conclusion>ticket_revoked</conclusion>
    <premises>[parking_exception]</premises>
    <weight>0.6</weight>
</Argument>

    <!> car <!>
<Argument>
    <name>arg_for_owning_a_car</name>
    <conclusion>own_car</conclusion>
    <premises>[car_documents]</premises>
    <exceptions>[car_hired_out, car_stolen]</exceptions>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_not_owning_a_car_1</name>
    <conclusion>neg_own_car</conclusion>
    <premises>[car_hired_out]</premises>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_not_owning_a_car_2</name>
    <conclusion>neg_own_car</conclusion>
    <premises>[car_stolen]</premises>
    <weight>0.8</weight>
</Argument>

    <!> parking <!>
Argument>
    <name>arg_for_not_legal_parking</name>
    <conclusion>neg_parking_legal</conclusion>
    <premises>[visible_parking_signs, neg_permit_valid]</premises>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_legal_parking_1</name>
    <conclusion>parking_legal</conclusion>
    <premises>[neg_visible_parking_signs]</premises>
    <exceptions>[neg_photo_of_parking_signs]</exceptions>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_legal_parking_2</name>
    <conclusion>parking_legal</conclusion>
    <premises>[permit_valid]</premises>
    <weight>0.8</weight>
</Argument>

    <!> permit <!>
<Argument>
    <name>arg_for_permit_valid</name>
    <conclusion>permit_valid</conclusion>
    <premises>[permit_displayed]</premises>
    <weight>0.8</weight>
</Argument>

    <!> parking exceptions <!>
<Argument>
    <name>arg_for_parking_exception_1</name>
    <conclusion>parking_exception</conclusion>
    <premises>[is_diplomat]</premises>
    <weight>0.8</weight>
</Argument>
<Argument>
    <name>arg_for_parking_exception_2</name>
    <conclusion>parking_exception</conclusion>
    <premises>[is_emergency]</premises>
    <weight>0.8</weight>
</Argument>

<!> CAES <!>

<CAES>
    <assumptions>[car_documents, photo_of_parking_signs, neg_visible_parking_signs, neg_permit_valid]</assumptions>
</CAES>
