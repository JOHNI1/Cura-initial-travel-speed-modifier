from ..Script import Script
import re

class AlterInitialTravelSpeed(Script):
    def __init__(self):
        super().__init__()

    def getSettingDataString(self):
        return """{
            "name": "Alter Initial Travel Speed",
            "key": "AlterInitialTravelSpeed",
            "metadata": {},
            "version": 2,
            "settings": {
                "new_speed": {
                    "label": "New Speed",
                    "description": "Enter speed for the initial travel",
                    "type": "int",
                    "enabled": true,
                    "unit": "mm/min",
                    "default_value": 6000
                }
            }
        }"""

    def execute(self, data):
        new_speed = self.getSettingValueByKey("new_speed")  # Get the value of the "new_speed" setting.
        modified_travel_speed = False  # Initialize a variable for tracking whether the speed has been modified.

        for index_num in range(len(data)):  # Loop through data layers.
            layer = data[index_num]  # Store the current layer.
            lines = layer.split("\n")  # Split the layer into individual lines.

            for line_num in range(len(lines)):  # Loop through lines in the current layer.
                if lines[line_num].startswith("G0 "):  # Check if the line starts with "G0".
                    if not modified_travel_speed:
                        pattern = r'F\w+'  # Define a regular expression pattern to match "G0" and following characters.
                        tempStr = lines[line_num]
                        lines[line_num] = re.sub(pattern, "F" + str(new_speed), tempStr)  # Replace the matched pattern.
                        modified_travel_speed = True  # Mark that the speed has been modified.

            data[index_num] = "\n".join(lines)  # Join modified lines to update the current layer.

        return data  # Return the modified data.