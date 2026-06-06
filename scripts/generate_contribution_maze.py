from __future__ import annotations

import argparse
import datetime as dt
import html
from html.parser import HTMLParser
import pathlib
import urllib.request


class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []

    def handle_starttag(self, tag, attrs):
        if tag != 'td':
            return
        data = dict(attrs)
        if 'data-date' not in data or 'data-level' not in data or 'data-count' not in data:
            return
        self.cells.append(
            {
                'date': data['data-date'],
                'level': int(data['data-level']),
                'count': int(data['data-count']),
            }
        )


def extract_cells(markup: str):
    parser = ContributionParser()
    parser.feed(markup)
    return sorted(parser.cells, key=lambda item: item['date'])


def build_calendar(cells):
    if not cells:
        return []

    by_date = {dt.date.fromisoformat(cell['date']): dict(cell) for cell in cells}
    start = min(by_date)
    end = max(by_date)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    end += dt.timedelta(days=(5 - end.weekday()) % 7 + 1)

    weeks = []
    cursor = start
    week = []

    while cursor <= end:
        week.append(by_date.get(cursor, {'date': cursor.isoformat(), 'level': 0, 'count': 0}))
        if len(week) == 7:
            weeks.append(week)
            week = []
        cursor += dt.timedelta(days=1)

    if week:
        weeks.append(week)

    return weeks


def build_route_path(weeks, start_x, start_y, cell_size, gap):
    points = []
    for week_index, week in enumerate(weeks):
        for day_index, cell in enumerate(week):
            if cell['count'] > 0:
                x = start_x + week_index * (cell_size + gap) + cell_size / 2
                y = start_y + day_index * (cell_size + gap) + cell_size / 2
                points.append((x, y))

    if not points:
        points = [(start_x + cell_size / 2, start_y + cell_size / 2)]

    head, *tail = points
    return 'M ' + f'{head[0]:.1f} {head[1]:.1f}' + ''.join(f' L {x:.1f} {y:.1f}' for x, y in tail)


def fetch_contributions(username: str) -> str:
    url = f'https://github.com/users/{username}/contributions'
    request = urllib.request.Request(url, headers={'User-Agent': 'profile-readme-maze-generator'})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode('utf-8')


def build_svg(username: str, weeks, route_path: str) -> str:
    width = max(760, 110 + len(weeks) * 14)
    height = 360
    updated = dt.datetime.now(dt.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    total = sum(cell['count'] for week in weeks for cell in week)
    active_days = sum(1 for week in weeks for cell in week if cell['count'] > 0)
    level_colors = ['#f7d6e5', '#f5a8c0', '#ee7ba5', '#d6578d', '#8b3f6c']
    cell_size = 10
    gap = 3
    grid_x = 52
    grid_y = 112

    rects = []
    for week_index, week in enumerate(weeks):
        for day_index, cell in enumerate(week):
            x = grid_x + week_index * (cell_size + gap)
            y = grid_y + day_index * (cell_size + gap)
            color = level_colors[min(cell['level'], len(level_colors) - 1)]
            rects.append(
                f"<rect x='{x}' y='{y}' width='{cell_size}' height='{cell_size}' rx='3' fill='{color}'><title>{html.escape(cell['date'])}: {cell['count']} contributions</title></rect>"
            )

    dash_length = max(600, len(route_path) * 2)
    lines = [
        f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' fill='none' xmlns='http://www.w3.org/2000/svg' role='img' aria-labelledby='title desc'>",
        f"<title id='title'>{html.escape(username)} contribution maze</title>",
        "<desc id='desc'>Anime-inspired contribution maze card generated from public GitHub contribution data.</desc>",
        "<defs>",
        "<linearGradient id='cardBg' x1='0' y1='0' x2='1' y2='1'><stop offset='0%' stop-color='#fff8fc' /><stop offset='100%' stop-color='#eef6ff' /></linearGradient>",
        "<linearGradient id='glowPath' x1='0' y1='0' x2='1' y2='0'><stop offset='0%' stop-color='#f38bb3' /><stop offset='50%' stop-color='#f8b6d2' /><stop offset='100%' stop-color='#ffd86b' /></linearGradient>",
        "<filter id='softGlow' x='-30%' y='-30%' width='160%' height='160%'><feGaussianBlur stdDeviation='3' result='blur' /><feMerge><feMergeNode in='blur' /><feMergeNode in='SourceGraphic' /></feMerge></filter>",
        "</defs>",
        f"<rect x='8' y='8' width='{width - 16}' height='{height - 16}' rx='28' fill='url(#cardBg)' stroke='#f2bfd3' stroke-width='2' />",
        "<circle cx='56' cy='52' r='20' fill='#ffd7e8' />",
        "<circle cx='112' cy='52' r='12' fill='#ffd86b' opacity='0.8' />",
        "<text x='88' y='46' font-size='24' font-family='Verdana, sans-serif' fill='#6b3956'>Contribution Maze</text>",
        f"<text x='88' y='74' font-size='13' font-family='Verdana, sans-serif' fill='#8d6080'>@{html.escape(username)} | {total} contributions | {active_days} active days</text>",
        f"<text x='52' y='98' font-size='12' font-family='Verdana, sans-serif' fill='#9b7590'>Daily auto-refresh via GitHub Actions | Updated {updated}</text>",
    ]
    lines.extend(rects)
    lines.extend(
        [
            f"<path d='{route_path}' stroke='url(#glowPath)' stroke-width='4' stroke-linecap='round' stroke-linejoin='round' opacity='0.95' fill='none' filter='url(#softGlow)' stroke-dasharray='{dash_length}' stroke-dashoffset='{dash_length}'><animate attributeName='stroke-dashoffset' from='{dash_length}' to='0' dur='6s' repeatCount='indefinite' /></path>",
            "<text x='52' y='318' font-size='12' font-family='Verdana, sans-serif' fill='#8d6080'>Entrance: first active day</text>",
            "<text x='260' y='318' font-size='12' font-family='Verdana, sans-serif' fill='#8d6080'>Goal: keep the route glowing brighter every day</text>",
            "<text x='52' y='338' font-size='12' font-family='Verdana, sans-serif' fill='#b3889f'>Generated locally by scripts/generate_contribution_maze.py</text>",
            "</svg>",
        ]
    )
    return '\n'.join(lines)


def write_svg(username: str, output_path: pathlib.Path):
    markup = fetch_contributions(username)
    cells = extract_cells(markup)
    weeks = build_calendar(cells)
    route_path = build_route_path(weeks, 52, 112, 10, 3)
    svg = build_svg(username, weeks, route_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description='Generate a contribution-maze SVG card from public GitHub data.')
    parser.add_argument('--username', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    write_svg(args.username, pathlib.Path(args.output))


if __name__ == '__main__':
    main()
