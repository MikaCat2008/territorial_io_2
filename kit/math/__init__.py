def clamp(value: float, min_value: float, max_value: float) -> float:
    if value > max_value:
        return max_value
    
    if value < min_value:
        return min_value
    
    return value
