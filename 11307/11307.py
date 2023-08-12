import KratosMultiphysics


model = KratosMultiphysics.Model()
mp1 = model.CreateModelPart("main_1")
mp2 = mp1.CreateSubModelPart("sub")

model.DeleteModelPart("main_1.sub")
print(mp1)