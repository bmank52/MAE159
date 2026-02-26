import numpy as np

pax = 250
businessClassPercent = .15
econWidth = 20 # in
econPitch = 31 # in
aisleCount = 2
aisleWidth = 19 #in
businessWidth = econWidth * 1.25  # in
businessPitch = econPitch * 1.7  # in
businessAisleWidth = 1.25 * aisleWidth  # in

wallThickness = 6 # in
abreast = 9 #Seats per row in econ

diameterInternal = aisleWidth * aisleCount + abreast * econWidth #Width of internal diameter based on econ class seating
diameterExternal = diameterInternal + 2 * wallThickness #internal diameter plus walls
abreastBusiness = np.floor((diameterInternal - businessAisleWidth * aisleCount) /businessWidth)
paxBusiness = pax * businessClassPercent
businessRows = np.ceil( paxBusiness/ abreastBusiness)
numBusinessSeats = businessRows * abreastBusiness

paxEcon = pax - paxBusiness
rowsEcon = np.ceil(paxEcon / abreast)

lengthEcon = rowsEcon * econPitch
lengthBusiness = businessRows * businessPitch
lengthNose = 1.35 * diameterExternal # Should be 1.2-1.5
lengthAft = 2.85 * diameterExternal # Should be 2.3-3.4
lengthLav = 40
lengthADoor = 42
lengthGalley = 100
lengthMisc = lengthLav * 2 + lengthADoor * 2 + 2 * lengthGalley

lengthFuselage = (lengthNose + lengthAft + lengthEcon + lengthBusiness + lengthMisc) / 12 #inches to feet

print(f"Total Fuselage Length: {lengthFuselage:.2f} ft")
print("-" * 30)
print(f"Business Class: {np.ceil(businessRows)} rows, {np.ceil(abreastBusiness)} abreast")
print(f"Economy Class:  {np.ceil(rowsEcon)} rows, {np.ceil(abreast)} abreast")
