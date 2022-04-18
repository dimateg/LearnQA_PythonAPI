class TestShortPhrase:
    def test_phrase_length(self):
        phrases = input("Set a phrase: ")
        sums = len(phrases)
        assert sums == 15, f"Phrase length is not 15 characters {sums}"
