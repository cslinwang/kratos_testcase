
import KratosMultiphysics
import KratosMultiphysics.FluidDynamicsApplication
import KratosMultiphysics.MeshingApplication as KratosMeshing
from KratosMultiphysics.gid_output_process import GiDOutputProcess


def CreateGidControlOutput(output_name, model_part):
    gid_output = GiDOutputProcess(
        model_part,
        output_name,
        KratosMultiphysics.Parameters("""
                {
                    "result_file_configuration" : {
                        "gidpost_flags": {
                            "GiDPostMode": "GiD_PostBinary",
                            "MultiFileFlag": "SingleFile"
                        },
                        "nodal_results"       : [],
                        "nodal_nonhistorical_results": ["NODAL_H","METRIC_SCALAR"],
                        "nodal_flags_results": []
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


model = KratosMultiphysics.Model()
main_model_part = model.CreateModelPart("main")
KratosMultiphysics.ModelPartIO(
    "/root/kratos_testcase/7209/RectangularCylinder2D_1k").ReadModelPart(main_model_part)
main_model_part.ProcessInfo.SetValue(KratosMultiphysics.DOMAIN_SIZE, 2)

find_nodal_h = KratosMultiphysics.FindNodalHNonHistoricalProcess(main_model_part)
find_nodal_h.Execute()

for node in main_model_part.Nodes:
    nodal_h = node.GetValue(KratosMultiphysics.NODAL_H)
    node.SetValue(KratosMeshing.METRIC_SCALAR, nodal_h/2)

CreateGidControlOutput("preremesh", main_model_part)

# Call MMG
if hasattr(KratosMeshing, "MmgProcess2D"):
    print('111111111')

# 获取模块的所有属性名
module_attributes = dir(KratosMeshing)

# 打印属性名
for attribute in module_attributes:
    print(attribute)
remesh_parameters = KratosMultiphysics.Parameters()
MmgProcess = KratosMeshing.MmgProcess2D(main_model_part, remesh_parameters)
MmgProcess.Execute()

find_nodal_h = KratosMultiphysics.FindNodalHNonHistoricalProcess(main_model_part)
find_nodal_h.Execute()

CreateGidControlOutput("remeshed_hessian", main_model_part)
