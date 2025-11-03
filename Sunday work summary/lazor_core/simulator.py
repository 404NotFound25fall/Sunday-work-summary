# lazor_core/simulator.py
"""Stage 3: Laser Physics Engine

This module implements the laser simulation engine for Lazor.
It handles laser path tracing with proper collision detection and interaction.
"""
from __future__ import annotations
from typing import Set, Tuple, List, Optional
from .models import Laser, Block, BlockType
from .board import Board


def get_block_at_position(board: Board, row: int, col: int) -> Block | None:
    """
    获取棋盘上指定位置的方块。
    
    参数:
        board: 棋盘对象
        row, col: 方块的网格坐标 (不是 half-block 坐标)
    
    返回:
        如果位置有方块返回 Block 对象，否则返回 None
    """
    if board.in_bounds(row, col):
        return board.fixed_blocks.get((row, col))
    return None


def _block_ch_at(board: Board, r: int, c: int) -> Optional[str]:
    if not board.in_bounds(r, c):
        return None
    # 1) 动态放置的块：grid 中的小写 a/b/c
    try:
        gch = board.grid[r][c]
        if isinstance(gch, str) and gch.lower() in ("a", "b", "c"):
            return gch.lower()
    except Exception:
        pass
    # 2) 固定块：fixed_blocks 字典
    blk = board.fixed_blocks.get((r, c))
    if blk:
        if blk.kind is BlockType.REFLECT:
            return 'a'
        if blk.kind is BlockType.OPAQUE:
            return 'b'
        if blk.kind is BlockType.REFRACT:
            return 'c'
    return None


def _reflect_by_boundary(vx: int, vy: int, boundary: str) -> Tuple[int, int]:
    # boundary in {"vertical", "horizontal"}
    if boundary == "vertical":
        return (-vx, vy)
    return (vx, -vy)


def _interact(block_ch: str, vx: int, vy: int, boundary: str) -> List[Tuple[int, int]]:
    # a=reflect, b=opaque, c=refract
    if block_ch == 'b':
        return []
    if block_ch == 'a':
        return [_reflect_by_boundary(vx, vy, boundary)]
    if block_ch == 'c':
        return [(vx, vy), _reflect_by_boundary(vx, vy, boundary)]
    return [(vx, vy)]


def _block_across_vertical_edge(board: Board, mx: int, y: int, vy: int) -> Optional[str]:
    # mx is odd if crossing vertical edge between column (mx-1)//2 and (mx+1)//2
    if mx % 2 != 1:
        return None
    c = (mx - 1) // 2
    up_r = (y - 1) // 2
    down_r = (y + 1) // 2
    # prioritize according to movement vertical direction when available
    candidates = []
    if vy > 0:
        candidates = [(down_r, c), (up_r, c)]
    elif vy < 0:
        candidates = [(up_r, c), (down_r, c)]
    else:
        candidates = [(up_r, c), (down_r, c)]
    for r, cc in candidates:
        ch = _block_ch_at(board, r, cc)
        if ch:
            return ch
    return None


def _block_across_horizontal_edge(board: Board, x: int, my: int, vx: int) -> Optional[str]:
    if my % 2 != 1:
        return None
    r = (my - 1) // 2
    left_c = (x - 1) // 2
    right_c = (x + 1) // 2
    candidates = []
    if vx > 0:
        candidates = [(r, right_c), (r, left_c)]
    elif vx < 0:
        candidates = [(r, left_c), (r, right_c)]
    else:
        candidates = [(r, left_c), (r, right_c)]
    for rr, cc in candidates:
        ch = _block_ch_at(board, rr, cc)
        if ch:
            return ch
    return None


def _step_and_collide(board: Board, x: int, y: int, vx: int, vy: int) -> Tuple[int, int, List[Tuple[int, int]]]:
    nx, ny = x + vx, y + vy
    mx = (x + nx) // 2
    my = (y + ny) // 2
    interactions: List[Tuple[str, str]] = []  # (boundary, block_ch)

    # diagonal first: check vertical then horizontal in fixed order
    if vx != 0 and vy != 0:
        blk_v = _block_across_vertical_edge(board, mx, y, vy)
        if blk_v:
            interactions.append(("vertical", blk_v))
        blk_h = _block_across_horizontal_edge(board, x, my, vx)
        if blk_h:
            interactions.append(("horizontal", blk_h))
    elif vx != 0:
        blk_v = _block_across_vertical_edge(board, mx, y, vy)
        if blk_v:
            interactions.append(("vertical", blk_v))
    elif vy != 0:
        blk_h = _block_across_horizontal_edge(board, x, my, vx)
        if blk_h:
            interactions.append(("horizontal", blk_h))

    # apply interactions sequentially, could branch (for refract)
    beams: List[Tuple[int, int]] = [(vx, vy)]
    for boundary, block_ch in interactions:
        next_beams: List[Tuple[int, int]] = []
        for bvx, bvy in beams:
            next_beams.extend(_interact(block_ch, bvx, bvy, boundary))
        beams = next_beams
        if not beams:
            break

    return nx, ny, beams


def simulate_board(board: Board) -> Set[Tuple[int, int]]:
    """
    模拟所有激光在棋盘上的路径，返回被击中的点集合。
    
    这是 Stage 3 的核心函数，实现完整的激光物理引擎。
    
    简化实现：将 half-block 坐标视为网格坐标进行模拟。
    
    参数:
        board: 完整的棋盘配置（包含所有已放置的方块）
    
    返回:
        被激光击中的所有目标点的集合 (half-block 坐标)
    """
    hit_points: Set[Tuple[int, int]] = set()
    
    # 使用队列模拟所有活动激光
    from collections import deque
    active_lasers = deque(board.lasers)
    
    # 用于检测循环（防止无限递归）
    visited_states: Set[Tuple[int, int, int, int]] = set()
    
    max_iterations = 5000  # 防止无限循环的安全阀（含分束更稳）
    
    iteration = 0
    while active_lasers and iteration < max_iterations:
        iteration += 1
        laser = active_lasers.popleft()
        
        # 注意：我们不在起点记录 hit_points，因为起点可能不是目标点
        # 记录当前点（但跳过初始激光的起点）
        if iteration > len(board.lasers) or (laser.x, laser.y) != (board.lasers[0].x, board.lasers[0].y):
            hit_points.add((laser.x, laser.y))
        
        # 推进一步并在半步中点判定碰撞（边界）
        new_x, new_y, out_dirs = _step_and_collide(board, laser.x, laser.y, laser.vx, laser.vy)

        # 记录新位置为命中点
        hit_points.add((new_x, new_y))

        # 边界检查（基于棋盘大小的宽松范围）
        if new_y < -10 or new_y > board.nrows * 2 + 10 or new_x < -10 or new_x > board.ncols * 2 + 10:
            continue

        # 分支后的光束入队
        for vx, vy in out_dirs:
            state_key = (new_x, new_y, vx, vy)
            if state_key in visited_states:
                continue
            visited_states.add(state_key)
            active_lasers.append(Laser(x=new_x, y=new_y, vx=vx, vy=vy))
    
    if iteration >= max_iterations:
        print(f"警告: 模拟达到最大迭代次数 ({max_iterations})")
    
    return hit_points

