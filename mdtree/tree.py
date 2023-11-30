import unittest

from mdtree.parser import parse_string
from mdtree.utils import read_md_file

md_content = read_md_file("./txt.md")
out = parse_string(md_content)
print(out)


class TestParser(unittest.TestCase):

    def test_code_block(self):
        text = '''
Title
=====

# Code

Code 1
------
Some text
\```
# TODO
\```

Code 2
------
\```python
# TODO
print('test')
\```

# Heading
'''
        out = parse_string(text)
        self.assertEqual(out.title, 'Title')
        self.assertEqual(out[0][0].text, 'Code 1')
        # self.assertEqual(out[0][0].source, 'Some text\n```\n# TODO\n```\n')
        self.assertEqual(out[0][0].source, 'Some text\n\\```')
        self.assertEqual(out[0][1].text, 'Code 2')
        self.assertEqual(out[0][1].source, "```python\n# TODO\nprint('test')\n```\n")
        self.assertEqual(out[1].text, 'Heading')


if __name__ == '__main__':
    unittest.main()
