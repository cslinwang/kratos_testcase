import KratosMultiphysics

parameters = KratosMultiphysics.Parameters("""{
    "array_of_vectors" : [],
    "array_of_strings" : []
}""")

vector = KratosMultiphysics.Vector([1, 2, 3])
string = "abc"

for i in range(2):
    parameters["array_of_vectors"].Append(vector)
    parameters["array_of_strings"].Append(string)
    print(parameters)