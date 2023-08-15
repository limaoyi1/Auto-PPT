import re
"""
这段代码是一个简单的 Markdown 解析器，用于解析 Markdown 格式的文本并构建相应的数据结构。它包含以下几个类和函数：

    Element 类：表示解析器中的元素。它具有以下属性和方法：
    
        source：元素的原始文本内容。
        children：子元素列表。
        full_source：返回包括元素及其子元素的完整文本内容。
        add_child(el)：向元素添加子元素。
        add_source(source)：向元素添加原始文本内容。
        
    Out 类（继承自 Element 类）：表示 Markdown 解析结果的顶层元素。它具有以下属性和方法：

        main：主标题元素。
        level：当前解析的标题级别。
        title：返回主标题的文本内容。
        full_source：返回包括源文本和所有子元素的完整文本内容。
        
    Heading 类（继承自 Element 类）：表示 Markdown 解析的标题元素。它具有以下属性和方法：

        root：指向解析结果的根元素。
        parent：指向父元素。
        level：标题级别。
        text：标题的文本内容。
        text_source：标题的原始文本内容。
        full_source：返回包括源文本和所有子元素的完整文本内容。
        
    Parser 类：Markdown 解析器类，负责解析 Markdown 文本并构建解析结果。它具有以下属性和方法：

        DEBUG：调试级别。
        parse(text)：解析 Markdown 文本并返回解析结果。
        _parse_heading_var_one(level, string, next_string)：解析第一种标题格式的辅助方法。
        _parse_heading_var_two(level, string)：解析第二种标题格式的辅助方法。
        _parse_heading_action(level, text, text_source)：处理解析到的标题元素。
"""


def parse_string(string, debug_level=0):
    return Parser(debug_level).parse(string)


def parse_file(file_path, debug_level=0, encoding='utf-8'):
    with open(file_path, encoding=encoding) as f:
        return parse_string(f.read(), debug_level)


class Element:
    def __init__(self):
        self.source = None
        self.children = []

    @property
    def full_source(self):
        if len(self.children) == 0:
            return ''

        return '\n' + '\n'.join([x.full_source for x in self.children])

    def add_child(self, el):
        self.children.append(el)

    def add_source(self, source):
        if self.source is None:
            self.source = source
        else:
            self.source += '\n' + source

    def __getitem__(self, item):
        return self.children[item]

    def __len__(self):
        return len(self.children)


class Out(Element):
    main = None
    level = 0

    @property
    def title(self):
        if self.main is not None:
            return self.main.text

    @property
    def full_source(self):
        result = ''
        if self.source is not None:
            result += f'{self.source}\n'
        result += self.main.full_source
        result += super().full_source
        return result

    def __str__(self):
        return 'Out'


class Heading(Element):
    def __init__(self, root, parent, level, text, text_source):
        super().__init__()
        self.root = root
        self.parent = parent
        self.level = level
        self._text = text
        self._text_source = text_source

    text = property()

    @text.getter
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text_source = self._text_source.replace(self._text, value)
        self._text = value

    @property
    def text_source(self):
        return self._text_source

    @property
    def full_source(self):
        result = f'{self._text_source}'
        if self.source is not None:
            result += f'\n{self.source}'
        result += super().full_source
        return result

    def __str__(self):
        return self._text


class Parser:
    def __init__(self, debug_level=0):
        self.DEBUG = debug_level

    def parse(self, text):
        self.out = Out()
        self.current = None
        jump_to_next = False
        code_block = False

        strings = text.split('\n')
        for index in range(len(strings)):
            if jump_to_next:
                jump_to_next = False
                continue

            string = strings[index]
            is_heading = False

            """ Search code block """
            if re.search(r'^\s*```.*$', string) is not None:
                code_block = not code_block

            """ Search and parse headings """
            if not code_block:
                next_string = strings[index + 1] if index + 1 < len(strings) else None

                for level in range(1, 3):
                    is_heading = self._parse_heading_var_one(level, string, next_string)
                    if is_heading:
                        break

                if is_heading:
                    jump_to_next = True
                    continue

                for level in range(1, 7):
                    is_heading = self._parse_heading_var_two(level, string)
                    if is_heading:
                        break

            if not is_heading:
                if self.current is None:
                    self.out.add_source(string)
                else:
                    self.current.add_source(string)

        return self.out

    def _parse_heading_var_one(self, level, string, next_string):
        if next_string is None or re.search(r'^\s*$', string) is not None:
            return False

        if self.DEBUG >= 2:
            print(f'- parse_heading_var_one with level: {level}, next_string: "{next_string}"')

        if level == 1:
            tmpl = '='
        elif level == 2:
            tmpl = '-'
        else:
            raise Exception(f'Not support level: {level}')

        regex = '^\s?%s{3,}\s*$' % tmpl
        result = re.search(regex, next_string)

        if result is None:
            return False

        return self._parse_heading_action(
            level=level,
            text=string.strip(),
            text_source=f'{string}\n{next_string}'
        )

    def _parse_heading_var_two(self, level, string):
        if self.DEBUG >= 2:
            print(f'- parse_heading_var_two with level: {level}, string: "{string}"')

        regex = '^(\s?#{%s}\s+)(.*)$' % level
        result = re.search(regex, string)

        if result is None:
            return False

        return self._parse_heading_action(
            level=level,
            text=result[2],
            text_source=result[1] + result[2]
        )

    def _parse_heading_action(self, level, text, text_source):
        if self.current is None:
            parent = self.out
        elif level > self.current.level:
            parent = self.current
        else:
            parent = self.current.parent
            while parent.level >= level:
                parent = parent.parent

        self.current = Heading(self.out, parent, level, text, text_source)

        if level == 1 and self.out.main is None:
            self.out.main = self.current
        else:
            parent.add_child(self.current)

        if self.DEBUG >= 1:
            spaces = '  '.join(['' for _ in range(parent.level + 1)]) if parent != self.out else ''
            print(f'{spaces}<{str(parent)}>')
            spaces = '  '.join(['' for _ in range(self.current.level + 1)])
            print(f'{spaces}(+) <{str(self.current)}>')

        return True