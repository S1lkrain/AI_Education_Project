def build_prompt(template: str, **kwargs: object) -> str:
    """Fill a prompt template with user-provided values."""
    normalized_values = {key: str(value).strip() for key, value in kwargs.items()}
    return template.format(**normalized_values)
