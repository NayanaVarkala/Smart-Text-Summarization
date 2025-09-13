class TextSummarizer:
    def summarize(self, text, max_sentences=3):
        sentences = text.split(". ")
        return ". ".join(sentences[:max_sentences]) + ("..." if len(sentences) > max_sentences else "")
