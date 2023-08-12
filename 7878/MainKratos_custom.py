# makes KratosMultiphysics backward compatible with python 2.6 and 2.7
from __future__ import print_function, absolute_import, division

import KratosMultiphysics
from KratosMultiphysics.FluidDynamicsApplication.fluid_dynamics_analysis import FluidDynamicsAnalysis

import sys
import time
import math


class FluidDynamicsAnalysisWithFlush(FluidDynamicsAnalysis):

    def __init__(self, model, project_parameters, flush_frequency=10.0):
        super(FluidDynamicsAnalysisWithFlush, self).__init__(model, project_parameters)
        self.flush_frequency = flush_frequency
        self.last_flush = time.time()

    def FinalizeSolutionStep(self):
        super(FluidDynamicsAnalysisWithFlush, self).FinalizeSolutionStep()

        if self.parallel_type == "OpenMP":
            now = time.time()
            if now - self.last_flush > self.flush_frequency:
                sys.stdout.flush()
                self.last_flush = now

    def ModifyInitialGeometry(self):
        super(FluidDynamicsAnalysisWithFlush, self).ModifyInitialGeometry()

        # Read the geometry
        sail_model_part = self.model.CreateModelPart('SailModelPart')
        sail_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.VELOCITY)
        sail_model_part.AddNodalSolutionStepVariable(KratosMultiphysics.DISPLACEMENT)
        KratosMultiphysics.ModelPartIO('collie2002_sailLine', KratosMultiphysics.ModelPartIO.READ |
                                       KratosMultiphysics.ModelPartIO.SKIP_TIMER).ReadModelPart(sail_model_part)

    def ModifyAfterSolverInitialize(self):
        super(FluidDynamicsAnalysisWithFlush, self).ModifyAfterSolverInitialize()

        # calculate level set functions
        sail_model_part = self.model.GetModelPart('SailModelPart')
        KratosMultiphysics.CalculateDiscontinuousDistanceToSkinProcess2D(
            self._GetSolver().GetComputingModelPart(), sail_model_part).Execute()


if __name__ == "__main__":

    with open("/root/kratos_testcase/7878/ProjectParameters_custom.json", 'r', encoding='utf-8') as parameter_file:
        parameters = KratosMultiphysics.Parameters(parameter_file.read())

    model = KratosMultiphysics.Model()
    simulation = FluidDynamicsAnalysisWithFlush(model, parameters)
    simulation.Run()
