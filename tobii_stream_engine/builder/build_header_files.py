from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

import requests
import unmarkd  # type: ignore
from bs4 import BeautifulSoup, Tag


@dataclass
class NamedRange:
    name: str
    start_position: int
    end_position: int


@dataclass
class FileInformation:
    name: str
    description: str | None
    functions: list[FunctionInformation]


@dataclass
class FunctionInformation:
    name: str
    description: str | None
    syntax: str | None
    # remarks: str
    # return_value: str
    # see_also: str
    # example: str


def _tag_matches_id_pattern(tag: Tag, tag_name: str, id_pattern: str) -> bool:
    if tag.name != tag_name:
        return False

    if not tag.get("id"):
        return False

    if isinstance(tag["id"], list):
        return False

    pattern = re.compile(id_pattern)
    if not pattern.match(tag["id"]):
        return False

    return True


def tag_is_footer(tag: Tag) -> bool:
    if tag.name != "div":
        return False

    if not tag.get("class"):
        return False

    if "footer" not in tag["class"]:
        return False

    return True


def tag_is_section_header(tag: Tag, max_depth: int = 3) -> bool:
    tags = [f"h{d}" for d in range(1, max_depth + 1)]
    return tag.name in tags


def tag_is_file_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h1", "^tobii(|_.*)h$")


def tag_is_function_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h2", "^tobii_.*$")


def tag_is_function_description_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^function(|-[0-9]+)$")


def tag_is_function_syntax_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^syntax(|-[0-9]+)$")


def tag_is_function_remarks_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^remarks(|-[0-9]+)$")


def tag_is_function_return_value_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^return-value(|-[0-9]+)$")


def tag_is_function_see_also_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^see-also(|-[0-9]+)$")


def tag_is_function_example_header(tag: Tag) -> bool:
    return _tag_matches_id_pattern(tag, "h3", "^example(|-[0-9]+)$")


def collect_file_ranges(container: Tag) -> list[NamedRange]:
    file_ranges: list[NamedRange] = []

    current_name = None
    current_start_position = None

    for tag in container.children:
        if not isinstance(tag, Tag):
            continue

        if not (tag_is_file_header(tag) or tag_is_footer(tag)):
            continue

        current_position = tag.sourceline

        if current_name is not None:
            file_range = NamedRange(
                name=current_name,
                start_position=current_start_position,
                end_position=current_position - 1,
            )
            file_ranges.append(file_range)

        current_name = tag.text.strip()
        current_start_position = current_position

    return file_ranges


def collect_function_ranges(
    container: Tag,
    file_range: NamedRange,
) -> list[NamedRange]:
    function_ranges: list[NamedRange] = []

    in_section = False
    current_name = None
    current_start_position = None

    for tag in container.children:
        if not isinstance(tag, Tag):
            continue

        if tag.sourceline <= file_range.start_position:
            continue

        if in_section and (tag_is_section_header(tag, 2) or tag_is_footer(tag)):
            assert current_name is not None
            assert current_start_position is not None
            function_range = NamedRange(
                name=current_name,
                start_position=current_start_position,
                end_position=tag.sourceline - 1,
            )
            function_ranges.append(function_range)
            current_name = None
            current_start_position = None
            in_section = False

        if not in_section and tag_is_function_header(tag):
            in_section = True
            current_name = tag.text.strip()
            current_start_position = tag.sourceline
            continue

        if tag.sourceline > file_range.end_position:
            break

    return function_ranges


def _get_section(
    container: Tag,
    named_range: NamedRange,
    start_fn: Callable[[Tag], bool],
) -> list[Tag]:
    tags = []
    in_section = False
    for tag in container.children:
        if not isinstance(tag, Tag):
            continue

        if tag.sourceline <= named_range.start_position:
            continue

        if tag.sourceline > named_range.end_position:
            break

        if not in_section and start_fn(tag):
            in_section = True
            continue

        if in_section and tag_is_section_header(tag):
            break

        if in_section:
            tags.append(tag)

    return tags


def get_file_description(container: Tag, file_range: NamedRange) -> str | None:
    description = None
    for tag in container.children:
        if not isinstance(tag, Tag):
            continue

        if tag.sourceline <= file_range.start_position:
            continue

        if tag.sourceline > file_range.end_position:
            break

        if tag_is_section_header(tag, 2):
            break

        if description is None:
            description = ""

        description += str(tag)

    if description is not None:
        description = unmarkd.unmark(description)

    return description


def get_function_description(
    container: Tag,
    function_range: NamedRange,
) -> str | None:
    section = _get_section(
        container,
        function_range,
        tag_is_function_description_header,
    )
    description = "\n".join([str(t) for t in section])
    description = unmarkd.unmark(description)
    return description


def get_function_syntax(
    container: Tag,
    function_range: NamedRange,
) -> str | None:
    section = _get_section(
        container,
        function_range,
        tag_is_function_syntax_header,
    )
    tag = section[0]
    code = tag.find_next(name="code")
    if not isinstance(code, Tag):
        return None
    return code.text.strip()


def get_functions(
    container: Tag,
    function_ranges: list[NamedRange],
) -> list[FunctionInformation]:
    functions: list[FunctionInformation] = []

    for function_range in function_ranges:
        function_description = get_function_description(container, function_range)
        function_syntax = get_function_syntax(container, function_range)
        # function_remarks = get_function_remarks(container, function_range)
        # function_return_value = get_function_return_value(container, function_range)
        # function_see_also = get_function_see_also(container, function_range)
        # function_example = get_function_example(container, function_range)
        function = FunctionInformation(
            name=function_range.name,
            description=function_description,
            syntax=function_syntax,
        )
        functions.append(function)

    return functions


def parse_page(container: Tag) -> list[FileInformation]:
    files: list[FileInformation] = []

    file_ranges = collect_file_ranges(container)

    for file_range in file_ranges:
        file_description = get_file_description(container, file_range)
        function_ranges = collect_function_ranges(container, file_range)
        functions = get_functions(container, function_ranges)
        file_information = FileInformation(
            name=file_range.name,
            description=file_description,
            functions=functions,
        )
        files.append(file_information)

    return files


def fetch_page() -> str:
    url = "https://tobiitech.github.io/stream-engine-docs/"
    response = requests.get(url)
    if not response.ok:
        raise Exception("Failed to fetch documentation")
    return response.text


def generate_header_file(output_path: Path, file: FileInformation) -> None:
    content = ""
    for function in file.functions:
        syntax = function.syntax
        if syntax is None:
            continue
        # cleanup: remove include statement
        syntax = re.sub(r"^#include .*", "", syntax)
        # cleanup: remove TOBII_CALL
        syntax = re.sub(r"TOBII_CALL ", "", syntax)
        # cleanup: remove TOBII_API
        syntax = re.sub(r"TOBII_API ", "", syntax)
        content += syntax
        content += "\n"

    output_file = output_path / file.name
    output_file.write_text(content)


def generate_header_files(output_path: Path, files: list[FileInformation]) -> None:
    if not output_path.exists():
        output_path.mkdir()

    for file in files:
        generate_header_file(output_path, file)


def main() -> None:
    page = fetch_page()
    soup = BeautifulSoup(markup=page, features="html.parser")
    container = soup.body.div  # type: ignore
    files = parse_page(container)  # type: ignore
    generate_header_files(Path("./include"), files)


if __name__ == "__main__":
    main()

# TODO extract typedefs
# TODO extract documentation
# TODO generate typedefs
# TODO generate documentation
