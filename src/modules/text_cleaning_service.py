import re


class CleaningService:

    SPACE_SUB = re.compile(r"\s{2,}")
    DOTS_SUB = re.compile(r"\.{2,}")
    NEWLINE_TO_DOT_SUB = re.compile(r"\n")
    NEWLINE_AFTER_PUNC_SUB = re.compile(r"(?<=[.;!?])\n")

    def clean(self, text):
        text = self.SPACE_SUB.sub(" ", text)
        text = self.NEWLINE_AFTER_PUNC_SUB.sub(" ", text)
        text = self.NEWLINE_TO_DOT_SUB.sub(r'. ', text)
        text = self.DOTS_SUB.sub(r"\.", text)

        return text
