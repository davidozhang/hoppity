# -*- coding: utf-8 -*-


class Configuration():
    def __init__(self, *args, **kwargs):
        self.required = {}
        self.accepted = {}
        self.file_path = kwargs['path']
        self.result = {}

    def read(self):
        with open(self.file_path) as f:
            for line in f:
                if line.startswith('#') or not line.strip():
                    continue
                (key, value) = line.split(' = ')
                self.result[key] = value.replace('\n', '')
                if key in self.required:
                    self.required.remove(key)
                elif key not in self.accepted:
                    self.result = {}
                    return False
                elif key in self.accepted:
                    self.accepted.remove(key)
        return True if len(self.required) == 0 else False
