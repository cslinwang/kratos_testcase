import KratosMultiphysics as KM
import KratosMultiphysics.KratosUnittest as KratosUnittest


class TestVariableUtilsSetNotFlag(KratosUnittest.TestCase):
    def test_set_not_flag(self):
        model = KM.Model()
        model_part = model.CreateModelPart("model_part")
        node = model_part.CreateNewNode(1, 0.0, 0.0, 0.0)

        self.assertFalse(node.Is(KM.INTERFACE))
        self.assertTrue(node.Is(KM.NOT_INTERFACE))

        KM.VariableUtils().SetFlag(KM.INTERFACE, True, model_part.Nodes)
        self.assertTrue(node.Is(KM.INTERFACE))

        KM.VariableUtils().SetFlag(KM.NOT_INTERFACE, True, model_part.Nodes)
        self.assertTrue(node.Is(KM.NOT_INTERFACE))


if __name__ == '__main__':
    KratosUnittest.main()
