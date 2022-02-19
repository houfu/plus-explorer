from __future__ import annotations

import re

tokenizer = re.compile(r"((?:[^()\s]+|[().?!-])\s*)")


def tokenize_text(text: str) -> list[str]:
    return re.findall(tokenizer, text)


class Redlines:
    _source: str = None
    _test: str = None
    _seq1: list[str] = None
    _seq2: list[str] = None

    @property
    def source(self):
        """
        The source text to be used as a basis for comparison.
        :return:
        """
        return self._source

    @source.setter
    def source(self, value):
        self._source = value
        self._seq1 = tokenize_text(value)

    @property
    def test(self):
        """The text to be compared with the source."""
        return self._test

    @test.setter
    def test(self, value):
        self._test = value
        self._seq2 = tokenize_text(value)

    def __init__(self, source: str, test: str | None = None, **options):
        """
        Redline is a class used to compare text, and producing human-readable differences or deltas
        which look like track changes in Microsoft Word.
        :param source: The source text to be used as a basis for comparison.
        :param test: Optional test text to compare with the source.
        """
        self.source = source
        self.options = options
        if test:
            self.test = test
            self.compare()

    @property
    def opcodes(self) -> list[tuple[str, int, int, int, int]]:
        """
        Return list of 5-tuples describing how to turn `source` into `test`.
        Similar to `SequenceMatcher.get_opcodes`
        """
        if self._seq2 is None:
            raise ValueError('No test string was provided when the function was called, or during initialisation.')

        from difflib import SequenceMatcher
        matcher = SequenceMatcher(None, self._seq1, self._seq2)
        return matcher.get_opcodes()

    @property
    def output_markdown(self) -> str:
        """Returns the delta in markdown format."""
        result = []
        style = 'red'

        if self.options.get('markdown_style'):
            style = self.options['markdown_style']

        if style == 'none':
            md_styles = {"ins": ('ins', 'ins'), "del": ('del', 'del')}
        elif 'red':
            md_styles = {"ins": ('span style="color:red;font-weight:700;"', 'span'),
                         "del": ('span style="color:red;font-weight:700;text-decoration:line-through;"', 'span')}

        for tag, i1, i2, j1, j2 in self.opcodes:
            if tag == 'equal':
                result.append("".join(self._seq1[i1:i2]))
            elif tag == 'insert':
                result.append(f"<{md_styles['ins'][0]}>{''.join(self._seq2[j1:j2])}</{md_styles['ins'][1]}>")
            elif tag == 'delete':
                result.append(f"<{md_styles['del'][0]}>{''.join(self._seq1[i1:i2])}</{md_styles['del'][1]}>")
            elif tag == 'replace':
                result.append(
                    f"<{md_styles['del'][0]}>{''.join(self._seq1[i1:i2])}</{md_styles['del'][1]}>"
                    f"<{md_styles['ins'][0]}>{''.join(self._seq2[j1:j2])}</{md_styles['ins'][1]}>")

        return "".join(result)

    def compare(self, test: str | None = None, output: str = "markdown", **options):

        """
        Compare `test` with `source`, and produce a delta in a format specified by `output`.
        :param test: Optional test string to compare. If None, uses the test string provided during initialisation.
        :param output: The format which the delta should be produced. Currently, only "markdown" is supported
        :return: The delta in the format specified by `output`.
        """
        if test:
            if self.test and test == self.test:
                return self.output_markdown
            else:
                self.test = test
        elif self.test is None:
            raise ValueError('No test string was provided when the function was called, or during initialisation.')

        if options:
            self.options = options

        if output == 'markdown':
            return self.output_markdown


def clean_text(text: str) -> str:
    import re
    # Remove subclause notations
    cleaned_text = re.sub(r'^\(\w*\)\s+', '', text, flags=re.MULTILINE)
    # Remove clause notation at beginning of clause
    cleaned_text_1 = re.sub(r'^\d+\w?\.(—\(1\))?\s+', '', cleaned_text)
    # Remove extra spacing at start of line
    cleaned_text_2 = re.sub(r'^\s+', '', cleaned_text_1, flags=re.MULTILINE)
    # Remove amendment info
    cleaned_text_3 = re.sub(r'\[\w+]$', '', cleaned_text_2, flags=re.MULTILINE)
    # Remove extra spaces
    return re.sub(r'[\t\n\r\f\v]', ' ', cleaned_text_3).strip()


def calculate_stats(cleaned_text: str):
    from textstat import textstat
    return (
        cleaned_text,
        textstat.flesch_reading_ease(cleaned_text),
        textstat.gunning_fog(cleaned_text),
        textstat.automated_readability_index(cleaned_text),
        textstat.sentence_count(cleaned_text),
        textstat.lexicon_count(cleaned_text)
    )


def compare_text(text1, text2):
    import difflib

    def split_text(text: str) -> list[str]:
        text_chunks = text.split()
        result = []
        for i in range(0, len(text_chunks), 15):
            text_section = ''
            for j in range(15):
                if i + j == len(text_chunks):
                    break
                else:
                    text_section += f"{text_chunks[i + j]} "
            result.append(text_section)
        return result

    return difflib.ndiff(split_text(text1), split_text(text2))
