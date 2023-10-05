from typing import Union


class Messages:
    @staticmethod
    def requesting_data(
        request_type: str, target_title: str, target: Union[str, tuple]
    ) -> str:
        return f"Requesting [green][italic]{request_type}[/][/] data for {target_title}: {target}..."

    @staticmethod
    def loaded_addresses(filename: str) -> str:
        return f"Loaded IP Addresses from file: [green][link file://{filename}]{filename}[/]"

    @staticmethod
    def opening_map(map_name: str) -> str:
        return f"Opening generated map: [link file://{map_name}]{map_name}..."

    @staticmethod
    def an_error_occurred(error: str) -> str:
        return f"An error occurred: [red]{error}[/]"
