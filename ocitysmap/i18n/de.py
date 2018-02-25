import re, gettext
from . import i18n, _install_language

class i18n_de_generic(i18n):
    #
    # German streets are often named after people and include a title.
    # The title will be captured as part of the <prefix>
    # Covering airport names and "New"/"Old" as prefixes as well
    #
    # APPELLATIONS = [ u"Alte", u"Alter", u"Doktor", u"Dr.",
    #                 u"Flughafen", u"Flugplatz", u"Gen.,", u"General",
    #                 u"Neue", u"Neuer", u"Platz",
    #                 u"Prinz", u"Prinzessin", u"Prof.",
    #                 u"Professor" ]

    APPELLATIONS = [ ]

    #
    # Surnames in german streets named after people tend to have the middle name
    # listed after the rest of the surname,
    # e.g. "Platz der deutschen Einheit" => "deutschen Einheit (Platz der)"
    # Likewise, articles are captured as part of the prefix,
    # e.g. "An der Märchenwiese" => "Märchenwiese (An der)"
    #
    # DETERMINANTS = [ u"\s?An den", u"\s?An der", u"\s?Am",
    #                  u"\s?Auf den" , u"\s?Auf der"
    #                  u" an", u" des", u" der", u" von", u" vor"]

    DETERMINANTS = [ ]

    SPACE_REDUCE = re.compile(r"\s+")
    PREFIX_REGEXP = re.compile(r"^(?P<prefix>(%s)(%s)?)\s?\b(?P<name>.+)" %
                                    ("|".join(APPELLATIONS),
                                     "|".join(DETERMINANTS)), re.IGNORECASE
                                                                 | re.UNICODE)

    # for IndexPageGenerator.upper_unaccent_string
    E_ACCENT = re.compile(r"[éèêëẽ]", re.IGNORECASE | re.UNICODE)
    I_ACCENT = re.compile(r"[íìîïĩ]", re.IGNORECASE | re.UNICODE)
    A_ACCENT = re.compile(r"[áàâäã]", re.IGNORECASE | re.UNICODE)
    O_ACCENT = re.compile(r"[óòôöõ]", re.IGNORECASE | re.UNICODE)
    U_ACCENT = re.compile(r"[úùûüũ]", re.IGNORECASE | re.UNICODE)

    def __init__(self, language, locale_path):
        self.language = str(language)
        _install_language(language, locale_path)

    def upper_unaccent_string(self, s):
        s = self.E_ACCENT.sub("e", s)
        s = self.I_ACCENT.sub("i", s)
        s = self.A_ACCENT.sub("a", s)
        s = self.O_ACCENT.sub("o", s)
        s = self.U_ACCENT.sub("u", s)
        return s.upper()

    def language_code(self):
        return self.language

    def user_readable_street(self, name):
        #
        # Make sure name actually contains something,
        # the PREFIX_REGEXP.match fails on zero-length strings
        #
        if len(name) == 0:
            return name

        name = name.strip()
        name = self.SPACE_REDUCE.sub(" ", name)
        # name = self.PREFIX_REGEXP.sub(r"\g<name> (\g<prefix>)", name)
        return name

    def first_letter_equal(self, a, b):
        return self.upper_unaccent_string(a) == self.upper_unaccent_string(b)

