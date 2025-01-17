import os
import sys

import pytest

import mlflow.utils.logging_utils as logging_utils
from mlflow.utils.autologging_utils import _is_testing, _AUTOLOGGING_TEST_MODE_ENV_VAR


PATCH_DESTINATION_FN_DEFAULT_RESULT = "original_result"


@pytest.fixture
def patch_destination():
    class PatchObj:
        def __init__(self):
            self.fn_call_count = 0

        def fn(self, *args, **kwargs):  # pylint: disable=unused-argument
            self.fn_call_count += 1
            return PATCH_DESTINATION_FN_DEFAULT_RESULT

    return PatchObj()


@pytest.fixture
def test_mode_off():
    try:
        prev_env_var_value = os.environ.pop(_AUTOLOGGING_TEST_MODE_ENV_VAR, None)
        os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR] = "false"
        assert not _is_testing()
        yield
    finally:
        if prev_env_var_value:
            os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR] = prev_env_var_value
        else:
            del os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR]


@pytest.fixture
def test_mode_on():
    try:
        prev_env_var_value = os.environ.pop(_AUTOLOGGING_TEST_MODE_ENV_VAR, None)
        os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR] = "true"
        assert _is_testing()
        yield
    finally:
        if prev_env_var_value:
            os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR] = prev_env_var_value
        else:
            del os.environ[_AUTOLOGGING_TEST_MODE_ENV_VAR]


@pytest.fixture(autouse=True)
def reset_stderr():
    prev_stderr = sys.stderr
    yield
    sys.stderr = prev_stderr


@pytest.fixture(autouse=True)
def reset_logging_enablement():
    yield
    logging_utils.enable_logging()
