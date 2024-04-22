from typing import Dict, Literal

ModeType = Literal["module", "chapter", "subchapter"]

MODE_MAPPING: Dict[ModeType, str] = {
    "module": "módulo",
    "chapter": "capítulo",
    "subchapter": "subseção",
}
