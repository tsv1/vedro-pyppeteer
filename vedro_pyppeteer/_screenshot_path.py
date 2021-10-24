from pathlib import Path
from typing import Union

__all__ = ("ScreenshotPath",)


class ScreenshotPath:
    def __init__(self, dir_: Path) -> None:
        self.dir = dir_
        self.rerun: Union[int, None] = None
        self.timestamp: Union[int, None] = None
        self.scenario_path: Union[Path, None] = None
        self.scenario_subject: Union[str, None] = None
        self.step_name: Union[str, None] = None
        self.tab_index: Union[int, None] = None

    def resolve(self) -> Path:
        dir_path = self.dir
        if self.scenario_path is not None:
            cwd = Path().resolve()
            rel_path = self.scenario_path.relative_to(cwd)
            dir_path = self.dir.joinpath(rel_path.with_suffix(""))

        file_path = "screenshot"
        if self.scenario_subject is not None:
            file_path = self.scenario_subject

        if self.rerun is not None:
            file_path = f"[{self.rerun}]{file_path}"

        if self.timestamp is not None:
            file_path += f"__{self.timestamp}"

        if self.step_name is not None:
            file_path += f"__{self.step_name}"

        if self.tab_index is not None:
            file_path = f"tab{self.tab_index}__{file_path}"

        return dir_path / (file_path + ".png")

    def __repr__(self) -> str:
        path = self.resolve()
        return f"{self.__class__.__name__}<{path}>"
