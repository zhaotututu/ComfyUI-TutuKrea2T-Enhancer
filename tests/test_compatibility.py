import importlib.util
import inspect
from pathlib import Path
import sys
import types
import unittest


def _load_node_module():
    patcher_extension = types.ModuleType("comfy.patcher_extension")

    class WrappersMP:
        DIFFUSION_MODEL = "diffusion_model"

    patcher_extension.WrappersMP = WrappersMP
    comfy = types.ModuleType("comfy")
    comfy.patcher_extension = patcher_extension
    sys.modules["comfy"] = comfy
    sys.modules["comfy.patcher_extension"] = patcher_extension

    module_path = Path(__file__).resolve().parents[1] / "__init__.py"
    spec = importlib.util.spec_from_file_location("tutu_krea2t_enhancer", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


NODE = _load_node_module()


class RecordingExecutor:
    def __init__(self, class_obj=None):
        self.class_obj = class_obj if class_obj is not None else object()
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append((args, kwargs))
        return "executor-result"


class FakeModel:
    def __init__(self):
        self.model_options = {}
        self.added = []
        self.removed = []

    def clone(self):
        return FakeModel()

    def remove_wrappers_with_key(self, wrapper_type, key):
        self.removed.append((wrapper_type, key))

    def add_wrapper_with_key(self, wrapper_type, key, wrapper):
        self.added.append((wrapper_type, key, wrapper))


class FakeTxtFusion:
    def forward(self, *args, **kwargs):
        return args, kwargs


class FakeKreaModel:
    def __init__(self):
        self.txtfusion = FakeTxtFusion()
        self.txtmlp = object()
        self.blocks = object()
        self._unpack_context = lambda value: value
        self.txtlayers = len(NODE.KREA2_TAP_LAYERS)
        self.txtdim = NODE.KREA2_TAP_DIM


class CompatibilityTests(unittest.TestCase):
    def assert_passthrough(self, args):
        executor = RecordingExecutor()
        result = NODE.tutu_krea2t_enhancer_wrapper(executor, *args)
        self.assertEqual(result, "executor-result")
        self.assertEqual(len(executor.calls), 1)
        recorded_args, recorded_kwargs = executor.calls[0]
        self.assertEqual(recorded_kwargs, {})
        self.assertEqual(len(recorded_args), len(args))
        for actual, expected in zip(recorded_args, args):
            self.assertIs(actual, expected)

    def test_wrapper_signature_accepts_future_positional_arguments(self):
        parameters = list(inspect.signature(NODE.tutu_krea2t_enhancer_wrapper).parameters.values())
        self.assertEqual(parameters[1].kind, inspect.Parameter.VAR_POSITIONAL)
        self.assertEqual(parameters[2].kind, inspect.Parameter.VAR_KEYWORD)

    def test_old_comfyui_five_model_arguments_are_preserved(self):
        transformer_options = {NODE.CONFIG_KEY: {"enabled": False}}
        args = (object(), object(), object(), object(), transformer_options)
        self.assert_passthrough(args)

    def test_new_comfyui_ref_latents_argument_is_preserved(self):
        transformer_options = {NODE.CONFIG_KEY: {"enabled": False}}
        ref_latents = object()
        args = (object(), object(), object(), object(), ref_latents, transformer_options)
        self.assert_passthrough(args)

    def test_enabled_non_krea_model_preserves_new_call_shape(self):
        transformer_options = {NODE.CONFIG_KEY: {"enabled": True, "strength": 1.0}}
        args = (object(), object(), object(), object(), object(), transformer_options)
        self.assert_passthrough(args)

    def test_enabled_krea_wrapper_accepts_new_call_shape_and_restores_forward(self):
        krea_model = FakeKreaModel()
        original_forward = krea_model.txtfusion.forward
        executor = RecordingExecutor(krea_model)
        transformer_options = {NODE.CONFIG_KEY: {"enabled": True, "strength": 1.0}}
        args = (object(), object(), object(), object(), object(), transformer_options)

        result = NODE.tutu_krea2t_enhancer_wrapper(executor, *args)

        self.assertEqual(result, "executor-result")
        self.assertEqual(len(executor.calls[0][0]), 6)
        self.assertEqual(krea_model.txtfusion.forward, original_forward)
        self.assertFalse(transformer_options[NODE.CONFIG_KEY]["_active"])

    def test_keyword_transformer_options_are_detected(self):
        transformer_options = {NODE.CONFIG_KEY: {"enabled": False}}
        executor = RecordingExecutor()
        result = NODE.tutu_krea2t_enhancer_wrapper(
            executor,
            object(),
            object(),
            object(),
            transformer_options=transformer_options,
        )
        self.assertEqual(result, "executor-result")
        self.assertIs(executor.calls[0][1]["transformer_options"], transformer_options)

    def test_node_uses_independent_mapping_and_wrapper_keys(self):
        self.assertEqual(set(NODE.NODE_CLASS_MAPPINGS), {"TutuKrea2TEnhancer"})
        self.assertNotEqual(NODE.WRAPPER_KEY, "krea2t_prompt_adherence_enhancer")
        self.assertNotEqual(NODE.CONFIG_KEY, "krea2t_prompt_adherence_enhancer")

        (patched,) = NODE.TutuKrea2TEnhancer().apply(FakeModel(), enabled=True, strength=1.25)
        config = patched.model_options["transformer_options"][NODE.CONFIG_KEY]
        self.assertEqual(config["strength"], 1.25)
        self.assertTrue(config["enabled"])
        self.assertEqual(patched.added[0][1], NODE.WRAPPER_KEY)
        self.assertIs(patched.added[0][2], NODE.tutu_krea2t_enhancer_wrapper)


if __name__ == "__main__":
    unittest.main()
