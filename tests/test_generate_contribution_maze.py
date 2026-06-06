import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).resolve().parents[1] / 'scripts' / 'generate_contribution_maze.py'


def load_module():
    spec = importlib.util.spec_from_file_location('generate_contribution_maze', MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ContributionMazeTests(unittest.TestCase):
    def test_build_calendar_fills_missing_days(self):
        module = load_module()
        cells = [
            {'date': '2026-06-01', 'level': 1, 'count': 2},
            {'date': '2026-06-03', 'level': 3, 'count': 5},
        ]

        weeks = module.build_calendar(cells)
        flattened = [cell for week in weeks for cell in week]

        self.assertTrue(weeks)
        self.assertIn('2026-06-02', {cell['date'] for cell in flattened})
        self.assertEqual(0, next(cell['count'] for cell in flattened if cell['date'] == '2026-06-02'))

    def test_extract_cells_reads_contribution_markup(self):
        module = load_module()
        quote = chr(34)
        sample_html = (
            '<table><tr>'
            + '<td class=' + quote + 'ContributionCalendar-day' + quote
            + ' data-date=' + quote + '2026-06-01' + quote
            + ' data-level=' + quote + '2' + quote
            + ' data-count=' + quote + '4' + quote
            + '></td>'
            + '<td class=' + quote + 'ContributionCalendar-day' + quote
            + ' data-date=' + quote + '2026-06-02' + quote
            + ' data-level=' + quote + '0' + quote
            + ' data-count=' + quote + '0' + quote
            + '></td>'
            + '</tr></table>'
        )

        cells = module.extract_cells(sample_html)

        self.assertEqual(2, len(cells))
        self.assertEqual('2026-06-01', cells[0]['date'])
        self.assertEqual(2, cells[0]['level'])
        self.assertEqual(4, cells[0]['count'])

    def test_build_route_path_creates_svg_commands(self):
        module = load_module()
        weeks = [
            [
                {'date': '2026-06-01', 'level': 0, 'count': 0},
                {'date': '2026-06-02', 'level': 1, 'count': 1},
                {'date': '2026-06-03', 'level': 2, 'count': 2},
                {'date': '2026-06-04', 'level': 0, 'count': 0},
                {'date': '2026-06-05', 'level': 3, 'count': 3},
                {'date': '2026-06-06', 'level': 0, 'count': 0},
                {'date': '2026-06-07', 'level': 1, 'count': 1},
            ]
        ]

        path = module.build_route_path(weeks, 24, 16, 92, 112)

        self.assertTrue(path.startswith('M '))
        self.assertIn('L', path)

    def test_build_svg_contains_expected_labels(self):
        module = load_module()
        weeks = [
            [
                {'date': '2026-06-01', 'level': 1, 'count': 2},
                {'date': '2026-06-02', 'level': 0, 'count': 0},
                {'date': '2026-06-03', 'level': 2, 'count': 3},
                {'date': '2026-06-04', 'level': 0, 'count': 0},
                {'date': '2026-06-05', 'level': 1, 'count': 1},
                {'date': '2026-06-06', 'level': 0, 'count': 0},
                {'date': '2026-06-07', 'level': 0, 'count': 0},
            ]
        ]

        svg = module.build_svg('Ltdaaa', weeks, 'M 10 10 L 20 20')

        self.assertIn('Contribution Maze', svg)
        self.assertIn('@Ltdaaa', svg)
        self.assertIn('animate', svg)
        self.assertIn('<svg', svg)


if __name__ == '__main__':
    unittest.main()
