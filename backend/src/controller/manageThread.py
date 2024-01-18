from backend.src.interpreter import interpreter
from backend.src.controller import controller
from backend.src.utils import utils


class ManageThread:
    """Class to manage threads for interpreting steps."""

    def __init__(self, current_step, flag):
        self.interpreter_instance = None
        self.thread = None
        self.init_interpreter_thread(current_step, flag)

    def init_interpreter_thread(self, current_step, flag):
        """Initializes the interpreter thread for the current step.
        Args:
            current_step (object): The current step object.
        """
        thread = utils.BaseThread(
            name="StepJob",
            target=lambda: (interpreter.detection_loop(current_step)),
            callback=self.end_thread,
            callback_args=(current_step,),
            flag=flag,
        )
        thread.start()

    def end_thread(self, current_step):
        controller.CONTROLLER_INSTANCE.progress_next_step()
