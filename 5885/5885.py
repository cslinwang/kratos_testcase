from __future__ import absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7

import KratosMultiphysics
import KratosMultiphysics.MappingApplication
import KratosMultiphysics.kratos_utilities as kratos_utilities

if __name__ == '__main__':

    origin_model = KratosMultiphysics.Model()
    origin_model_part = origin_model.CreateModelPart("Main")
    origin_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.PRESSURE)
    sub1 = origin_model_part.CreateSubModelPart("sub1")
    sub1.CreateNewNode(1, 1.0,0.0,0.0)
    sub1.CreateNewNode(2, 2.0,0.0,0.0)
    sub1.CreateNewNode(3, 3.0,0.0,0.0)
    origin_model_part.AddProperties(KratosMultiphysics.Properties(1))
    sub1.CreateNewElement("Element2D2N", 1, [1,2], origin_model_part.GetProperties()[1])
    sub1.CreateNewElement("Element2D2N", 2, [2,3], origin_model_part.GetProperties()[1])
    origin_model_part.ProcessInfo.SetValue(KratosMultiphysics.DOMAIN_SIZE,2)

    destination_model = KratosMultiphysics.Model()
    destination_model_part = destination_model.CreateModelPart("Main")
    destination_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.PRESSURE)
    sub2 = destination_model_part.CreateSubModelPart("sub2")
    sub2.CreateNewNode(1, 1.5,0.0,0.0)
    sub2.CreateNewNode(2, 2.5,0.0,0.0)
    destination_model_part.AddProperties(KratosMultiphysics.Properties(1))
    sub2.CreateNewElement("Element2D2N", 1, [1,2], destination_model_part.GetProperties()[1])
    destination_model_part.ProcessInfo.SetValue(KratosMultiphysics.DOMAIN_SIZE,2)

    KratosMultiphysics.VariableUtils().SetNonHistoricalVariableToZero(KratosMultiphysics.PRESSURE,origin_model_part.Nodes)

    KratosMultiphysics.VariableUtils().SetNonHistoricalVariableToZero(KratosMultiphysics.PRESSURE,destination_model_part.Nodes)

    value = 1.0
    for node in sub1.Nodes:
        node.SetValue(KratosMultiphysics.PRESSURE,value)
        value = value + 1.0

    for node in origin_model_part.Nodes:
        print(node.Id,node.GetValue(KratosMultiphysics.PRESSURE))

    # map from current model part of interest to reference model part
    mapping_parameters = KratosMultiphysics.Parameters("""{
        "mapper_type": "nearest_element",
        "interface_submodel_part_origin": "sub1",
        "interface_submodel_part_destination": "sub2",
        "echo_level" : 3
        }""")


    mapper = KratosMultiphysics.MappingApplication.MapperFactory.CreateMapper(origin_model_part,destination_model_part,mapping_parameters)

    mapper.Map(KratosMultiphysics.PRESSURE, \
        KratosMultiphysics.PRESSURE, \
        KratosMultiphysics.MappingApplication.Mapper.FROM_NON_HISTORICAL | \
        KratosMultiphysics.MappingApplication.Mapper.TO_NON_HISTORICAL)

    # mapper.Map(KratosMultiphysics.PRESSURE, \
    #     KratosMultiphysics.PRESSURE)

    for node in destination_model_part.Nodes:
        print(node.Id,node.GetValue(KratosMultiphysics.PRESSURE))