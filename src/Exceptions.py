
# https://github.com/w-okada/voice-changer/blob/08d07c599718a1395ae6a4d1eda71de1f8defd88/server/Exceptions.py

class NoModeLoadedException(Exception):
    def __init__(self, framework):
        self.framework = framework

    def __str__(self):
        return repr(f"No model for {self.framework} loaded. Please confirm the model uploaded.")


class ONNXInputArgumentException(Exception):
    def __str__(self):
        return repr(f"ONNX received invalid argument.")

