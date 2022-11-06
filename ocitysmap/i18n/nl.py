import re, gettext
from . import i18n, _install_language

class i18n_nl_generic(i18n):
    #
    # Dutch streets are often named after people and include a title.
    # The title will be captured as part of the <prefix>
    #
    APPELLATIONS = [ u"St.", u"Sint", u"Ptr.", u"Pater",
                     u"Prof.", u"Professor", u"Past.", u"Pastoor",
                     u"Pr.", u"Prins", u"Prinses", u"Gen.", u"Generaal",
                     u"Mgr.", u"Monseigneur", u"Mr.", u"Meester",
                     u"Burg.", u"Burgermeester", u"Dr.", u"Dokter",
                     u"Ir.", u"Ingenieur", u"Ds.", u"Dominee", u"Deken",
                     u"Drs.", u"Maj.", u"Majoor",
                     # counting words before street name,
                     # e.g. "1e Walstraat" => "Walstraat (1e)"
                     u"\d+e",
                     u"" ]
    #
    # Surnames in Dutch streets named after people tend to have the middle name
    # listed after the rest of the surname,
    # e.g. "Prins van Oranjestraat" => "Oranjestraat (Prins van)"
    # Likewise, articles are captured as part of the prefix,
    # e.g. "Den Urling" => "Urling (Den)"
    #
    DETERMINANTS = [ u"\s?van der", u"\s?van den", u"\s?van de", u"\s?van",
                     u"\s?Den", u"\s?D'n", u"\s?D'", u"\s?De", u"\s?'T", u"\s?Het",
                     u"" ]

    SPACE_REDUCE = re.compile(r"\s+")
    PREFIX_REGEXP = re.compile(r"^(?P<prefix>(%s)(%s)?)\s?\b(?P<name>.+)" %
                                    ("|".join(APPELLATIONS),
                                     "|".join(DETERMINANTS)),
                                      re.IGNORECASE | re.UNICODE)

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
        matches = self.PREFIX_REGEXP.match(name)
        #
        # If no prefix was captured, that's okay. Don't substitute
        # the name however, "<name> ()" looks silly
        #
        if matches == None:
            return name

        if matches.group('prefix'):
            name = self.PREFIX_REGEXP.sub(r"\g<name> (\g<prefix>)", name)
        return name

    def first_letter_equal(self, a, b):
        return self.upper_unaccent_string(a) == self.upper_unaccent_string(b)


    def language_desc(self):
        return 'Nederlands (%s)' % self.language

