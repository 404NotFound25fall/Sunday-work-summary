from .parser import parse_bff, Board
from .solver import solve_optimized, get_placeable_positions, get_blocks_to_place

def solve(*args, **kwargs):
    return solve_optimized(*args, **kwargs)

__all__ = [
    "parse_bff",
    "Board",
    "solve",
    "solve_optimized",
    "get_placeable_positions",
    "get_blocks_to_place",
]
