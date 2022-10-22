"""
Basic layout to control the server execution
and output the stdout to the user in case
it's needed
"""

from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *
import re


class PydeskaSt(QMainWindow):
    """Main window class"""

    def __init__(self):
        super().__init__(mw)
        # Set the basic window properties
        self.setWindowTitle("Pydeska")
        self.setGeometry(100, 100, 500, 400)
        # Set the process to be None
        self.st_process = None
        # Create basic widgets
        self.start_btn = QPushButton("Start Pydeska Server")
        self.start_btn.pressed.connect(self.start_pydeska_st)
        self.stop_btn = QPushButton("Stop Pydeska Server")
        self.stop_btn.pressed.connect(self.stop_st_server)
        self.output = QPlainTextEdit()
        self.output.setReadOnly(True)
        # Create layout(s)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        global_layout = QVBoxLayout()
        global_layout.addLayout(btn_layout)
        global_layout.addWidget(self.output)
        # Add layouts to the main window
        central_widget = QWidget()
        central_widget.setLayout(global_layout)
        self.setCentralWidget(central_widget)

    def write_output(self, message):
        """Helper function that adds the message to the output widget"""
        self.output.appendPlainText(message)

    def start_pydeska_st(self):
        """Function that starts the st server"""
        # Check if there is a process already running
        if self.st_process is None:
            # Notify that a process is starting
            self.write_output("Starting local pydeska server...")
            # Locate the entry file to execute
            st_home_file_name = mw.addonManager.addonsFolder() + "/pydeska/home.py"
            # Create the process handler
            self.st_process = QProcess()
            # Connect the handler to the output function
            self.st_process.readyReadStandardOutput.connect(self.handle_output)
            # Connect the handler to the cleanup function
            self.st_process.finished.connect(self.process_finished)
            # Start the server
            self.st_process.start("streamlit", ["run", st_home_file_name])

    def handle_output(self):
        """Function that handles the output"""
        # Get and convert the data
        data = self.st_process.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        # Add a customised welcome message if needed
        stdout += self.custom_welcome_message(stdout)
        # Write the stdout
        self.write_output(stdout)

    def process_finished(self):
        """Function that handles the process when it's finished"""
        self.write_output("Server shut down.")
        self.st_process = None

    def stop_st_server(self):
        """Function that terminates the process"""
        self.st_process.terminate()

    def custom_welcome_message(self, stdout):
        """Function that generates and prints a custom welcome message"""
        last_url = re.findall(r"Local URL: (.+)", stdout)
        if len(last_url):
            return f"""
            
            ヽ(•‿•)ノ Welcome to Pydeska!
            The server should start the default browser
            and open the addon right away. Please wait for
            few seconds. If nothing happens, please open
            the following link in your default browser.
            ↣ {last_url[0]}
            Enjoy!
            """
        return ""


def show_pydeska_st_window():
    """Function that shows the main window"""
    pydeska_st_main_window = PydeskaSt()
    pydeska_st_main_window.show()


# Create an action item
pydeska_st_action = QAction("Pydeska", mw)
# Attach the menu item to the appropriate function
qconnect(pydeska_st_action.triggered, show_pydeska_st_window)
# Create a menu item
mw.form.menuTools.addAction(pydeska_st_action)
