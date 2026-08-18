#!/usr/bin/env python3
"""检查 draw.io XML 的可预测几何问题；返回非零表示存在阻断项。"""

import argparse
import base64
import html
import math
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from pathlib import Path


EPSILON = 0.01


@dataclass(frozen=True)
class Box:
    """保存根坐标 bbox，供线段和净空检查共享同一坐标系。"""

    x: float
    y: float
    width: float
    height: float

    @property
    def right(self):
        return self.x + self.width

    @property
    def bottom(self):
        return self.y + self.height


def number(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def parse_model(diagram):
    """读取未压缩模型；压缩页面先解码以避免静默漏检。"""
    model = diagram.find("mxGraphModel")
    if model is not None:
        return model
    encoded = (diagram.text or "").strip()
    if not encoded:
        raise ValueError("页面没有 mxGraphModel 或压缩内容")
    try:
        xml = zlib.decompress(base64.b64decode(encoded), -15).decode("utf-8")
        return ET.fromstring(urllib.parse.unquote(xml))
    except Exception as error:
        raise ValueError(f"无法解码压缩页面: {error}") from error


def style_has(style, key, value=None):
    pairs = dict(item.split("=", 1) for item in style.split(";") if "=" in item)
    return key in pairs and (value is None or pairs[key] == value)


def is_container(cell, child_parents):
    style = cell.get("style", "")
    return cell.get("id") in child_parents or style_has(style, "dashed", "1")


def line_intersects_box(a, b, box):
    """判断水平/垂直段是否穿入 bbox 内部；端点贴边不算穿越。"""
    ax, ay = a
    bx, by = b
    if abs(ax - bx) < EPSILON:
        if box.x + EPSILON < ax < box.right - EPSILON:
            low, high = sorted((ay, by))
            return low < box.bottom - EPSILON and high > box.y + EPSILON
    elif abs(ay - by) < EPSILON:
        if box.y + EPSILON < ay < box.bottom - EPSILON:
            low, high = sorted((ax, bx))
            return low < box.right - EPSILON and high > box.x + EPSILON
    else:
        # 对角段用 Liang-Barsky 的简化实现，兼容手工自由连线。
        dx, dy = bx - ax, by - ay
        t0, t1 = 0.0, 1.0
        for p, q in ((-dx, ax - box.x), (dx, box.right - ax), (-dy, ay - box.y), (dy, box.bottom - ay)):
            if abs(p) < EPSILON:
                if q < 0:
                    return False
                continue
            ratio = q / p
            if p < 0:
                t0 = max(t0, ratio)
            else:
                t1 = min(t1, ratio)
        return t0 < t1 and t0 < 1 - EPSILON and t1 > EPSILON
    return False


def is_axis_aligned(start, end):
    """仅把完全声明的正交段交给静态碰撞计算，避免猜测编辑器自动弯折。"""
    return abs(start[0] - end[0]) < EPSILON or abs(start[1] - end[1]) < EPSILON


def segment_clearance(a, b, box):
    """返回 axis-aligned 段到 bbox 的最短距离，用于走廊净空告警。"""
    ax, ay = a
    bx, by = b
    if abs(ax - bx) < EPSILON:
        x_gap = max(box.x - ax, 0, ax - box.right)
        low, high = sorted((ay, by))
        y_gap = max(box.y - high, 0, low - box.bottom)
    elif abs(ay - by) < EPSILON:
        y_gap = max(box.y - ay, 0, ay - box.bottom)
        low, high = sorted((ax, bx))
        x_gap = max(box.x - high, 0, low - box.right)
    else:
        return float("inf")
    return (x_gap * x_gap + y_gap * y_gap) ** 0.5


def port(box, x, y):
    return (box.x + box.width * x, box.y + box.height * y)


def inspect_page(diagram, minimum_clearance, max_edge_label, max_direct_span):
    model = parse_model(diagram)
    root = model.find("root")
    if root is None:
        return ["页面缺少 root"], 0
    cells = {cell.get("id"): cell for cell in root.findall("mxCell") if cell.get("id")}
    child_parents = {cell.get("parent") for cell in cells.values() if cell.get("parent")}
    cache = {}

    def bbox(cell_id):
        if cell_id in cache:
            return cache[cell_id]
        cell = cells.get(cell_id)
        if cell is None:
            return None
        geometry = cell.find("mxGeometry")
        if geometry is None:
            return None
        parent = bbox(cell.get("parent"))
        origin_x = parent.x if parent else 0
        origin_y = parent.y if parent else 0
        result = Box(origin_x + number(geometry.get("x")), origin_y + number(geometry.get("y")), number(geometry.get("width")), number(geometry.get("height")))
        cache[cell_id] = result
        return result

    blockers = {}
    for cell_id, cell in cells.items():
        if cell.get("vertex") != "1" or is_container(cell, child_parents):
            continue
        candidate = bbox(cell_id)
        if candidate and candidate.width > 0 and candidate.height > 0:
            blockers[cell_id] = candidate

    errors = []
    edge_count = 0

    def top_domain(cell_id):
        """返回根画布下的直接容器，用于识别真正跨域的连线。"""
        current = cell_id
        while current and current in cells:
            parent_id = cells[current].get("parent")
            if parent_id == "1":
                return current
            current = parent_id
        return None

    for cell_id, edge in cells.items():
        if edge.get("edge") != "1":
            continue
        edge_count += 1
        source_id, target_id = edge.get("source"), edge.get("target")
        source, target = bbox(source_id), bbox(target_id)
        if source is None or target is None:
            errors.append(f"{cell_id}: 缺少可解析的 source/target bbox")
            continue
        geometry = edge.find("mxGeometry")
        points = []
        if geometry is not None:
            parent = bbox(edge.get("parent"))
            origin_x = parent.x if parent else 0
            origin_y = parent.y if parent else 0
            for point in geometry.findall("./Array[@as='points']/mxPoint"):
                points.append((origin_x + number(point.get("x")), origin_y + number(point.get("y"))))
        style = edge.get("style", "")
        exit_x = number(dict(item.split("=", 1) for item in style.split(";") if "=" in item).get("exitX"), 0.5)
        exit_y = number(dict(item.split("=", 1) for item in style.split(";") if "=" in item).get("exitY"), 0.5)
        entry_x = number(dict(item.split("=", 1) for item in style.split(";") if "=" in item).get("entryX"), 0.5)
        entry_y = number(dict(item.split("=", 1) for item in style.split(";") if "=" in item).get("entryY"), 0.5)
        route = [port(source, exit_x, exit_y), *points, port(target, entry_x, entry_y)]
        value = html.unescape(edge.get("value", ""))
        if len(value.replace("<br>", "").strip()) > max_edge_label:
            errors.append(f"{cell_id}: 连线标签超过 {max_edge_label} 字符；改为卡片说明或独立 label chip")
        direct_span = math.dist(route[0], route[-1])
        crosses_domain = top_domain(source_id) != top_domain(target_id)
        if not points and (crosses_domain or direct_span > max_direct_span):
            reason = "跨域" if crosses_domain else f"直线跨度 {direct_span:.0f}"
            errors.append(f"{cell_id}: {reason} 连线缺少显式 waypoint；为长边和跨域边指定走廊")
        for index, (start, end) in enumerate(zip(route, route[1:]), 1):
            if not is_axis_aligned(start, end):
                errors.append(f"{cell_id}: 第 {index} 段不是显式正交段；补充 waypoint 后再做确定性碰撞检查")
                continue
            for blocker_id, blocker in blockers.items():
                if blocker_id in {source_id, target_id}:
                    continue
                if line_intersects_box(start, end, blocker):
                    errors.append(f"{cell_id}: 第 {index} 段穿过 {blocker_id}")
                elif minimum_clearance and segment_clearance(start, end, blocker) < minimum_clearance:
                    errors.append(f"{cell_id}: 第 {index} 段距 {blocker_id} 小于走廊净空 {minimum_clearance:g}")
    return errors, edge_count


def main():
    parser = argparse.ArgumentParser(description="检查 draw.io 连线、标签与走廊净空")
    parser.add_argument("file", type=Path)
    parser.add_argument("--min-clearance", type=float, default=24, help="非端点阻挡物的最小净空；0 表示关闭")
    parser.add_argument("--max-edge-label", type=int, default=18, help="允许保留在线上的最大标签字符数")
    parser.add_argument("--max-direct-span", type=float, default=240, help="超过此跨度且无 waypoint 的边将失败")
    args = parser.parse_args()
    try:
        document = ET.parse(args.file).getroot()
    except (ET.ParseError, OSError) as error:
        print(f"ERROR: 无法读取 XML: {error}", file=sys.stderr)
        return 2
    diagrams = document.findall("diagram") or [document]
    all_errors, edges = [], 0
    for diagram in diagrams:
        try:
            errors, edge_count = inspect_page(diagram, args.min_clearance, args.max_edge_label, args.max_direct_span)
        except ValueError as error:
            errors, edge_count = [str(error)], 0
        name = diagram.get("name", "未命名页面")
        all_errors.extend(f"{name}: {error}" for error in errors)
        edges += edge_count
    if all_errors:
        print(f"FAIL: {args.file}，检查 {edges} 条边，发现 {len(all_errors)} 项")
        print("\n".join(f"- {error}" for error in all_errors))
        return 1
    print(f"PASS: {args.file}，检查 {edges} 条边；未发现节点穿越、长标签或走廊净空问题")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
