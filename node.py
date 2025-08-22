# AutoPromptSchedule Node for ComfyUI
# Copyright (C) 2025 Your Name
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

class AutoPromptSchedule:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "tooltip": "Enter the text lines here. Each line will generate a separate image."
                    }
                ),
                "file_path": (
                    "STRING",
                    {
                        "default": "",
                        "tooltip": "Optional: path to a text file to load lines from. Overrides the 'text' field if provided."
                    }
                ),
                "multiplier": (
                    "FLOAT",
                    {
                        "default": 1.0,
                        "min": 1.0,
                        "tooltip": "Multiplier for spacing between keyframes."
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING", "STRING")  # both outputs as STRING
    RETURN_NAMES = ("schedule_text", "info_text")
    FUNCTION = "generate_schedule"
    CATEGORY = "Text"

    def generate_schedule(self, text, file_path, multiplier):
        # Ensure multiplier is valid
        try:
            multiplier = float(multiplier)
        except (ValueError, TypeError):
            multiplier = 1.0
        if multiplier < 1.0:
            multiplier = 1.0

        # Read lines from file or multiline text
        lines = []
        if file_path.strip():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f if l.strip()]
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = [l.strip() for l in f if l.strip()]
        else:
            lines = [l.strip() for l in text.splitlines() if l.strip()]

        # Create schedule string with keyframes
        schedule_lines = []
        for i, line in enumerate(lines):
            keyframe = 0 if i == 0 else int(i * multiplier)  # Keyframe calculation
            schedule_lines.append(f'"{keyframe}":"{line}",')  # Append line to schedule

        schedule_text = "\n".join(schedule_lines)

        # Info text: number of runs = number_of_lines * multiplier
        number_of_lines = len(lines)                        # Count the number of lines
        number_of_runs = int(number_of_lines * multiplier)  # Calculate number of runs
        info_text = f"Number of lines: {number_of_lines}\nNumber of runs: {number_of_runs}"

        return (schedule_text, info_text)
