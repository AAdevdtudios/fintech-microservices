def convert_to_seconds(days: int = 0, hours: int = 0, minutes: int = 0, seconds: int = 0):
    """
        # Convert time information to seconds.

        - Args:
            - `days` (`int`): Number of days. `Default: 0`.
            - `hours` (`int`): Number of hours. `Default: 0`.
            - `minutes` (`int`): Number of minutes. `Default: 0`.
            - `seconds` (`int`): Number of seconds. `Default: 0`.

        - Returns:
            - int: Total seconds for the specified time.

        Example:
        ```
        >>> convert_to_seconds(days=2, hours=12, minutes=30, seconds=15)
        210015
        >>> convert_to_seconds(hours=1, minutes=30)
        5400
        >>> convert_to_seconds(minutes=30)
        1800
        >>> convert_to_seconds(minutes=30, seconds=10)
        1810
        >>> convert_to_seconds(minutes=30, seconds=155550)
        157350
        >>> convert_to_seconds(days=365)
        31536000
        >>> 

        ```
    """
    total_seconds = days * 24 * 60 * 60  # Convert days to seconds
    total_seconds += hours * 60 * 60  # Convert hours to seconds
    total_seconds += minutes * 60  # Convert minutes to seconds
    total_seconds += seconds  # Seconds to seconds
    return int(total_seconds)

