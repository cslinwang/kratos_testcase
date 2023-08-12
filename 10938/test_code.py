import KratosMultiphysics as Kratos
from KratosMultiphysics.testing.utilities import ReadModelPart
model = Kratos.Model()
model_part = model.CreateModelPart("test")
import_settings = Kratos.Parameters("""{
            "model_import_settings": {
                "input_type": "mdpa",
                "input_filename": \"quads\",
                "partition_in_memory" : false
            },
            "echo_level" : 0
}""")
ReadModelPart("model_part_utils_test/quads", model_part, settings=Kratos.Parameters(import_settings))
