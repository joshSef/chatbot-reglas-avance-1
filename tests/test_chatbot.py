from asistente.chatbot import RuleBasedChatbot, normalize


def make_bot() -> RuleBasedChatbot:
    return RuleBasedChatbot(seed=7)


def test_normalize_removes_accents_and_uses_lowercase():
    assert normalize("¿QUÉ Tecnología?") == "¿que tecnologia?"


def test_classifies_phrase_with_accents():
    match = make_bot().classify("¿Cuál es el propósito de este avance?")
    assert match.intent == "objetivo"
    assert match.score > 0


def test_classifies_nltk_query():
    assert make_bot().classify("¿Para qué usamos NLTK?").intent == "tecnologias"


def test_does_not_match_substrings_as_words():
    assert make_bot().classify("holanda").intent == "fallback"


def test_returns_fallback_for_unknown_question():
    response = make_bot().respond("¿Cuál es el clima en Mérida?")
    assert "No identifiqué" in response or "no tengo una regla" in response


def test_response_is_reproducible_with_seed():
    first = RuleBasedChatbot(seed=42).respond("hola")
    second = RuleBasedChatbot(seed=42).respond("hola")
    assert first == second
