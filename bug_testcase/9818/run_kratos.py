import errno
import numpy as np
from datetime import datetime
import KratosMultiphysics
import KratosMultiphysics.StructuralMechanicsApplication as StructuralMechanics

from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import StructuralMechanicsAnalysis

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Time at Start =", current_time)

class StructuralMechanicsAnalysisWithEigenPostProcessing(StructuralMechanicsAnalysis):
    """This class prints information abt the computen Eigenvectors
    It also shows how the "StructuralMechanicsAnalysis" can be customized by deriving from it
    """
    def Finalize(self):
        super().Finalize()
        main_model_part_name = self.project_parameters["solver_settings"]["model_part_name"].GetString()
        main_model_part = self.model[main_model_part_name]
        # Postprocessing the output in the terminal:
        # print("Computed Eigenvalues:\n", main_model_part.ProcessInfo[StructuralMechanics.EIGENVALUE_VECTOR])
        # print("Computed Eigenvectors on Node 1:\n", main_model_part.GetNode(1).GetValue(StructuralMechanics.EIGENVECTOR_MATRIX)) # for node with id 1
        # to get the output on every node (A lot!):
        # for node in main_model_part.Nodes:
        #     print(node.GetValue(StructuralMechanics.EIGENVECTOR_MATRIX))
        #     print('')

        # print("Computed Eigenfrequencies:\n", np.around(np.sqrt(main_model_part.ProcessInfo[StructuralMechanics.EIGENVALUE_VECTOR])/2/np.pi,3))
        print('--- Eigenfrequencies')
        for eval in main_model_part.ProcessInfo[StructuralMechanics.EIGENVALUE_VECTOR]:
            efreq = np.round(np.sqrt(eval)/2/np.pi,3)
            print(efreq)
        print('---')

if __name__ == "__main__":

    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    model = KratosMultiphysics.Model()
    simulation = StructuralMechanicsAnalysisWithEigenPostProcessing(model,parameters)
    simulation.Run()

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print("Time at End =", current_time)

    # main_model_part_name = parameters["solver_settings"]["model_part_name"].GetString()
    # main_model_part = model[main_model_part_name]
    # for eval in main_model_part.ProcessInfo[StructuralMechanics.EIGENVALUE_VECTOR]:
    #     efreq = np.round(np.sqrt(eval)/2/np.pi,3)
    #     print(efreq)
    # print('---')

    # print(KratosMultiphysics.SpecificationsUtilities.GetDofsListFromSpecifications(model.GetModelPart('Structure')))