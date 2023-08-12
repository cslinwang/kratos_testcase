from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7
import KratosMultiphysics
import KratosMultiphysics.MeshingApplication as KratosMeshing
import math


model = KratosMultiphysics.Model()
main_model_part = model.CreateModelPart('main')

main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISTANCE)
main_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISTANCE_GRADIENT)
KratosMultiphysics.ModelPartIO('mmg_test').ReadModelPart(main_model_part)

#creating line sub model part
line_sub_model_part = main_model_part.CreateSubModelPart('line')
y_line = 0.7
for node in main_model_part.Nodes:
    distance = node.Y - y_line
    node.SetValue(KratosMultiphysics.DISTANCE,distance)
for element in main_model_part.Elements:
    npos = 0
    nneg = 0
    for elnode in element.GetNodes():
        distance = elnode.GetValue(KratosMultiphysics.DISTANCE)
        if distance > 0:
            npos += 1
        else:
            nneg += 1
    if npos > 0 and nneg > 0:
        element.Set(KratosMultiphysics.STRUCTURE)
        line_sub_model_part.Elements.append(element)


radius = 0.1
for node in main_model_part.Nodes:
    distance_sq = node.X**2+node.Y**2-radius**2
    if distance_sq >= 0:
        distance = math.sqrt(distance_sq)
        node.SetSolutionStepValue(KratosMultiphysics.DISTANCE,distance)
    else:
        distance = -math.sqrt(-distance_sq)
        node.SetSolutionStepValue(KratosMultiphysics.DISTANCE,distance)



find_nodal_h = KratosMultiphysics.FindNodalHNonHistoricalProcess(main_model_part)
find_nodal_h.Execute()

MetricParameters = KratosMultiphysics.Parameters("""
{
    "minimal_size"                              : 0.01,
    "maximal_size"                              : 2.0,
    "sizing_parameters": {
        "reference_variable_name"               : "DISTANCE",
        "boundary_layer_max_distance"           : 0.1,
        "interpolation"                         : "constant"
    },
    "enforce_current"                           : false,
    "anisotropy_remeshing"                      : false,
    "anisotropy_parameters": {
        "reference_variable_name"               : "DISTANCE",
        "hmin_over_hmax_anisotropic_ratio"      : 0.5,
        "boundary_layer_max_distance"           : 1,
        "interpolation"                         : "linear"
    }
}
""")
##COMPUTE LEVEL SET METRIC
metric_process = KratosMultiphysics.MeshingApplication.ComputeLevelSetSolMetricProcess2D(main_model_part,  KratosMultiphysics.DISTANCE_GRADIENT, MetricParameters)
metric_process.Execute()

from gid_output_process import GiDOutputProcess
gid_output = GiDOutputProcess(main_model_part,
                            'metric_tensor',
                            KratosMultiphysics.Parameters("""
                                {
                                    "result_file_configuration" : {
                                        "gidpost_flags": {
                                            "GiDPostMode": "GiD_PostBinary",
                                            "WriteDeformedMeshFlag": "WriteUndeformed",
                                            "WriteConditionsFlag": "WriteConditions",
                                            "MultiFileFlag": "SingleFile"
                                        },
                                        "nodal_results" : ["DISTANCE"],
                                        "nodal_nonhistorical_results": ["METRIC_TENSOR_2D"],
                                        "elemental_conditional_flags_results": ["STRUCTURE"]

                                    }
                                }
                                """)
                            )

gid_output.ExecuteInitialize()
gid_output.ExecuteBeforeSolutionLoop()
gid_output.ExecuteInitializeSolutionStep()
gid_output.PrintOutput()
gid_output.ExecuteFinalizeSolutionStep()
gid_output.ExecuteFinalize()

##PERFORM REMESHING
mmg_parameters = KratosMultiphysics.Parameters("""
{
    "discretization_type"                  : "STANDARD",
    "initialize_entities"              : false,
    "echo_level"                       : 0
}
""")
mmg_process = KratosMultiphysics.MeshingApplication.MmgProcess2D(main_model_part, mmg_parameters)
mmg_process.Execute()

from gid_output_process import GiDOutputProcess
gid_output = GiDOutputProcess(main_model_part,
                            'remeshed',
                            KratosMultiphysics.Parameters("""
                                {
                                    "result_file_configuration" : {
                                        "gidpost_flags": {
                                            "GiDPostMode": "GiD_PostBinary",
                                            "WriteDeformedMeshFlag": "WriteUndeformed",
                                            "WriteConditionsFlag": "WriteConditions",
                                            "MultiFileFlag": "SingleFile"
                                        },
                                        "nodal_results" : ["DISTANCE"],
                                        "nodal_nonhistorical_results": ["METRIC_TENSOR_2D"]
                                    }
                                }
                                """)
                            )

gid_output.ExecuteInitialize()
gid_output.ExecuteBeforeSolutionLoop()
gid_output.ExecuteInitializeSolutionStep()
gid_output.PrintOutput()
gid_output.ExecuteFinalizeSolutionStep()
gid_output.ExecuteFinalize()

