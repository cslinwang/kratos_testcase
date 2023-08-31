
import KratosMultiphysics

params = KratosMultiphysics.Parameters("[0, 1]")
lst = []

for item in params:
    lst.append(item)
    print(item.GetInt())

for item in lst:
    print(item.GetInt())
