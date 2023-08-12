from __future__ import print_function, absolute_import, division #makes KratosMultiphysics backward compatible with python 2.6 and 2.7

import KratosMultiphysics
from KratosMultiphysics.StructuralMechanicsApplication.structural_mechanics_analysis import StructuralMechanicsAnalysis

"""
For user-scripting it is intended that a new class is derived
from StructuralMechanicsAnalysis to do modifications
"""

class StructuralMechanicsAnalysisMSConstraints(StructuralMechanicsAnalysis):

    def ModifyInitialGeometry(self):
        # pass
        model_part = self.model.GetModelPart("Structure")

        constraint_id = 100
        constant = 0.0

        # Trusses
        print("Setting master-slave constraints for trusses")
        
        master_nodes_sub_model_part_name = "GENERIC_Surface_Mid"
        slave_node_sub_model_part_name = "GENERIC_Point_Mid"
        
        master_nodes_sub_model_part = model_part.GetSubModelPart(master_nodes_sub_model_part_name)
        slave_node_sub_model_part = model_part.GetSubModelPart(slave_node_sub_model_part_name)
        
        master_nodes = master_nodes_sub_model_part.Nodes
        # slave_node = slave_node_sub_model_part.Nodes[0]

        weight = 1.0/float(len(master_nodes))
        for slave_node in slave_node_sub_model_part.Nodes:
            for master_node in master_nodes:
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_X, slave_node, KratosMultiphysics.DISPLACEMENT_X, weight, constant)
                constraint_id += 1
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_Y, slave_node, KratosMultiphysics.DISPLACEMENT_Y, weight, constant)
                constraint_id += 1
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_Z, slave_node, KratosMultiphysics.DISPLACEMENT_Z, weight, constant)
                constraint_id += 1

        # Top
        print("Setting master-slave constraints for top")
        master_nodes_sub_model_part_name = "GENERIC_Line_Top"
        slave_node_sub_model_part_name = "GENERIC_Point_Top"
        
        master_nodes_sub_model_part = model_part.GetSubModelPart(master_nodes_sub_model_part_name)
        slave_node_sub_model_part = model_part.GetSubModelPart(slave_node_sub_model_part_name)
        
        master_nodes = master_nodes_sub_model_part.Nodes
        # slave_node = slave_node_sub_model_part.Nodes[0]

        weight = 1.0/float(len(master_nodes))
        for slave_node in slave_node_sub_model_part.Nodes:
            for master_node in master_nodes:
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_X, slave_node, KratosMultiphysics.DISPLACEMENT_X, weight, constant)
                constraint_id += 1
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_Y, slave_node, KratosMultiphysics.DISPLACEMENT_Y, weight, constant)
                constraint_id += 1
                model_part.CreateNewMasterSlaveConstraint("LinearMasterSlaveConstraint", constraint_id, master_node, KratosMultiphysics.DISPLACEMENT_Z, slave_node, KratosMultiphysics.DISPLACEMENT_Z, weight, constant)
                constraint_id += 1

if __name__ == "__main__":

    with open("ProjectParameters.json",'r') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    model = KratosMultiphysics.Model()
    simulation = StructuralMechanicsAnalysisMSConstraints(model,parameters)
    simulation.Run()
