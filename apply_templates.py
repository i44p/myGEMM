from pathlib import Path
from string import Template


class FileTemplate:
    def __init__(self, template_path, orig_path, mapping):
        self.template_path = Path(template_path)
        self.orig_path = Path(orig_path)
        self.mapping = mapping

    def replace(self):
        with open(self.template_path, 'r') as template:
            self.template = Template(template.read())

        with open(self.orig_path, 'w') as orig:
            orig.write(self.template.substitute(self.mapping))


defaults = [
    FileTemplate("templates/settings.h", "src/settings.h", {
        "SELECTED_KERNEL": "8",
        "WORK_GROUP_SIZE": "32",
        "CL_COMPILER_OPTIONS": '-cl-std=CL2.0',
    })
]


if __name__ == "__main__":
    for template in defaults:
        template.replace()
